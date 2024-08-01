import pygame
import random

class Enemy:
    def __init__(self, screen_width, screen_height, enemy_image_path, scale, speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load(enemy_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale)
        self.position = self.spawn_position()  # Pozycja startowa wroga
        self.speed = speed
        self.rect = self.image.get_rect(center=self.position)
        self.active = True  # Status aktywności wroga

    def spawn_position(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.uniform(0, self.screen_width)
            y = 0
        elif edge == 'bottom':
            x = random.uniform(0, self.screen_width)
            y = self.screen_height
        elif edge == 'left':
            x = 0
            y = random.uniform(0, self.screen_height)
        elif edge == 'right':
            x = self.screen_width
            y = random.uniform(0, self.screen_height)
        return pygame.math.Vector2(x, y)

    def update(self, player_position, dt):
        direction = player_position - self.position
        if direction.length() != 0:
            direction = direction.normalize()
        self.position += direction * self.speed * dt

        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def get_rect(self):
        return self.rect

