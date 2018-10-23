# Snake Game!
# By root
# Coded by Halsey

# Our imports
import pygame
import random
import sys
import time

count = 0

check_errors = pygame.init()

if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...").fomrat(check_errors[1])
    sys.exit(-1)  # -1 convention for exiting with error
else:
    print("(+) PyGame successfully initialized!")


# Screen Play Surface
play_surface = pygame.display.set_mode((720, 460))  # TODO make height and width global variables
pygame.display.set_caption("Snake Game!")

# Colors
red = pygame.Color(255, 0, 0)  # Game Over Message Color
green = pygame.Color(0, 255, 0)  # Snake Color
black = pygame.Color(0, 0, 0)  # Score Color
white = pygame.Color(255, 255, 255)  # Background Color
brown = pygame.Color(165, 42, 42)  # Food Color

# Frames Per Second Controller
fps_controller = pygame.time.Clock()

# Important Variables
snake_position = [100, 50]  # [x-cord, y-cord]
snake_body = [[100, 50], [90, 50], [80, 50]]  # [x-cord, y-cord] for each snake block. Starts at 3 blocks

food_position = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]  # Random numbers multiplied by 10 since we are using block length of 10
food_spawn = True

direction = "RIGHT"
change_to = direction

score = 0


# Game Over Function
def game_over():
    my_font = pygame.font.SysFont("monaco", 72)
    game_over_surface = my_font.render("Game Over!", True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (360, 100)  # [x-cord, y-cord]
    play_surface.blit(game_over_surface, game_over_rectangle)
    #pygame.display.flip()
    show_score(2)
    pygame.display.update(game_over_rectangle)
    pygame.display.set_mode((720, 460))  # Hacky solution for updating display
    time.sleep(4)
    pygame.quit()   # Exits pygame window
    sys.exit()     # Exits console


def show_score(choice=1):
    score_font = pygame.font.SysFont("monaco", 36)
    score_surface = score_font.render("Score: %d" % score, True, black)
    score_rectangle = score_surface.get_rect()

    if choice == 1:
        score_rectangle.midtop = (80, 10)  # [x-cord, y-cord]
    else:
        score_rectangle.midtop = (360, 180)  # [x-cord, y-cord]

    play_surface.blit(score_surface, score_rectangle)


# Main Logic of the Game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = "RIGHT"
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = "LEFT"
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = "UP"
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = "DOWN"
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validation of Direction
    if change_to == "RIGHT" and direction != "LEFT":
        direction = change_to
    if change_to == "LEFT" and direction != "RIGHT":
        direction = change_to
    if change_to == "UP" and direction != "DOWN":
        direction = change_to
    if change_to == "DOWN" and direction != "UP":
        direction = change_to

    # Update Snake Position
    if direction == "RIGHT":
        snake_position[0] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10

    # Snake Body Mechanism - Inserts new position to front of snake
    snake_body.insert(0, list(snake_position))

    # Checks x-coordinate and y-coordinate of snake head and food
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        food_spawn = False;
        score += 1
    else:
        snake_body.pop()  # Removes Snake tail giving illusion the snake is moving

    # Spawns Food
    if not food_spawn:
        food_position = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    food_spawn = True

    # Sets Background Color
    play_surface.fill(white)

    # Draws Snake
    for body_part in snake_body:
        body_part_rectangle = pygame.Rect(body_part[0], body_part[1], 10, 10)
        pygame.draw.rect(play_surface, green, body_part_rectangle)

    # Draws Food
    food_rectangle = pygame.Rect(food_position[0], food_position[1], 10, 10)
    pygame.draw.rect(play_surface, brown, food_rectangle)

    # Checks if Boundaries are hit
    if snake_position[0] >= 720 or snake_position[0] < 0 or snake_position[1] >= 460 or snake_position[1] < 0:
        game_over()

    for body_part in snake_body[1:]:
        if snake_position[0] == body_part[0] and snake_position[1] == body_part[1]:
            game_over()

    show_score()
    pygame.display.flip()
    fps_controller.tick(30)

    # TODO pyinstaller for executables
    # TODO Different Levels
    # TODO Images for Icons
    # TODO Start Menu with Instructions and High Score Screens
    # TODO Replay Button
    # TODO Better Functions for Readability
    # TODO Pause Button
