import pygame
from pygame.locals import *

import time
import random


pygame.init()

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

enemyWalkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
enemyWalkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

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


class Game:
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
        #object level background
        levelbg = LevelBg(screen_height=self.display_height)
        player = Player(200, 578, 64, 64)
        enemy = Enemy(100, 588, 64, 64, 450)

        if self.username:
            gameExit = False

            while not gameExit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == VIDEORESIZE:
                        self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                        self.display_width, self.display_height = pygame.display.get_surface().get_size()
                        levelbg.rescale(self.display_height, self.display_width)
                        self.screen.blit(pygame.transform.scale(levelbg.lvl_bg_img, (levelbg.bg_scale_w,levelbg.bg_scale_h)),(levelbg.mx,0))

                # new game after intro
                # COMMENT BIG see down -> 'line 248'

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT] and player.x > player.vel:
                    player.x -= player.vel
                    player.left = True
                    player.right = False
                elif keys[pygame.K_RIGHT] and player.x < self.display_width - player.width - player.vel:
                    player.x += player.vel
                    player.right = True
                    player.left = False
                else:
                    player.right = False
                    player.left = False
                    player.walkCount = 0

                if not player.isJump:
                    if keys[pygame.K_UP]:
                        player.isJump = True
                        player.right = False
                        player.left = False
                        player.walkCount = 0
                else:
                    if player.jumpCount >= -10:
                        neg = 1
                        if player.jumpCount < 0:
                            neg = -1
                        player.y -= (player.jumpCount ** 2) * 0.5 * neg
                        player.jumpCount -= 1
                    else:
                        player.isJump = False
                        player.jumpCount = 10

                # pygame.display.update()

                levelbg.move(-1)
                self.screen.blit(levelbg.lvl_bg_img, (0, 0))
                self.screen.blit(pygame.transform.scale(levelbg.lvl_bg_img, (levelbg.bg_scale_w,levelbg.bg_scale_h)),(levelbg.mx,0))
                player.draw(self.screen)
                enemy.draw(self.screen)

                #tu niekde bude zrejme blit postavy, skalovanie velkosti postavy by malo byt take iste ako backgroundu meni sa podla vysky okna
                #malo by sa dat pouzit toto -> int()(levelbg.display_height/levelbg.bg_height)* vyska_hraca )
                #pohyb pozadia je pomocou levelbg.move(-1)
                #kde -1 je hracov pohyb doprava...
                # .move() nie je uplne top doladeny...


                pygame.display.update()
                # clock.tick(60) # na toto nesahat, nedokoncene
        else:
            self.show_warning_empty_username = True

    # def redrawGameWindow():
    #     self.screen.blit(levelbg, (0, 0))
    #     player.draw(win)
    #     enemy.draw(self.screen)
    #     pygame.display.update()


class LevelBg:
    def __init__(self, lvl_bg_num='1-1', screen_height=720, screen_width=1280):
        self.lvl_bg_name = 'textures/World ' + lvl_bg_num + '.png'
        self.lvl_bg_img = None
        self.bg_width = 3392
        self.bg_height = 224
        self.bg_scale_w = 1
        self.bg_scale_h = 1
        self.display_height = screen_height
        self.display_width = screen_width
        self.mx = 0

        self.testrun = False
        #auto itself initialization
        self.load_img()
        self.crop_img()
        self.rescale()

    def load_img(self):
        try:
            self.lvl_bg_img = pygame.image.load(self.lvl_bg_name).convert()
        except pygame.error:
            print("ERROR: Cannot load image: " + self.lvl_bg_name)
        if self.testrun: print('Loading img')

    def crop_img(self, left_up_x=0, left_up_y=0, right_down_x = 0, right_down_y=0):
        if right_down_x == 0: right_down_x = self.bg_width
        if right_down_y == 0: right_down_y = self.bg_height
        try:
            self.lvl_bg_img = self.lvl_bg_img.subsurface(left_up_x,left_up_y,right_down_x,right_down_y)
        except:
            print('ERROR: BAD crop coordinates. Actual cor: left up x:{} y:{}, right down x:{} y:{}'.format(left_up_x,left_up_y,right_down_x,right_down_y))
        if self.testrun: print('Cropping img')

    def rescale(self, screen_height=720, screen_width=1280):
        self.display_height = screen_height
        self.display_width = screen_width
        self.bg_scale_w = int(self.display_height/self.bg_height*self.bg_width)
        self.bg_scale_h = int(self.display_height/self.bg_height*self.bg_height)

        if self.testrun: print('Rescale img')
        if self.testrun: print(self.bg_scale_w)

    def move(self, x):
        #mx = 0 lavy okraj zarovnany
        #mx = - (self.bg_scale_w - self.display_width)
        #treba doriesit centrovanie pri zmensovani zvacsovani okna
        #a meniacu sa rzchlost pri Resizeovani okna
        if self.mx <= - (self.bg_scale_w - self.display_width):
            self.mx = - (self.bg_scale_w - self.display_width)
        else:
            self.mx += x
        if self.testrun: print(self.mx, self.bg_scale_w - self.display_width)


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.character = pygame.image.load('standing.png')

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.character, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(enemyWalkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(enemyWalkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


if __name__ == '__main__':
    game = Game()
    game.game_intro()




    #################### COMMENT BIG see down - this is him
    # '''(this is idea) - call some game state handler
    # if not created game -> level = 1
    # else level += 1
    # od state handlera sa nasledne odvodi ktore data sa maju nacitat
    # level == 1 -> World 1-1.png atd....'''
    ####################
