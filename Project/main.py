import pygame
import pyjokes # type: ignore
from typing import Tuple
pygame.font.init()

# Window setup
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Racer")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
GREEN = (0, 255, 0)
RED = (255, 0, 0,)

# Fonts
FONT_MAIN = pygame.font.SysFont('courier', 32, True)

# Misc
FPS = 60

def draw_text(txt: str, txt_colour: Tuple[int, int, int], coords: Tuple[int, int] ) -> None:
    txt_to_display = FONT_MAIN.render(txt, True, txt_colour)
    WIN.blit(txt_to_display, coords)

def draw_window(msg: list, input_text_list: list) -> None:
    WIN.fill(WHITE)
    for i, (line, y_position) in enumerate(msg):
        matched_text, incorrect_text = get_matched_text(line, input_text_list[i])
        remaining_text = line[len(matched_text) + len(incorrect_text):]
        
        draw_text(matched_text, GREEN, (50, y_position))
        draw_text(incorrect_text, RED, (50 + FONT_MAIN.size(matched_text)[0], y_position))
        draw_text(remaining_text, BLACK, (50 + FONT_MAIN.size(matched_text)[0] 
                                    + FONT_MAIN.size(incorrect_text)[0], y_position))
    pygame.display.update()

def get_matched_text(current_line: str,current_input: str) -> tuple:
    matched_text = ''
    incorrect_text = ''

    if len(current_input) != 0: 
        for i, char in enumerate(current_input): 
            if char != current_line[i]:
                matched_text = current_input[:i]
                incorrect_text = current_input[i:]
                break
        else:
            matched_text = current_input
                
    return(matched_text, incorrect_text)

def wrap_text(game_text: str) -> list[Tuple[str, int]]:
    font_height = FONT_MAIN.get_height()
    line_spacing = 2
    line_y = 0
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

        # Add the line of text to the list along with the y cords
        game_text_line_list.append((game_text[:i], line_y))
        line_y += font_height + line_spacing
        
        # updates the string to remove the line that has been dispalyed
        game_text = game_text[i:]

    return game_text_line_list

def add_space_char(words: list[str]) -> list[str]:
    lst_len = len(words)
    for i, word in enumerate(words):
        if i != lst_len - 1:
            words[i] = word + ' '
    return words

def get_game_text() -> str:
    return pyjokes.get_joke()

def main() -> None:
    clock = pygame.time.Clock()
    
    input_text= ''
    game_text = get_game_text()
    game_text_line_list = wrap_text(game_text)
    game_text_words = add_space_char(game_text.split())
    # words_per_line = pass
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        input_text_lst = wrap_text(input_text)
        draw_window(game_text_line_list, input_text_lst)
        
    pygame.quit()

if __name__ == '__main__':
    main()
    
