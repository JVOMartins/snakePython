# Example file showing a basic snake game
import pygame
import random

# pygame setup
pygame.init()
pygame.font.init()

font = pygame.font.Font(None, 36)

score = 0

square_width = 800
screen_height = 480
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True

#sfx
target_sound = pygame.mixer.Sound("sfx/coin-sfx.wav")
reset_sound = pygame.mixer.Sound("sfx/reset-sfx.wav")

def draw_score(screen, score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return random.randrange(*position_range), random.randrange(*position_range)

def reset():
    reset_sound.play()
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    snake = [snake_pixel.copy()]
    return snake

def isOutOfBounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 or snake_pixel.left < 0 or snake_pixel.right > square_width

# playground
pixel_width = 50

#snake
snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1

#target
target = pygame.rect.Rect([0, 0, pixel_width, pixel_width])
target.center = generate_starting_position()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    if isOutOfBounds():
        reset()
        snake_length = 1
        score = 0
        snake_direction = (0, 0)

    if snake_pixel.center == target.center:
        target.center = generate_starting_position()
        target_sound.play()
        snake_length += 1
        snake.append(snake_pixel.copy())
        score += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != (0, pixel_width):
        snake_direction = (0, - pixel_width)
    elif keys[pygame.K_s] and snake_direction != (0, - pixel_width):
        snake_direction = (0, pixel_width)
    elif keys[pygame.K_a] and snake_direction != (pixel_width, 0):
        snake_direction = (- pixel_width, 0)
    elif keys[pygame.K_d] and snake_direction != (- pixel_width, 0):
        snake_direction = (pixel_width, 0)

    snake_pixel.move_ip(snake_direction)
    snake.append(snake_pixel.copy())
    snake = snake[-snake_length:]

    if len(snake) > 1 and snake_pixel.collidelist(snake[:-1]) != -1:
        snake = reset()
        snake_length = 1
        snake_direction = (0, 0)
    for snake_part in snake:
        pygame.draw.rect(screen, "green", snake_part)

    pygame.draw.rect(screen, "red", target)

    draw_score(screen, score)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 10

pygame.quit()