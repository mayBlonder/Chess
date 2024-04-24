
"""
Handling user input and displaying current game state.
"""
import os
import time
import pygame
import constants
from engine import *
from chess_piece import Empty
from pieces.pawn import Pawn
from pieces.king import King


images = {}
PIECES = [BLACK_ROOK_1, BLACK_ROOK_2, BLACK_KNIGHT_1, BLACK_KNIGHT_2,
          BLACK_BISHOP_1, BLACK_BISHOP_2, BLACK_QUEENS[0], BLACK_KING,
          WHITE_ROOK_1, WHITE_ROOK_2, WHITE_KNIGHT_1, WHITE_KNIGHT_2,
          WHITE_BISHOP_1, WHITE_BISHOP_2, WHITE_QUEENS[0], WHITE_KING] \
         + BLACK_PAWNS + WHITE_PAWNS

def int_color_to_string(color):
    """
    :return: A string representing the color of a piece.
    """
    return "white" if color == 0 else "black"


def construct_image_path(piece):
    """
    Constructing image path from piece color and name.
    """
    pic_path = os.path.join("pics", int_color_to_string(piece.get_color()) + "_")
    pic_path += piece.__class__.__name__.lower() + ".png"
    return pic_path


def load_images():
    """
    Adds to a dictionary where the key is a piece and the value is a picture of the piece.
    """
    for piece in PIECES:
        pic_path = construct_image_path(piece)
        images[piece] = pygame.transform.scale(pygame.image.load(pic_path),
                                          (constants.SQUARE_SIZE, constants.SQUARE_SIZE))


#  responsible for all the graphics
def draw_game_state(screen, game_state):
    """
    Draws on the screen the board and the pieces.
    """
    colors = [pygame.Color("white"), pygame.Color("light blue")]
    for row in range(constants.DIMENSION):
        for col in range(constants.DIMENSION):
            color = colors[((row + col) % 2)]
            location = pygame.Rect(col * constants.SQUARE_SIZE, row * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE)
            pygame.draw.rect(screen, color, location)
            piece = game_state.board[row][col]
            if not isinstance(piece, Empty):
                screen.blit(images[piece], location)


def change_pawn_to_queen(screen, row, col, color, game_state):
    """
    Replaces a pawn for a queen when pawn promotion is needed.
    """
    location = pygame.Rect(col * constants.SQUARE_SIZE, row * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE)
    queen = game_state.add_queen(color, row, col)

    # Load image
    pic_path = construct_image_path(queen)
    images[queen] = pygame.transform.scale(pygame.image.load(pic_path),
                                      (constants.SQUARE_SIZE, constants.SQUARE_SIZE))
    
    screen.blit(images[queen], location)
    game_state.board[row][col] = queen
    pygame.display.update(location)


def castling(game_state, dst_col, color, piece_to_move):
    """
    Calls the castling function with the right rook.
    """
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
    pygame.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = GameState()
    
    running = True
    load_images()
    # last click of the user : (row, col)
    square_selected = ()
    # from square to square : [(src_row, src_col), (dst_row, dst_col)]
    player_clicks = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # x, y
                dst_col = location[0] // constants.SQUARE_SIZE
                dst_row = location[1] // constants.SQUARE_SIZE
                
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

                    if not game_state.pre_conditions(color, move_to.get_color()):
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
                        if game_state.check():
                            if game_state.mate():
                                winner_color = not move.piece_moved.get_color()
                                pic_path = "pics\\winner_" + int_color_to_string(winner_color) + ".png"
                                winner_pic = pygame.transform.scale(pygame.image.load(pic_path), (constants.WIDTH, constants.HEIGHT))
                                screen.blit(winner_pic, (0, 0))
                                pygame.display.flip()
                                time.sleep(5)
                                print("MATE: the winner is: {}!".format(int_color_to_string(winner_color)))
                                running = False
                                continue
                            else:
                                print("ERROR: this move is causing your king to be in check.")
                                square_selected, player_clicks = (), []
                                continue
                        # If pawn promotion is needed
                        elif isinstance(piece_to_move, Pawn):
                            color = piece_to_move.get_color()
                            if (color == WHITE and dst_row == 0) or (
                                    color == BLACK and dst_row == 7
                            ):
                                change_pawn_to_queen(screen, dst_row, dst_col, color, game_state)

                    game_state.is_white_turn = not game_state.is_white_turn  # Switch turns
                    square_selected, player_clicks = (), []
        draw_game_state(screen, game_state)
        clock.tick(constants.MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
