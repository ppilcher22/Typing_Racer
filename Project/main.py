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

def draw_window(correct_words: int, matched_input: str, incorrect_text: str, 
                game_text: str, game_text_words: list[str], words_per_line: list[int]) -> None:
    
    WIN.fill(WHITE)
    # loop through all words to display
    current_line = 0
    current_line_text = ''
    correct_words_display = FONT_MAIN.render('', True, GREEN)
    for i, word in enumerate(game_text_words):
        if i >= words_per_line[current_line]:
            current_line =+ 1
            current_line_text = ''
        current_line_text += word
        if i < correct_words:
            correct_words_display = FONT_MAIN.render(current_line_text, True, GREEN)
            WIN.blit(correct_words_display, (0, get_line_spacing(current_line)))
        elif incorrect_text:
            pass
        else:
            remaining_text = ''.join(game_text_words[correct_words:words_per_line[current_line]])
            remaining_text_display = FONT_MAIN.render(remaining_text, True, BLACK)
            WIN.blit(remaining_text_display, (correct_words_display.get_width(), get_line_spacing(current_line)))

    
    pygame.display.update()

#TODO needs improving
def get_line_spacing(current_line: int) -> int:
    return current_line * FONT_MAIN.get_height() * 2 

def get_matched_text(current_word: str, current_input: str) -> Tuple[str, str]:
    matched_text = ''
    incorrect_text = ''

    if len(current_input) != 0: 
        for i, char in enumerate(current_input): 
            if char != current_word[i]:
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

def get_words_per_line(game_text_line_list: list[Tuple[str, int]], game_text_words: list[str]) -> list[int]:
    line_word_count = []
    lst_len = len(game_text_line_list)
    for i, line in enumerate(game_text_line_list):
        if i != lst_len - 1:
            line_word_count.append(line[0].count(' '))
        else:
            line_word_count.append(line[0].count(' ') + 1)
    return line_word_count

def get_game_text() -> str:
    return pyjokes.get_joke()

def game_complete():
    pass

def main() -> None:
    clock = pygame.time.Clock()
    
    input_text= ''
    correct_words: int = 0
    game_text = get_game_text()
    
    #TODO - remove after testing
    print(game_text)
   
    game_text_words = add_space_char(game_text.split())
    words_per_line = get_words_per_line(wrap_text(game_text), game_text_words)
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        
        # check if the current input matches the current word
        if correct_words < len(game_text_words):
            matched_input, incorrect_text = get_matched_text(game_text_words[correct_words], input_text)
            if matched_input == game_text_words[correct_words]:
                correct_words += 1
                input_text = ''
        else:
            game_complete()

        draw_window(correct_words, matched_input, incorrect_text, game_text, 
                                        game_text_words, words_per_line)
        
    pygame.quit()

if __name__ == '__main__':
    main()
    
