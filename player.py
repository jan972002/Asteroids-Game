import pygame
from weapons import Bullet
from enemy import Enemy

class Player:
    def __init__(self, position, size, player_speed, player_image_path, scale, fire_rate, initial_angle, enemy_image_path, enemy_scale, enemy_speed, enemy_spawn_interval):
        self.image = pygame.image.load(player_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale)
        self.position = pygame.math.Vector2(position)
        self.size = size
        self.speed = player_speed
        self.collision_size = 40, 30
        self.collision_offset_x = -10  # Początkowy offset X dla prostokąta kolizji
        self.collision_offset_y = -10
        self.rect = pygame.Rect(self.position.x + self.collision_offset_x, self.position.y + self.collision_offset_y,
                                self.collision_size[0], self.collision_size[1])
        self.bullets = []
        self.is_shooting = False
        self.last_shot_time = 0
        self.fire_rate = fire_rate
        self.angle = initial_angle
        self.initial_angle = initial_angle

        # Enemy attributes
        self.enemies = []
        self.enemy_image_path = enemy_image_path
        self.enemy_scale = enemy_scale
        self.enemy_speed = enemy_speed
        self.enemy_spawn_interval = enemy_spawn_interval
        self.last_spawn_time = 0

        self.shot_sound_path = pygame.mixer.Sound("C:\\Users\jan97\Documents\PyCharm\Platform_Game\\assets\\blaster-2-81267.mp3")
        self.shot_sound_path.set_volume(0.5)
        self.death_sound_path = pygame.mixer.Sound("C:\\Users\jan97\Documents\PyCharm\Platform_Game\\assets\medium-explosion-40472.mp3")
        self.death_sound_path.set_volume(1.2)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.position.x -25, self.position.y-33)).center)
        screen.blit(rotated_image, new_rect.topleft)
        #pygame.draw.rect(screen, 'red', self.rect, 2)

        for bullet in self.bullets:
            if bullet.active:  # Rysowanie tylko aktywnych pocisków
                bullet.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

    def update_angle(self, mouse_x, mouse_y):
        # Obliczanie kierunku do kursora
        direction = pygame.math.Vector2(mouse_x, mouse_y) - self.position  # Obliczanie kierunku
        self.angle = direction.angle_to(pygame.math.Vector2(1, 0)) + self.initial_angle # Obliczanie kąta względem osi X

    def move(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Pozycja kursora
        direction = pygame.math.Vector2(mouse_x, mouse_y) - self.position  # Obliczanie kierunku do kursora

        if direction.length() != 0:  # Sprawdź, czy długość kierunku nie jest zerowa
            direction = direction.normalize()  # Normalizowanie kierunku

        keys = pygame.key.get_pressed()
        move_vector = pygame.math.Vector2(0, 0)  # Wektor ruchu

        # Ruch do przodu i do tyłu w kierunku kursora
        if keys[pygame.K_w]:  # Ruch do przodu w kierunku kursora
            move_vector += direction
        if keys[pygame.K_s]:  # Ruch do tyłu (w przeciwnym kierunku)
            move_vector -= direction

        # Ruch w lewo i prawo (odpowiadający kierunkowi kursora)
        if keys[pygame.K_d]:  # Ruch w lewo
            move_vector += direction.rotate(90)  # Obrót o 90 stopni w lewo
        if keys[pygame.K_a]:  # Ruch w prawo
            move_vector += direction.rotate(-90)  # Obrót o 90 stopni w prawo

        self.position += move_vector * self.speed * dt  # Aktualizacja pozycji gracza

        # Ograniczanie ruchu gracza do rozmiarów okna
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.position.x = max(0, min(self.position.x, screen_width))
        self.position.y = max(0, min(self.position.y, screen_height))

        # Aktualizacja prostokąta kolizji na podstawie pozycji
        self.rect.topleft = (self.position.x + self.collision_offset_x,
                             self.position.y + self.collision_offset_y)

    def shoot(self):
        current_time = pygame.time.get_ticks()  # Pobranie aktualnego czasu w milisekundach
        if current_time - self.last_shot_time >= self.fire_rate:  # Sprawdzenie, czy upłynął czas strzału
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Pozycja myszy
            direction = pygame.math.Vector2(mouse_x, mouse_y) - self.position  # Obliczanie kierunku strzału
            bullet = Bullet(self.position, direction, speed=300)  # Tworzenie pocisku
            self.bullets.append(bullet)  # Dodawanie pocisku do listy
            self.last_shot_time = current_time
            self.shot_sound_path.play()
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.enemy_spawn_interval:
            enemy = Enemy(
                screen_width=pygame.display.get_surface().get_width(),
                screen_height=pygame.display.get_surface().get_height(),
                enemy_image_path=self.enemy_image_path,
                scale=self.enemy_scale,
                speed=self.enemy_speed
            )
            self.enemies.append(enemy)
            self.last_spawn_time = current_time

    def update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.update(self.position, dt)
            if self.check_collision(enemy):
                print("Collision with player!")

    def check_collision(self, enemy):
        for bullet in self.bullets:
            if bullet.active and enemy.get_rect().colliderect(bullet.get_rect()):
                bullet.active = False
                self.enemies.remove(enemy)
                self.death_sound_path.play()
                return True
        return False
