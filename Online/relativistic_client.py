import socket
import chess
import time

from threading import Thread
from chessboard import display

from socket_client import HOST, PORT1, PORT0, player


class Display(Thread):

    def __init__(self):
        super().__init__()
        self.display_window = display.start(caption='Relativistic Chess')
        self.go = True

    def run(self):
        while self.go:
            display.check_for_quit()
        display.terminate()


class RelativisticClient(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket()  # instantiate
        self.board_history = []
        self.player = player
        self.player_color = 'White' if port == PORT1 else 'Black'
        self.display_window = display.start(caption=f'Relativistic Chess - {self.player_color}')
        self.visible_board = chess.Board()
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
        return self.player.random_player(self.board_history[-1])

    def send_move(self, uci):
        self.client_socket.send(str(uci).encode())

    def calculate_relativistic_board(self):
        self.visible_board = chess.Board(self.board_history[-1])

    def update_display(self):
        print(self.visible_board)
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
