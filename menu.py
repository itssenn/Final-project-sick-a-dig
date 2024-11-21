import pygame
from setting import *
pygame.init()

def main_menu():
    display_surface = pygame.display.set_mode((sc_w, sc_h))
    pygame.display.set_caption("Menu")
    clock = pygame.time.Clock()
    while True:
        font = pygame.font.Font(None, 50)
        text = font.render("Press any key to start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(sc_w / 2, sc_h / 2))
        display_surface.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return
    quit()