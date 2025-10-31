import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from utils import Cooldown
from random import choice
from utils import Spritesheet
from os import path
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        # creates the sprite
        Sprite.__init__(self)
        self.game = game
        self.sprite_sheet = Spritesheet(path.join(self.game.img_folder, "player_spritesheet.png"))
        self.load_images()
        self.image = pg.Surface(TILESIZE)
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.image_inv = game.player_img_inv
        # how big the sprite is
       # self.image = pg.Surface(TILESIZE)
        # sprite color
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # sprite coordinates
        # self.rect.x = x * TILESIZE[0]
        # self.rect.y = y * TILESIZE[1]
        # velocity
        self.vel = vec(0, 0)
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # speed
        self.speed = 250
        # health
        self.health = HEALTH
        # coins
        self.coins = 0
        # cooldown
        self.cd = Cooldown(1000)
        # jump
        self.jump_strength = -10
        self.dir = vec(0, 0)
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0
    def load_images(self):
        self.standing_frames = [self.sprite_sheet.get_image(0, 0, 32, 32).
                                self.spritesheet.get_image(0, 32, 32, 32)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        # when space is pressed the player shoots
        if keys[pg.K_SPACE]:
            self.vel[1] = self.jump_strength
            #p = PewPew(self.game, self.rect.x, self.rect.y, self.dir)
        # when w is pressed the player moves up
        if keys[pg.K_w]:
            self.vel.y = -self.speed * self.game.dt
            self.dir = (0, -1)
        # when a is pressed the player moves to the left
        if keys[pg.K_a]:
            self.vel.x = -self.speed * self.game.dt
            self.dir = (-1, 0)
        # when s is pressed the player moves down
        if keys[pg.K_s]:
            self.vel.y = self.speed * self.game.dt
            self.dir = (0, 1)
        # when d is pressed the player moves to the right
        if keys[pg.K_d]:
            self.vel.x = self.speed * self.game.dt
            self.dir = (1, 0)
        # accounting for diagonal movement
        if self.vel[0] != 0 and self.vel[1] != 0:
            self.vel *= 0.7071
    def collide_with_walls(self, dir):
        # handles collsion with walls
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # detects if the wall is moveable
                    if hits[0].state == "moveable":
                        print("i hit a moveable block...")
                    # moves if the wall is moveable
                        hits[0].pos.x += self.vel.x
                    else:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def collide_with_stuff(self, group, kill):
        # makes collisions happen
        hits = pg.sprite.spritecollide(self, group, kill)
        # collides with mob
        if hits: 
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                    self.cd.start()
        # collides with coin
            elif str(hits[0].__class__.__name__) == "Coin":
                self.coins += 1
    def update(self):
        self.get_keys()
        # moves the player
        self.pos += self.vel
        self.rect.x = self.pos.x
        # handles collision with walls
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        # kills game if player is dead
        if self.health == 0:
            self.game.playing = False
        # makes mob collide
        self.collide_with_stuff(self.game.all_mobs, False)
        # makes coin disappear
        self.collide_with_stuff(self.game.all_coins, True)
        if not self.cd.ready():
            self.image = self.game.player_img
        else:
            self.image = self.game.player_img_inv


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        # creates the mob
        Sprite.__init__(self)
        self.game = game
        # how big the mob is
        self.image = pg.Surface((32, 32))
        # mob color
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # velocity
        self.vel =vec(choice([-1,1]), choice([-1,1]))
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # speed
        self.speed = 5
        print(self.pos)
    def collide_with_walls(self, dir):
        # handles collision with walls
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                # self.vel.x = 0
                self.rect.x = self.pos.x
                # bounces off in random direction
                self.vel *= choice([-1,1])
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                # self.vel.y = 0
                self.rect.y = self.pos.y
                # bounces off in random direction
                self.vel *= choice([-1,1])
    def update(self):
        pass
        # mob behavior
        if self.game.player.pos.x > self.pos.x:
            self.vel.x = 1
        else:
            self.vel.x = -1
            print("I don't need to chase the player x")
        if self.game.player.pos.y > self.pos.y:
            self.vel.y = 1
        else:
            self.vel.y = -1
            print("I don't need to chase the player x")
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        # creates the coin
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
    def update(self):
        # coin behavior
        pass

class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        # creats the wall
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE[0]
        self.state = state
    def update(self):
        # wall
        # moves if the wall is moveable
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class PewPew(Sprite):
    def __init__(self, game, x, y, dir):
        self.game = game
        self.groups = game.all_sprites, game.all_pewpews
        Sprite.__init__(self, self.groups)
        # creates the mob
        Sprite.__init__(self)
        self.game = game
        # how big the mob is
        self.image = pg.Surface((16, 16))
        # mob color
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # velocity
        self.vel = vec(dir)
        # position
        self.pos = vec(x, y)
        # speed
        self.speed = 10
    def update(self):
        # pewpew behavior
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        # pewpew collides with wall 
        hits_wall = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits_wall:
            self.kill()
        # pewpew collides with mob
        hits_mob = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if hits_mob:
            self.kill()