import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sound effects
move_sound = pygame.mixer.Sound("move.mp3")   # 블록 이동 소리
rotate_sound = pygame.mixer.Sound("move.mp3")  # 회전 소리
drop_sound = pygame.mixer.Sound("drop.mp3")  # 하드 드롭 소리
clear_sound = pygame.mixer.Sound("clear.mp3")  # 줄 클리어 소리
gameover_sound = pygame.mixer.Sound("game_over.mp3")  # 줄 클리어 소리
combo1_sound = pygame.mixer.Sound("combo_1.ogg")  # 콤보 소리
combo2_sound = pygame.mixer.Sound("combo_2.ogg")  # 콤보 소리
combo3_sound = pygame.mixer.Sound("combo_3.ogg")  # 콤보 소리
combo4_sound = pygame.mixer.Sound("combo_4.ogg")  # 콤보 소리
combo5_sound = pygame.mixer.Sound("combo_5.ogg")  # 콤보 소리
combo6_sound = pygame.mixer.Sound("combo_6.ogg")  # 콤보 소리
combo7_sound = pygame.mixer.Sound("combo_7.ogg")  # 콤보 소리
combo8_sound = pygame.mixer.Sound("combo_8.ogg")  # 콤보 소리
combo9_sound = pygame.mixer.Sound("combo_9.ogg")  # 콤보 소리
combo10_sound = pygame.mixer.Sound("combo_10.ogg")  # 콤보 소리
combo11_sound = pygame.mixer.Sound("combo_11.ogg")  # 콤보 소리
combo12_sound = pygame.mixer.Sound("combo_12.ogg")  # 콤보 소리
combo13_sound = pygame.mixer.Sound("combo_13.ogg")  # 콤보 소리
combo14_sound = pygame.mixer.Sound("combo_14.ogg")  # 콤보 소리
combo15_sound = pygame.mixer.Sound("combo_15.ogg")  # 콤보 소리
combo16_sound = pygame.mixer.Sound("combo_16.ogg")  # 콤보 소리

# Set volume for combo sounds
move_sound.set_volume(0.4)
rotate_sound.set_volume(0.4)
drop_sound.set_volume(0.4)
clear_sound.set_volume(0.4)
gameover_sound.set_volume(0.4)
combo1_sound.set_volume(1.0)
combo2_sound.set_volume(1.0)
combo3_sound.set_volume(1.0)
combo4_sound.set_volume(1.0)
combo5_sound.set_volume(1.0)
combo6_sound.set_volume(1.0)
combo7_sound.set_volume(1.0)
combo8_sound.set_volume(1.0)
combo9_sound.set_volume(1.0)
combo10_sound.set_volume(1.0)
combo11_sound.set_volume(1.0)
combo12_sound.set_volume(1.0)
combo13_sound.set_volume(1.0)
combo14_sound.set_volume(1.0)
combo15_sound.set_volume(1.0)
combo16_sound.set_volume(1.0)

# Screen dimensions
SCREEN_WIDTH = 300  # 기존 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SIDE_PANEL_WIDTH = 150  # 좌측과 우측 패널의 너비
TOTAL_WIDTH = SCREEN_WIDTH + 2 * SIDE_PANEL_WIDTH  # 전체 화면 너비

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0), # Yellow
    (128, 0, 128),  # Purple
    (0, 0, 255),  # Blue
    (255, 127, 0),    # Orange
    (0, 255, 0),  # Green
    (255, 0, 0)     # Red
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # Cyan
    [[1, 1], [1, 1]],  # Yellow
    [[0, 1, 0], [1, 1, 1]],  # Purple
    [[1, 0, 0], [1, 1, 1]],  # Blue
    [[0, 0, 1], [1, 1, 1]],  # Orange
    [[0, 1, 1], [1, 1, 0]],  # Green
    [[1, 1, 0], [0, 1, 1]]  # Red
]

