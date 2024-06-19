import random

import chess


class KeyboardPlayer:
    def __init__(self) -> None:
        self.board = chess.Board()

    def display_board(self):
        print(self.board)

    def keyboard_player(self, board_fen=None):
        if board_fen:
            self.board.set_fen(board_fen)
        moves = [m.uci() for m in self.board.legal_moves]
        valid = False
        move = None
        while not valid:
            move = input('Enter move: ')
            if move in moves:
                valid = True
                continue
            else:
                print('Invalid move')
        return move


if __name__ == '__main__':
    player = KeyboardPlayer()
    while True:
        player.display_board()
        uci_str = player.keyboard_player()
        print(f'Played move: {uci_str}')
        move_uci = chess.Move.from_uci(uci_str)
        player.board.push(move_uci)
