import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Hide pygame support message
import chess
import sys
import pygame

from pygame.locals import QUIT, KEYUP, K_ESCAPE

from chessboard.board import Board, Color
from chessboard.constants import FPS, STARTING_FEN, WINDOW_CAPTION, WINDOW_WIDTH, WINDOW_HEIGHT

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre display window.

fps_clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for _ in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def start(fen=STARTING_FEN, bg_color=Color.ASH, caption=WINDOW_CAPTION):
    pygame.init()

    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(caption)

    display_surf.fill(bg_color)
    game_board = Board(bg_color, display_surf)
    color = chess.Board(fen).turn

    update(fen, game_board, color)

    return game_board


def draw_timewarp(game_board: Board, player_color):
    board = chess.Board(game_board.current_fen)
    king_square = board.king(not player_color)
    king_pos = (chess.square_file(king_square), 7-chess.square_rank(king_square))
    game_pos = game_board.board_rect[king_pos[1]][king_pos[0]]
    game_pos = (game_pos[0] + 24, game_pos[1] + 24)
    #game_board.draw_timewarp(game_pos)


def update(fen, game_board, color: bool):
    color = not color
    check_for_quit()
    game_board.update_pieces(fen)
    draw_timewarp(game_board, color)

    pygame.display.update()
    fps_clock.tick(FPS)


def flip(game_board: Board):
    check_for_quit()
    game_board.flip()

    pygame.display.update()
    fps_clock.tick(FPS)
