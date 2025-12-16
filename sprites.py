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
        # sprite animation
        self.sprite_sheet = Spritesheet(path.join(self.game.img_folder, "Triple_T.png"))
        # loads images for animation
        self.load_images()
        # adding player image
        self.image = pg.Surface(TILESIZE)
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.image_inv = game.player_img_inv
        self.rect = self.image.get_rect()
        # velocity
        self.vel = vec(0, GRAVITY)
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # speed
        self.speed = 250
        # cooldown
        self.cd = Cooldown(1000)
        # health
        self.health = 3
        # jump
        self.jump_count = 0
        self.jump_max = 2
        self.jump_strength = 100
    # jump input edge detection (prevents holding space to spam jumps)
        self.jump_pressed = False
        # direction
        self.dir = vec(0, 0)
        # animation
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.current_frame = 0
    def jump(self):
        # check if standing on a platform (simple grounded check)
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 1
        # if touching ground, ensure jump_count is reset
        if hits:
            self.jump_count = 0
        # allow jump if we haven't exceeded max jumps
        if self.jump_count < self.jump_max:
            self.vel.y = -self.jump_strength
            self.jump_count += 1
    def load_images(self):
        # loads images for animation
        self.standing_frames = [self.sprite_sheet.get_image(0, 0, 32, 32),
                                self.sprite_sheet.get_image(0, 32, 32, 32)]
        # sets colorkey for transparency and scale to TILESIZE
        for i, frame in enumerate(self.standing_frames):
            frame.set_colorkey(BLACK)
            img = pg.transform.scale(frame, TILESIZE)
            self.standing_frames[i] = img
    def animate(self):
        # handles animation
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            # handles standing animation
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def get_keys(self):
        self.vel = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        # when W is pressed the player jumps (edge-detected)
        if keys[pg.K_w]:
            if not self.jump_pressed:
                # key was just pressed
                self.jump()
                self.jump_pressed = True
        else:
            # key released
            self.jump_pressed = False
        # when a is pressed the player moves to the left
        if keys[pg.K_a]:
            self.vel.x = -self.speed * self.game.dt
            self.dir = (-1, 0)
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
                    # wall on right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    # wall on left
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # wall below
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.jump_count = 0
                if self.vel.y < 0:
                    # wall above
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def collide_with_stuff(self, group, kill):
        # makes collisions happen
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: 
            # collides with coins
            if str(hits[0].__class__.__name__) == "Coin":
                self.game.coins += 1
            # collides with pewpews
            if str(hits[0].__class__.__name__) == "PewPew":
                if self.cd.ready():
                    self.health -= 1
                    self.cd.start()
                    if self.health <= 0:
                        self.kill()
    def update(self):
        self.get_keys()
        # handles animation
        self.animate()
        # moves the player
        self.pos += self.vel
        self.rect.x = self.pos.x
        # handles collision with walls
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        # makes coin disappear
        self.collide_with_stuff(self.game.all_coins, True)
        # collision with pewpews
        self.collide_with_stuff(self.game.all_pewpews, True)

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        # sprite animation
        self.sprite_sheet = Spritesheet(path.join(self.game.img_folder, "Bombardillo_Crocodillo.png"))
        self.load_images()
        # adding mob image
        self.image = pg.Surface(TILESIZE)
        self.image = game.player_img
        self.image.set_colorkey(BLACK)
        self.image_inv = game.player_img_inv
        self.rect = self.image.get_rect()
        # velocity
        self.vel = vec(choice([-1,1]), choice([-1,1]))
        # position
        self.pos = vec(x, y) * TILESIZE[0]
        # speed
        self.speed = 5
        print(self.pos)
        self.shoot_cooldown = Cooldown(2000)
        # animation
        self.jumping = False
        self.walking = False
        self.last_update = 0
        self.current_frame = 0
    def load_images(self):
        # loads images for animation
        self.standing_frames = [self.sprite_sheet.get_image(0, 0, 32, 32),
                                self.sprite_sheet.get_image(0, 32, 32, 32)]
        # sets colorkey for transparency and scale to TILESIZE
        for i, frame in enumerate(self.standing_frames):
            frame.set_colorkey(BLACK)
            img = pg.transform.scale(frame, TILESIZE)
            self.standing_frames[i] = img
    def shoot(self):
        # mob shooting behavior
        if self.shoot_cooldown.ready():
            self.dir = choice([(1,0), (-1,0), (0,1), (0,-1)])
            # move bullet outside shooter
            offset = vec(self.dir) * (TILESIZE[0] // 2)
            spawn_pos = vec(self.rect.center) + offset
            PewPew(self.game, spawn_pos.x, spawn_pos.y, self.dir)
            self.shoot_cooldown.start()
    def animate(self):
        # handles animation
        now = pg.time.get_ticks()
        # handles standing animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
    def collide_with_walls(self, dir):
        # handles collision with walls
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # wall on right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    # wall on left
                    self.pos.x = hits[0].rect.right
                # self.vel.x = 0
                self.rect.x = self.pos.x
                # bounces off in random direction
                self.vel.x *= -1
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # wall below
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    # wall above
                    self.pos.y = hits[0].rect.bottom
                # self.vel.y = 0
                self.rect.y = self.pos.y
                # bounces off in random direction
                self.vel.y *= -1
    def update(self):
        self.shoot()
        # handles animation
        self.animate()
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        # creates the coin
        # sprite
        self.image = pg.Surface((32, 32))
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        self.vel = vec(0, GRAVITY)
    def update(self):
        # gravity effect on coin
        self.vel.y += GRAVITY
        self.rect.y += self.vel.y
        # wall
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
        # place coin on top of wall
            self.rect.bottom = hits[0].rect.top
            self.vel.y = 0


class Wall(Sprite):
    def __init__(self, game, x, y, state):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        # creates the wall
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
        super().__init__(game.all_sprites, game.all_pewpews)
        self.game = game
        self.groups = game.all_sprites, game.all_pewpews
        # creates the projectile
        Sprite.__init__(self, self.groups)
        # how big the projectile is
        self.image = pg.Surface((16, 16))
        # projectile color
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
        self.rect.center = self.pos
        # pewpew collides with player
        hits_player = pg.sprite.spritecollide(self, [self.game.player], False)
        if hits_player:
            self.kill()
        # pewpew collides with walls
        hits_wall = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits_wall:
            self.kill()