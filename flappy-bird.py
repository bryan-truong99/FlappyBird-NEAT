import pygame
import neat
import os
import time
import random

dir = "C:\\Users\\bryan\\Documents\\Python\\FlappyBird-NEAT"
os.chdir(dir)
print (os.getcwd())

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.velocity = 0
        self.tick_count = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        #Displacement formula
        d = self.velocity*self.tick_count +1.5*self.tick_count**2

        #Terminal velocity where the velocity maxes out
        if d>=16:
            d = 16

        #Move up more when jumping
        if d < 0:
            d -= 2

        #Change y position based on displacement
        self.y = self.y + d

        #Checks to see if bird is still jumping to determine tilt
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                    self.tilt -= self.ROTATION_VELOCITY


    def draw(self,win):
        self.img_count +=1

        #Determines which image should be used to make bird flap wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

            #Rotates flappy bird image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft =(self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 500
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

        def set_height(self):
            self.height = random.randrange(50, 450)
            self.top = self.height - self.PIPE_TOP.get_height()
            self.bottom = self.height + self.GAP

        def move(self):
            self.x =- self.VELOCITY

        def draw(self, win):
            win.blit(self.PIPE_TOP, (self.x, self.top))
            win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

        def collide(self, bird):
            bird_mask = bird.get_mask()
            top_mask = pygame.mask.from_surface(self.PIPE_TOP)
            bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

            top_offset = (self.x - bird.x, self.top - round(bird.y))
            bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

            b_point = bird_mask.overlap(bottom_mask, bottom_offset)
            t_point = bird_mask.overlap(top_mask, top_offset)

            if t_point or b_point:
                return True

            return False

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
#Draws window for game using pygame
def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win,bird)

    pygame.quit()
    quit()

main()
