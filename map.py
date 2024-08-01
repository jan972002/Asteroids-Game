import pygame
import random




class Map:
    def __init__(self, map_image, map_width, map_height, map_pos_x, map_pos_y):
        self.background = pygame.image.load(map_image).convert()
        self.background = pygame.transform.scale(self.background, (map_width, map_height))
        self.width = map_width
        self.height = map_height
        self.position_x = map_pos_x
        self.position_y= map_pos_y
    def draw(self, screen):
        screen.blit(self.background,(self.position_x, self.position_y ))
