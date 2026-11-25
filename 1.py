import random
import tkinter as tk

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = "black"
SNAKE_COLOR = "green"
APPLE_COLOR = "red"
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
FPS = 20
DELAY = 1000 // FPS  

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        
        self.position = position if position is not None else CENTER_POSITION
        self.body_color = body_color

    def draw(self, canvas):
        pass


class Apple(GameObject):

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)
        self.item_id = None 

    def randomize_position(self, occupied_positions=None):
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

    def draw(self, canvas):
        x, y = self.position
        if self.item_id is None:
            self.item_id = canvas.create_rectangle(
                x, y, x + GRID_SIZE, y + GRID_SIZE,
                fill=self.body_color, outline=""
            )
        else:
            canvas.coords(self.item_id, x, y, x + GRID_SIZE, y + GRID_SIZE)


class Snake(GameObject):

    def __init__(self):
        super().__init__(position=CENTER_POSITION, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.items = {}  

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
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

    def draw(self, canvas):
        if self.last and self.last in self.items:
            canvas.delete(self.items[self.last])
            del self.items[self.last]
        for pos in self.positions:
            if pos not in self.items:
                x, y = pos
                self.items[pos] = canvas.create_rectangle(
                    x, y, x + GRID_SIZE, y + GRID_SIZE,
                    fill=self.body_color, outline=""
                )

    def get_head_position(self):
        return self.positions[0]

    def reset(self, canvas):
        for item in self.items.values():
            canvas.delete(item)
        self.items.clear()

        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def main():
    root = tk.Tk()
    root.title("Изгиб Питона")
    root.resizable(False, False)

    canvas = tk.Canvas(
        root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
        bg=BOARD_BACKGROUND_COLOR, highlightthickness=0
    )
    canvas.pack()

    snake = Snake()
    apple = Apple(snake.positions)

    def handle_keys(event):
        key = event.keysym
        if key == "Up" and snake.direction != DOWN:
            snake.next_direction = UP
        elif key == "Down" and snake.direction != UP:
            snake.next_direction = DOWN
        elif key == "Left" and snake.direction != RIGHT:
            snake.next_direction = LEFT
        elif key == "Right" and snake.direction != LEFT:
            snake.next_direction = RIGHT

    root.bind("<Key>", handle_keys)

    def game_loop():
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset(canvas)
            apple.randomize_position(snake.positions)

        snake.draw(canvas)
        apple.draw(canvas)

        root.after(DELAY, game_loop)

    game_loop()
    root.mainloop()


if __name__ == "__main__":
    main()
