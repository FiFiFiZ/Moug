import pygame
from math import*
import sys
sys.path.append("./bin")
from player import Player # type: ignore
from assets import Assets # type: ignore

class Game:
    def __init__(self):

        # Initial Setup
        pygame.init()

        self.run = True
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        self.assets.load_assets()
        self.SCREEN_WIDTH = self.assets.SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.assets.SCREEN_HEIGHT
        self.screen = self.assets.screen
        self.last_tick = 0
        # self.mode = 0
        self.player = Player()
        # pygame.display.set_icon
        # self.player_pos = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        # self.player_x, self.player_y = self.player_pos
        # self.player_xs = 500/500
        # self.player_ys = 320/500
        # self.factor = 1

    def draw_and_center_image(self, img, pos, special="None"):
        if special != "None":
            pass
        x, y = pos
        x -= img.get_width()/2
        y -= img.get_height()/2
        pos = (x, y)
        self.screen.blit(img, pos)
        return pos

    def lose(self):
        pass

    def game_run(self):
        while self.run:
            self.clock.tick(500)

            FPS = 1000/(pygame.time.get_ticks()-self.last_tick)
            # print(FPS)
            self.last_tick = pygame.time.get_ticks()
            
            self.key = pygame.key.get_just_pressed()

            self.player.main()
            self.mode = self.player.mode # update mode

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()

