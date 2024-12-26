import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Runner")

# Load images
character_img = pygame.image.load("character.png")  # Load character image
obstacle_img = pygame.image.load("obstacle.png")    # Load obstacle image
ground_img = pygame.image.load("ground.png")        # Load ground image
nuke_img = pygame.image.load("nuke.png")            # Load nuke image

# Resize images to appropriate sizes (if needed)
character_img = pygame.transform.scale(character_img, (50, 50))  # Resize character image
obstacle_img = pygame.transform.scale(obstacle_img, (50, 50))    # Resize obstacle image
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))    # Resize ground image to match the width of the screen
nuke_img = pygame.transform.scale(nuke_img, (50, 50))           # Resize nuke image

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 255, 0)  # Color of the restart button
TEXT_COLOR = (0, 0, 0)  # Text color
RED = (255, 0, 0)  # Color of the hitbox border for obstacles and nukes
GREEN = (0, 255, 0)  # Color of the hitbox border for the character

# Game variables
character_pos = [100, HEIGHT - 100]  # Start position of the character
character_velocity_y = 0
gravity = 0.7
jump_power = -10  # Reduced jump power to prevent jumping over obstacles
move_speed = 7
is_jumping = False

obstacle_speed = 10
obstacle_width = 50
obstacle_height = 50
obstacles = []

nukes = []  # List to store nukes
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Timer variables
game_start_timer = 3  # 3 second timer before the game starts
timer_started = False

# Function to add obstacles
def add_obstacle():
    x_pos = random.randint(WIDTH + 100, WIDTH + 300)
    obstacles.append([x_pos, HEIGHT - 100])

# Function to add two nukes at once with different positions
def add_nukes():
    x_pos_1 = random.randint(100, WIDTH - 100)
    x_pos_2 = random.randint(100, WIDTH - 100)
    while x_pos_1 == x_pos_2:  # Ensure nukes don't spawn in the same position
        x_pos_2 = random.randint(100, WIDTH - 100)
    nukes.append([x_pos_1, 0])  # Nuke 1 starts from top
    nukes.append([x_pos_2, 0])  # Nuke 2 starts from top

# Function to reset the game
def reset_game():
    global character_pos, character_velocity_y, obstacles, nukes, score, is_jumping
    character_pos = [100, HEIGHT - 100]
    character_velocity_y = 0
    is_jumping = False
    obstacles.clear()
    nukes.clear()  # Clear nukes on reset
    score = 0  # Reset the score

# Function to draw text
def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Game loop
running = True
game_over = False
show_hitboxes = False  # Flag for toggling hitbox visibility
while running:
    screen.fill(WHITE)  # Fill the screen with white color
    
    # Draw ground using custom image
    screen.blit(ground_img, (0, HEIGHT - 50))

    # Event handling
    keys = pygame.key.get_pressed()  # Get pressed keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Toggle hitboxes visibility when 'A' is pressed
            if event.key == pygame.K_a:
                show_hitboxes = not show_hitboxes

            if event.key == pygame.K_r and game_over:  # If R is pressed after game over
                reset_game()  # Reset the game and start fresh
                game_over = False  # Reset game over state

    # Handle game start timer
    if not timer_started:
        pygame.time.delay(1000)  # Wait for 1 second for the timer
        game_start_timer -= 1
        if game_start_timer <= 0:
            timer_started = True  # Start the game after the timer reaches 0
            game_start_timer = 3  # Reset timer for future use

    if not game_over and timer_started:
        # Increase speed after score 1000
        if score > 1000:
            obstacle_speed = 7  # Increase obstacle speed
            gravity = 0.7  # Make gravity stronger, making jumping harder
            move_speed = 7  # Increase character movement speed

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            character_pos[0] -= move_speed
        elif keys[pygame.K_RIGHT]:
            character_pos[0] += move_speed

        # Prevent character from leaving screen horizontally
        character_pos[0] = max(0, min(WIDTH - 50, character_pos[0]))

        # Jumping logic with gravity
        if keys[pygame.K_SPACE] and not is_jumping:
            character_velocity_y = jump_power
            is_jumping = True

        character_velocity_y += gravity
        character_pos[1] += character_velocity_y

        # Prevent character from falling below the ground
        if character_pos[1] >= HEIGHT - 100:
            character_pos[1] = HEIGHT - 100
            is_jumping = False

        # Add obstacles at regular intervals
        if len(obstacles) == 0 or obstacles[-1][0] < WIDTH - 300:
            add_obstacle()

        # Move obstacles to the left
        for obstacle in obstacles:
            obstacle[0] -= obstacle_speed
        obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]

        # Add nukes after score 500 (every 5 seconds)
        if score > 500 and len(nukes) == 0:
            add_nukes()  # Drop two nukes at once

        # Move nukes down
        for nuke in nukes:
            nuke[1] += 5  # Move nuke down

            # Remove nuke if it hits the ground
            if nuke[1] >= HEIGHT - 100:
                nukes.remove(nuke)

            # Check for collision with player
            nuke_rect = pygame.Rect(nuke[0], nuke[1], 50, 50)
            player_rect = pygame.Rect(character_pos[0], character_pos[1], 50, 50)
            if player_rect.colliderect(nuke_rect):
                game_over = True  # Game over if player collides with nuke
                break

        # Check for collision between player and obstacles
        character_rect = pygame.Rect(character_pos[0], character_pos[1], 50, 50)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            if character_rect.colliderect(obstacle_rect):
                game_over = True
                break

        # Update score
        if not game_over:
            score += 1
            score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

        # Draw the character
        screen.blit(character_img, (character_pos[0], character_pos[1]))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_img, (obstacle[0], obstacle[1]))
            if show_hitboxes:
                pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height), 2)

        # Draw nukes
        for nuke in nukes:
            screen.blit(nuke_img, (nuke[0], nuke[1]))  # Assuming nuke.png is the image
            if show_hitboxes:
                pygame.draw.rect(screen, RED, (nuke[0], nuke[1], 50, 50), 2)

        # Draw the character's hitbox (if 'A' is pressed)
        if show_hitboxes:
            pygame.draw.rect(screen, GREEN, (character_pos[0], character_pos[1], 50, 50), 2)

    # If game over, show restart screen with final score
    if game_over:
        draw_text("GAME OVER", font, TEXT_COLOR, WIDTH // 2 - 100, HEIGHT // 2 - 100)
        draw_text(f"Final Score: {score}", font, TEXT_COLOR, WIDTH // 2 - 100, HEIGHT // 2 - 60)
        draw_text("Press 'R' to Restart", font, TEXT_COLOR, WIDTH // 2 - 100, HEIGHT // 2 - 30)

    pygame.display.flip()  # Update the display
    clock.tick(30)  # Control the frame rate (30 FPS)

pygame.quit()
sys.exit()

