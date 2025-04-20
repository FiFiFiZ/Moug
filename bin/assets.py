import pygame
from math import*

# if unpractical to use, i could just load the needed images within the files

class Assets:
    def __init__(self):
        # Load Images
        self.sprites = {
            
        }

    def load_assets(self):
        self.SCREEN_WIDTH = 300
        self.SCREEN_HEIGHT = 300
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)

        to_load = [ # Load Images from the Images folder
            ("circle", "keep_transparency"),
            ("blank", "keep_transparency"),
            ("pixel", ""),
            ("arrow", "keep_transparency")
        ]  # names with special second (or more) item get special treatment in loading (like loading both 0 and 1 name-ending variants)

        for i in range (len(to_load)):
            image_path = "src\\images\\"
            image_path += f"{to_load[i][0]}.png"
            if to_load[i][1] == "keep_transparency":
                self.sprites[to_load[i][0]] = pygame.image.load(image_path)
            else:
                self.sprites[to_load[i][0]] = pygame.Surface.convert(pygame.image.load(image_path))
