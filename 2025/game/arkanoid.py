import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Arkanoid")

# Colors
BACKGROUND = (20, 30, 70)
PADDLE_COLOR = (0, 200, 255)
BALL_COLOR = (255, 255, 0)
BRICK_COLORS = [
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (100, 100, 255),  # Blue
    (255, 200, 100),  # Orange
    (200, 100, 255),  # Purple
]
TEXT_COLOR = (220, 220, 220)

# Game elements
class Paddle:
    def __init__(self):
        self.width = 120
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 8
        
    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, (self.x, self.y, self.width, self.height), 0, 10)
        # Add some detail
        pygame.draw.rect(screen, (0, 150, 200), (self.x, self.y, self.width, self.height), 3, 10)
        
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

class Ball:
    def __init__(self):
        self.radius = 12
        self.speed = 5  # Moved this line before reset()
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1]) * self.speed
        self.dy = -self.speed
        
    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (220, 220, 0), (self.x, self.y), self.radius-4)
        # Add shine effect
        pygame.draw.circle(screen, (255, 255, 200), (self.x-4, self.y-4), 4)
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Wall collisions
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius:
            self.dy *= -1
            
    def collide_paddle(self, paddle):
        if (self.y + self.radius >= paddle.y and 
            self.y - self.radius <= paddle.y + paddle.height and
            self.x >= paddle.x and self.x <= paddle.x + paddle.width):
            # Calculate bounce angle based on where the ball hits the paddle
            relative_x = (self.x - paddle.x) / paddle.width
            angle = relative_x * 2 - 1  # -1 to 1
            self.dx = angle * self.speed
            self.dy = -abs(self.dy)
            return True
        return False

class Brick:
    def __init__(self, x, y, color):
        self.width = 70
        self.height = 25
        self.x = x
        self.y = y
        self.color = color
        self.hits = 1
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, 5)
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height), 2, 5)
        
    def collide(self, ball):
        if (ball.x + ball.radius >= self.x and 
            ball.x - ball.radius <= self.x + self.width and
            ball.y + ball.radius >= self.y and 
            ball.y - ball.radius <= self.y + self.height):
            self.hits -= 1
            return True
        return False

def create_bricks():
    bricks = []
    for row in range(5):
        for col in range(10):
            x = col * 75 + 25
            y = row * 35 + 50
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            bricks.append(Brick(x, y, color))
    return bricks

# Create game objects
paddle = Paddle()
ball = Ball()
bricks = create_bricks()
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
game_over = False
level = 1

# Main game loop
clock = pygame.time.Clock()
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
                paddle = Paddle()
                ball = Ball()
                bricks = create_bricks()
                score = 0
                lives = 3
                game_over = False
                level = 1
    
    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")
            
        # Ball movement
        ball.move()
        
        # Ball-paddle collision
        if ball.collide_paddle(paddle):
            # Add some spin effect
            if paddle.x < ball.x:
                ball.dx += 0.5
            else:
                ball.dx -= 0.5
            ball.dx = max(min(ball.dx, 8), -8)  # Limit speed
            
        # Ball-brick collision
        for brick in bricks[:]:
            if brick.collide(ball):
                score += 10
                bricks.remove(brick)
                # Change ball direction
                ball.dy *= -1
                break
                
        # Ball out of bounds
        if ball.y > HEIGHT:
            lives -= 1
            ball.reset()
            if lives <= 0:
                game_over = True
                
        # Level complete
        if len(bricks) == 0:
            level += 1
            ball.speed += 0.5
            bricks = create_bricks()
            ball.reset()
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw stars in background
    for i in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, (200, 200, 255), (x, y), 1)
    
    # Draw game elements
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()
    
    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    level_text = font.render(f"Level: {level}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))
    
    # Game over message
    if game_over:
        game_over_text = font.render("GAME OVER - Press R to Restart", True, (255, 100, 100))
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
    
    # Draw instructions at the bottom
    if not game_over:
        instruct_text = font.render("Use LEFT and RIGHT arrow keys to move the paddle", True, (200, 200, 200))
        screen.blit(instruct_text, (WIDTH // 2 - 250, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)