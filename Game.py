import pygame
import pygame.time

FPS = 60

class Game:
    pygame.init()

    screen = pygame.display.set_mode([800, 600])

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 100)

        pygame.display.flip()

    pygame.quit()
