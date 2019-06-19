import pygame as pg
from settings import *
from sprites import *
from os import path

import time
import random


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        assert type(x) in {int, float}, 'X parameter has wrong type!'
        assert type(y) in {int, float}, 'Y parameter has wrong type!'
        assert type(w) in {int, float}, 'W parameter has wrong type!'
        assert type(h) in {int, float}, 'H parameter has wrong type!'
        assert type(text) == str, 'Text parameter has wron type!'

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
                    assert self.text != '', 'Text of input box is empty!'
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
        assert type(x) in {float, int}, 'X parameter has wrong type!'
        assert type(y) in {float, int}, 'Y parameter has wrong type!'
        width = max(200, self.txt_surface.get_width() + 10)
        assert width >= 200, 'Width of input box is smaller than expected'
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
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.username = ''
        self.show_warning_empty_username = False
        self.load_data()
        self.lives, self.score = 0, 0

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = path.join(self.dir, 'SOUNDS')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump21.wav'))


    def text_objects(self, text, font, color = BLACK):
        assert type(text) == str, 'Text parameter should be the str type!'
        assert type(font) == pygame.font.Font, 'Font parameter has wrong type!'
        assert type(color) == tuple, 'Color should be the tuple type!'
        for c in color:
            assert type(c) in {int, float}, 'Wrong color type!'
            assert 0 <= c <= 255, 'Color parameter out of range!'
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def quit_game(self):
        pygame.quit()
        quit()

    def button(self, msg,x,y,w,h,ic,ac,action=None):
        assert type(msg) == str, 'msg should be the str type!'
        assert type(x) in {int, float} , 'x position should be the int type'
        assert type(y) in {int, float}, 'y position should be the int type'
        assert type(w) in {int, float}, 'width parameter should be the int type'
        assert type(h) in {int, float}, 'height parameter should be the int type'
        assert type(ic) == tuple, 'inactive color parameter should be the tuple type'
        assert type(ac) == tuple, 'active color parameter should be the tuple type'

        for color in ic, ac:
            for c in color:
                assert type(c) in {int, float}, 'Wrong color type!'
                assert 0 <= c <= 255, 'Color parameter out of range!'

        # display_width, display_height = pygame.display.get_surface().get_size()
        # assert x <= display_width - w/2, 'Button is partly out of screen! Change coords.'
        # assert y <= display_height - h / 2, 'Button is partly out of screen! Change coords.'

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
        pg.mixer.music.load(path.join(self.snd_dir, 'Menu.ogg'))
        pg.mixer.music.play(loops=-1)
        intro = True
        input_box = InputBox(self.display_width / 2, self.display_height / 2, 140, 32)

        while intro:
            for event in pygame.event.get():
                # print(event)
                self.username = input_box.handle_event(event)
                if event.type == pygame.QUIT:
                    self.quit_game()
                # elif event.type == VIDEORESIZE:
                #     self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                #     self.display_width, self.display_height = pygame.display.get_surface().get_size()


            self.screen.fill(WHITE)
            #input_box = InputBox(display_width/2, display_height/2, 140, 32)
            input_box.update(self.display_width/2, self.display_height/2)
            input_box.draw(self.screen)

            # super mario text
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects("Super cpt.Danko", largeText)
            TextRect.center = ((self.display_width / 2), (self.display_height / 3))
            self.screen.blit(TextSurf, TextRect)

            # input box text
            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = self.text_objects("Enter your name: ", smallText)
            TextRect.center = ((self.display_width / 2 - 90), (self.display_height / 2) + 20)
            self.screen.blit(TextSurf, TextRect)

            if self.show_warning_empty_username:
                assert self.username == '', 'Username should be empty!'
                smallText = pygame.font.Font('freesansbold.ttf', 20)
                TextSurf, TextRect = self.text_objects("You forgot to enter your name!!!", smallText, RED)
                TextRect.center = ((self.display_width / 2 - 60), (self.display_height / 2) + 50)
                self.screen.blit(TextSurf, TextRect)

            self.button("GO!", self.display_width*1/4, self.display_height*2/3, 100, 50, GREEN, BRIGHT_GREEN, self.new)
            self.button("Quit", self.display_width*3/4, self.display_height*2/3, 100, 50, RED, BRIGHT_RED, self.quit_game)

            pygame.display.update()

    def new(self):
        # start a new game
        self.spritesheet_player = Spritesheet(SPRITESHEET_PLAYER)
        self.spritesheet_enemy = Spritesheet(SPRITESHEET_ENEMY)
        self.spritesheet_other = Spritesheet(SPRITESHEET_OTHER)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.treats = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST_LEVEL_1:
            Platform(self, plat[0], plat[1])

        p = Ground(WIDTH*5, 70, 0, HEIGHT - 40)
        self.all_sprites.add(p)
        self.platforms.add(p)

        self.run()
        pg.mixer.music.fadeout(500)

    def run(self):
        # Game Loop
        pg.mixer.music.load(path.join(self.snd_dir, 'Rise_of_spirit.ogg'))
        pg.mixer.music.play(loops=-1)
        self.playing = True
        self.fps = 0 # testing
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        # fadeout of music after ending of game
        # pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # spawn enemies
        self.fps += 1
        if self.fps > 180:
            Enemy(self)
            self.fps = 0
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                        self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        # if player hits coin
        treat_hits = pg.sprite.spritecollide(self.player, self.treats, True)
        for t in treat_hits:
            if t.type == 'coin':
                self.score += 1
                print(self.score)

        # if player reaches top 1/4 of screen
        if self.player.rect.right >= WIDTH - WIDTH / 4:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                # plat.rect.x -= abs(self.player.vel.x)
                # print(self.player.vel)
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    plat.rect.x -= self.player.posun
        if self.player.rect.left <= WIDTH / 4:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                # plat.rect.x += abs(self.player.vel.x)
                # print(self.player.vel)
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    plat.rect.x += self.player.posun


        # spawn new platforms to keep same average number
        # while len(self.platforms) < 6:
        #     width = random.randrange(50, 100)
        #     p = Platform(random.randrange(0, WIDTH - width),
        #                  random.randrange(-75, -30),
        #                  width, 20)
        #     self.platforms.add(p)
        #     self.all_sprites.add(p)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def game_loop(self):
        #object level background
        levelbg = LevelBg(screen_height=self.display_height)
        self.spritesheet = Spritesheet(SPRITESHEET)
        self.player = Player(self)
        # enemy = Enemy(100, 588, 64, 64, 450)

        if self.username:
            gameExit = False
            assert self.username != '', 'Username is empty!'
            while not gameExit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    # elif event.type == VIDEORESIZE:
                    #     self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    #     self.display_width, self.display_height = pygame.display.get_surface().get_size()
                    #     levelbg.rescale(self.display_height, self.display_width)
                    #     self.screen.blit(pygame.transform.scale(levelbg.lvl_bg_img, (levelbg.bg_scale_w,levelbg.bg_scale_h)),(levelbg.mx,0))

                # new game after intro
                # COMMENT BIG see down -> 'line 248'

                # keys = pygame.key.get_pressed()
                #
                # if keys[pygame.K_LEFT] and player.x > player.vel:
                #     player.x -= player.vel
                #     player.left = True
                #     player.right = False
                # elif keys[pygame.K_RIGHT] and player.x < self.display_width - player.width - player.vel:
                #     player.x += player.vel
                #     player.right = True
                #     player.left = False
                # else:
                #     player.right = False
                #     player.left = False
                #     player.walkCount = 0
                #
                # if not player.isJump:
                #     if keys[pygame.K_UP]:
                #         player.isJump = True
                #         player.right = False
                #         player.left = False
                #         player.walkCount = 0
                # else:
                #     if player.jumpCount >= -10:
                #         neg = 1
                #         if player.jumpCount < 0:
                #             neg = -1
                #         player.y -= (player.jumpCount ** 2) * 0.5 * neg
                #         player.jumpCount -= 1
                #     else:
                #         player.isJump = False
                #         player.jumpCount = 10
                #
                # # pygame.display.update()
                #
                # levelbg.move(-1)
                self.screen.blit(levelbg.lvl_bg_img, (0, 0))
                self.screen.blit(pygame.transform.scale(levelbg.lvl_bg_img, (levelbg.bg_scale_w,levelbg.bg_scale_h)),(levelbg.mx,0))
                self.player.update()
                # enemy.draw(self.screen)

                #tu niekde bude zrejme blit postavy, skalovanie velkosti postavy by malo byt take iste ako backgroundu meni sa podla vysky okna
                #malo by sa dat pouzit toto -> int()(levelbg.display_height/levelbg.bg_height)* vyska_hraca )
                #pohyb pozadia je pomocou levelbg.move(-1)
                #kde -1 je hracov pohyb doprava...
                # .move() nie je uplne top doladeny...


                pygame.display.update()
                # clock.tick(60) # na toto nesahat, nedokoncene
        else:
            self.show_warning_empty_username = True
            assert self.username == '', 'Username should be empty!'


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


