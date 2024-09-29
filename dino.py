import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
FPS = 60

dino_image = pygame.Surface((40, 40))
dino_image.fill(GREEN)
cactus_image = pygame.Surface((20, 40))
cactus_image.fill((255, 0, 0))

gravity = 0.5
jump_strength = 10
ground_y = SCREEN_HEIGHT - 40
score = 0

class Dino:
    def __init__(self):
        self.rect = dino_image.get_rect()
        self.rect.x = 50
        self.rect.y = ground_y
        self.jump_speed = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.jump_speed = jump_strength
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            self.rect.y -= self.jump_speed
            self.jump_speed -= gravity
            if self.rect.y >= ground_y:
                self.rect.y = ground_y
                self.is_jumping = False

    def draw(self):
        screen.blit(dino_image, self.rect)

class Cactus:
    def __init__(self):
        self.rect = cactus_image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = ground_y

    def update(self):
        self.rect.x -= 5

    def draw(self):
        screen.blit(cactus_image, self.rect)

def main():
    global score
    score = 0
    dino = Dino()
    cacti = []
    spawn_cactus_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_cactus_event, 1500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
            if event.type == spawn_cactus_event:
                cacti.append(Cactus())

        dino.update()
        for cactus in cacti:
            cactus.update()
            if dino.rect.colliderect(cactus.rect):
                game_over(score)

        cacti = [cactus for cactus in cacti if cactus.rect.x > -20]

        screen.fill(WHITE)

        dino.draw()
        for cactus in cacti:
            cactus.draw()

        score += 1
        show_score(score)

        pygame.display.flip()
        clock.tick(FPS)

def game_over(score):
    font = pygame.font.SysFont('Arial', 50)
    game_over_surface = font.render(f'Game Over! Score: {score}', True, BLACK)
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    main()
    

def show_score(score):
    font = pygame.font.SysFont('Arial', 30)
    score_surface = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_surface, (10, 10))

if __name__ == "__main__":
    main()
