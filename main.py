# Created by Conor Chan with the help of Chat GPT and Mr. Cozort's class code
# Goal: create a top-down shooter game where the player collects coins and avoids enemies
# Rules: player collects coins to advance levels, and avoid enemies, player has three lives
# Freedom: player can move in 4 directions and double jump
# import necessary modules
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
        self.coins = 0
        self.level = 1
    # sets up a game folder directory path using the current folder containg this file
    # gives the Game class a map property which use the Map class to parse the level1.txt file
    def load_data(self):
        # load game data
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, "level1.txt"))
        self.img_folder = path.join(self.game_folder, "images")
        # load character images
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
                self.playing = False
    def load_level(self, level):
        self.map = Map(path.join(self.game_folder, level))
        # wipes data
        for sprite in self.all_sprites:
            sprite.kill()
        # recreate sprite groups
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
        if self.level == 1 and self.coins == 10:
            self.level = 2
            self.load_level("level2.txt")
        if self.level == 2 and self.coins == 25:
            self.level = 3
            self.load_level("level3.txt")
        if self.level == 3 and self.coins == 45:
            self.level = 4
            self.load_level("win.txt")
        # goes to game over screen
        if self.player.health <= 0:
            self.load_level("GameOver.txt")
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
        self.draw_text(self.screen, "Lives: " + str(self.player.health), 24, BLACK, 100, 100)
        self.draw_text(self.screen, "Coins: " + str(self.coins), 24, BLACK, 400, 400)
      #  self.draw_text(self.screen, str(self.time), 24, BLACK, 100, 400)
        self.all_sprites.draw(self.screen)
        pg.display.flip()



if __name__ == "__main__":
    # creating an instance or instianting the Game class
    g = Game()
    g.new()
    g.run()