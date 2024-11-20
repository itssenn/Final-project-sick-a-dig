from setting import *

class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_postion):
        self.offset.x = - (target_postion[0] - sc_w / 2)
        self.offset.y = - (target_postion[1] - sc_h / 2)

        for sprite in self:
            # print(sprite.image)
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)