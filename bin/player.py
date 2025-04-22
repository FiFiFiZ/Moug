import pygame
from math import*
from assets import Assets
from random import*

class Player:
    def __init__(self):
        self.assets = Assets()
        self.assets.load_assets()
        self.sprites = self.assets.sprites
        self.SCREEN_WIDTH = self.assets.SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.assets.SCREEN_HEIGHT
        self.screen = self.assets.screen
        self.player_pos = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        self.player_x, self.player_y = self.player_pos
        self.player_xs = 500/500
        self.player_ys = 320/500
        self.factor = 1
        self.mode = -2 # game init
        self.player_img = self.sprites["circle"]
        self.iterations = 0

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
    
    def speed_vector(self, call):
        if call == "get_values":
            speed_vector = pygame.Vector2()
            speed_vector.xy = self.player_xs, self.player_ys
            speed_vector = speed_vector.rotate(50/500)
            self.player_xs, self.player_ys = speed_vector
        elif call == "draw_vector":
            self.draw_and_center_image(pygame.transform.rotate(self.sprites["arrow"], atan2(self.player_ys, self.player_xs)*-180/pi), (self.player_x, self.player_y))
    
    def check_edge_bounce(self, player_pos, current_img): # bounce player on screen edge
        player_rect = pygame.rect.Rect(player_pos[0], player_pos[1], self.player_img.get_width(), self.player_img.get_height())
        screen_rect = pygame.rect.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        if screen_rect.contains(player_rect) == False: # check where circle collided with screen (create a hitbox on each side of the circle to check collision)
            iw = self.player_img.get_width()/2
            ih = self.player_img.get_height()/2
            px = player_pos[0]
            py = player_pos[1]
            hitbox_list = [(px+iw, py), (px, py+ih), (px+iw, py+2*ih), (px+2*iw, py+ih)] # up, left, down, right
            for i in range (len(hitbox_list)):
                # hitbox = pygame.rect.Rect(hitbox_list[i]) 
                hitbox = hitbox_list[i]
                if screen_rect.collidepoint(hitbox) == False:
                    self.player_xs *= 1-(2*(i%2==1))
                    self.player_ys *= 1-(2*(i%2==0))
                    if self.factor > 0.4:
                        self.factor -= 0.01
                        self.player_img = self.sprites[current_img]
                        self.player_img = pygame.transform.scale_by(self.player_img, self.factor)
                    # print(self.factor)

    def check_mouse_touching(self, player_pos, condition): # check whether hovering over player
        mask = pygame.mask.from_surface(self.player_img)
        mask_overlap = mask.overlap(pygame.mask.from_surface(self.sprites["pixel"]), (self.mousex-player_pos[0], self.mousey-player_pos[1]))

        mask.invert()
        mask = pygame.mask.Mask.to_surface(mask)
        mask.set_colorkey((255,255,255))

        if mask_overlap == None: # if touching mouse
            self.lose()
        else: # if not touching mouse
            self.screen.blit(mask, player_pos)

    def square_set_pos(self, posx, speedx, posy, speedy, path_render_frame_n):
        self.player_x = posx
        self.player_y = posy
        self.player_xs = speedx
        self.player_ys = speedy
        self.mode_specific_idx[1] = round(path_render_frame_n) # renders path on this frame

    def spawn_square_at_different_place(self): # for mode 2 where you avoid color
        # line direction
        random = 1 - randint(0,1)*2 # randomly pick between -1 or 1
        pos1 = -1 * (random+1)/2
        speed1 = 1 * random

        if randint(0,1) == 0: # make a horizontal line
            val1 = self.SCREEN_WIDTH
            val2 = self.SCREEN_HEIGHT
            speed1 *= (5/500)
            self.square_set_pos((val1*pos1), speed1, randint(0, val2), 0, randint(0, val1)/speed1)
        else: # make a vertical line
            val1 = self.SCREEN_HEIGHT
            val2 = self.SCREEN_WIDTH
            speed1 *= (5/500)
            self.square_set_pos((val2*pos1), 0, randint(0, val1), speed1, randint(0, val2)/speed1)

    def switch_mode_setup(self):
        self.mode_specific_idx = [0,0,0] # we can use these variable for mode-specific things, and it will reset every mode change
        # mode 2: 1st variable is how many lines were drawn, 2nd is at which frame does the black square draw to make for a path, 3rd is iterations (frames passed) for that specific line

        if self.mode == -2: 
            self.mode = -1
            self.player_xs = 0
            self.player_ys = 0
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]
        elif self.mode == 0:
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]            
            self.player_xs = 500/500
            self.player_ys = 320/500
        elif self.mode == 1:
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]
        elif self.mode == 2:
            self.factor = 0.2
            self.img_name = "square"
            self.player_img = pygame.transform.scale_by(self.sprites[self.img_name], self.factor) # scale player sprite based on factor
            self.screen.fill((200,10,10))
            self.spawn_square_at_different_place()

    def mode_specific(self, call):
        # mode -2: init game
        # mode -1: main menu
        # mode 0: follow circle with mouse, vector drawn, circle bounce, gets smaller with each bounce
        # mode 1: mode 0 but with solitaire effect and without vector
        # mode 2: avoid white color (paths forming where a big black square blits in the middle making for a path)

        if call == 0:
            if self.mode == -1:
                self.screen.fill((10,10,10))
            elif self.mode == 0:
                self.speed_vector("get_values") # get player speed to draw speed vector
            elif self.mode == 1:
                self.screen.fill((50,50,50))
        elif call == 1:
            if self.mode == 0:
                self.speed_vector("draw_vector") # draw speed vector
            elif self.mode == 2:
                pass
            pass

    def main(self):
        # switch between modes (switching with arrows is temporary & for dev purposes) 
        self.key = pygame.key.get_just_pressed()
        previous_mode = self.mode
        self.mode += (self.key[pygame.K_RIGHT]) - (self.key[pygame.K_LEFT])
        print(self.mode)
        if previous_mode != self.mode or self.mode == -2:
            setup_mode = 1
        else:
            setup_mode = 0
        if setup_mode == 1:
            self.switch_mode_setup()

        # different modes do different things
        self.mode_specific(0)

        # update player position
        self.player_x += self.player_xs
        self.player_y += self.player_ys
        player_pos = (self.player_x, self.player_y)
        print(player_pos)

        self.mousex, self.mousey = pygame.mouse.get_pos() # get mouse pos
        # self.player_img = pygame.transform.scale_by(self.player_img, self.factor) # scale player sprite based on factor
        # print(factor, self.player_img)
        player_pos = self.draw_and_center_image(self.player_img, player_pos) # draw player // THIS SHOULDNT BE LIKE THIS, THIS SHOULDNT MAKE A CENTERED POS, maybe only use it for rendering more things afterwards
        
        if self.mode == 2:
            print(self.mode_specific_idx[1], self.mode_specific_idx[2])
            if self.mode_specific_idx[1] > self.mode_specific_idx[2]:
                print(self.mode_specific_idx[1], self.mode_specific_idx[2])
                self.mode_specific_idx[1] = self.SCREEN_HEIGHT*self.SCREEN_WIDTH # sets it to a value that's higher than screen dimensions to make sure it doesn't get called again
                self.screen.blit(pygame.transform.scale_by(self.sprites["square_path"], self.factor), player_pos)
            if self.player_x > self.SCREEN_WIDTH or self.player_y > self.SCREEN_HEIGHT or self.player_x < 0 or self.player_y <0: # if reached end of screen, spawn another line
                self.spawn_square_at_different_place()
                self.mode_specific_idx[0] += 1
                if self.mode_specific_idx[0] > 5:
                    self.mode = -1
        else:
            self.check_edge_bounce(player_pos, self.img_name) # check player bouncing off screen edge
            
        
        if self.mode != 2:
            self.check_mouse_touching(player_pos, self.mode==2) # check mouse hovering over player

        self.player_pos = player_pos # update player position globally
        self.mode_specific(1) # last mode-specific call

        if self.mode == 2:
            self.mode_specific_idx[2] += 1 # iterations but for individual lines
        self.iterations += 1
