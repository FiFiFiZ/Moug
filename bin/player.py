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

    def scale_image(self, img, factor):
        return pygame.transform.scale(img, (img.get_width()*factor, img.get_height()*factor))

    def draw_and_center_image(self, type, img, pos, special="None"): # draws or centers or both
        if special != "None":
            pass
        if type == "center" or type == "both":
            x, y = pos
            x -= img.get_width()/2
            y -= img.get_height()/2
            pos = (x, y)
        if type == "draw" or type == "both":
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
            self.draw_and_center_image("both", pygame.transform.rotate(self.sprites["arrow"], atan2(self.player_ys, self.player_xs)*-180/pi), (self.player_x, self.player_y))
    
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
                        self.player_img = self.scale_image(self.player_img, self.factor)
                    # print(self.factor)

    def get_mouse_touching_color(self, pos): # checks whether mouse is touching color
        return self.screen.get_at(pos)

    def check_mouse_touching(self, player_pos): # check whether hovering over player
        mask = pygame.mask.from_surface(self.player_img)
        mask_overlap = mask.overlap(pygame.mask.from_surface(self.sprites["pixel"]), (self.mousex-player_pos[0], self.mousey-player_pos[1]))

        mask.invert()
        mask = pygame.mask.Mask.to_surface(mask)
        mask.set_colorkey((255,255,255))

        if mask_overlap == None: # if not touching mouse
            return None
            self.lose()
        else: # if touching mouse
            return mask
            return (mask, 1)
            self.screen.blit(mask, self.real_player_pos)

    def square_set_pos(self, posx, speedx, posy, speedy, path_render_frame_n):
        self.player_x = posx
        self.player_y = posy
        self.player_xs = speedx
        self.player_ys = speedy
        self.mode_specific_idx[1] = round(abs(path_render_frame_n)) # renders path on this frame

    def spawn_square_at_different_place(self): # for mode 2 where you avoid color
        # line direction
        random = randint(0,1) # randomly pick between 0 or 1
        # random = 0
        pos1 = random
        speed1 = random*-2+1

        random = randint(0,1)
        # random = 1
        val1 = self.SCREEN_WIDTH
        val2 = self.SCREEN_HEIGHT
        if random == 0: # make a horizontal line
            speed1 *= (5/5)
            self.square_set_pos((val1*pos1), speed1, randint(0, val2), 0, randint(0, val1)/speed1)
            # print(self.player_x, self.player_xs, self.player_y, self.player_ys)
            # exit()
        else: # make a vertical line
            speed1 *= (5/5)
            self.square_set_pos(randint(0, val1), 0, (val2*pos1), speed1, randint(0, val2)/speed1)
        self.mode_specific_idx[2] = 0

    def switch_mode_setup(self):
        self.mode_specific_idx = [0,0,0,0] # we can use these variable for mode-specific things, and it will reset every mode change
        # mode 2: 1st variable is how many lines were drawn, 2nd is at which frame does the black square draw to make for a path, 3rd is iterations (frames passed) for that specific line, 4th is a timer for which the path draws (when timer > 0 path draws)

        if self.mode == -2 or self.mode == -1:
            self.mode = -1
            self.player_x = self.SCREEN_WIDTH/2
            self.player_y = self.SCREEN_HEIGHT/2
            self.player_xs = 0
            self.player_ys = 0
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]
            self.menu_fade = 255
        elif self.mode == 0:
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]            
            self.player_xs = 500/500
            self.player_ys = 320/500
        elif self.mode == 1:
            self.img_name = "circle"
            self.player_img = self.sprites[self.img_name]
            self.factor = 1
        elif self.mode == 2:
            self.factor = 0.2
            self.img_name = "square"
            self.player_img = self.scale_image(self.sprites[self.img_name], self.factor) # scale player sprite based on factor
            self.screen.fill((0,0,0))
            self.spawn_square_at_different_place()

    def mode_specific(self, call):
        # mode -2: init game
        # mode -1: main menu
        # mode 0: follow circle with mouse, vector drawn, circle bounce, gets smaller with each bounce
        # mode 1: mode 0 but with solitaire effect and without vector
        # mode 2: avoid white color (paths forming where a big black square blits in the middle making for a path)

        # initial call
        if call == 0:
            if self.mode == -1:
                self.screen.fill((10,10,10))
            elif self.mode == 0:
                self.speed_vector("get_values") # get player speed to draw speed vector
            elif self.mode == 1:
                self.screen.fill((10,10,10))

        # render call
        elif call == 0.5:
            if self.mode == 2: # if mode 2:
                # render path when path cooldown enabled
                self.mode_specific_idx[3] -= 1
                if self.mode_specific_idx[3] >= 0:
                    self.screen.blit(self.scale_image(self.sprites["square_path"], self.factor), self.real_player_pos)

                # trigger cooldown at the defined mark
                if self.mode_specific_idx[1] < self.mode_specific_idx[2]:
                    print(self.mode_specific_idx[1], self.mode_specific_idx[2])
                    self.mode_specific_idx[3] = 8
                    self.mode_specific_idx[1] = self.SCREEN_HEIGHT*self.SCREEN_WIDTH # sets it to a value that's higher than screen dimensions to make sure it doesn't get called again

                # if reached end of screen, spawn another line
                if self.player_x > self.SCREEN_WIDTH or self.player_y > self.SCREEN_HEIGHT or self.player_x < 0 or self.player_y <0:
                    self.spawn_square_at_different_place()
                    self.mode_specific_idx[0] += 1
                    if self.mode_specific_idx[0] > 5:
                        self.mode = -1
                        self.switch_mode_setup()

                self.draw_and_center_image("draw", self.scale_image(self.sprites["square"], self.factor), self.real_player_pos)

            else: # if not mode 2:
                if self.mode == -1:
                    self.real_player_pos = self.draw_and_center_image("center", self.player_img, self.real_player_pos)                    

                else:
                    self.real_player_pos = self.draw_and_center_image("both", self.player_img, self.real_player_pos) # center and render player
                    self.check_edge_bounce(self.real_player_pos, self.img_name) # check player bouncing off screen edge
                
            
            if self.mode > -2:
                if self.mode == 2:
                    # check if touching bad color
                    touching_color = self.get_mouse_touching_color((self.mousex, self.mousey))
                    if touching_color == (255, 255, 255, 0) or touching_color == (255, 255, 255):
                        self.lose()

                else:
                    touching = self.check_mouse_touching(self.real_player_pos) # check mouse hovering over player

                    if self.mode == -1:
                        # get button (player) position and create a mask with it that inverts on hover-over
                        # self.real_player_pos = self.draw_and_center_image("draw", self.player_img, self.real_player_pos)
                        # self.sprites["logo"] = pygame.transform.scale(self.sprites["logo"], (250, 250))
                        # logo_pos = self.draw_and_center_image("both", self.sprites["logo"], (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)) # draw logo
                        if touching != None: # touching mouse
                            self.menu_fade += (0-self.menu_fade)/30
                            if pygame.mouse.get_just_pressed()[0] == 1:
                                self.mode = 0
                                self.switch_mode_setup()
                        else: # not touching
                            self.menu_fade += (255-self.menu_fade)/30
                        
                        self.sprites["init_ts"].set_alpha(self.menu_fade)
                        self.sprites["init_ts_hoverover"].set_alpha(255-self.menu_fade)
                        self.screen.fill((self.menu_fade,self.menu_fade,self.menu_fade))
                        mask = pygame.mask.from_surface(self.player_img)
                        mask.invert()
                        mask = mask.to_surface(setcolor=(self.menu_fade,self.menu_fade,self.menu_fade) ,unsetcolor=(255-self.menu_fade, 255-self.menu_fade, 255-self.menu_fade))

                        self.real_player_pos = self.draw_and_center_image("draw", mask, self.real_player_pos)
                        self.draw_and_center_image("both", pygame.transform.scale(self.sprites["init_ts"], (300, 300)), (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2))
                        self.draw_and_center_image("both", pygame.transform.scale(self.sprites["init_ts_hoverover"], (300, 300)), (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2))


                    if touching != None:
                        if self.mode == -1:
                            pass
                        else:
                            self.screen.blit(touching, self.real_player_pos)

            

        # last call
        elif call == 1:
            if self.mode == 0:
                self.speed_vector("draw_vector") # draw speed vector
            elif self.mode == 2:
                pass
            pass

    def main(self):
        # get mouse pos
        self.mousex, self.mousey = pygame.mouse.get_pos()

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

        # call initial mode instructions
        self.mode_specific(0)

        # update player position
        self.player_x += self.player_xs
        self.player_y += self.player_ys
        self.real_player_pos = (self.player_x, self.player_y)
        print(self.real_player_pos)

        # # draw player // THIS SHOULDNT BE LIKE THIS, THIS SHOULDNT MAKE A CENTERED POS, maybe only use it for rendering more things afterwards
        # self.real_player_pos = self.draw_and_center_image("both", self.player_img, self.real_player_pos)
        
        # post-render call
        self.mode_specific(0.5)

        # update player position globally
        self.player_pos = self.real_player_pos

        # last mode-specific call
        self.mode_specific(1)

        # signal iteration
        if self.mode == 2:
            self.mode_specific_idx[2] += 1 # iterations but for individual lines
        self.iterations += 1
