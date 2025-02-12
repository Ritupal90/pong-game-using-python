import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

# Ball settings
BALL_RADIUS = 10

# Speed settings
PADDLE_SPEED = 10
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Clock
clock = pygame.time.Clock()

# Font for scoring
font = pygame.font.SysFont('Arial', 30)

# Initial positions of paddles and ball
player_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Player and opponent scores
player_score = 0
opponent_score = 0

def draw_window():
    window.fill(BLACK)  # Fill the window with black color

    # Draw paddles and ball
    pygame.draw.rect(window, WHITE, player_paddle)
    pygame.draw.rect(window, WHITE, opponent_paddle)
    pygame.draw.ellipse(window, WHITE, ball)

    # Draw the center line
    pygame.draw.aaline(window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Draw scores
    player_text = font.render(f'{player_score}', True, WHITE)
    window.blit(player_text, (WIDTH//4 - player_text.get_width()//2, 20))
    
    opponent_text = font.render(f'{opponent_score}', True, WHITE)
    window.blit(opponent_text, (WIDTH*3//4 - opponent_text.get_width()//2, 20))

    pygame.display.update()  # Update the screen

def handle_ball_movement():
    global BALL_SPEED_X, BALL_SPEED_Y, player_score, opponent_score

    # Move the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        BALL_SPEED_X = -BALL_SPEED_X

    # Scoring
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()

def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x = WIDTH // 2 - BALL_RADIUS
    ball.y = HEIGHT // 2 - BALL_RADIUS
    BALL_SPEED_X = random.choice([7, -7])
    BALL_SPEED_Y = random.choice([7, -7])

def handle_paddle_movement():
    keys = pygame.key.get_pressed()

    # Player paddle movement (up and down)
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # Opponent paddle movement (AI-controlled)
    if opponent_paddle.centery < ball.centery and opponent_paddle.bottom < HEIGHT:
        opponent_paddle.y += PADDLE_SPEED
    if opponent_paddle.centery > ball.centery and opponent_paddle.top > 0:
        opponent_paddle.y -= PADDLE_SPEED

def main():
    global player_score, opponent_score

    # Game loop
    running = True
    while running:
        clock.tick(60)  # Limit the game to 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_ball_movement()
        handle_paddle_movement()
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
