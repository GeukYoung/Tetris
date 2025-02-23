import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
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
            pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, WHITE, (x * GRID_SIZE, 0), (x * GRID_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, WHITE, (0, y * GRID_SIZE), (SCREEN_WIDTH, y * GRID_SIZE))

def draw_window(surface, grid, next_piece):
    surface.fill(BLACK)
    draw_grid(surface, grid)

    # Draw next piece
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next', 1, WHITE)

    surface.blit(label, (SCREEN_WIDTH + 10, 30))
    format = next_piece.shape

    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == 1:
                pygame.draw.rect(surface, next_piece.color, (SCREEN_WIDTH + 10 + j * GRID_SIZE, 70 + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

    pygame.display.update()

def clear_rows(grid, locked):
    increment = 0
    rows_to_clear = []
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            rows_to_clear.append(i)
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue

    if increment > 0:
        # Add blinking effect for all rows to clear
        for ind in rows_to_clear:
            for j in range(len(grid[ind])):
                grid[ind][j] = WHITE
        draw_window(screen, grid, next_piece)
        pygame.display.update()
        pygame.time.delay(50)  # Shorter delay for faster blinking

        for ind in rows_to_clear:
            for j in range(len(grid[ind])):
                grid[ind][j] = BLACK
        draw_window(screen, grid, next_piece)
        pygame.display.update()
        pygame.time.delay(50)  # Shorter delay for faster blinking

        # Move rows down
        for ind in rows_to_clear:
            for y in range(ind, 0, -1):
                for x in range(GRID_WIDTH):
                    grid[y][x] = grid[y-1][x]
                    if (x, y-1) in locked:
                        locked[(x, y)] = locked.pop((x, y-1))
                    else:
                        locked.pop((x, y), None)
            for x in range(GRID_WIDTH):
                grid[0][x] = BLACK

        # Adjust locked positions
        for i in range(len(grid)-1, -1, -1):
            for j in range(GRID_WIDTH):
                if grid[i][j] != BLACK:
                    locked[(j, i)] = grid[i][j]

    return increment

def main():
    global screen, next_piece, grid
    screen = pygame.display.set_mode((SCREEN_WIDTH + 150, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    current_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
    next_piece = Tetrimino(random.randint(0, len(SHAPES) - 1))
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
                change_piece = True

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_LEFT]:
            if not key_pressed[pygame.K_LEFT]:
                key_pressed[pygame.K_LEFT] = True
                key_down_time[pygame.K_LEFT] = current_time
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
            elif current_time - key_down_time[pygame.K_LEFT] >= initial_move_delay * 1000:
                if move_left_time == 0 or move_left_time / 1000 >= move_speed:
                    move_left_time = 0
                    current_piece.x -= 1
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
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif current_time - key_down_time[pygame.K_RIGHT] >= initial_move_delay * 1000:
                if move_right_time == 0 or move_right_time / 1000 >= move_speed:
                    move_right_time = 0
                    current_piece.x += 1
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
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            elif current_time - key_down_time[pygame.K_DOWN] >= initial_move_delay * 1000:
                if move_down_time == 0 or move_down_time / 1000 >= move_speed:
                    move_down_time = 0
                    current_piece.y += 1
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
                    if not current_piece.is_valid_position():
                        current_piece.rotate()
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not current_piece.is_valid_position():
                        current_piece.rotate_counterclockwise()
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
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

            clear_rows(grid, locked_positions)

            if check_lost(locked_positions):
                draw_text_middle("YOU LOST!", 80, WHITE, screen)
                pygame.display.update()
                pygame.time.delay(1500)
                locked_positions = {}
                grid = create_grid(locked_positions)

        draw_window(screen, grid, next_piece)

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
