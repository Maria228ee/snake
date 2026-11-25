import random

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
CENTER_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
FPS = 20

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует позицию и цвет."""
        self.position = position if position is not None else CENTER_POSITION
        self.body_color = body_color

    def draw(self, surface):
        """Метод для переопределения."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализирует яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию."""
        occupied = set(occupied_positions) if occupied_positions else set()
        all_cells = {
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        }
        free_cells = tuple(all_cells - occupied)
        if free_cells:
            self.position = random.choice(free_cells)
        else:
            self.position = CENTER_POSITION

    def draw(self, surface):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(position=CENTER_POSITION, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx) % SCREEN_WIDTH
        new_y = (head_y + dy) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        head_rect = pygame.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.positions)

    running = True
    while running:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
