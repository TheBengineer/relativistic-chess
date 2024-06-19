import socket
import chess
import time
import math

from threading import Thread
from chessboard import display

from socket_client import HOST, PORT1, PORT0
from player import KeyboardPlayer


class Display:

    def __init__(self, client, player_name='White'):
        super().__init__()
        self.client = client
        self.player_name = player_name
        self.display_window = display.start(caption=f'{self.player_name} - Relativistic Chess')
        self.visible_board = chess.Board()
        self.go = True

    def main(self):
        while self.go:
            display.check_for_quit()
            if self.client.updated:
                self.client.updated = False
                self.visible_board = self.client.visible_board.copy()
            display.update(self.visible_board.fen(), self.display_window)
            if not self.display_window.flipped:
                display.flip(self.display_window)
        display.terminate()


class RelativisticClient(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket()  # instantiate
        self.board_history = ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'] * 6
        self.player = KeyboardPlayer()
        self.visible_board = chess.Board()
        if port == PORT0:
            self.player_color = 'Black'
        else:
            self.player_color = 'White'
            self.visible_board = self.visible_board.mirror()
        self.display_window = display.start(caption=f'Relativistic Chess - {self.player_color}')
        self.updated = True
        self.go = True

    def connect(self):
        self.client_socket.connect((self.host, self.port))  # connect to the server
        print(f'{self.port} connected!')

    def time_buffering(self):
        # time buffering calculation with socket server
        for ite in range(5):
            data = self.client_socket.recv(2048).decode()
            self.client_socket.send(data.encode())
            ite += 1
        print('Calculating time buffering complete')

    def get_next_board_state(self):
        try:
            self.client_socket.settimeout(.1)
            board_fen = self.client_socket.recv(8192).decode()
            self.client_socket.settimeout(None)
        except socket.timeout:
            return False
        print(f'Got fen {board_fen} from server')
        if not board_fen:
            return False
        self.board_history.append(board_fen)
        return True

    def next_move(self):
        self.update_display()
        current_board_fen = self.board_history[-1]
        move = self.player.random_player(current_board_fen)
        board = chess.Board(current_board_fen)
        board.push_uci(move.uci())
        self.board_history[-1] = board.fen()
        self.calculate_relativistic_board()
        self.update_display()
        return move

    def send_move(self, uci):
        self.client_socket.send(str(uci).encode())

    def calculate_relativistic_board(self):
        current_board = chess.Board(self.board_history[-1])
        color = self.player_color == 'White'
        king_pos = current_board.king(color)
        for layer, next_board_fen in enumerate(reversed(self.board_history[-5:])):
            next_board = chess.Board(next_board_fen)
            distance = (layer + 1) * 2
            for i, square in enumerate(chess.SQUARES):
                # square_distance = math.sqrt(pow(chess.square_rank(square) - chess.square_rank(king_pos), 2) + pow(
                #     chess.square_file(square) - chess.square_file(king_pos), 2))
                if chess.square_distance(king_pos, square) >= distance:
                    new_piece = next_board.piece_at(square)
                    old_piece = current_board.piece_at(square)
                    if new_piece != old_piece:
                        if not (new_piece and new_piece.color == color):
                            current_board.set_piece_at(square, new_piece)
        self.transform_board_for_display(current_board)

    def transform_board_for_display(self, board):
        if self.player_color == 'White':
            board.apply_transform(chess.flip_vertical)
            board.apply_transform(chess.flip_horizontal)
        self.visible_board = board
        self.updated = True

    def update_display(self):
        print(self.visible_board.transform(chess.flip_vertical).transform(chess.flip_horizontal))
        fen = self.visible_board.fen()
        print(fen)
        display.update(fen, self.display_window)
        if not self.display_window.flipped:
            display.flip(self.display_window)

    def stop(self):
        self.go = False
        display.terminate()

    def run(self):
        # main process
        while self.go:
            display.check_for_quit()
            try:
                updated = self.get_next_board_state()
                if not updated:
                    continue
                t0 = time.time()
                if self.board_history[-1] == 'Quit':
                    self.stop()
                    break
                self.calculate_relativistic_board()
                move_uci = self.next_move()
                print(f'Sending move {move_uci} to server, time taken: {str(time.time() - t0)} ms')
                self.send_move(move_uci)
            except Exception as e:
                print(f'Got unexpected error: {e}\nclosing connection...')
                self.client_socket.close()
                break
            self.update_display()

        self.client_socket.close()  # close the connection
        display.terminate()
        print('Good bye!')


if __name__ == '__main__':
    rc = RelativisticClient(host=HOST, port=PORT1)
    b = Display(rc)
    b.main()
    input('Press any key to exit...')
    b.go = False
    print('Main Good bye!')

if __name__ == '__main__2':
    rc0 = RelativisticClient(host=HOST, port=PORT0)
    rc1 = RelativisticClient(host=HOST, port=PORT1)
    rc0.connect()
    rc1.connect()
    rc0.time_buffering()
    rc1.time_buffering()
    rc0.start()
    rc1.start()
    input('Press any key to exit...')
    rc0.go = False
    rc1.go = False
    rc0.join()
    rc1.join()
    print('Main Good bye!')
