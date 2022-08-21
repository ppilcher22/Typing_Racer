import pygame

WIDTH, HEIGHT = 750, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TEST_TEXT = 'The quick brown fox jumped over the lazy dog'
pygame.display.set_caption('Typing Racer')

def main():

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()

if __name__ == '__main__':
    main()
