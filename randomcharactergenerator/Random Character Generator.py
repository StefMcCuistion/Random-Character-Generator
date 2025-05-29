import io
from random import randint, uniform
import pygame as pg

import datetime

import json

from pygame import mixer
from os.path import join
import os
from os import walk
import sys
from sys import exit

from PIL import Image

import tkinter
from tkinter import filedialog
import ctypes
import pywinauto

import pyautogui

import numpy

# from random import randint

import webbrowser

import settings

def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return join(base_path, relative_path)

class Player(pg.sprite.Sprite):
    def __init__(self, groups, parts):
        super().__init__(groups)
        # Apperance options
        self.parts = parts
        self.skin_colors = ["fair", "less_fair", "pale_brown", "medium_brown", "dark_brown", "black"]
        self.races = ["human", "cat", "dragon"]
        self.hairstyles = ["emo", "bubble_braid"]
        self.hair_colors = ["black", "blonde", "brown", "purple", "white", "pink1", "pink2"]
        self.panties = ["lacy_dark", "microkini"]
        self.bottoms = [ "none", "shorts", "skirt", "skirt_dark","jeans"]
        self.bras = ["microkini", "bra", "turtleneck", "bunny"]
        self.chests = ["none", "cropped_tank_dark", "cropped_tank_light", "cropped_shirt"]
        self.tops = ["none", "jacket", "coat", "maid_dress", "bunny", "cropped_hoodie", "colored_cropped_hoodie"]
        self.socks = ["none", "leggings", "thigh_highs_black", "fishnet"]
        self.eye_colors = ["purple", "red", "blue", "green", "brown"]
        
        # Index Defaults, used when not randomized
        self.skin_colors_idx = 0
        self.hairstyles_idx = 1
        self.hair_colors_idx = 0
        self.races_idx = 0
        self.tops_idx = 0
        self.panties_idx = 0
        self.bras_idx = 0
        self.bottoms_idx = 0
        self.socks_idx = 0
        self.chests_idx = 0
        self.eye_colors_idx = 0
        
        # Initial appearance as question mark
        surf = self.parts['question_mark']
        surf = pg.transform.scale_by(surf, .46)
        self.appearance = surf
        self.image = self.appearance
        self.rect = self.image.get_frect(center=(1300, 550))
        self.initial_center_y = self.rect.centery
        self.zoom_rect = self.rect
        
        # Animation
        self.tick = 1
        self.h = 2513
        self.w = 1766
        self.breathing = False
        
        self.twitch_time_remaining = 0
        self.twitch_h = 1
        self.twitch_w = 1
        self.twitch_magnitude = .1

    def update(self, dt, zoom):
        self.tick += 1 * dt
        if self.twitch_time_remaining > 0:
            # Track time
            self.twitch_time_remaining -= .04
            self.twitch_time_remaining = round(self.twitch_time_remaining, 2)
            # Change self.twitch_h and self.twitch_w to animate
            self.twitch_h = 1 + numpy.sin(6.28319 * self.twitch_time_remaining) * self.twitch_time_remaining * self.twitch_magnitude
            self.twitch_h = 1 - numpy.sin(6.28319 * self.twitch_time_remaining) * self.twitch_time_remaining * self.twitch_magnitude
            
        speed = 1
        magnitude = 10
        if self.breathing:
            img_x = 1766
            img_y = 2513
            self.w = img_x * self.twitch_w * (.322 + (.0018 * zoom))
            self.h = img_y * self.twitch_h * (.322 + (.0018 * zoom))
            self.zoom_rect = pg.transform.smoothscale(self.appearance, (self.w, self.h)).get_frect(center = self.zoom_rect.center)
            self.w -= numpy.sin(speed * self.tick) * magnitude
            self.h += numpy.sin(speed * self.tick) * magnitude * .5
            self.image = pg.transform.smoothscale(self.appearance, (self.w, self.h))
            self.rect = self.image.get_frect(centerx = self.rect.centerx, bottom = self.zoom_rect.bottom)

    def randomize_attributes(self):
        self.skin_colors_idx = randint(0, len(self.skin_colors) - 1)
        self.hairstyles_idx = randint(0, len(self.hairstyles) - 1)
        self.hair_colors_idx = randint(0, len(self.hair_colors) - 1)
        self.races_idx = randint(0, len(self.races) - 1)
        self.tops_idx = randint(0, len(self.tops) - 1)
        self.bottoms_idx = randint(0, len(self.bottoms) - 1)
        self.panties_idx = randint(0, len(self.panties) - 1)
        self.socks_idx = randint(0, len(self.socks) - 1)
        self.chests_idx = randint(0, len(self.chests) - 1)
        self.eye_colors_idx = randint(0, len(self.eye_colors) - 1)
        # Prevents cropped shirt from being selected if a cropped hoodie is selected. 
        if self.chests[self.chests_idx] == "cropped_shirt":
            if self.tops[self.tops_idx] == "cropped_hoodie" or self.tops[self.tops_idx] == "colored_cropped_hoodie":
                self.chests_idx = randint(0, len(self.chests) - 2)
            

    def change_appearance(self):

        self.randomize_attributes()

        # Draws character and updates self.image
        self.breathing = True
        surf = self.return_image()
        #surf = pg.transform.scale_by(surf)
        self.appearance = surf
        self.twitch_time_remaining = 1
        
    def return_image(self):
        # Draws character at max res and returns it
        surf = pg.Surface((1766, 2513), pg.SRCALPHA)
        if self.tops[self.tops_idx] != 'none':
            if self.tops[self.tops_idx] == "colored_cropped_hoodie":
                surf.blit(self.parts[f'top_{self.eye_colors[self.eye_colors_idx]}_{self.tops[self.tops_idx]}_back1'])
            else:
                surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back1'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_back'])
        if self.races[self.races_idx] == "cat" or self.races[self.races_idx] == "bunny":
            surf.blit(self.parts[f'tail_{self.races[self.races_idx]}_{self.hair_colors[self.hair_colors_idx]}'])
        if self.races[self.races_idx] == "dragon":
            surf.blit(self.parts[f'tail_{self.races[self.races_idx]}'])
        if self.tops[self.tops_idx] != 'none':
            if self.tops[self.tops_idx] == "colored_cropped_hoodie":
                surf.blit(self.parts[f'top_{self.eye_colors[self.eye_colors_idx]}_{self.tops[self.tops_idx]}_back2'])
            else:
                surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back2'])
        surf.blit(self.parts[f'body_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'panties_{self.panties[self.panties_idx]}'])
        surf.blit(self.parts[f'socks_{self.socks[self.socks_idx]}'])
        surf.blit(self.parts[f'chest_{self.bras[self.bras_idx]}'])
        surf.blit(self.parts[f'bottom_{self.bottoms[self.bottoms_idx]}'])
        surf.blit(self.parts[f'arm_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'chest_{self.chests[self.chests_idx]}'])
        if self.tops[self.tops_idx] == "colored_cropped_hoodie":
            surf.blit(self.parts[f'top_{self.eye_colors[self.eye_colors_idx]}_{self.tops[self.tops_idx]}_front'])
        else:
            surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_front'])
        surf.blit(self.parts[f'face_{self.eye_colors[self.eye_colors_idx]}'])
        if self.races[self.races_idx] == "cat" or self.races[self.races_idx] == "bunny":
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_back_{self.hair_colors[self.hair_colors_idx]}'])
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_under_hair_{self.hair_colors[self.hair_colors_idx]}'])
        elif self.races[self.races_idx] == "dragon":
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_back'])
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_under_hair'])
        else:
            surf.blit(self.parts[f'humanear_{self.skin_colors[self.skin_colors_idx]}'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_front'])
        if self.races[self.races_idx] == "cat" or self.races[self.races_idx] == "bunny":
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_front_{self.hair_colors[self.hair_colors_idx]}'])
        elif self.races[self.races_idx] == "dragon":
            surf.blit(self.parts[f'{self.races[self.races_idx]}ear_front'])

        data = pg.image.tobytes(surf, "RGBA")
        final_surf = pg.image.frombytes(data, (1766, 2513), "RGBA")
        return final_surf
    
class SplashArt(pg.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.og_img = surf
        self.image = self.og_img
        self.pos = pos
        self.rect = self.image.get_frect(center = pos)
        self.size = 1
        self.tick = 1
        
    def update(self, dt):
        self.tick += 1 * dt
        speed = .8
        magnitude = .05
        self.size = 1 + (magnitude * numpy.sin(self.tick * speed))
        self.image = pg.transform.smoothscale_by(self.og_img, self.size)
        self.rect = self.image.get_frect(center = self.rect.center)

class Heart(pg.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.og_surf = surf
        self.image = self.og_surf
        self.rect = self.image.get_frect(center = pos)
        self.creation_time = pg.time.get_ticks()
        self.dir = pg.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = randint(0, 360)
        self.roto_speed = randint(20, 40)

    def update(self, dt):
        self.rect.center += self.dir * self.speed * dt
        current_time = pg.time.get_ticks()
        if self.rect.top > settings.H or self.rect.left > settings.W or self.rect.right < 0:
            self.kill()

        # Rotation
        self.rotation += self.roto_speed * dt
        self.image = pg.transform.rotozoom(self.og_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Button(pg.sprite.Sprite):
    def __init__(self, groups, name, surfs, pos, font, txt_color):
        super().__init__(groups)
        self.selected = False
        self.surfs = surfs
        self.image = self.surfs['unselected']
        self.pos = pos
        self.rect = self.image.get_frect(center = self.pos)
        self.font = font
        if txt_color == 'light':
            self.selected_color = '#ffe8f9'
            self.unselected_color = '#ffb5ed'
        else: 
            self.selected_color = 'white'
            self.unselected_color = '#eb95d6'
        self.font_color = self.selected_color
        self.name = name
        self.text = self.font.render(self.name, True, self.font_color)
        if self.name != 'randomize': 
            self.text_rect = self.text.get_frect(center = (self.rect.center[0], self.rect.center[1] + 22))
        else: 
            self.text_rect = self.text.get_frect(center = (self.rect.center[0] + 95, self.rect.center[1] + 20))


    def update(self, display):
        if self.check_for_input():
            self.selected = True
            self.font_color = self.selected_color
        else:
            self.selected = False
            self.font_color = self.unselected_color
        self.text = self.font.render(self.name, True, self.font_color)
        if self.selected:
            if pg.mouse.get_pressed()[0]:
                if self.name == 'randomize' or self.name == 'save image':
                    self.image = self.surfs['pressed']  
            else:
                self.image = self.surfs['selected']
        else:
            self.image = self.surfs['unselected']
        self.rect = self.image.get_frect(center = self.pos)
        display.blit(self.text, self.text_rect)



    def check_for_input(self):
        pos = (pg.mouse.get_pos())
        if pos[0] in (range(int(self.rect.left), int(self.rect.right))) and pos[1] in range(int(self.rect.top), int(self.rect.bottom)):
            return 1
        
class BackgroundsButton(pg.sprite.Sprite):
    def __init__(self, groups, name, selected, surfs, pos):
        super().__init__(groups)
        self.name = name
        self.selected = selected
        self.surfs = surfs
        self.image = self.surfs[f'{self.name}_{self.selected}']
        self.pos = pos
        self.rect = self.image.get_frect(center = self.pos)


    def update(self, display):
        if self.check_for_input():
            self.selected = 'selected'
        self.image = self.surfs[f'{self.name}_{self.selected}']
        self.rect = self.image.get_frect(center = self.pos)
        
    def change_appearance(self, bg):
        if self.name == bg:
            self.selected = 'selected'
        else:
            self.selected = 'unselected'
        self.image = self.surfs[f'{self.name}_{self.selected}']
        self.rect = self.image.get_frect(center = self.pos)

    def check_for_input(self):
        pos = (pg.mouse.get_pos())
        if pos[0] in (range(int(self.rect.left), int(self.rect.right))) and pos[1] in range(int(self.rect.top), int(self.rect.bottom)) and pg.mouse.get_just_pressed()[0]:
            return 1

class Slider(pg.sprite.Sprite):
    def __init__(self, groups, surfs, pos, user_settings, name, axis):
        super().__init__(groups)
        self.pos = pos
        self.initial_pos = pos
        self.surfs = surfs
        self.selected = False
        self.in_use = False
        self.image = self.surfs['unselected']
        self.rect = self.image.get_frect(center = self.pos)
        self.axis = axis
        self.user_settings = user_settings
        if self.axis == 'x':
            self.length = 6
            self.bounds = (self.rect.centerx - (100 * self.length), self.rect.centerx)
            self.idx = int(self.user_settings[name])
            self.rect.centerx += (self.idx * self.length) - (100 * self.length)
        else:
            self.length = 4
            self.bounds = (self.rect.centery - (100 * self.length), self.rect.centery)
            self.idx = 70
            self.rect.centery -= self.idx * self.length
        self.name = name
        
        
    def update(self, display):
        if not self.in_use:
            if self.check_for_input():
                self.selected = True
                if pg.mouse.get_just_pressed()[0]:
                    self.in_use = True
            else:
                self.selected = False
            if self.selected:
                if not pg.mouse.get_pressed()[0]:
                    self.image = self.surfs['selected']
            else:
                self.image = self.surfs['unselected']
        else: 
            if not pg.mouse.get_pressed()[0]:
                self.in_use = False
            else: 
                if self.axis == 'x':
                    mouse_x = pg.mouse.get_pos()[0]
                    if mouse_x > self.bounds[0] and mouse_x < self.bounds[1]:
                        self.rect.center = (mouse_x, self.pos[1])
                    elif mouse_x < self.bounds[0]:
                        self.rect.centerx = self.initial_pos[0] - (100 * self.length)
                    else:
                        self.rect.centerx = self.initial_pos[0]
                    self.idx = 100 - round((self.bounds[1] - self.rect.centerx) / self.length)
                else:
                    mouse_y = pg.mouse.get_pos()[1]
                    if mouse_y > self.bounds[0] and mouse_y < self.bounds[1]:
                        self.rect.center = (self.pos[0], mouse_y)
                    elif mouse_y < self.bounds[0]:
                        self.rect.centery = self.initial_pos[1] - (self.length * 100)
                    else: 
                        self.rect.centery = self.initial_pos[1]
                    self.idx = round((self.bounds[1] - self.rect.centery) / self.length)
            
    def check_for_input(self):
        pos = (pg.mouse.get_pos())
        if pos[0] in (range(int(self.rect.left), int(self.rect.right))) and pos[1] in range(int(self.rect.top), int(self.rect.bottom)):
            return 1

    def give_idx(self):
        return self.idx
    
class Checkbox(pg.sprite.Sprite):
    def __init__(self, groups, surfs, pos, user_settings, name):
        super().__init__(groups)
        self.user_settings = user_settings
        self.name = name
        self.selected = self.user_settings[name]
        self.surfs = surfs
        self.pos = pos
        self.image = self.surfs['unselected']
        self.rect = self.image.get_frect(center = self.pos)
        
    def update(self, display):
        if not self.selected: 
            if self.check_for_input():
                if not pg.mouse.get_pressed()[0]:
                    self.image = self.surfs['unselected_hover']
                if pg.mouse.get_just_pressed()[0]:
                    self.selected = True
            else: 
                self.image = self.surfs['unselected']
        else: 
            if self.check_for_input():
                if pg.mouse.get_just_pressed()[0]:
                    self.image = self.surfs['unselected_hover']
                    self.selected = False
                elif not pg.mouse.get_pressed()[0]:
                    self.image = self.surfs['selected_hover']
            else: 
                self.image = self.surfs['selected']
        
    def check_for_input(self):
        pos = (pg.mouse.get_pos())
        if pos[0] in (range(int(self.rect.left), int(self.rect.right))) and pos[1] in range(int(self.rect.top), int(self.rect.bottom)):
            return 1
        
    def give_state(self):
        return self.selected
    
class StaticUI(pg.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.pos = pos
        self.rect = self.image.get_frect(center=self.pos)

class Background(pg.sprite.Sprite):
    def __init__(self, groups, surfs):
        super().__init__(groups)
        self.surfs = surfs
        self.surf = self.surfs['halftone']
        self.size = 1 + ((85 / 100) / 20)
        self.image = pg.transform.smoothscale_by(self.surf, self.size)
        self.rect = self.image.get_frect(center = (settings.W / 2, settings.H / 2))


    def update(self, dt):
        x = 1
        
    def zoom(self, zoom_idx, bg_img):
        self.size = 1 + ((zoom_idx / 100) / 20)
        print(f'size = {self.size}')
        print(f'zoom = {zoom_idx}')

        self.image = pg.transform.smoothscale_by(self.surf, self.size)
        self.rect = self.image.get_frect(center = self.rect.center)
        
        print(f'rectleft = {self.rect.left}\nrectbottom = {self.rect.bottom}')
        
    def change_appearance(self, bg_img):
        self.surf = self.surfs[bg_img]
        self.image = pg.transform.smoothscale_by(self.surf, self.size)
        self.rect = self.image.get_frect(center = self.rect.center)
        
    

class Game:

    def __init__(self):

        # Setup
        pg.init()
        pg.font.init()
        pg.mixer.init()
        
        self.user_settings = {
                              "Fullscreen": False,
                              "Master Volume": 100,
                              "Music Volume": 100,
                              "SFX Volume": 100
        }
        
        try:
            with open(resource_path(join('user settings', 'user_settings.csv'))) as settings_file:
                self.user_settings = json.load(settings_file)
                print(self.user_settings)
        except: 
            print('could not load user settings')
            
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        #asset_location = os.path.join(current_dir, "assets")
        
        ctypes.windll.user32.SetProcessDPIAware()  # keeps Windows GUI scale settings from messing with resolution
        monitor_size = pg.display.list_modes()[0]
        self.fullscreen = self.user_settings['Fullscreen']
        if self.fullscreen:
            self.display = pg.display.set_mode((settings.W, settings.H), pg.SCALED | pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode((settings.W, settings.H))
        self.font = pg.font.Font(resource_path(join('assets', 'fonts', 'motley_forces.ttf')), 90)
        self.playscreen_button_font = pg.font.Font(resource_path(join('assets', 'fonts', 'motley_forces.ttf')), 80)
        pg.display.set_caption("Random Character Generator")
        if not self.fullscreen:  # These just slow down game launch if done in fullscreen
            os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centers window
            # app = pywinauto.Application().connect(title_re="Random Character Generator")
            # app.top_window().set_focus() # Activates window
        self.clock = pg.time.Clock()
        self.running = True

        

        # Imports: Cursor
        cursor_surf = pg.image.load(resource_path(join('assets', 'img', 'ui', 'mouse.png'))).convert_alpha()
        cursor = pg.cursors.Cursor((0,0), cursor_surf)
        pg.mouse.set_cursor(cursor)

        # Imports: Player
        self.player_parts = {}
        for folder_path, sub_folders, file_names in walk(resource_path(join('assets', "img", "player_pieces"))):
            if file_names:
                for file_name in file_names:
                    path = resource_path(join(folder_path, file_name))
                    surf = pg.image.load(path).convert_alpha()
                    self.player_parts[file_name.split('.')[0]] = surf
                    
        # Imports: Backgrounds
        self.background_surfs = {
                                'halftone': pg.image.load(resource_path(join('assets', 'img', 'backgrounds', 'halftone.png'))).convert_alpha(),
                                'outdoors': pg.image.load(resource_path(join('assets', 'img', 'backgrounds', 'outdoors.png'))).convert_alpha(),
                                'hotel': pg.image.load(resource_path(join('assets', 'img', 'backgrounds', 'hotel.png'))).convert_alpha(),
                                'piza': pg.image.load(resource_path(join('assets', 'img', 'backgrounds', 'piza.png'))).convert_alpha()
        }

        # Imports: Buttons and Sliders
        self.button_surfs = {
                             'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'button_selected.png'))).convert_alpha(),
                             'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'button_unselected.png'))).convert_alpha()
        }
        
        self.return_button_surfs = {
                                    'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'return_button_selected.png'))).convert_alpha(),
                                    'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'return_button_unselected.png'))).convert_alpha()                                    
        }
        
        self.slider_surfs = {
                             'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'slider_knob_unselected.png'))).convert_alpha(),
                             'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'slider_knob_selected.png'))).convert_alpha()
        }
        
        self.zoom_slider_surfs = {
                             'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'zoom_slider_knob_unselected.png'))).convert_alpha(),
                             'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'slider_knob_selected.png'))).convert_alpha()
        }
        
        self.checkbox_surfs = {
                               'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'checkbox_unchecked.png'))).convert_alpha(),
                               'unselected_hover': pg.image.load(resource_path(join('assets', 'img', 'ui', 'checkbox_unchecked_hover.png'))).convert_alpha(),
                               'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'checkbox_checked.png'))).convert_alpha(),
                               'selected_hover': pg.image.load(resource_path(join('assets', 'img', 'ui', 'checkbox_checked_hover.png'))).convert_alpha()
        }
        
        self.randomize_button_surfs = {
                                       'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'randomize_unselected.png'))).convert_alpha(),
                                       'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'randomize_selected.png'))).convert_alpha(),
                                       'pressed': pg.image.load(resource_path(join('assets', 'img', 'ui', 'randomize_pressed.png'))).convert_alpha()
        }
        
        self.save_image_button_surfs = {
                                        'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'save_image_unselected.png'))).convert_alpha(), 
                                        'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'save_image_selected.png'))).convert_alpha(),
                                        'pressed': pg.image.load(resource_path(join('assets', 'img', 'ui', 'save_image_pressed.png'))).convert_alpha()
        }
        
        self.back_button_surfs = {
                                  'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'back_button_unselected.png'))).convert_alpha(),
                                  'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'back_button_selected.png'))).convert_alpha()
        }
        
        self.background_button_surfs = {
                                        'halftone_unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_halftone_button_unselected.png'))).convert_alpha(),
                                        'halftone_selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_halftone_button_selected.png'))).convert_alpha(),
                                        'outdoors_unselected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_outdoors_button_unselected.png'))).convert_alpha(),
                                        'outdoors_selected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_outdoors_button_selected.png'))).convert_alpha(),
                                        'hotel_unselected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_hotel_button_unselected.png'))).convert_alpha(),
                                        'hotel_selected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_hotel_button_selected.png'))).convert_alpha(),
                                        'piza_unselected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_piza_button_unselected.png'))).convert_alpha(),
                                        'piza_selected':pg.image.load(resource_path(join('assets', 'img', 'ui', 'bg_piza_button_selected.png'))).convert_alpha()
        }
        
        self.patreon_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_patreon_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_patreon_selected.png'))).convert_alpha(),
        }
        
        self.twitter_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_twitter_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_twitter_selected.png'))).convert_alpha(),
        }
        
        self.bluesky_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_bluesky_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_bluesky_selected.png'))).convert_alpha(),
        }
        
        self.cara_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_cara_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_cara_selected.png'))).convert_alpha(),
        }
        
        self.tumblr_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_tumblr_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_tumblr_selected.png'))).convert_alpha(),
        }
        
        self.nsfw_button_surfs = {
                                     'unselected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_18_unselected.png'))).convert_alpha(),
                                     'selected': pg.image.load(resource_path(join('assets', 'img', 'ui', 'socials_button_18_selected.png'))).convert_alpha(),
        }
        
        self.backgrounds_label_surf = pg.image.load(resource_path(join('assets', 'img', 'ui', 'play_screen_unresponsive_ui.png'))).convert_alpha()
        
        # Imports: Background Hearts
        self.heart_surf = pg.image.load(resource_path(join('assets', 'img', 'ui', 'heart.png'))).convert_alpha()
        
        # Imports: Audio
        
        pg.mixer.music.load(resource_path(join('assets', 'audio', 'synthlofibeats-onetent.mp3')))
        
        self.sfx_button_click = pg.mixer.Sound(resource_path(join('assets', 'audio', 'sfx', 'Minimalist3.ogg')))
        self.sfx_save_image = pg.mixer.Sound(resource_path(join('assets', 'audio', 'sfx', 'Minimalist13.ogg')))
        self.sfx_randomize = pg.mixer.Sound(resource_path(join('assets', 'audio', 'sfx', 'Minimalist9.ogg')))
        self.sfx_invalid = pg.mixer.Sound(resource_path(join('assets', 'audio', 'sfx', 'Invalid.mp3')))
        self.sfx_button_click.set_volume((self.user_settings['Master Volume'] / 100) * (self.user_settings['SFX Volume'] / 100))
        self.sfx_save_image.set_volume((self.user_settings['Master Volume'] / 100) * (self.user_settings['SFX Volume'] / 100))
        self.sfx_randomize.set_volume((self.user_settings['Master Volume'] / 100) * (self.user_settings['SFX Volume'] / 100))
        self.sfx_invalid.set_volume((self.user_settings['Master Volume'] / 100) * (self.user_settings['SFX Volume'] / 100))
        
        # Imports: Icon
        
        icon = pg.image.load(resource_path(join('assets', 'img', 'ui', 'icon.png'))).convert_alpha()

        # Sprite groups
        self.start_sprites = pg.sprite.Group()
        self.time_sensitive_sprites = pg.sprite.Group()
        self.play_sprites = pg.sprite.Group()
        self.about_sprites = pg.sprite.Group()
        self.options_sprites = pg.sprite.Group()
        self.splash_art_group = pg.sprite.Group()
        
        # Play music
        
        music_volume = (self.user_settings['Master Volume'] / 100) * (self.user_settings['Music Volume'] / 100)
        pg.mixer.music.set_volume(music_volume)
        pg.mixer.music.play(loops = -1)
        
        pg.display.set_icon(icon)
                

    def start(self):

        # Sprites
        splash_art_surf = pg.image.load(resource_path(join('assets', 'img', 'ui', 'splash_art_placeholder.png'))).convert_alpha()
        self.splash_art = SplashArt(self.splash_art_group, splash_art_surf, (600, 500))
        
        start_button = Button(self.start_sprites, 'start', self.button_surfs, (1495, 290), self.font, 'light')
        options_button = Button(self.start_sprites, 'options', self.button_surfs, (1495, 475), self.font, 'light')
        about_button = Button(self.start_sprites, 'about', self.button_surfs, (1495, 660), self.font, 'light')
        close_button = Button(self.start_sprites, 'close', self.button_surfs, (1495, 845), self.font, 'light')

        menu_box = pg.image.load(resource_path(join('assets', 'img', 'ui', 'start_menu_box.png'))).convert_alpha()

        # Custom heart event
        heart_event = pg.event.custom_type()
        pg.time.set_timer(heart_event, 1000)
        
        for i in range(0, 2):
            x, y = randint(265, settings.W - 265), 0
            Heart(self.heart_surf, (x, y), self.time_sensitive_sprites)

        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == heart_event:
                    x, y = randint(0, settings.W), randint(-300, -221)
                    Heart(self.heart_surf, (x, y), self.time_sensitive_sprites)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_button.check_for_input():
                        self.sfx_button_click.play()
                        for sprite in self.start_sprites:
                            sprite.kill()
                        for sprite in self.time_sensitive_sprites:
                            sprite.kill()
                        for sprite in self.splash_art_group:
                            sprite.kill()
                        self.play()
                    elif options_button.check_for_input():
                        self.sfx_button_click.play()
                        for sprite in self.start_sprites:
                            sprite.kill()
                        for sprite in self.time_sensitive_sprites:
                            sprite.kill()
                        for sprite in self.splash_art_group:
                            sprite.kill()
                        self.options()
                    elif about_button.check_for_input():
                        self.sfx_button_click.play()
                        for sprite in self.start_sprites:
                            sprite.kill()
                        for sprite in self.time_sensitive_sprites:
                            sprite.kill()
                        for sprite in self.splash_art_group:
                            sprite.kill()
                        self.about()
                    elif close_button.check_for_input():
                        self.sfx_button_click.play()
                        self.running = False

            # Render
            self.display.fill('#ffe3f8')
            self.time_sensitive_sprites.update(self.dt)
            self.time_sensitive_sprites.draw(self.display)
            self.splash_art_group.update(self.dt)
            self.splash_art_group.draw(self.display)
            self.display.blit(menu_box)
            self.start_sprites.draw(self.display)
            self.start_sprites.update(self.display)
            pg.display.flip()
        pg.quit()
        exit()

    def options(self):
                
        # Sprites
        options_bg = pg.image.load(resource_path(join('assets', 'img', 'ui', 'options_background.png'))).convert_alpha()
        
        return_button = Button(self.options_sprites, 'return to main menu', self.return_button_surfs, (settings.W / 2, 965), self.font, 'dark')
        
        fullscreen_checkbox = Checkbox(self.options_sprites, self.checkbox_surfs, (1480, 260), self.user_settings, "Fullscreen")
        master_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 430), self.user_settings, "Master Volume", "x")
        music_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 610), self.user_settings, "Music Volume", "x")
        sfx_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 790), self.user_settings, "SFX Volume", "x")
                
        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if return_button.check_for_input():
                        self.sfx_button_click.play()
                        with open((resource_path(join('user settings', 'user_settings.csv'))), 'w') as settings_file:
                            json.dump(self.user_settings, settings_file)
                        for sprite in self.options_sprites:
                            sprite.kill()
                        self.start()
                if event.type == pg.MOUSEBUTTONUP:
                    if sfx_volume_slider.in_use or music_volume_slider.in_use or master_volume_slider.in_use:
                        self.sfx_button_click.play()
                    prior_fullscreen = self.fullscreen
                    self.fullscreen = self.user_settings['Fullscreen']
                    if prior_fullscreen != self.fullscreen:
                        if self.fullscreen:
                            self.display = pg.display.set_mode((settings.W, settings.H), pg.SCALED | pg.FULLSCREEN)
                        else:
                            self.display = pg.display.set_mode((settings.W, settings.H))

            
            # Update User Settings
            if pg.mouse.get_pressed()[0]:
                self.user_settings['Fullscreen'] = fullscreen_checkbox.give_state()
                self.user_settings['Master Volume'] = master_volume_slider.give_idx()
                self.user_settings['Music Volume'] = music_volume_slider.give_idx()
                self.user_settings['SFX Volume'] = sfx_volume_slider.give_idx()
                music_volume = (self.user_settings['Master Volume'] / 100) * (self.user_settings['Music Volume'] / 100)
                sfx_volume = (self.user_settings['Master Volume'] / 100) * (self.user_settings['SFX Volume'] / 100)

            pg.mixer.music.set_volume(music_volume)
            self.sfx_button_click.set_volume(sfx_volume)
            self.sfx_save_image.set_volume(sfx_volume)
            self.sfx_randomize.set_volume(sfx_volume)
            self.sfx_invalid.set_volume(sfx_volume)

            # Render
            self.display.blit(options_bg)
            self.options_sprites.draw(self.display)
            self.options_sprites.update(self.display)
            pg.display.flip()
        pg.quit()
        exit()

    def about(self):
        
        # Sprites
        about_bg = self.background_surfs['halftone']
        about_box = pg.image.load(resource_path(join('assets', 'img', 'ui', 'about_box.png'))).convert_alpha()
        
        patreon_button = Button(self.about_sprites, '', self.patreon_button_surfs, (580, 760), self.font, 'dark')
        twitter_button = Button(self.about_sprites, '', self.twitter_button_surfs, (710, 760), self.font, 'dark')
        bluesky_button = Button(self.about_sprites, '', self.bluesky_button_surfs, (840, 760), self.font, 'dark')
        cara_button = Button(self.about_sprites, '', self.cara_button_surfs, (970, 760), self.font, 'dark')
        tumblr_button = Button(self.about_sprites, '', self.tumblr_button_surfs, (1100, 760), self.font, 'dark')
        nsfw_button = Button(self.about_sprites, '', self.nsfw_button_surfs, (1230, 760), self.font, 'dark')
        
        return_button = Button(self.about_sprites, 'return to main menu', self.return_button_surfs, (settings.W / 2, 965), self.font, 'dark')
                        
        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if patreon_button.check_for_input():
                        webbrowser.open('https://www.patreon.com/c/stekken')
                    if twitter_button.check_for_input():
                        webbrowser.open('https://x.com/stekken_')
                    if bluesky_button.check_for_input():
                        webbrowser.open('https://bsky.app/profile/stekken.bsky.social')
                    if cara_button.check_for_input():
                        webbrowser.open('https://cara.app/stekken/all')
                    if tumblr_button.check_for_input():
                        webbrowser.open('https://www.tumblr.com/blog/stekken')
                    if nsfw_button.check_for_input():
                        webbrowser.open('https://linktr.ee/stekkennsfw')
                    if return_button.check_for_input():
                        self.sfx_button_click.play()
                        for sprite in self.about_sprites:
                            sprite.kill()
                        self.start()
            
            # Render
            self.display.blit(about_bg)
            self.display.blit(about_box)
            self.about_sprites.draw(self.display)
            self.about_sprites.update(self.display)
            pg.display.flip()


    def play(self):
        
        bg_img = 'halftone'

        # Sprites
        background = Background(self.play_sprites, self.background_surfs)
        
        self.player = Player(self.time_sensitive_sprites, self.player_parts)
                
        backgrounds_label = StaticUI(self.play_sprites, self.backgrounds_label_surf, (settings.W / 2, settings.H / 2))
        halftone_bg_button = BackgroundsButton(self.play_sprites, 'halftone', 'selected', self.background_button_surfs, (450, 675))
        outdoors_bg_button = BackgroundsButton(self.play_sprites, 'outdoors', 'unselected', self.background_button_surfs, (550, 675))
        hotel_bg_button = BackgroundsButton(self.play_sprites, 'hotel', 'unselected', self.background_button_surfs, (650, 675))
        piza_bg_button = BackgroundsButton(self.play_sprites, 'piza', 'unselected', self.background_button_surfs, (750, 675))
        
        randomize_button = Button(self.play_sprites, 'randomize', self.randomize_button_surfs, (470, 260), self.playscreen_button_font, 'light')
        save_image_button = Button(self.play_sprites, 'save image', self.save_image_button_surfs, (495, 465), self.playscreen_button_font, 'light')
        back_button = Button(self.play_sprites, 'main menu', self.back_button_surfs, (450, 890), self.playscreen_button_font, 'light')
        
        zoom_slider = Slider(self.play_sprites, self.zoom_slider_surfs, (1810, 725), self.user_settings, 'zoom', 'y')

        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            self.display.fill('black')
            zoom_idx = zoom_slider.give_idx()
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if randomize_button.check_for_input():
                        self.sfx_randomize.play()
                        self.player.change_appearance()
                    elif halftone_bg_button.check_for_input():
                        self.sfx_button_click.play()
                        bg_img = halftone_bg_button.name
                    elif outdoors_bg_button.check_for_input():
                        self.sfx_button_click.play()
                        bg_img = outdoors_bg_button.name
                    elif hotel_bg_button.check_for_input():
                        self.sfx_button_click.play()
                        bg_img = hotel_bg_button.name
                    elif piza_bg_button.check_for_input():
                        self.sfx_button_click.play()
                        bg_img = piza_bg_button.name
                    elif save_image_button.check_for_input():
                        if self.player.breathing:
                            self.sfx_save_image.play()
                            path = filedialog.asksaveasfilename(defaultextension=".png")
                            if path != "":
                                pg.image.save(self.player.return_image(), path)
                        else:
                            self.sfx_invalid.play()
                    elif back_button.check_for_input():
                        self.sfx_button_click.play()
                        for sprite in self.play_sprites:
                            sprite.kill()
                        for sprite in self.time_sensitive_sprites:
                            sprite.kill()
                        self.start()
                if event.type == pg.MOUSEBUTTONUP and zoom_slider.in_use:
                    self.sfx_button_click.play()
                
            if zoom_slider.in_use:
                background.zoom(zoom_idx, bg_img)
            
            # Render
            halftone_bg_button.change_appearance(bg_img)
            outdoors_bg_button.change_appearance(bg_img)
            hotel_bg_button.change_appearance(bg_img)
            piza_bg_button.change_appearance(bg_img)
            
            #self.display.blit(self.background_surfs[bg_img])
            background.change_appearance(bg_img)
            
            self.play_sprites.draw(self.display)
            self.play_sprites.update(self.display)
            self.time_sensitive_sprites.draw(self.display)
            self.time_sensitive_sprites.update(self.dt, zoom_idx)
            pg.display.flip()

        pg.quit()
        exit()


if __name__ == "__main__":
    game = Game()    
    game.start()