import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 1000
IMAGE_SCALE_STEP = .1

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Image Manipulation")

# Load the image
image = pygame.image.load("man.jpg")
image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
current_scale = 100  # Start with 100% scale
vertical_scale = 100  # Vertical scale percentage
max_vertical_scale = 100  # Maximum vertical scale percentage
horizontal_scale = 100  # Horizontal scale percentage
max_horizontal_scale = 100  # Maximum horizontal scale percentage
angle = 0  # Initialize rotation angle

# Growth direction variables
vertical_growth_direction = 1  # 1 for increasing, -1 for decreasing
horizontal_growth_direction = 1  # 1 for increasing, -1 for decreasing

# Flip states
flip_horizontal = False
flip_vertical = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Move the image with arrow keys
    if keys[pygame.K_UP]:
        image_rect.y -= 5
    if keys[pygame.K_DOWN]:
        image_rect.y += 5
    if keys[pygame.K_LEFT]:
        image_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        image_rect.x += 5

    # Resize the image uniformly with [ and ]
    if keys[pygame.K_LEFTBRACKET]:
        max_vertical_scale -= IMAGE_SCALE_STEP
        max_horizontal_scale -= IMAGE_SCALE_STEP
        vertical_scale -= IMAGE_SCALE_STEP * vertical_growth_direction
        horizontal_scale -= IMAGE_SCALE_STEP * horizontal_growth_direction
        
    if keys[pygame.K_RIGHTBRACKET]:
        max_vertical_scale += IMAGE_SCALE_STEP
        max_horizontal_scale += IMAGE_SCALE_STEP
        vertical_scale += IMAGE_SCALE_STEP * vertical_growth_direction
        horizontal_scale += IMAGE_SCALE_STEP * horizontal_growth_direction
        
    # Stretch the image vertically with 1 and 2
    if keys[pygame.K_1]:
        vertical_scale += IMAGE_SCALE_STEP * vertical_growth_direction
    if keys[pygame.K_2]:
        vertical_scale -= IMAGE_SCALE_STEP * vertical_growth_direction

    # Stretch the image horizontally with 3 and 4
    if keys[pygame.K_3]:
        horizontal_scale += IMAGE_SCALE_STEP * horizontal_growth_direction
    if keys[pygame.K_4]:
        horizontal_scale -= IMAGE_SCALE_STEP * horizontal_growth_direction

    # Flip the image horizontally with F and vertically with V
    if keys[pygame.K_f]:
        flip_horizontal = not flip_horizontal
    if keys[pygame.K_v]:
        flip_vertical = not flip_vertical

    # Ensure scale is not zero or negative and toggle growth direction
    if vertical_scale < 0:
        vertical_scale = 1
        vertical_growth_direction *= -1  # Reverse growth direction
        flip_vertical = not flip_vertical
    if horizontal_scale < 0:
        horizontal_scale = 1
        horizontal_growth_direction *= -1  # Reverse growth direction
        flip_horizontal = not flip_horizontal
    if vertical_scale > max_vertical_scale:
        vertical_scale = max_vertical_scale
        vertical_growth_direction *= -1
        #flip_vertical = not flip_vertical
    if horizontal_scale > max_horizontal_scale:
        horizontal_scale = max_horizontal_scale
        horizontal_growth_direction *= -1
        #flip_horizontal = not flip_horizontal
    
    # Create a new surface with scaling applied
    scaled_width = image.get_width() * horizontal_scale // 100
    scaled_height = image.get_height() * vertical_scale // 100
    scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

    # Flip the image if needed
    flipped_image = pygame.transform.flip(scaled_image, flip_horizontal, flip_vertical)

    # Update the scaled image rect
    scaled_rect = flipped_image.get_rect(center=image_rect.center)

    # Rotate the scaled image
    rotated_image = pygame.transform.rotate(flipped_image, angle)
    rotated_rect = rotated_image.get_rect(center=scaled_rect.center)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(rotated_image, rotated_rect)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
