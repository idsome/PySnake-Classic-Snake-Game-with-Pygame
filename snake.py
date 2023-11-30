import pygame
import sys
import random


pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 10
global FPS
FPS = 15
damage = 0
EAT_SOUND_FILE = "data\eating-sound-effect.mp3"
STAGE_SOUND_FILE = "data\Feel-Good.mp3"
WALL_HIT_SOUND_FILE = "data\wall_hit.mp3"
LOSING_SOUND_FILE = "data/negative_beeps.mp3"
high_score_file = "data\high_score.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.mixer.init()
EAT_SOUND_FILE = pygame.mixer.Sound(EAT_SOUND_FILE)
STAGE_SOUND_FILE = pygame.mixer.Sound(STAGE_SOUND_FILE)
WALL_HIT_SOUND_FILE = pygame.mixer.Sound(WALL_HIT_SOUND_FILE)
LOSING_SOUND_FILE = pygame.mixer.Sound(LOSING_SOUND_FILE)

# Load or initialize high score
try:
    with open(high_score_file, "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0


# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = WHITE

    def get_snake_color(self, color):
        self.color = color

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            ((cur[0] + (x * GRID_SIZE)) % WIDTH),
            (cur[1] + (y * GRID_SIZE)) % HEIGHT,
        )
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def center(self):
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def check_collision(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            ((cur[0] + (x * GRID_SIZE)) % WIDTH),
            (cur[1] + (y * GRID_SIZE)) % HEIGHT,
        )
        return len(self.positions) > 2 and new in self.positions[2:]

    def colliding_with_walls(self):
        cur = self.get_head_position()
        Snake_y_position = cur[1]
        if (
            Snake_y_position < w1.position_y + 20
            or Snake_y_position > w2.position_y - 20
        ):
            return True
        else:
            return False


# ... (remaining code)
class Fruit:
    def __init__(self, color):
        self.position = (0, 0)
        self.color = color
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(4, (WIDTH // GRID_SIZE) - 4) * GRID_SIZE,
            random.randint(8, (HEIGHT // GRID_SIZE) - 4) * GRID_SIZE,
        )

    def render(self, surface, x_size, y_size):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position[0], self.position[1], x_size, y_size),
        )


class Walls:
    def __init__(self, position_y):
        self.width = 200
        self.position = (0, 40)
        self.position_y = position_y
        self.color = WHITE

    def render(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.position[0], self.position_y, WIDTH, GRID_SIZE / 4),
        )


w1 = Walls(40)
w2 = Walls(395)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, WHITE, rect, 1)


def display_score(surface, score):
    font = pygame.font.SysFont("calibri", 25, True)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))


def display_level(surface, level):
    font = pygame.font.SysFont("calibri", 25, True)
    score_level = font.render(f"level: {level}", True, WHITE)
    surface.blit(score_level, (500, 10))


def display_damage(surface, damage):
    font = pygame.font.SysFont("calibri", 25, True)
    score_damage = font.render(f"damage: {damage}", True, WHITE)
    surface.blit(score_damage, (220, 10))


def display_message(surface, message):
    font = pygame.font.SysFont("calibri", 30, True)
    message_text = font.render(message, True, WHITE)
    surface.blit(message_text, (WIDTH // 2 - 140, HEIGHT // 2 - 15))


def display_pause(surface, message):
    font = pygame.font.SysFont("calibri", 30, True)
    message_text = font.render(message, True, WHITE)
    surface.blit(message_text, (WIDTH // 2 - 140, HEIGHT // 2 + 15))


def display_high_score(surface, message):
    font = pygame.font.SysFont("calibri", 25, True)
    message_text = font.render(f"High Score: {high_score}", True, WHITE)
    surface.blit(message_text, (420, 10))


def main():
    # ... (previous code)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    green_fruit = Fruit(GREEN)
    red_fruit = Fruit(GREEN)

    global high_score

    speed = FPS
    speeding_factor = 1.1
    score = 0
    damage = 0
    level = 1
    rendering_score = 50
    winning_score = 6000
    paused = True
    lost = False
    won = False
    started_lost = 0
    started_level = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != DOWN:
                        snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    if snake.direction != UP:
                        snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    if snake.direction != RIGHT:
                        snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != LEFT:
                        snake.direction = RIGHT
                elif event.key == pygame.K_s:
                    speed = speed * speeding_factor

                elif event.key == pygame.K_SPACE:
                    STAGE_SOUND_FILE.stop()
                    started_level = 0
                    if lost or score >= winning_score:
                        # Reset the game when space is pressed after losing

                        if not lost:
                            level += 1
                        snake.reset()
                        green_fruit.randomize_position()
                        red_fruit.randomize_position()
                        score = 0
                        lost = False
                        won = False
                        damage = 0
                        snake.color = WHITE
                        green_fruit.color = GREEN
                        red_fruit.color = GREEN
                        speed = FPS
                        started_lost = 0

                    else:
                        # Toggle pause when space is pressed
                        paused = not paused
                        snake.color = WHITE
                        green_fruit.color = GREEN
                        red_fruit.color = GREEN
        if not paused and not lost and not won:
            snake.update()
            if started_level < 1:
                STAGE_SOUND_FILE.play(-1)
                started_level += 1

            # Check if the snake hits itself
            if snake.check_collision():
                score = 0
                lost = True

            if snake.get_head_position() == green_fruit.position:
                snake.length += 2
                green_fruit.randomize_position()
                score += 10
                EAT_SOUND_FILE.play()
            if snake.get_head_position() == red_fruit.position:
                snake.length += 5
                red_fruit.randomize_position()
                score += 50
                EAT_SOUND_FILE.play()
                rendering_score = rendering_score * 3
            if snake.colliding_with_walls():
                WALL_HIT_SOUND_FILE.play()
                snake.center()
                speed = speed * speeding_factor
                damage += 1

            if damage == 5:
                snake.get_snake_color((255, 255, 0))
            if damage == 10:
                snake.get_snake_color((255, 165, 0))
            if damage == 15:
                snake.get_snake_color(RED)

            if damage == 20:
                lost = True

            if score > high_score:
                high_score = score
            with open(high_score_file, "w") as file:
                file.write(str(high_score))

        surface.fill(BLACK)
        # draw_grid(surface)
        snake.render(surface)
        green_fruit.render(surface, GRID_SIZE // 2, GRID_SIZE // 2)
        if score // rendering_score:
            red_fruit.render(surface, GRID_SIZE, GRID_SIZE)
        w1.render(surface)
        w2.render(surface)
        display_score(surface, score)
        # display_level(surface, level)
        display_damage(surface, damage)
        display_high_score(surface, high_score)
        # Display high score
        # font = pygame.font.SysFont("calibri", 30, True)
        # high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        # surface.blit(high_score_text, (WIDTH // 2 + 100, HEIGHT - 395))

        if score >= winning_score:
            display_message(surface, "You won!")
            display_pause(surface, "Press SPACE to restart")
            snake.color = BLACK
            green_fruit.color = BLACK
            red_fruit.color = BLACK
            won = True

        if lost:
            if started_lost < 1:
                STAGE_SOUND_FILE.stop()
                LOSING_SOUND_FILE.play()
                started_lost += 1
            display_message(surface, "You lost!")
            display_pause(surface, "Press SPACE to restart")
            snake.color = BLACK
            green_fruit.color = BLACK
            red_fruit.color = BLACK

        if paused:
            # Display a pause or game over message
            display_pause(surface, "Press SPACE to continue")
            snake.color = BLACK
            green_fruit.color = BLACK
            red_fruit.color = BLACK

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(speed)


if __name__ == "__main__":
    main()
