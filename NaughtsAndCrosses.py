import random
import sys
import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_CAPTION = "Naughts and Crosses"

PLAYER = "player"
COMPUTER = "computer"
X = "x"
O = "o"
BOARD_SIZE = 300
BOX_SIZE = BOARD_SIZE / 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 75, 255)
GREY = (100, 100, 100)

pygame.init()
WINDOW_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=True)
pygame.display.set_caption(WINDOW_CAPTION)
CLOCK = pygame.time.Clock()


class TextButton:
    def __init__(self, width, height, x, y, text, text_color, text_size, outline_color):
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.outline_color = outline_color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        draw_text(surface, self.text, self.text_color, self.rect.center, self.text_size)
        if self.is_over(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, self.outline_color, self.rect, width=3)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)


def main():
    game_board = [" " for _ in range(9)]
    player_letter, computer_letter = assign_letters()
    current_turn = PLAYER if player_letter == X else COMPUTER
    boxes = create_boxes(BOX_SIZE)

    play_again_button = TextButton(200, 75, WINDOW_WIDTH / 2 - 200 / 2, 70, "Play Again", GREEN, 32, WHITE)
    quit_button = TextButton(150, 75, WINDOW_WIDTH / 2 - 150 / 2, WINDOW_HEIGHT - 70 - 50, "Quit", RED, 32, WHITE)

    game_over = False
    running = True
    while running:  # game loop
        check_for_quit()

        WINDOW_SURFACE.fill(BLACK)

        current_turn = update_board(game_board, boxes, current_turn, player_letter, computer_letter) if not game_over else COMPUTER
        draw_board(WINDOW_SURFACE, game_board, boxes, BOARD_SIZE, player_letter, True if current_turn == PLAYER else False)

        if is_winner(game_board, player_letter):
            draw_text(WINDOW_SURFACE, "Well Done! You have won!", WHITE, (WINDOW_WIDTH / 2, 50), 32)
            game_over = True
        elif is_winner(game_board, computer_letter):
            draw_text(WINDOW_SURFACE, "Oh no! You Lost!", WHITE, (WINDOW_WIDTH / 2, 50), 32)
            game_over = True
        elif is_board_full(game_board):
            draw_text(WINDOW_SURFACE, "The game is Tie!", WHITE, (WINDOW_WIDTH / 2, 50), 32)
            game_over = True

        if game_over:
            play_again_button.draw(WINDOW_SURFACE)
            quit_button.draw(WINDOW_SURFACE)

            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if event.button == pygame.BUTTON_LEFT:
                    if play_again_button.is_over(pygame.mouse.get_pos()):
                        main()
                    elif quit_button.is_over(pygame.mouse.get_pos()):
                        terminate()
        else:
            draw_text(WINDOW_SURFACE, "Click a box to make a move...", WHITE, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50), 38)

        pygame.display.flip()

    terminate()


def draw_text(surface, text, color, center, size):
    font = pygame.font.Font("freesansbold.ttf", size)
    font_surface = font.render(text, True, color)
    font_rect = font_surface.get_rect()
    font_rect.center = center
    surface.blit(font_surface, font_rect)


def draw_cross(surface, color, center, size, line_width=1):
    pygame.draw.line(surface, color, (center[0] - size / 2, center[1] - size / 2), (center[0] + size / 2, center[1] + size / 2), width=line_width)
    pygame.draw.line(surface, color, (center[0] - size / 2, center[1] + size / 2), (center[0] + size / 2, center[1] - size / 2), width=line_width)


def draw_letter_selection_screen(surface, x_rect, o_rect):
    surface.fill(BLACK)

    draw_text(surface, "Choose Your Letter", WHITE, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100), 48)

    # draw the X and O options
    if x_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(surface, WHITE, x_rect, width=3)  # box outline for X
    if o_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(surface, WHITE, o_rect, width=3)  # box outline for O
    draw_cross(surface, GREEN, x_rect.center, 60, line_width=3)
    pygame.draw.circle(surface, BLUE, o_rect.center, 30, width=3)


def assign_letters():
    player_letter, computer_letter = "", ""

    x_rect = pygame.Rect(WINDOW_WIDTH / 2 - 100 - 10, WINDOW_HEIGHT / 2 - 100 / 2, 100, 100)
    o_rect = pygame.Rect(WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 - 100 / 2, 100, 100)

    getting_letters = True
    while getting_letters:
        check_for_quit()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if x_rect.collidepoint(pygame.mouse.get_pos()):
                        player_letter, computer_letter = X, O
                        getting_letters = False
                    elif o_rect.collidepoint(pygame.mouse.get_pos()):
                        player_letter, computer_letter = O, X
                        getting_letters = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player_letter, computer_letter = X, O
                    getting_letters = False
                elif event.key == pygame.K_o:
                    player_letter, computer_letter = O, X
                    getting_letters = False

        draw_letter_selection_screen(WINDOW_SURFACE, x_rect, o_rect)
        pygame.display.flip()

    return player_letter, computer_letter


