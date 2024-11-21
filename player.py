from setting import *
import time
import math
import pygame

pygame.init()

# Sound Effects
level_up_sound = pygame.mixer.Sound("sounds/level_up.mp3")
dig_sound = pygame.mixer.Sound("sounds/dig.mp3")
dig_sound.set_volume(0.2)


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'spin', 0
        self.original_image = pygame.image.load("pics/drill/spin/1.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = position)
        self.hitbox_rect = self.rect.inflate(-20,0)
        self.screen = pygame.display.set_mode((sc_w, sc_h))

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        self.dig_radius_x = 5
        self.dig_radius_y = 5
        self.damage_multiplier = 1.0
        self.last_dig_time = time.time()
        self.press = True

        self.max_fuel = 10
        self.fuel = 10

        self.inventory = {}
        self.max_inventory = 30

        self.coin = 100
        self.level = 1

        self.angle = 0

    def display_message(self, message, duration):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(duration * 250)  # Wait for 1 second

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        if keys[pygame.K_SPACE] and self.press:
            current_time = time.time()
            if self.fuel > 0:
                if current_time - self.last_dig_time >= 0.5:  # Check if 0.5 seconds have passed
                    self.dig()
                    dig_sound.play()
                    self.fuel -= 1
                    self.last_dig_time = current_time  # Update the last dig time

        elif keys[pygame.K_u] and self.press:
            if self.hitbox_rect.colliderect((6500, 1950), (400 , 250)):
                if self.coin >= 50 * self.level:
                    level_up_sound.play()
                    self.display_message("Level up!", 1)
                    self.press = False
                    self.max_inventory += 10 * self.level
                    self.max_fuel += 10 * self.level
                    self.dig_radius_x += 5
                    self.dig_radius_y += 5
                    self.damage_multiplier += 0.3335
                    self.coin -= 50 * self.level
                    self.speed += 50
                    self.level += 1
                elif self.coin < 50 * self.level:
                    self.display_message(f'You need {50 * self.level} coins!', 1)

        elif keys[pygame.K_e] and self.press:
            self.press = False
            if self.hitbox_rect.colliderect((6500, 2110), (140 , 150)):
                if self.coin >= self.max_fuel and self.max_fuel != self.fuel:
                    self.fuel = self.max_fuel
                    self.coin -= self.max_fuel
                    self.display_message('Fuel Refilled!', 1)
                    
                elif self.coin < self.max_fuel and self.coin > 0:
                    self.fuel += self.coin
                    self.coin -= self.coin
                    self.display_message('Fuel Refilled!', 1)
                else:
                    self.display_message('Not enough coin!', 1)

            if self.hitbox_rect.colliderect((6670, 1950), (250 , 250)):
                if sum(list(self.inventory.values())) > 0:
                    self.display_message("Inventory Sold!", 1)
                    for block,amount in self.inventory.items():
                        if block == "grass" or block == "stone" or block == "dirt" or block == "flower":
                            self.coin += amount
                        elif block == "coal":
                            self.coin += amount * 5
                        elif block == "gold":
                            self.coin += amount * 10
                        elif block == "diamond":
                            self.coin += amount * 50
                    self.inventory = {}
                else:
                    self.display_message("Inventory is empty!", 1)

            if self.hitbox_rect.colliderect((1440, 2000), (400 , 200)):
                if self.coin >= 999:
                    self.display_message('You Won!', 10)
                    pygame.quit()
                elif self.coin < 999:
                    self.display_message('You need 999 coins to pass!', 1)

        elif not keys[pygame.K_e] and not keys[pygame.K_SPACE] and not keys[pygame.K_u]:
            self.press = True

    def dig(self):
        for sprite in self.collision_sprites:
            if (
                sprite.is_diggable 
                and  
                sprite.rect.colliderect(self.hitbox_rect.inflate(self.dig_radius_x, self.dig_radius_y)) 
            ):
                if sprite.ore_type:
                    if sum(list(self.inventory.values())) < self.max_inventory:
                        if sprite.take_damage(math.floor(self.damage_multiplier)):
                            if sprite.ore_type in self.inventory:
                                self.inventory[sprite.ore_type] += 1
                            else:
                                self.inventory[sprite.ore_type] = 1
                    
    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.frame_index += 1000 * dt
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
            self.image = pygame.transform.rotate(self.image, self.angle)
                    
    def rotate(self):
        if self.direction.length() != 0:
            self.angle = math.degrees(math.atan2(self.direction.x, self.direction.y))
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def load_images(self):
        self.frames = {'spin' : []}

        for folder_path, sub_folders, file_names in walk(join('pics', 'drill')):
            if file_names:
                for file_name in file_names:
                    if file_name != '.DS_Store':
                        full_path = f'{folder_path}/{file_name}'
                        surf = pygame.image.load(full_path).convert_alpha()
                        surf = pygame.transform.scale(surf, (50,50))
                        self.frames['spin'].append(surf)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.rotate()
        self.animate(dt)
