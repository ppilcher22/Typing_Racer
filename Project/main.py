import os
import pygame
import pyjokes  # type: ignore
from typing import Tuple
pygame.font.init()

# Window setup
WIDTH, HEIGHT = 900, 600
os.environ['SDL_VIDEO_WINDOW_POS'] = '1920, 300'
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Racer")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
GREEN = (0, 255, 0)
RED = (255, 0, 0,)
INCORRECT_TEXT_RED = (54, 33, 34)
INCORRECRT_TEXT_BG = (181, 69, 73)

# Fonts
FONT_MAIN = pygame.font.SysFont('courier', 60, True)

# Misc
FPS = 60


def draw_game_text(game_text_lst: list[Tuple[str, str, str]]) -> None:
    WIN.fill(BLACK)
    for line, (correct_text, incorrect_text, remaining_text) in enumerate(game_text_lst):
        # display correct text
        correct_text_disp = FONT_MAIN.render(correct_text, True, GREEN)
        WIN.blit(correct_text_disp, (0, get_line_spacing(line)))
        # display incorrect text
        incorrect_text_disp = FONT_MAIN.render(
            incorrect_text, True, INCORRECT_TEXT_RED, INCORRECRT_TEXT_BG)
        WIN.blit(incorrect_text_disp,
                 (correct_text_disp.get_width(), get_line_spacing(line)))
        # display remaining text
        remaining_text_disp = FONT_MAIN.render(remaining_text, True, WHITE)
        WIN.blit(remaining_text_disp, (correct_text_disp.get_width() +
                 incorrect_text_disp.get_width(), get_line_spacing(line)))
    pygame.display.update()


def get_line_spacing(current_line: int) -> int:
    # TODO needs improving
    return current_line * (FONT_MAIN.get_height() + 2)


def get_correct_text(input_text: str, game_text: str) -> Tuple[str, str, str]:
    correct_text = ''
    incorrect_text = ''
    remaining_text = ''

    if len(input_text):
        for i, char in enumerate(input_text):
            if char != game_text[i]:
                correct_text = input_text[:i]
                incorrect_text = game_text[len(correct_text):len(input_text)]
                break
        else:
            correct_text = input_text
    remaining_text = game_text[len(correct_text) + len(incorrect_text):]

    return (correct_text, incorrect_text, remaining_text)


def wrap_text(game_text: str) -> list[str]:
    game_text_line_list = []

    # loop until game_text is empty
    while game_text:
        i = 1

        # determine width of the line relative to the width of the window
        while FONT_MAIN.size(game_text[:i])[0] < WIDTH - 100 and i < len(game_text):
            i += 1

        # adjust index to find last space before end of line to avoid word chopping
        if i < len(game_text):
            i = game_text.rfind(' ', 0, i) + 1

        # Add the line of text to the list
        game_text_line_list.append(game_text[:i])

        # updates the string to remove the line that has been dispalyed
        game_text = game_text[i:]

    return game_text_line_list


def get_game_text() -> str:
    return pyjokes.get_joke()


def game_complete():
    print('You won')


def main() -> None:
    clock = pygame.time.Clock()

    input_text = ''
    previous_line_input_text = ''
    game_text = wrap_text(get_game_text())
    current_line = 0
    proccessed_game_lst = [('', '', line) for line in game_text]

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # if deleting will take the user back a line, reset the input text from the previous line
                    if proccessed_game_lst[current_line][2] == game_text[current_line] \
                            and current_line != 0:
                        current_line -= 1
                        input_text = previous_line_input_text
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        proccessed_game_lst[current_line] = get_correct_text(
            input_text, game_text[current_line])

        # check if the length of the current input equals the length of the current line
        if len(input_text) == len(game_text[current_line]):
            # check if the last line of the game text is matched to last line of the input
            if proccessed_game_lst[current_line][0] == game_text[len(game_text) - 1] and current_line == len(game_text) - 1:
                game_complete()
                run = False
            # set variables for new line
            current_line += 1
            previous_line_input_text = input_text
            input_text = ''

        draw_game_text(proccessed_game_lst)

    pygame.quit()


if __name__ == '__main__':
    main()
