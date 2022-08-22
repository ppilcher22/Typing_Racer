from operator import index
import pygame

WIDTH, HEIGHT = 750, 500
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font & Strings
pygame.font.init()
FONT = pygame.font.SysFont('Courier', 22)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Typing Racer')

FPS = 60

def draw_window(matched_text: str, unmatched_text: str, TEST_TEXT: str):
    
    matched_text_disp = FONT.render(matched_text, True, GREEN, BLACK)
    unmatched_text_disp = FONT.render(unmatched_text, True, RED, BLACK)
    test_text_disp = FONT.render(TEST_TEXT[-(len(TEST_TEXT) \
        - len(matched_text) - len(unmatched_text)):], True, WHITE, BLACK)

    WIN.fill(BLACK)
    WIN.blit(matched_text_disp, (0,0))
    WIN.blit(unmatched_text_disp, (matched_text_disp.get_width(),0))
    WIN.blit(test_text_disp, (matched_text_disp.get_width() + unmatched_text_disp.get_width(),0))
    pygame.display.update()

def check_text(TEST_TEXT: str, INPUT_TEXT: str):
    matched_text = ''
    unmatched_text = ''
    if len(INPUT_TEXT) != 0:
        if INPUT_TEXT[-1] != TEST_TEXT[len(INPUT_TEXT)-1]:
            #TODO - need refactoring
            for i in range(len(INPUT_TEXT)):
                if INPUT_TEXT[i] == TEST_TEXT[i]:
                    matched_text += INPUT_TEXT[i]
                else:
                    unmatched_text += INPUT_TEXT[i]
        else:
            matched_text = INPUT_TEXT
    draw_window(matched_text, unmatched_text, TEST_TEXT)

def main() -> None:
    clock = pygame.time.Clock()
    
    # Text Strings
    INPUT_TEXT = ''
    TEST_TEXT = 'The quick brown fox jumped over the lazy dog'

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    INPUT_TEXT = ''
                elif event.key == pygame.K_BACKSPACE:
                    INPUT_TEXT = INPUT_TEXT[:-1]
                else:
                    INPUT_TEXT += event.unicode       
        check_text(TEST_TEXT, INPUT_TEXT)
            
if __name__ == '__main__':
    main()
    pygame.quit()
