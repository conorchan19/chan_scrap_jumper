# Created by Conor Chan with the help of Chat GPT
# import necesary modules
# core game loop
# input
# update
# draw

# yay I can use github from VS CODE

import math
import random
import sys
from typing import List, Tuple, Optional
import pygame as pg
from settings import *
from sprites import *
from utils import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Conor Chan's awesome game!!!!!")
        self.playing = True
    # sets up a game folder directory path using the current folder containg this file
    # gives the Game class a map property which use the Map class to parse the level1.txt file
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, "level1.txt"))
        self.img_folder = path.join(self.game_folder, "images")
        self.player_img = pg.image.load(path.join(self.img_folder, "player.png")).convert_alpha()
        self.player_img_inv = pg.image.load(path.join(self.img_folder, 'player.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, "Brr_Brr.png")).convert_alpha()
    def new(self):
        # the sprite Group allows us to update and draw sprite in grouped batches
        self.load_data()
        # create all sprite groups
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_pewpews = pg.sprite.Group()
        # takes the map data and creates the appropriate object for each tile
        for row, tiles, in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row, "")
                elif tile == '2':
                    Wall(self, col, row, "moveable")
                elif tile == "C":
                    Coin(self, col, row)
                elif tile == "P":
                    self.player = Player(self, col, row)
                elif tile == "M":
                    Mob(self, col, row)
    def run(self):
        # game loop
        while self.playing == True:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()
        pg.quit()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # breaks the code and gets rid of screen
                print("this is happening")
                self.playing = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print("I can get input from mousey mouse mouse")
    def load_level(self, level):
        self.map = Map(path.join(self.game_folder, level))
        # clear existing sprites
        self.all_sprites = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_pewpews = pg.sprite.Group()
        # recreate sprites based on new level data
        for row, tiles, in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row, "")
                elif tile == '2':
                    Wall(self, col, row, "moveable")
                elif tile == "C":
                    Coin(self, col, row)
                elif tile == "P":
                    self.player = Player(self, col, row)
                elif tile == "M":
                    Mob(self, col, row)
    def update(self):
        # creates a countdown timer
        self.all_sprites.update()
        # goes to level 2
        if self.player.coins >= 10:
            self.load_level("level2.txt")
        # handle pewpew vs mob collisions
        hits = pg.sprite.groupcollide(self.all_mobs, self.all_pewpews, True, True)
        countdown = 10
        seconds = pg.time.get_ticks()//1000
        self.time = countdown - seconds
        # once there are no coins left, spawns more coins
        if len(self.all_coins) == 0:
         for i in range(2,5):
            Coin(self, randint(1, 20), randint(1,20))
         print("I'm BROKE!")
    def draw_text(self, surface, text, size, color, x, y):
        # draws text on screen
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        # calls on draw_text
        self.screen.fill(WHITE)
        #self.draw_text(self.screen, str(self.player.health), 24, BLACK, 100, 100)
        self.draw_text(self.screen, str(self.player.coins), 24, BLACK, 400, 400)
        self.draw_text(self.screen, str(self.time), 24, BLACK, 100, 400)
        self.all_sprites.draw(self.screen)
        pg.display.flip()



if __name__ == "__main__":
    # creating an instance or instianting the Game class
    g = Game()
    g.new()
    g.run()