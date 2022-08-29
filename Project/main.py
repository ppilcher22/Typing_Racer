import os
import time
import pygame
import pyjokes  # type: ignore
from typing import Tuple
pygame.font.init()

# Window setup
WIDTH, HEIGHT = 1200, 750
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
TEXT_BOX_BG = (41, 38, 38)

# Fonts
FONT_MAIN = pygame.font.SysFont('courier', 45)
FONT_STATS = pygame.font.SysFont('arial', 36)

# Assets
BG_MAIN = pygame.transform.scale(pygame.image.load
(os.path.join('Project\\assets', 'mechanicalkeyboards_bg.png')), (WIDTH, HEIGHT))


# Misc
FPS = 60


def draw(game_text_lst: list[Tuple[str, str, str]], current_line: int, current_time: int, 
            wpm: float) -> None:
    
    WIN.blit(BG_MAIN, (0, 0))
    # draw stats rect
    stats_rect = pygame.draw.rect(WIN, TEXT_BOX_BG, (0, 0, WIDTH, FONT_STATS.get_height() + 10), 0)

    # draw timer
    time_text = FONT_STATS.render(f"| Time elapsed: {round(current_time, 2)}", True, WHITE)
    WIN.blit(time_text, (stats_rect.width/2, stats_rect.centery - FONT_STATS.get_height() / 2))

    # draw wpm
    wpm_text = FONT_STATS.render(f"WPM: {round(wpm)}", True, WHITE)
    WIN.blit(wpm_text, (stats_rect.centerx - wpm_text.get_width() - 10, stats_rect.centery - FONT_STATS.get_height() / 2))
    
    # draw game text
    text_box_position = (50, 200)
    pygame.draw.rect(WIN, TEXT_BOX_BG, (text_box_position[0], text_box_position[1], 
    WIDTH - 100, HEIGHT / 2 ), 0)
    for line, (correct_text, incorrect_text, remaining_text) in enumerate(game_text_lst):
        line_spacing = get_line_spacing(line) + text_box_position[1]
        # display correct text
        correct_text_disp = FONT_MAIN.render(correct_text, True, GREEN)
        WIN.blit(correct_text_disp, (text_box_position[0], line_spacing))
        # display incorrect text
        incorrect_text_disp = FONT_MAIN.render(
            incorrect_text, True, INCORRECT_TEXT_RED, INCORRECRT_TEXT_BG)
        WIN.blit(incorrect_text_disp,
                 (correct_text_disp.get_width() + text_box_position[0], line_spacing))
        # display remaining text
        remaining_text_disp = FONT_MAIN.render(remaining_text, True, WHITE)
        WIN.blit(remaining_text_disp, (correct_text_disp.get_width() +
                 incorrect_text_disp.get_width() + text_box_position[0], line_spacing))

        # draw cursor
        if line == current_line:
            cursor_position_x = correct_text_disp.get_width() \
                + incorrect_text_disp.get_width() + text_box_position[0]
            # blink the cursor
            if time.time() % 1 > 0.5:
                pygame.draw.rect(WIN, WHITE, pygame.Rect(
                    cursor_position_x, line_spacing , 3, FONT_MAIN.get_height()))
    
    pygame.display.update()


def get_line_spacing(current_line: int) -> int:
    # TODO needs improving
    return current_line * (FONT_MAIN.get_height() + 2)


def get_correct_text(input_text: str, game_text: str, previous_line_incorrect_text: str
                                                                ) -> Tuple[str, str, str]:
    correct_text = ''
    incorrect_text = ''
    remaining_text = ''

    if previous_line_incorrect_text:
        incorrect_text = game_text[len(correct_text):len(input_text)]
    elif len(input_text):
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
        while FONT_MAIN.size(game_text[:i])[0] < WIDTH - 105 and i < len(game_text):
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

def get_wpm(game_text_lst: list[Tuple[str, str, str]], current_time: float) -> float:
    correct_chars = 0
    for line in game_text_lst:
        correct_chars += len(line[0])
    wpm = correct_chars / 5 / current_time * 60
    return wpm

def main() -> None:
    clock = pygame.time.Clock()

    input_text = ''
    current_line = 0
    start_time = 0
    wpm = 0
    while True:
        game_text = wrap_text(get_game_text())
        if len(game_text) >= 2:
            break
        
    input_text_for_line = ['' for _ in game_text]
    proccessed_game_lst = [('', '', line) for line in game_text]

    run = True
    while run:
        clock.tick(FPS)

        if start_time > 0:
            current_time = time.time() - start_time
            wpm = get_wpm(proccessed_game_lst, current_time)
        else:
            current_time = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if start_time == 0:
                    start_time = time.time()
                if event.key == pygame.K_BACKSPACE:
                    # if deleting will take the user back a line, reset the input text from the previous line
                    if proccessed_game_lst[current_line][2] == game_text[current_line] \
                            and current_line != 0:
                        current_line -= 1
                        input_text = input_text_for_line[current_line]
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        proccessed_game_lst[current_line] = get_correct_text(
            input_text, game_text[current_line], proccessed_game_lst[current_line - 1][1])

        # check if the length of the current input equals the length of the current line
        if len(input_text) == len(game_text[current_line]):
            # check if the last line of the game text is matched to last line of the input
            if proccessed_game_lst[current_line][0] == game_text[len(game_text) - 1] and current_line == len(game_text) - 1:
                game_complete()
                run = False
            # set variables for new line if not at last line a
            if current_line != len(game_text) - 1:
                input_text_for_line[current_line] = input_text
                input_text = ''
                current_line += 1
        # limit the length of the input for incorrect inputs on the last line
        elif len(input_text) > len(game_text[current_line]):
            input_text = input_text[:-1]

        draw(proccessed_game_lst, current_line, current_time, wpm)

        


    pygame.quit()


if __name__ == '__main__':
    main()
