import pygame
import random
import speech_recognition as sr

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice-Controlled Catch Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Basket parameters
basket_width, basket_height = 100, 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 20

# Falling object parameters
object_size = 20
object_x = random.randint(0, WIDTH - object_size)
object_y = 0
object_speed = 5

# Score
score = 0
font = pygame.font.Font(None, 36)

# Voice recognition setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def get_voice_command():
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for command...")
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.UnknownValueError:
        return None

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the voice command to move the basket
    command = get_voice_command()
    if command == "left":
        basket_x -= basket_speed
    elif command == "right":
        basket_x += basket_speed

    # Keep basket within screen bounds
    basket_x = max(0, min(basket_x, WIDTH - basket_width))

    # Update object position
    object_y += object_speed

    # Check for collision
    if object_y + object_size >= basket_y and object_x + object_size > basket_x and object_x < basket_x + basket_width:
        score += 1
        object_x = random.randint(0, WIDTH - object_size)
        object_y = 0
        object_speed += 0.5  # Increase speed for difficulty

    # Reset object if it falls off screen
    if object_y > HEIGHT:
        object_x = random.randint(0, WIDTH - object_size)
        object_y = 0

    # Draw basket
    pygame.draw.rect(screen, BLACK, (basket_x, basket_y, basket_width, basket_height))

    # Draw falling object
    pygame.draw.rect(screen, RED, (object_x, object_y, object_size, object_size))

    # Draw score
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