class Tetrimino:
    def __init__(self, shape_index):
        self.shape_index = shape_index
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.adjust_position()

    def rotate_counterclockwise(self):
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        self.adjust_position()

    def adjust_position(self):
        while not self.is_valid_position():
            if self.x < 0:
                self.x += 1
            elif self.x + len(self.shape[0]) > GRID_WIDTH:
                self.x -= 1
            elif self.y + len(self.shape) > GRID_HEIGHT:
                self.y -= 1
            else:
                self.y -= 1  # Move up if blocked by other blocks
                if self.y < 0:
                    break

    def is_valid_position(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.x + j
                    y = self.y + i
                    if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and grid[y][x] != BLACK):
                        return False
        return True

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (SIDE_PANEL_WIDTH + x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, WHITE, (SIDE_PANEL_WIDTH + x * GRID_SIZE, 0), (SIDE_PANEL_WIDTH + x * GRID_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, WHITE, (SIDE_PANEL_WIDTH, y * GRID_SIZE), (SIDE_PANEL_WIDTH + SCREEN_WIDTH, y * GRID_SIZE))

def draw_window(surface, grid, next_piece, score, saved_piece):
    surface.fill(BLACK)
    draw_grid(surface, grid)

    # Draw next piece
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next', 1, WHITE)

    surface.blit(label, (SCREEN_WIDTH + SIDE_PANEL_WIDTH + 10, 30))
    format = next_piece.shape

    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == 1:
                pygame.draw.rect(surface, next_piece.color, (SCREEN_WIDTH + SIDE_PANEL_WIDTH + 10 + j * GRID_SIZE, 70 + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    # Draw score
    score_label = font.render(f'{score}', 1, WHITE)
    surface.blit(score_label, (SCREEN_WIDTH + SIDE_PANEL_WIDTH + 10, SCREEN_HEIGHT - 60))

    # Draw saved piece
    draw_saved_piece(surface, saved_piece)

    pygame.display.update()

def draw_saved_piece(surface, saved_piece):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Saved', 1, WHITE)
    surface.blit(label, (10, 30))
    if saved_piece:
        format = saved_piece.shape
        for i, line in enumerate(format):
            for j, column in enumerate(line):
                if column == 1:
                    pygame.draw.rect(surface, saved_piece.color, (10 + j * GRID_SIZE, 70 + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def clear_rows(grid, locked_positions):
    rows_to_clear = []
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            rows_to_clear.append(i)
    
    if not rows_to_clear:
        return 0  # 삭제할 행이 없으면 0 반환

    # 삭제 애니메이션 (흰색으로 깜빡이기)
    for _ in range(1):
        for row in rows_to_clear:
            for col in range(GRID_WIDTH):
                grid[row][col] = WHITE
        draw_window(screen, grid, next_piece, score, saved_piece)
        pygame.display.update()
        pygame.time.delay(50)

        for row in rows_to_clear:
            for col in range(GRID_WIDTH):
                grid[row][col] = BLACK
        draw_window(screen, grid, next_piece, score, saved_piece)
        pygame.display.update()
        pygame.time.delay(50)

    # 삭제된 줄 개수
    num_rows_cleared = len(rows_to_clear)

    # 행을 아래로 이동
    for row in sorted(rows_to_clear):
        for y in range(row, 0, -1):
            for x in range(GRID_WIDTH):
                grid[y][x] = grid[y-1][x]
                if (x, y-1) in locked_positions:
                    locked_positions[(x, y)] = locked_positions.pop((x, y-1))
                else:
                    locked_positions.pop((x, y), None)
        for x in range(GRID_WIDTH):
            grid[0][x] = BLACK  # 최상단 행을 비움
    return num_rows_cleared

def update_score(rows_cleared, combo):
    base_scores = {1: 1000, 2: 2000, 3: 4000, 4: 6000}
    score = base_scores.get(rows_cleared, 0)
    if rows_cleared > 0:
        if combo > 1:
            score += (combo-1) * 1000
            if combo == 2:
                combo1_sound.play()
            if combo == 3:
                combo2_sound.play()
            elif combo == 4:
                combo3_sound.play()
            elif combo == 5:
                combo4_sound.play()
            elif combo == 6:
                combo5_sound.play()
            elif combo == 7:
                combo6_sound.play()
            elif combo == 8:
                combo7_sound.play()
            elif combo == 9:
                combo8_sound.play()
            elif combo == 10:
                combo9_sound.play()
            elif combo == 11:
                combo10_sound.play()
            elif combo == 12:
                combo11_sound.play()
            elif combo == 13:
                combo12_sound.play()
            elif combo == 14:
                combo13_sound.play()
            elif combo == 15:
                combo14_sound.play()
            elif combo >= 16:
                combo15_sound.play()
        elif combo < 2:
            clear_sound.play()        
    return score

def main():
    global screen, next_piece, grid, score, saved_piece, can_save
    screen = pygame.display.set_mode((TOTAL_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    current_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
    next_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
    saved_piece = None
    can_save = True
    fall_time = 0
    move_left_time = 0
    move_right_time = 0
    move_down_time = 0
    initial_move_delay = 0.25  # Initial delay before continuous movement
    move_speed = 0.05  # Speed of continuous movement
    key_down_time = {
        pygame.K_LEFT: 0,
        pygame.K_RIGHT: 0,
        pygame.K_DOWN: 0
    }
    key_pressed = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_DOWN: False
    }
    lock_delay = 1000  # 1초 유예시간
    lock_start_time = None
    score = 0
    combo = 0

    while True:
        grid = create_grid(locked_positions)
        fall_speed = 0.27
        fall_time += clock.get_rawtime()
        move_left_time += clock.get_rawtime()
        move_right_time += clock.get_rawtime()
        move_down_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                if lock_start_time is None:
                    lock_start_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - lock_start_time >= lock_delay:
                    change_piece = True
            else:
                lock_start_time = None

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_LEFT]:
            if not key_pressed[pygame.K_LEFT]:
                key_pressed[pygame.K_LEFT] = True
                key_down_time[pygame.K_LEFT] = current_time
                current_piece.x -= 1
                move_sound.play() 
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
            elif current_time - key_down_time[pygame.K_LEFT] >= initial_move_delay * 1000:
                if move_left_time == 0 or move_left_time / 1000 >= move_speed:
                    move_left_time = 0
                    current_piece.x -= 1
                    move_sound.play() 
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
        else:
            key_pressed[pygame.K_LEFT] = False
            move_left_time = 0

        if keys[pygame.K_RIGHT]:
            if not key_pressed[pygame.K_RIGHT]:
                key_pressed[pygame.K_RIGHT] = True
                key_down_time[pygame.K_RIGHT] = current_time
                current_piece.x += 1
                move_sound.play() 
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif current_time - key_down_time[pygame.K_RIGHT] >= initial_move_delay * 1000:
                if move_right_time == 0 or move_right_time / 1000 >= move_speed:
                    move_right_time = 0
                    current_piece.x += 1
                    move_sound.play() 
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
        else:
            key_pressed[pygame.K_RIGHT] = False
            move_right_time = 0

        if keys[pygame.K_DOWN]:
            if not key_pressed[pygame.K_DOWN]:
                key_pressed[pygame.K_DOWN] = True
                key_down_time[pygame.K_DOWN] = current_time
                current_piece.y += 1
                move_sound.play() 
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            elif current_time - key_down_time[pygame.K_DOWN] >= initial_move_delay * 1000:
                if move_down_time == 0 or move_down_time / 1000 >= move_speed:
                    move_down_time = 0
                    current_piece.y += 1
                    move_sound.play() 
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
        else:
            key_pressed[pygame.K_DOWN] = False
            move_down_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    current_piece.rotate_counterclockwise()
                    move_sound.play() 
                    if not current_piece.is_valid_position():
                        current_piece.rotate()
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    move_sound.play() 
                    if not current_piece.is_valid_position():
                        current_piece.rotate_counterclockwise()
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
                    drop_sound.play()
                if event.key == pygame.K_LSHIFT and can_save:
                    if saved_piece is None:
                        saved_piece = Tetrimino(current_piece.shape_index)
                        current_piece = next_piece
                        next_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
                    else:
                        temp_piece = Tetrimino(current_piece.shape_index)
                        current_piece = Tetrimino(saved_piece.shape_index)
                        saved_piece = temp_piece
                    can_save = False

            if event.type == pygame.KEYUP:
                if event.key in key_pressed:
                    key_pressed[event.key] = False

        shape_pos = convert_shape_format(current_piece)

        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
            change_piece = False
            can_save = True

            rows_cleared = clear_rows(grid, locked_positions)
            if rows_cleared > 0:
                combo += 1
            else:
                combo = 0
            score += update_score(rows_cleared, combo)

            if check_lost(locked_positions):
                draw_text_middle("   T_T", 250, WHITE, screen)
                pygame.display.update()
                pygame.time.delay(1500)
                locked_positions = {}
                grid = create_grid(locked_positions)
                score = 0
                combo = 0

        draw_window(screen, grid, next_piece, score, saved_piece)

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(GRID_WIDTH) if grid[y][x] == BLACK] for y in range(GRID_HEIGHT)]
    accepted_positions = [x for item in accepted_positions for x in item]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            gameover_sound.play()
            return True
    return False

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 1:
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])

    return positions

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (SCREEN_WIDTH / 2 - (label.get_width() / 2), SCREEN_HEIGHT / 2 - (label.get_height() / 2)))

if __name__ == "__main__":
    main()
