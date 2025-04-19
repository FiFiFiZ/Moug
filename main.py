import pygame
from math import*


class Game:
    def __init__(self):

        # Initial Setup
        pygame.init()

        self.run = True
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = 300
        self.SCREEN_HEIGHT = 300
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)
        # pygame.display.set_icon

        # Load Images
        self.sprites = {
            
        }

        to_load = [ # Load Images from the Images folder
            ("circle", "keep_transparency"),
            ("blank", "keep_transparency"),
            ("pixel", "")
        ]  # names with special second (or more) item get special treatment in loading (like loading both 0 and 1 name-ending variants)

        for i in range (len(to_load)):
            image_path = "src\\images\\"
            image_path += f"{to_load[i][0]}.png"
            if to_load[i][1] == "keep_transparency":
                self.sprites[to_load[i][0]] = pygame.image.load(image_path)
            else:
                self.sprites[to_load[i][0]] = pygame.Surface.convert(pygame.image.load(image_path))

        self.player_pos = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.player_x, self.player_y = self.player_pos
        self.player_xs = 700/500
        self.player_ys = 550/500

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

    def player(self):
        player_img = self.sprites["circle"]
        self.player_x += self.player_xs
        self.player_y += self.player_ys
        player_pos = (self.player_x, self.player_y)
        # print(player_pos)

        self.mousex, self.mousey = pygame.mouse.get_pos()

        factor = 1
        player_img = pygame.transform.scale_by(player_img, factor)
        # print(factor, player_img)
        player_pos = self.draw_and_center_image(player_img, player_pos)

        player_rect = pygame.rect.Rect(player_pos[0], player_pos[1], player_img.get_width(), player_img.get_height())
        screen_rect = pygame.rect.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if screen_rect.contains(player_rect) == False: # check where circle collided with screen (create a hitbox on each side of the circle to check collision)
            iw = player_img.get_width()/2
            ih = player_img.get_height()/2
            px = player_pos[0]
            py = player_pos[1]
            hitbox_list = [(px+iw, py), (px, py+ih), (px+iw, py+2*ih), (px+2*iw, py+ih)] # up, left, down, right
            for i in range (len(hitbox_list)):
                # hitbox = pygame.rect.Rect(hitbox_list[i]) 
                hitbox = hitbox_list[i]
                if screen_rect.collidepoint(hitbox) == False:
                    self.player_xs *= 1-(2*(i%2==1))
                    self.player_ys *= 1-(2*(i%2==0))

        mask = pygame.mask.from_surface(player_img)
        mask_overlap = mask.overlap(pygame.mask.from_surface(self.sprites["pixel"]), (self.mousex-player_pos[0], self.mousey-player_pos[1]))

        mask.invert()
        mask = pygame.mask.Mask.to_surface(mask)
        mask.set_colorkey((255,255,255))

        if mask_overlap == None:
            self.lose()
        else:
            self.screen.blit(mask, player_pos)

        self.player_pos = player_pos



    def game_run(self):
        while self.run:
            self.clock.tick(500)

            self.screen.fill((50,50,50))
            self.player()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()

