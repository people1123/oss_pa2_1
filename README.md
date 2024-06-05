import pygame
import random

# 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
grid_size = 50  # 격자 크기
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('길건너 친구들')

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 플레이어 설정
player_size = grid_size
player_pos = [screen_width // 2, screen_height - grid_size]

# 자동차 설정
car_size = [grid_size, grid_size // 2]
car_speed = 1

# 자동차 리스트 생성 함수
def create_cars(num_cars):
    cars = []
    occupied_positions = set()
    for _ in range(num_cars):
        while True:
            car_x = random.randint(0, (screen_width // grid_size) - 1) * grid_size
            car_y = random.randint(0, (screen_height // 2 // grid_size) - 1) * grid_size
            if (car_x, car_y) not in occupied_positions:
                occupied_positions.add((car_x, car_y))
                cars.append({'pos': [car_x, car_y], 'speed': random.choice([-car_speed, car_speed])})
                break
    return cars

cars = create_cars(10)

# 시계 설정
clock = pygame.time.Clock()

def detect_collision(player_pos, car_pos):
    px, py = player_pos
    cx, cy = car_pos

    if (px >= cx and px < cx + car_size[0]) or (cx >= px and cx < px + player_size):
        if (py >= cy and py < cy + car_size[1]) or (cy >= py and cy < py + player_size):
            return True
    return False

def draw_player():
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

def draw_cars(cars):
    for car in cars:
        pygame.draw.rect(screen, RED, (car['pos'][0], car['pos'][1], car_size[0], car_size[1]))

# 게임 루프
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= grid_size
    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size:
        player_pos[0] += grid_size
    if keys[pygame.K_UP] and player_pos[1] > 0:
        for car in cars:
            car['pos'][1] += grid_size

    screen.fill(WHITE)

    # 자동차 움직임 및 화면 경계에서 위치 재설정
    occupied_positions = set((car['pos'][0], car['pos'][1]) for car in cars)
    for car in cars:
        new_x = car['pos'][0] + car['speed'] * grid_size
        if new_x >= screen_width or new_x < 0 or (new_x, car['pos'][1]) in occupied_positions:
            car['speed'] = -car['speed']
            new_x = car['pos'][0] + car['speed'] * grid_size
        occupied_positions.discard((car['pos'][0], car['pos'][1]))
        car['pos'][0] = new_x
        occupied_positions.add((car['pos'][0], car['pos'][1]))

        if detect_collision(player_pos, car['pos']):
            game_over = True

    draw_player()
    draw_cars(cars)

    pygame.display.update()
    clock.tick(10)

pygame.quit()
