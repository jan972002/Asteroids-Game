import pygame
import sys
from player import Player
from enemy import Enemy
from map import Map

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption('Test Game')
running = True
clock = pygame.time.Clock()
FPS = 144
screen_width = screen.get_width()
screen_height = screen.get_height()

map_image = "C:\\Users\\jan97\\Documents\\PyCharm\\Platform_Game\\assets\\bg_02_h.png"
map = Map(map_image, 1400, 800, 0, 0)
player_image_path = "C:\\Users\\jan97\\Documents\\PyCharm\\Platform_Game\\assets\\obraz_2024-07-31_232644492-removebg-preview.png"
enemy_image_path = "C:\\Users\\jan97\\Documents\\PyCharm\\Platform_Game\\assets\\obraz_2024-07-31_234551217-removebg-preview.png"


player = Player(
    position=(600, 500),
    size=30,
    player_speed=250,
    player_image_path=player_image_path,
    scale=(70, 70),
    fire_rate=150,
    initial_angle=-60,
    enemy_image_path=enemy_image_path,
    enemy_scale=(70, 70),
    enemy_speed=120,
    enemy_spawn_interval=1000,  # Spawnowanie co 1 sekunda

)

while running:
    dt = clock.tick(FPS) / 1000.0  # Czas pomiędzy klatkami w sekundach
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Obsługa kliknięcia myszą
            if event.button == 1:  # LPM
                player.is_shooting = True  # Ustawienie na True, gdy przycisk jest wciśnięty
        if event.type == pygame.MOUSEBUTTONUP:  # Obsługa zwolnienia przycisku myszy
            if event.button == 1:  # LPM
                player.is_shooting = False


    mouse_x, mouse_y = pygame.mouse.get_pos()  # Pozycja kursora
    player.update_angle(mouse_x, mouse_y)
    player.move(dt)

    if player.is_shooting:
        player.shoot()

    for bullet in player.bullets:
        bullet.update(dt)

    player.spawn_enemy()
    player.update_enemies(dt)

    map.draw(screen)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