# class Player:
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.vel = 5
#         self.isJump = False
#         self.left = False
#         self.right = False
#         self.walkCount = 0
#         self.jumpCount = 10
#         self.character = pygame.image.load('IMAGES/standing.png')
#
#     def draw(self, win):
#         assert len(walkLeft) != 0, 'Zoznam obrazkov je prazdny'
#         assert len(walkRight) != 0, 'Zoznam obrazkov je prazdny'
#         if self.walkCount + 1 >= 27:
#             self.walkCount = 0
#
#         if self.left:
#             win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
#             self.walkCount += 1
#         elif self.right:
#             win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
#             self.walkCount += 1
#         else:
#             win.blit(self.character, (self.x, self.y))
#
#
# class Enemy:
#     def __init__(self, x, y, width, height, end):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.end = end
#         self.path = [self.x, self.end]
#         self.walkCount = 0
#         self.vel = 3
#
#     def draw(self, win):
#         self.move()
#         assert len(enemyWalkLeft) != 0, 'Zoznam obrazkov je prazdny'
#         assert len(enemyWalkRight) != 0, 'Zoznam obrazkov je prazdny'
#         if self.walkCount + 1 >= 33:
#             self.walkCount = 0
#
#         if self.vel > 0:
#             win.blit(enemyWalkRight[self.walkCount//3], (self.x, self.y))
#             self.walkCount += 1
#         else:
#             win.blit(enemyWalkLeft[self.walkCount//3], (self.x, self.y))
#             self.walkCount += 1
#
#     def move(self):
#         if self.vel > 0:
#             if self.x + self.vel < self.path[1]:
#                 self.x += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walkCount = 0
#         else:
#             if self.x - self.vel > self.path[0]:
#                 self.x += self.vel
#             else:
#                 self.vel = self.vel * -1
#                 self.walkCount = 0


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
