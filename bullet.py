import pygame
import random
import sys
import math

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SHAPES = ['square', 'circle', 'triangle']
SHAPE_COLORS = {
    'square': RED,
    'circle': GREEN,
    'triangle': BLUE
}

ENEMY_SPEED = 5
ENEMY_LIFETIME = 3000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.shape = 'square'
        self.size = 40
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.hp = 10

    def draw(self):
        if self.shape == 'square':
            pygame.draw.rect(screen, SHAPE_COLORS[self.shape], (self.x, self.y, self.size, self.size))
        elif self.shape == 'circle':
            pygame.draw.circle(screen, SHAPE_COLORS[self.shape], (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
        elif self.shape == 'triangle':
            points = [(self.x, self.y + self.size), (self.x + self.size // 2, self.y), (self.x + self.size, self.y + self.size)]
            pygame.draw.polygon(screen, SHAPE_COLORS[self.shape], points)

    def change_shape(self, new_shape):
        if new_shape in SHAPES:
            self.shape = new_shape

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.size:
            self.y += self.speed

    def take_damage(self):
        self.hp -= 1
        if self.hp == 0:
            print("You died! Returning to menu...")
            return

class Enemy:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.size = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        self.direction = random.uniform(0, 2 * math.pi)

    def update(self):
        self.x += ENEMY_SPEED * math.cos(self.direction)
        self.y += ENEMY_SPEED * math.sin(self.direction)
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.direction = -self.direction

    def draw(self):
        if self.shape == 'square':
            pygame.draw.rect(screen, SHAPE_COLORS[self.shape], (self.x, self.y, self.size, self.size))
        elif self.shape == 'circle':
            pygame.draw.circle(screen, SHAPE_COLORS[self.shape], (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)
        elif self.shape == 'triangle':
            points = [(self.x, self.y + self.size), (self.x + self.size // 2, self.y), (self.x + self.size, self.y + self.size)]
            pygame.draw.polygon(screen, SHAPE_COLORS[self.shape], points)

def main_menu():
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        title_text = font.render("Bullet Hell Game", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        start_button = font.render("Start", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)
        screen.blit(start_button, (SCREEN_WIDTH // 2 - start_button.get_width() // 2, 300))
        screen.blit(exit_button, (SCREEN_WIDTH // 2 - exit_button.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_loop():
    player = Player()
    enemies = []
    score = 0
    enemy_timer = pygame.time.get_ticks()

    while True:
        screen.fill(BLACK)
        player.draw()
        keys = pygame.key.get_pressed()
        player.move(keys)

        for enemy in enemies:
            enemy.update()
            enemy.draw()

        if pygame.time.get_ticks() - enemy_timer > 1000:
            enemies.append(Enemy())
            enemy_timer = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.change_shape('square')
                elif event.key == pygame.K_x:
                    player.change_shape('circle')
                elif event.key == pygame.K_c:
                    player.change_shape('triangle')

        for enemy in enemies[:]:
            if (player.x < enemy.x + enemy.size and
                player.x + player.size > enemy.x and
                player.y < enemy.y + enemy.size and
                player.y + player.size > enemy.y):
                if player.shape != enemy.shape:
                    enemies.remove(enemy)
                    score += 1
                    player.take_damage()
                else:
                    enemies.remove(enemy)
                    score += 1

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        hp_text = font.render(f"HP: {player.hp}", True, WHITE)
        screen.blit(hp_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

        if player.hp == 0:
            print("You died! Returning to menu...")
            return

if __name__ == "__main__":
    while True:
        main_menu()
        game_loop()
