#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 15:13:24 2021

@author: pratik_pande
"""


import pygame, random, math

from pygame.locals import *

pygame.display.set_caption("Pong- 2 Player Version")


class Paddle(pygame.sprite.Sprite): # Sprite is an object on the screen

    WIDTH, HEIGHT = 15, 150
    SPEED = 20 # All capital letters means that these should not change
    def __init__(self, pos, up, down):
        pygame.sprite.Sprite.__init__(self) # Initialize the sprite

        self.rect = Rect(0,0,Paddle.WIDTH, Paddle.HEIGHT)
        self.rect.center = pos

        self.image = pygame.Surface(self.rect.size) # Creates image based on rectangle size
        self.image.fill(Color('red'))

        self.up = up
        self.down = down

    def handle_keystate(self, keys, screen):
        if keys[self.up] and self.rect.top >= 0:
            self.rect.top -= self.SPEED
        if keys[self.down] and self.rect.bottom <= screen.get_height():
            self.rect.top += self.SPEED


class Ball(pygame.sprite.Sprite):
    SPEED = 7
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.rect = Rect(400,300,20,20)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(Color('grey80'))
        self.screen = screen
        self.velx = self.SPEED # "vel" is velocity
        self.vely = self.SPEED

    def update(self, game):
        self.rect.x += self.velx # Adds to x velocity value of rectangle
        self.rect.y += self.vely

        if self.rect.top <= 0:
            self.vely *= -1
        if self.rect.bottom >= self.screen.get_height():
            self.vely *= -1

        # Did the ball go off the screen?
        if not self.rect.colliderect(self.screen.get_rect()):
            if self.velx > 0:
                game.score1 += 1
            elif self.velx < 0:
                game.score2 += 1
            self.reset()

    def reset(self):
        self.rect.center = (self.screen.get_width() / 2,
                            self.screen.get_height() / 2) # Puts ball at center of screen
        self.velx = 0
        self.vely = 0


    def handle_collision(self, paddle, game): # Handles when the ball hits either of the paddles
        if self.velx > 0:
            self.rect.right = paddle.rect.left
            self.velx *= -1
            self.vely += random.randint(-3, 3) # Adding some variation to the angle that the ball hits the paddle
        elif self.velx < 0:
            self.rect.left = paddle.rect.right
            self.velx *= -1
            self.vely += random.randint(-3, 3)



class GameMain:

    done = False
    color_bg = Color('black')

    def __init__(self, width = 800, height = 600): # A screen and a clock will be required for every videogame
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.player_1 = Paddle((50, 300), K_w, K_s)
        self.player_2 = Paddle((self.width - 50, 300), K_UP, K_DOWN)

        # Creating a Group (a list of sprites)
        self.paddles = pygame.sprite.Group()
        self.paddles.add(self.player_1, self.player_2)

        self.ball = Ball(self.screen)
        self.balls = pygame.sprite.Group()
        self.balls.add(self.ball)

        self.score1 = 0
        self.score2 = 0

        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def main_loop(self): # This loop runs all the time and waits for something to happen (like hitting a key)
        while not self.done:
            self.handle_events() # How the program reacts when the user hits akey
            self.draw() # This draws everything to the screen
            self.clock.tick(60)
            self.balls.update(self)

            for p in self.paddles:
                if self.ball.rect.colliderect(p.rect): # If the ball collided with the paddle
                    self.ball.handle_collision(p, self)

        pygame.quit() # If done = True, pygame quits.

    def draw(self):
        self.screen.fill(self.color_bg) # This keeps the background color consistent as you draw over it

        # Draw stuff
        self.paddles.draw(self.screen)
        self.balls.draw(self.screen)
        self.score1_label = self.font.render(str(self.score1), True, Color('white'))
        self.score1_rect = self.score1_label.get_rect()
        self.score1_rect.left = 10
        self.score1_rect.top = 10
        self.screen.blit(self.score1_label, self.score1_rect)
        self.score2_label = self.font.render(str(self.score2), True, Color('white'))
        self.score2_rect = self.score2_label.get_rect()
        self.score2_rect.right = self.screen.get_width()-10
        self.score2_rect.top = 10
        self.screen.blit(self.score2_label, self.score2_rect)
        pygame.display.flip()


    def handle_events(self):

        events = pygame.event.get() # Listens for anything that has happened and gets every event

        keys = pygame.key.get_pressed()
        self.player_1.handle_keystate(keys, self.screen)
        self.player_2.handle_keystate(keys, self.screen)

        for event in events:

            if event.type == pygame.QUIT: # Click on the X in the top right corner to quit
                self.done = True
                pygame.quit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC causes the program to quit
                    self.done = True
                elif event.key == K_SPACE and self.ball.velx == 0 and self.ball.vely == 0: # Ball will move at random angle when Spacebar is pressed
                    ranges = list(range(0, 75)) + list(range(105, 255)) + list(range(285- 259))
                    angle = math.radians(random.choice(ranges)) # The degrees need to be turned back into radiants.
                    self.ball.velx = math.cos(angle) * self.ball.SPEED
                    self.ball.vely = math.sin(angle) * self.ball.SPEED

if __name__ == '__main__':
    game = GameMain() # Create the game
    game.main_loop()  # Run the main loop of the game
