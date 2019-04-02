import pygame
from pygame.locals import *

import time
import random

pygame.init()

RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.help_text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.help_text = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

        return self.help_text

    def update(self, x, y):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Game():
    def __init__(self):
        self.display_width = 1280
        self.display_height = 720
        self.screen = pygame.display.set_mode((self.display_width, self.display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.username = ''
        self.show_warning_empty_username = False

    def text_objects(self, text, font, color = BLACK):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def quit_game(self):
        pygame.quit()
        quit()

    def button(self, msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def game_intro(self):
        intro = True
        input_box = InputBox(self.display_width / 2, self.display_height / 2, 140, 32)

        while intro:
            for event in pygame.event.get():
                # print(event)
                self.username = input_box.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.display_width, self.display_height = pygame.display.get_surface().get_size()


            self.screen.fill(WHITE)
            #input_box = InputBox(display_width/2, display_height/2, 140, 32)
            input_box.update(self.display_width/2, self.display_height/2)
            input_box.draw(self.screen)

            # super mario text
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects("Super Mario", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 3))
            self.screen.blit(TextSurf, TextRect)

            # input box text
            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = self.text_objects("Enter your name: ", smallText)
            TextRect.center = ((self.display_width / 2 - 90), (self.display_height / 2) + 20)
            self.screen.blit(TextSurf, TextRect)

            if self.show_warning_empty_username:
                smallText = pygame.font.Font('freesansbold.ttf', 20)
                TextSurf, TextRect = self.text_objects("You forgot to enter your name!!!", smallText, RED)
                TextRect.center = ((self.display_width / 2 - 60), (self.display_height / 2) + 50)
                self.screen.blit(TextSurf, TextRect)

            self.button("GO!", self.display_width*1/4, self.display_height*2/3, 100, 50, GREEN, BRIGHT_GREEN, self.game_loop)
            self.button("Quit", self.display_width*3/4, self.display_height*2/3, 100, 50, RED, BRIGHT_RED, self.quit_game)

            pygame.display.update()


    def game_loop(self):
        if self.username:
            gameExit = False

            while not gameExit:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                # new game after intro
                self.screen.fill(BLACK)
                pygame.display.update()
                # clock.tick(60)
        else:
            self.show_warning_empty_username = True

if __name__ == '__main__':
    game = Game()
    game.game_intro()
