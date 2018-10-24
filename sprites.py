import pygame

space_ship_1 = pygame.image.load('sprites/space_ship.png')
space_ship_2 = pygame.image.load('sprites/space_ship.png')
space_ship_crash = pygame.image.load('sprites/explosion.png')
space_ship_damage = pygame.image.load('sprites/space_ship_damage.png')

enemy_space_ship_1 = pygame.image.load('sprites/enemy_space_ship.png')
enemy_space_ship_2 = pygame.image.load('sprites/enemy_space_ship.png')

space_ship_list = [space_ship_1, space_ship_2]
space_ship_damage_list = [space_ship_damage]
enemy_space_ship_list = [enemy_space_ship_1, enemy_space_ship_2]

asteroid = pygame.image.load('sprites/asteroid.png')

missile = pygame.image.load('sprites/missile.png')

icon = pygame.image.load('sprites/icon.png')
background = pygame.image.load('sprites/background.png')


all_sprites = [space_ship_1, space_ship_2, space_ship_crash, space_ship_damage, asteroid, enemy_space_ship_1, enemy_space_ship_2, missile, icon, background]
