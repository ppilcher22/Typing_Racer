import pygame
import pyjokes
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
FONT_MAIN = pygame.font.SysFont('courier', 22)

# Misc
FPS = 60

def draw_window() -> None:
    WIN.fill(WHITE)
    pygame.display.update()

def draw_text(msg: list, input_text: str) -> None:
    WIN.fill(WHITE)
    for line, y_position in msg:
        comparison_result = get_matched_text(line, input_text)
        game_text_disp = FONT_MAIN.render(line, 1, BLACK)
        WIN.blit(game_text_disp, (50, y_position)) 
    pygame.display.update()

def get_matched_text(current_line: str,current_input: str):
    matched_text = ''
    unmatched_text = ''

    if len(current_input) != 0:
        for i, char in enumerate(current_input):
            if char == current_line[i]:
                matched_text += char
            else:
                unmatched_text = current_input[i:]
                break
    return(matched_text, unmatched_text)

def wrap_game_text(game_text: str) -> list[str]:
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

def get_game_text() -> str:
    return pyjokes.get_joke()

def main() -> None:
    clock = pygame.time.Clock()
    
    input_text = ''
    game_text: str = get_game_text()
    game_text_line_list: list = wrap_game_text(game_text)
    
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
        
        draw_text(game_text_line_list)
        
    pygame.quit()

if __name__ == '__main__':
    main()
    