def draw_board(surface, board, boxes, size, player_letter, is_player_turn):
    screen_center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    box_size = size / 3
    half_box_size = box_size / 2
    center_board_edge_dist = box_size / 2 + box_size

    # draw the board lines
    pygame.draw.line(surface, WHITE, (screen_center[0] - half_box_size, screen_center[1] - center_board_edge_dist), (screen_center[0] - half_box_size, screen_center[1] + center_board_edge_dist))
    pygame.draw.line(surface, WHITE, (screen_center[0] + half_box_size, screen_center[1] - center_board_edge_dist), (screen_center[0] + half_box_size, screen_center[1] + center_board_edge_dist))
    pygame.draw.line(surface, WHITE, (screen_center[0] - center_board_edge_dist, screen_center[1] - half_box_size), (screen_center[0] + center_board_edge_dist, screen_center[1] - half_box_size))
    pygame.draw.line(surface, WHITE, (screen_center[0] - center_board_edge_dist, screen_center[1] + half_box_size), (screen_center[0] + center_board_edge_dist, screen_center[1] + half_box_size))

    # draw the board contents (the naughts and crosses)
    for letter, box in zip(board, boxes, strict=True):
        if box.collidepoint(pygame.mouse.get_pos()) and is_player_turn and letter not in "xo":
            if player_letter == X:
                draw_cross(surface, GREY, box.center, box.width - 40)
            elif player_letter == O:
                pygame.draw.circle(surface, GREY, box.center, (box.width - 40) / 2, width=1)

        if letter == X:
            draw_cross(surface, GREEN, box.center, box.width - 40)
        elif letter == O:
            pygame.draw.circle(surface, BLUE, box.center, (box.width - 40) / 2, width=1)


def create_boxes(box_size):
    # returns an array of pygame.Rect objects that represent each square on the board
    screen_center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    half_box_size = box_size / 2
    center_board_edge_dist = box_size / 2 + box_size

    rect0 = pygame.Rect(screen_center[0] - center_board_edge_dist, screen_center[1] + half_box_size, box_size, box_size)
    rect1 = pygame.Rect(screen_center[0] - half_box_size, screen_center[1] + half_box_size, box_size, box_size)
    rect2 = pygame.Rect(screen_center[0] + half_box_size, screen_center[1] + half_box_size, box_size, box_size)

    rect3 = pygame.Rect(screen_center[0] - center_board_edge_dist, screen_center[1] - half_box_size, box_size, box_size)
    rect4 = pygame.Rect(screen_center[0] - half_box_size, screen_center[1] - half_box_size, box_size, box_size)
    rect5 = pygame.Rect(screen_center[0] + half_box_size, screen_center[1] - half_box_size, box_size, box_size)

    rect6 = pygame.Rect(screen_center[0] - center_board_edge_dist, screen_center[1] - center_board_edge_dist, box_size, box_size)
    rect7 = pygame.Rect(screen_center[0] - half_box_size, screen_center[1] - center_board_edge_dist, box_size, box_size)
    rect8 = pygame.Rect(screen_center[0] + half_box_size, screen_center[1] - center_board_edge_dist, box_size, box_size)

    return [rect0, rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8]


def make_move(board, letter, move):
    board[move] = letter


def get_random_move(board):
    # returns a random, valid move
    while True:
        # generate a random move, then check if it's valid
        move = random.randint(0, len(board) - 1)
        if board[move] == " ":
            return move


def is_board_full(board):
    # returns True if the given board has no " " left
    return " " not in board


def get_board_copy(board: list):
    # returns a copy of the given board
    return board.copy()


def is_winner(bo, le):
    # bo: board, le: letter (shortened cos of the typing)
    return ((bo[0] == le and bo[1] == le and bo[2] == le) or # across bottom
            (bo[3] == le and bo[4] == le and bo[5] == le) or # across middle
            (bo[6] == le and bo[7] == le and bo[8] == le) or # across top
            (bo[0] == le and bo[3] == le and bo[6] == le) or # down left
            (bo[1] == le and bo[4] == le and bo[7] == le) or # down middle
            (bo[2] == le and bo[5] == le and bo[8] == le) or # down right
            (bo[0] == le and bo[4] == le and bo[8] == le) or # diagonal
            (bo[2] == le and bo[4] == le and bo[6] == le))   # diagonal


def update_board(board: list, boxes, turn, player_letter, computer_letter):
    if turn == PLAYER:
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if event.button == pygame.BUTTON_LEFT:
                for index, box in enumerate(boxes): # loop through each box, see if it was clicked
                    if box.collidepoint(pygame.mouse.get_pos()) and board[index] == " ": # make sure the box does not already contain a letter
                        make_move(board, player_letter, index)
                        return COMPUTER

    elif turn == COMPUTER:
        # the general structure of the algorithm is defined below

        # can computer win on current turn?
        #   if yes then play the move
        #   if no then check if the player will win on their next turn
        #     if yes then block their move (obviously doesn't matter if the player has 2 ways of winning, can only block 1)
        #     if no then play a random move

        # loop through all the board squares
        # looking to see if computer can win or can block the player from winning
        for index, board_letter in enumerate(board):
            if board_letter == " ": # only check box if it is empty

                # check for computer win first
                board_copy = get_board_copy(board)
                make_move(board_copy, computer_letter, index)
                if is_winner(board_copy, computer_letter): # computer can win - so win
                    make_move(board, computer_letter, index)
                    return PLAYER

                # check for player win second
                board_copy = get_board_copy(board)
                make_move(board_copy, player_letter, index)
                if is_winner(board_copy, player_letter): # player can win - so block their move
                    make_move(board, computer_letter, index)
                    return PLAYER

        # not a game changing turn, so play a random move
        make_move(board, computer_letter, get_random_move(board))
        return PLAYER

    return turn


def check_for_quit():
    if pygame.event.get(pygame.QUIT):
        terminate()


def terminate():
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
