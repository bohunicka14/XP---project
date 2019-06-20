import pygame
import pygame as pg
from settings import *
from sprites import *
from os import path

import random
import unittest


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        assert type(x) in {int, float}, 'X parameter has wrong type!'
        assert type(y) in {int, float}, 'Y parameter has wrong type!'
        assert type(w) in {int, float}, 'W parameter has wrong type!'
        assert type(h) in {int, float}, 'H parameter has wrong type!'
        assert type(text) == str, 'Text parameter has wrong type!'

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
        assert type(self.rect.x) in {float, int}, "self.rect.x has wrong type"
        assert type(self.rect.y) in {float, int}, "self.rect.x has wrong type"
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Game:
    def __init__(self):
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
        self.enemspawnsped = ENEMY_SPAWN_SPEED


        self.lvl_bg_name = 'IMAGES/background.png'
        assert path.isfile(self.lvl_bg_name), 'file {} does not exist'.format(self.lvl_bg_name)
        self.lvl_bg_img = pygame.image.load(self.lvl_bg_name).convert()
        self.screen.blit(self.lvl_bg_img, (0, 0))



    def load_data(self):
        self.dir = path.dirname(__file__)
        assert path.isdir(path.join(self.dir, 'SOUNDS')), 'dir SOUNDS does not exist'
        self.snd_dir = path.join(self.dir, 'SOUNDS')

        assert path.isfile(path.join(self.snd_dir, 'Jump21.wav')), 'file Jump21.wav does not exist'
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump21.wav'))
        self.dmg_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Randomize37.wav'))


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
        assert path.isfile(path.join(self.snd_dir, 'Menu.ogg')), 'file Menu.ogg does not exist'
        pg.mixer.music.load(path.join(self.snd_dir, 'Menu.ogg'))
        pg.mixer.music.play(loops=-1)
        intro = True
        input_box = InputBox(WIDTH / 2, HEIGHT / 2, 140, 32)

        while intro:
            for event in pygame.event.get():
                # print(event)
                self.username = input_box.handle_event(event)
                if event.type == pygame.QUIT:
                    self.quit_game()
                # elif event.type == VIDEORESIZE:
                #     self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                #     WIDTH, HEIGHT = pygame.display.get_surface().get_size()


            self.screen.fill(WHITE)
            #input_box = InputBox(display_width/2, display_height/2, 140, 32)
            input_box.update(WIDTH/2, HEIGHT/2)
            input_box.draw(self.screen)

            # super mario text
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects("Super cpt.Danko", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 3))
            self.screen.blit(TextSurf, TextRect)

            # input box text
            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = self.text_objects("Enter your name: ", smallText)
            TextRect.center = ((WIDTH / 2 - 90), (HEIGHT / 2) + 20)
            self.screen.blit(TextSurf, TextRect)

            if self.show_warning_empty_username:
                assert self.username == '', 'Username should be empty!'
                smallText = pygame.font.Font('freesansbold.ttf', 20)
                TextSurf, TextRect = self.text_objects("You forgot to enter your name!!!", smallText, RED)
                TextRect.center = ((WIDTH / 2 - 60), (HEIGHT / 2) + 50)
                self.screen.blit(TextSurf, TextRect)

            self.button("GO!", WIDTH*1/4, HEIGHT*2/3, 100, 50, GREEN, BRIGHT_GREEN, self.new)
            self.button("Quit", WIDTH*3/4, HEIGHT*2/3, 100, 50, RED, BRIGHT_RED, self.quit_game)

            pygame.display.update()

    def new(self):
        assert self.username != '', 'username is not defined'
        # start a new game
        self.spritesheet_player = Spritesheet(SPRITESHEET_PLAYER)
        self.spritesheet_enemy = Spritesheet(SPRITESHEET_ENEMY)
        self.spritesheet_other = Spritesheet(SPRITESHEET_OTHER)
        self.spritesheet_tiles = Spritesheet(SPRITESHEET_TILES)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.treats = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.finish = Finish(self, WIDTH*5 - 50, HEIGHT - 75)
        self.score = 0

        for plat in PLATFORM_LIST_LEVEL_1:
            assert len(plat) == 2, "Platform coords are wrong. Check settings.py"
            assert type(plat[0]) in {int, float}, "Wrong type of platform coordinates"
            assert type(plat[1]) in {int, float}, "Wrong type of platform coordinates"
            Platform(self, plat[0], plat[1], self.spritesheet_other, PLATFORM_IMG_COORDS)

        p = Ground(self, WIDTH*5, 70, 0, HEIGHT - 40, True)
        left_wall = Ground(self, 350, HEIGHT, -350, 0)
        right_wall = Ground(self, 350, HEIGHT, WIDTH*5, 0)

        self.run()
        pg.mixer.music.fadeout(500)

    @property
    def visible_platforms(self):
        visible_platforms = pg.sprite.Group()
        for plat in self.platforms:
            if plat.rect.left <= WIDTH and plat.rect.right >= 0:
                visible_platforms.add(plat)

        return visible_platforms

    @property
    def visible_enemies(self):
        visible_enemies = pg.sprite.Group()
        for enemy in self.enemies:
            if enemy.rect.left <= WIDTH and enemy.rect.right >= 0:
                visible_enemies.add(enemy)

        return visible_enemies


    def run(self):
        # Game Loop
        assert path.isfile(path.join(self.snd_dir, 'Rise_of_spirit.ogg')), 'file Rise_of_spirit.ogg does not exist'
        pg.mixer.music.load(path.join(self.snd_dir, 'Rise_of_spirit.ogg'))
        pg.mixer.music.play(loops=-1)
        self.playing = True
        self.fps = 0 # testing
        self.spawntimer = 0
        self.spawnt2 = 0
        self.wasenemyhit = False

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
        self.spawntimer += 1

        assert type(self.enemspawnsped) == int, 'wrong self.enemspawnsped type'
        assert type(self.spawntimer) == int, 'wrong self.spawntimer type'
        if self.spawntimer > self.enemspawnsped:
            Enemy(self)
            self.spawnt2 += self.spawntimer
            self.spawntimer = 0
            # speed up spawning
            if self.spawnt2 > ENEMY_SPAWN_TIMER and self.enemspawnsped > 40:
                self.enemspawnsped -= 10
                self.spawnt2 = 0

        #enemies collides PLAYER
        # print("self.enemies", self.enemies)
        enemy_hit = pg.sprite.spritecollide(self.player, self.visible_enemies, False)
        if enemy_hit and not self.wasenemyhit:
            if enemy_hit[0].rect.y - self.player.rect.y > 0 and enemy_hit[0].rect.y - self.player.rect.y < \
                    enemy_hit[0].rect.height/2 + self.player.rect.height/2:
                # player jumped on top of enemy
                enemy_hit[0].kill()
            else:
                self.player.health -= self.player.damage
                self.wasenemyhit = True
                if self.player.health <= 0:
                    self.game_over_screen('lose')
                # print("hitted enemy", self.player.health)

            self.dmg_sound.play()
            # print("hitted enemy", self.player.health)

        else:
            if not enemy_hit:
                self.wasenemyhit = False


        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.visible_platforms, False)
            if hits:
                lowest = hits[0]
                is_obstacle = False
                for hit in hits:
                    if isinstance(hit, Obstacle) or (isinstance(hit, Ground) and hit.is_floor == False):
                        is_obstacle = True
                        lowest = hit
                        break
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if is_obstacle:
                    self.player.vel.x = 0
                    # collision from right side of obstacle
                    if self.player.pos.x >= lowest.rect.x:
                        self.player.pos.x = lowest.rect.right + self.player.rect.width / 2 + 1
                    # collision from left side of obstacle
                    elif self.player.pos.x <= lowest.rect.x:
                        self.player.pos.x = lowest.rect.left - self.player.rect.width / 2 - 1


                else:
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

        # if player hits exit
        col = pg.sprite.collide_rect(self.player, self.finish)
        if col:
            if self.score > 5:
                self.game_over_screen('win')

        # if player reaches 3/4 width of screen
        if self.player.rect.right >= WIDTH - WIDTH / 4:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                # plat.rect.x -= abs(self.player.vel.x)
                # if plat.rect.right <= 0:
                #     plat.kill()

                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    plat.rect.x -= self.player.posun

            for treat in self.treats:
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    treat.rect.x -= self.player.posun

            for enemy in self.enemies:
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    enemy.rect.x -= self.player.posun

            # if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
            #     self.finish.rect.x -= self.player.posun

        # if player reaches 1/4 width of screen
        if self.player.rect.left <= WIDTH / 4:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                # plat.rect.x += abs(self.player.vel.x)
                # if plat.rect.left >= WIDTH:
                #     plat.kill()
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    plat.rect.x += self.player.posun

            for treat in self.treats:
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    treat.rect.x += self.player.posun

            for enemy in self.enemies:
                if (round(self.player.vel[0]), round(self.player.vel[1])) != (0, 0):
                    enemy.rect.x += self.player.posun

        # spawn new platforms to keep same average number
        while len(self.visible_platforms) < 5:
            Platform(self, WIDTH,
                     random.randrange(50, HEIGHT - 300), self.spritesheet_other, PLATFORM_IMG_COORDS)
            if random.randint(0, 1):
                Obstacle(self, WIDTH, HEIGHT - 115, self.spritesheet_tiles, OBSTACLE_IMG_COORDS)

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

    def game_over_screen(self, result):
        assert type(result) is str, 'wrong param type'
        top_ten_list = self.make_top_ten_list(self.username, self.score)
        if result == 'lose':
            color = YELLOW
            self.screen.fill(LIGHTBLUE)
            self.draw_text("GAME OVER", 50, color, WIDTH / 2, HEIGHT / 4)
        else:
            color = LIGHTBLUE
            self.screen.fill(YELLOW)
            self.draw_text("YOU WON", 50, color, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 40, color, WIDTH / 2, HEIGHT / 2 - 80)
        for i in range(len(top_ten_list[:10])):
            self.draw_text(str(i+1) + ". " + top_ten_list[i][0] + " " + str(top_ten_list[i][1]), 22, color, WIDTH / 2, HEIGHT / 2 + i * 25)
        self.draw_text("Press space key to play again", 22, color, WIDTH / 2, HEIGHT - 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.new()
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        assert type(text) is str, 'wrong text param type'
        assert type(size) is int, 'wrong size param type'
        assert type(color) is tuple, 'wrong color param type'
        assert type(x) in (int, float), 'wrong x param type'
        assert type(y) in (int, float), 'wrong y param type'


        font = pg.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def make_top_ten_list(self, player_name, player_score):
        top_ten_list = []
        data = str(player_name) + "-" + str(player_score)
        self.dir = path.dirname(__file__)
        assert path.isfile(path.join(self.dir, HS_FILE)), 'file [] does not exist'.format(HS_FILE)

        with open(path.join(self.dir, HS_FILE), 'a') as fa:
            fa.write(data + '\n')
            fa.close()


        with open(path.join(self.dir, HS_FILE), 'r') as fr:
            for row in fr:
                r = row.rstrip('\n').split('-')
                top_ten_list.append((r[0], int(r[1])))
        top_ten_list.sort(key=self.sortSecond, reverse=True)
        return top_ten_list

    def sortSecond(self, val):
        return val[1]

    def draw(self):
        # Game Loop - draw
        # self.screen.fill(BLACK)

        self.screen.blit(self.lvl_bg_img, (0, 0))

        self.all_sprites.draw(self.screen)

        assert type(self.score) is int, 'score is wrong type'
        assert type(self.player.health) is int, 'player.health is wrong type'
        assert type(self.username) is str, 'username is wrong type'

        self.draw_text("Coins: " + str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.draw_text("Health: " + str(self.player.health), 22, WHITE, WIDTH / 2, 40)
        self.draw_text("Player: " + str(self.username), 22, WHITE, WIDTH / 2, 65)
        # *after* drawing everything, flip the display
        pg.display.flip()



class Tester(unittest.TestCase):
    # self.assertEqual(, )

    def test_settings(self):
        self.assertEqual(TITLE, "Super Space Cpt Dankis")
        self.assertEqual(WIDTH, 1280)
        self.assertEqual(HEIGHT, 600)
        self.assertEqual(FPS, 60)

        self.assertEqual(SPRITESHEET_PLAYER, "IMAGES/p1_spritesheet.png")
        self.assertEqual(SPRITESHEET_ENEMY, "IMAGES/enemies_spritesheet.png")
        self.assertEqual(SPRITESHEET_OTHER, "IMAGES/spritesheet_jumper.png")
        self.assertEqual(SPRITESHEET_TILES, "IMAGES/tiles_spritesheet.png")
        self.assertEqual(HS_FILE, "highscore.txt")

        self.assertEqual(TREAT_IMG_COORDS, (244, 1981, 61, 61))
        self.assertEqual(PLATFORM_IMG_COORDS, (0, 288, 380, 94))
        self.assertEqual(OBSTACLE_IMG_COORDS, (864, 0, 48, 146))

        self.assertEqual(PLAYER_ACC, 0.5)
        self.assertEqual(PLAYER_FRICTION, -0.12)
        self.assertEqual(PLAYER_GRAV, 0.8)
        self.assertEqual(PLAYER_JUMP, 25)
        self.assertEqual(TREAT_SPAWN, 50)

        self.assertEqual(PLATFORM_LIST_LEVEL_1, [(0, HEIGHT - 40),(WIDTH / 2 - 50, HEIGHT * 3 / 4),(125, HEIGHT - 350),(350, 200),(175, 100)])
        self.assertEqual(WHITE, (255, 255, 255))
        self.assertEqual(BLACK, (0, 0, 0))
        self.assertEqual(RED, (255, 0, 0))
        self.assertEqual(GREEN, (0, 255, 0))
        self.assertEqual(BLUE, (0, 0, 255))
        self.assertEqual(YELLOW, (255, 255, 0))
        self.assertEqual(LIGHTBLUE, (0, 155, 155))
        self.assertEqual(BRIGHT_RED, (255, 0, 0))
        self.assertEqual(BRIGHT_GREEN,  (0, 255, 0))

        self.assertEqual(COLOR_INACTIVE, pygame.Color('lightskyblue3'))
        self.assertEqual(COLOR_ACTIVE, pygame.Color('dodgerblue2'))
        self.assertEqual(type(FONT), type(pygame.font.Font(None, 32)))



if __name__ == '__main__':
    # unittest.main(verbosity=2)
    game = Game()
    game.game_intro()



