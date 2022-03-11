# TODO
# mate

"""
Handling user input and displaying current game state.
"""

import pygame as p

from chess_piece import Pawn, Empty, King
from engine import *

IMAGES = {}
DIMENSION = 8
MAX_FPS = 15  # for animation
WIDTH = HEIGHT = 512
SQUARE_SIZE = HEIGHT // DIMENSION

pieces = [BLACK_ROOK_1, BLACK_ROOK_2, BLACK_KNIGHT_1, BLACK_KNIGHT_2,
          BLACK_BISHOP_1, BLACK_BISHOP_2, BLACK_QUEENS[0], BLACK_KING,
          WHITE_ROOK_1, WHITE_ROOK_2, WHITE_KNIGHT_1, WHITE_KNIGHT_2,
          WHITE_BISHOP_1, WHITE_BISHOP_2, WHITE_QUEENS[0], WHITE_KING] \
         + BLACK_PAWNS + WHITE_PAWNS


def int_color_to_string(color):
    return "white" if color == 0 else "black"


def load_images():
    for piece in pieces:
        pic_path = "pics\\" + int_color_to_string(piece.get_color()) + "_"
        pic_path += piece.__class__.__name__.lower() + ".png"
        IMAGES[piece] = p.transform.scale(p.image.load(pic_path),
                                          (SQUARE_SIZE, SQUARE_SIZE))


#  responsible for all the graphics
def draw_game_state(screen, game_state):
    colors = [p.Color("white"), p.Color("light blue")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            location = p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            p.draw.rect(screen, color, location)
            piece = game_state.board[row][col]
            if not isinstance(piece, Empty):
                screen.blit(IMAGES[piece], location)


def change_pawn_to_queen(screen, row, col, color, game_state):
    location = p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    queen = game_state.add_queen(color, row, col)

    # Load image
    pic_path = "pics\\" + int_color_to_string(queen.get_color()) + "_"
    pic_path += "queen.png"
    IMAGES[queen] = p.transform.scale(p.image.load(pic_path),
                                      (SQUARE_SIZE, SQUARE_SIZE))
    screen.blit(IMAGES[queen], location)
    game_state.board[row][col] = queen
    p.display.update(location)


def pre_conditions(is_white_turn, this_color, other_color):
    correct_color = right_color(is_white_turn, this_color)
    eat_opponent_or_empty = this_color != other_color

    if not correct_color:
        print("ERROR: not your turn.")
        return False
    elif not eat_opponent_or_empty:
        print("ERROR: can not eat your own piece.")
    return True


def right_color(is_white_turn, color):
    if (is_white_turn and not color == WHITE) or (
            not is_white_turn and not color == BLACK):
        return False
    return True


def castling(game_state, dst_col, color, piece_to_move):
    if dst_col == 2:
        if color == WHITE:
            game_state.castle(piece_to_move, WHITE_ROOK_1)
        else:
            game_state.castle(piece_to_move, BLACK_ROOK_1)
    else:
        if color == WHITE:
            game_state.castle(piece_to_move, WHITE_ROOK_2)
        else:
            game_state.castle(piece_to_move, BLACK_ROOK_2)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = GameState()
    running = True
    load_images()
    # last click of the user : (row, col)
    square_selected = ()
    # from square to square : [(src_row, src_col), (dst_row, dst_col)]
    player_clicks = []
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x, y
                dst_col = location[0] // SQUARE_SIZE
                dst_row = location[1] // SQUARE_SIZE
                # user clicked twice on the same square
                if square_selected == (dst_row, dst_col):
                    square_selected, player_clicks = (), []
                else:
                    square_selected = (dst_row, dst_col)
                    player_clicks.append(square_selected)
                # user's 2nd click
                if len(player_clicks) == 2:
                    from_square = player_clicks[0]
                    src_row, src_col = from_square
                    to_square = player_clicks[1]

                    move = Move(from_square, to_square, game_state.board)
                    piece_to_move = game_state.board[src_row][src_col]
                    move_to = game_state.board[dst_row][dst_col]
                    color = piece_to_move.get_color()

                    if not pre_conditions(game_state.is_white_turn, color, move_to.get_color()):
                        square_selected, player_clicks = (), []
                        continue

                    #  Castling
                    if isinstance(piece_to_move, King) and (
                            src_row in (0, 7)) and (src_col == 4) and (
                            dst_row in (0, 7)) and (dst_col in (6, 2)):
                        castling(game_state, dst_col, color, piece_to_move)
                    else:
                        valid_move = piece_to_move.is_valid_move(game_state.board, from_square, to_square)
                        if not valid_move:
                            print("ERROR: not a valid move for {}.".format(piece_to_move.__class__.__name__))
                            square_selected, player_clicks = (), []
                            continue

                        game_state.make_move(move)
                        if game_state.caused_check():  # works for check also.
                            print("ERROR: this move is causing your king to be in check.")
                            game_state.undo_move()
                            square_selected, player_clicks = (), []
                            continue  # added to check!!!

                        elif isinstance(piece_to_move, Pawn):
                            color = piece_to_move.get_color()
                            if (color == WHITE and dst_row == 0) or (
                                    color == BLACK and dst_row == 7
                            ):
                                change_pawn_to_queen(screen, dst_row, dst_col, color, game_state)

                    game_state.is_white_turn = not game_state.is_white_turn  # Switch turns
                    square_selected, player_clicks = (), []
        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
