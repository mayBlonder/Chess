"""
Eat:
    X :
    V :
        Rook
        Queen

Exposing:
    X:
        bishop
    V:
        Rook
"""

# Add can't move if exposes king to check
# Add check and mate
# Castling, Pawn promotion and en-passant

"""
Handling user input and displaying current game state.
"""
import engine
import pygame as p
from engine import *
from chess_piece import Pawn

IMAGES = {}
WIDTH = 512
HEIGHT = 512
DIMENSION = 8
MAX_FPS = 15  # for animation
SQUARE_SIZE = HEIGHT // DIMENSION

pieces = [BLACK_ROOK_1, BLACK_ROOK_2, BLACK_KNIGHT_1, BLACK_KNIGHT_2,
          BLACK_BISHOP_1, BLACK_BISHOP_2, BLACK_QUEEN, BLACK_KING,
          WHITE_ROOK_1, WHITE_ROOK_2, WHITE_KNIGHT_1, WHITE_KNIGHT_2,
          WHITE_BISHOP_1, WHITE_BISHOP_2, WHITE_QUEEN, WHITE_KING]\
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
    draw_board(screen, game_state.board)


# Draw squares on board
def draw_board(screen, board):
    colors = [p.Color("white"), p.Color("light blue")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                              SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if not isinstance(piece, chess_piece.Empty):
                screen.blit(IMAGES[piece], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                  SQUARE_SIZE, SQUARE_SIZE))


def change_pawn_to_queen(screen, row, col, color):
    if color == WHITE:
        screen.blit(IMAGES[WHITE_QUEEN], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                SQUARE_SIZE, SQUARE_SIZE))
    else:
        screen.blit(IMAGES[WHITE_QUEEN], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                SQUARE_SIZE, SQUARE_SIZE))
    p.display.update()


def right_color(is_white_turn, color):
    if (is_white_turn and not color == WHITE) or (
            not is_white_turn and not color == BLACK):
        return False
    return True


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = GameState()
    # valid_moves = game_state.get_valid_moves()
    # move_made = False  # When a move is made.
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

                    move = engine.Move(from_square, to_square, game_state.board)
                    # if move in valid_moves:
                    piece_to_move = game_state.board[src_row][src_col]
                    move_to = game_state.board[dst_row][dst_col]
                    color = piece_to_move.get_color()
                    correct_color = right_color(game_state.is_white_turn, color)
                    valid_move = piece_to_move.is_valid_move(game_state.board, from_square, to_square)
                    eat_opponent_or_empty = color != move_to.get_color()
                    if (not correct_color) or (not valid_move) or (not eat_opponent_or_empty):
                        square_selected, player_clicks = (), []
                        continue

                    game_state.make_move(move)
                    if game_state.check():
                        game_state.undo_move(move)
                    game_state.is_white_turn = not game_state.is_white_turn  # Switch turns (can be done with XOR 1)

                    # Pawn promotion- TODO: change
                    if isinstance(move_to, Pawn):
                        color = move_to.get_color()
                        if (color == WHITE and dst_row == 0) or (
                                color == BLACK and dst_row == 8
                        ):
                            change_pawn_to_queen(screen, dst_row, dst_col, color)
                        # move_made = True
                    square_selected, player_clicks = (), []
            # elif event.type == p.KEYDOWN:
            #     if event.key == p.K_z:  # undo when z iz pressed
            #         game_state.undo_move()
            #         move_made = True  # Todo: maybe remove
        # if move_made:
        #     valid_moves = game_state.get_valid_moves()
        #     move_made = False
        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
