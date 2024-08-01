import pygame

class Bullet:
    def __init__(self, position, direction, speed):
        self.position = pygame.math.Vector2(position)
        self.direction = direction.normalize()  # Normalizuje kierunek
        self.speed = speed
        self.radius = 5  # Promień pocisku
        self.active = True  # Status aktywności pocisku
        self.lifetime = 0  # Czas życia pocisku

    def update(self, dt):
        # Aktualizacja pozycji pocisku
        self.position += self.direction * self.speed * dt
        self.lifetime += dt  # Zwiększenie czasu życia pocisku

        # Dezaktywacja pocisku po upływie 3 sekund
        if self.lifetime > 3:
            self.active = False

    def draw(self, screen):
        if self.active:  # Rysuj tylko aktywne pociski
            pygame.draw.circle(screen, 'white', (int(self.position.x+10), int(self.position.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.position.x - self.radius, self.position.y - self.radius, self.radius * 2, self.radius * 2)
