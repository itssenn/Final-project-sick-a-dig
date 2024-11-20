import pygame
import time

from setting import *
from player import Player
from sprite import *
from pytmx.util_pygame import load_pygame, pytmx
from groups import Allsprites
from random import randint
from menu import main_menu

pygame.init()

# Menu Screen
main_menu()
  
running = True
display_surface = pygame.display.set_mode((sc_w, sc_h))
pygame.display.set_caption("Dig")
clock = pygame.time.Clock()

# Sounds

# sell_sound = pygame.mixer.Sound("sounds/sell.wav")
# refuel_sound = pygame.mixer.Sound("sounds/refuel.wav")
background_sound = pygame.mixer.Sound("sounds/background.mp3")
background_sound.set_volume(0.2)

#groups
collision_sprites = pygame.sprite.Group()
all_sprites = Allsprites()

def setup():
    map = load_pygame("maps/map.tmx")

    for x, y, image in map.get_layer_by_name("sky").tiles():
        Sprite((x * TILE_SIZE ,y * TILE_SIZE), image, all_sprites)

    for x, y, image in map.get_layer_by_name("block").tiles():
        tile_properties = map.get_tile_properties(x, y, 1)  
        ore_type = tile_properties.get("name") if tile_properties else None  
        if ore_type:
            Block(
                (x * TILE_SIZE, y * TILE_SIZE), 
                image, 
                (all_sprites, collision_sprites), 
                ore_type=ore_type, is_diggable=True
            )
          
    for x, y, image in map.get_layer_by_name("collisionblock").tiles():
        Block(
                (x * TILE_SIZE, y * TILE_SIZE), 
                image, 
                (all_sprites, collision_sprites), 
                ore_type=ore_type, is_diggable=False
            )
    
    for obj in map.get_layer_by_name('obj'):
        Sprite((obj.x ,obj.y), obj.image, all_sprites)
        
setup()

def draw_ui():
    font = pygame.font.Font(None, 74)

    text = font.render(f'Fuel: {player.fuel}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(sc_w / 2, sc_h - 50))
    display_surface.blit(text, text_rect)

    text = font.render(f'Coin: {player.coin}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(sc_w / 2, sc_h - 100))
    display_surface.blit(text, text_rect)

    text = font.render(f'{sum(list(player.inventory.values()))} / {player.max_inventory}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(sc_w / 2, sc_h - 150))
    display_surface.blit(text, text_rect)

    if player.fuel <= 0:
        text = font.render('Fuel is empty!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(sc_w / 2, sc_h / 5))
        display_surface.blit(text, text_rect)
    
    

#Sprite 
player = Player((6400,2050), all_sprites, collision_sprites) 
# Background Sound
background_sound.play(-1)


while running:

    MOUSE_POS = pygame.mouse.get_pos()
    
    #Data
    dt = clock.tick()/1000

    #Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update
    all_sprites.update(dt)

    #Draw
    display_surface.fill('black')
    all_sprites.draw(player.rect.center)
    draw_ui()
    pygame.display.update()

pygame.quit()