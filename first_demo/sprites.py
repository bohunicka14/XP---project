# Sprite classes for platform game
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.posun = 5
        self.health = 100
        self.damage = 10

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_player.get_image(67, 196, 66, 92),
                                self.game.spritesheet_player.get_image(0, 196, 66, 92)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet_player.get_image(0, 0, 72, 97),
                              self.game.spritesheet_player.get_image(73, 0, 72, 97)]
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet_player.get_image(438, 93, 67, 94)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # # wrap around the sides of the screen
        # if self.pos.x > WIDTH:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        assert game is not None, 'Game instance is None!'

        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.enemytype = random.randint(1,2)
        self.load_images()
        self.actualframe = 0
        self.image = self.fly_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH+100])
        self.vxspeed = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vxspeed *= -1
        self.rect.centery = random.randrange(40, HEIGHT-40)
        self.vyspeed = 0
        self.dy = 0.5
        self.updatespeed = 0
        self.updatediff = 5
        self.animationdirection = -1 #-1 up, 1 down


    def load_images(self):
        if self.enemytype == 1:
            self.fly_frames = [self.game.spritesheet_other.get_image(382, 635, 174, 126),
                               self.game.spritesheet_other.get_image(0, 1879, 206, 107),
                               self.game.spritesheet_other.get_image(0, 1559, 216, 101),
                               self.game.spritesheet_other.get_image(0, 1456, 216, 101),
                               self.game.spritesheet_other.get_image(382, 510, 182, 123)]
        elif self.enemytype == 2:
            self.fly_frames = [self.game.spritesheet_other.get_image(566, 510, 122, 139),
                               self.game.spritesheet_other.get_image(568, 1534, 122, 135)]
        for frame in self.fly_frames:
            frame.set_colorkey(BLACK)

    def update(self):
        self.rect.x += self.vxspeed
        self.vyspeed += self.dy
        self.updatespeed += 1

        if self.updatespeed > self.updatediff:
            self.updatespeed = 0

            if self.vyspeed > 3 or self.vyspeed < -3:
                self.dy *= -1

            if self.dy < 0:
                if self.animationdirection == -1:
                    if self.actualframe < len(self.fly_frames)-1:
                        self.actualframe += 1
                    else:
                        self.animationdirection = 1
            else:
                if self.actualframe > 0:
                    self.actualframe -= 1
                else:
                    self.animationdirection = -1


        self.image = self.fly_frames[self.actualframe]
        self.rect.y += self.vyspeed

        if self.rect.left > WIDTH+100 or self.rect.left < -150:
            self.kill()



class RigidObject(pg.sprite.Sprite):
    def __init__(self, game, x, y, sprite_sheet, picture_coords):
        assert game is not None, 'Game instance is None!'
        assert type(x) in {int, float}, 'Wrong type of x arg'
        assert type(y) in {int, float}, 'Wrong type of y arg'
        assert isinstance(sprite_sheet, Spritesheet), 'spritesheet arg is not Spritesheet instance'
        assert len(picture_coords) == 4, 'wrong picture coord arg'
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = sprite_sheet.get_image(*picture_coords)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstacle(RigidObject):
    def __init__(self, game, x, y, sprite_sheet, picture_coords):
        super().__init__(game, x, y, sprite_sheet, picture_coords)


class Platform(RigidObject):
    def __init__(self, game, x, y, sprite_sheet, picture_coords):
        super().__init__(game, x, y, sprite_sheet, picture_coords)
        if random.randrange(100) < TREAT_SPAWN:
            Treat(self.game, self)


class Ground(pg.sprite.Sprite):
    def __init__(self, game, w, h, x, y, is_floor = False):
        assert game is not None, 'Game instance is None!'
        assert type(x) in {int, float}, 'Wrong type of x arg'
        assert type(y) in {int, float}, 'Wrong type of y arg'
        assert type(w) in {int, float}, 'Wrong type of w arg'
        assert type(h) in {int, float}, 'Wrong type of h arg'


        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_floor = is_floor


class Finish(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet_tiles.get_image(*FINISH_IMG_COORDS)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Treat(pg.sprite.Sprite):
    def __init__(self, game, plat):
        assert game is not None, 'Game instance is None!'
        assert plat is not None, 'Platform instance is None!'
        self.groups = game.all_sprites, game.treats
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['coin'])
        self.image = self.game.spritesheet_other.get_image(*TREAT_IMG_COORDS)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()
