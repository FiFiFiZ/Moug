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
        self.mode = 0
        self.player = Player()
        # pygame.display.set_icon

        # # Load Images
        # self.sprites = {
            
        # }

        # to_load = [ # Load Images from the Images folder
        #     ("circle", "keep_transparency"),
        #     ("blank", "keep_transparency"),
        #     ("pixel", ""),
        #     ("arrow", "keep_transparency")
        # ]  # names with special second (or more) item get special treatment in loading (like loading both 0 and 1 name-ending variants)

        # for i in range (len(to_load)):
        #     image_path = "src\\images\\"
        #     image_path += f"{to_load[i][0]}.png"
        #     if to_load[i][1] == "keep_transparency":
        #         self.sprites[to_load[i][0]] = pygame.image.load(image_path)
        #     else:
        #         self.sprites[to_load[i][0]] = pygame.Surface.convert(pygame.image.load(image_path))

        self.player_pos = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.player_x, self.player_y = self.player_pos
        self.player_xs = 500/500
        self.player_ys = 320/500
        self.factor = 1

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

            self.screen.fill((50,50,50))
            self.player.main()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()

