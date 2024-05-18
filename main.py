import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the new size for the images
new_size = (200, 300) 

RUNNING = [
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentRun1.png")), new_size),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentRun2.png")), new_size)
]

JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentJump.png")), new_size)

DUCKING = [
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentDuck1.png")), new_size),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentDuck2.png")), new_size)
]
HIT = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Student", "StudentHit.png")), new_size)


slim_width = 100 
security_height = 280  
SMALL_SECURITY = [
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecuritySmall1.png")), (slim_width, security_height)),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecuritySmall2.png")), (slim_width, security_height)),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecuritySmall3.png")), (slim_width, security_height))
]

LARGE_SECURITY = [
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecurityLarge1.png")), (slim_width, security_height)),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecurityLarge2.png")), (slim_width, security_height)),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/SecurityGuard", "SecurityLarge3.png")), (slim_width, security_height))
]

BIRD = [
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), (slim_width, slim_width)),
    pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")), (slim_width, slim_width))
]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Constants for obstacle positions
STUDENT_Y_POS = 310
OBSTACLE_Y_POS = SCREEN_HEIGHT - security_height - 10  # Adjusted for alignment

class Student:
    X_POS = 50
    Y_POS = STUDENT_Y_POS
    Y_POS_DUCK = 340
    JUMP_VEL = 13

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.hit_img = HIT

        self.student_duck = False
        self.student_run = True
        self.student_jump = False
        self.student_hit = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.student_rect = self.image.get_rect()
        self.student_rect.x = self.X_POS
        self.student_rect.y = self.Y_POS

    def update(self, userInput):
        if self.student_hit:
            self.image = self.hit_img
            return  # Do not update any other state when hit
        
        if self.student_duck:
            self.duck()
        elif self.student_run:
            self.run()
        elif self.student_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.student_jump:
            self.student_duck = False
            self.student_run = False
            self.student_jump = True
        elif userInput[pygame.K_DOWN] and not self.student_jump:
            self.student_duck = True
            self.student_run = False
            self.student_jump = False
        elif not (self.student_jump or userInput[pygame.K_DOWN]):
            self.student_duck = False
            self.student_run = True
            self.student_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.student_rect = self.image.get_rect()
        self.student_rect.x = self.X_POS
        self.student_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.student_rect = self.image.get_rect()
        self.student_rect.x = self.X_POS
        self.student_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.student_jump:
            self.student_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.student_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.student_rect.x, self.student_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.width *= 0.5  # For example, reduce the width by 50% (adjust as needed)
        self.rect.height *= 0.5
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallSecurity(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = OBSTACLE_Y_POS


class LargeSecurity(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = OBSTACLE_Y_POS


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 280
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Student()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 510
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallSecurity(SMALL_SECURITY))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeSecurity(LARGE_SECURITY))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.student_rect.colliderect(obstacle.rect):
                player.student_hit = True  # Set the hit state
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)
                        
            background()
            cloud.draw(SCREEN)
            cloud.update()
            score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 50)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)

        # Display the starting image (RUNNING[0])
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 8 - 100, SCREEN_HEIGHT // 2 - 200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                run = False

menu(death_count=0)