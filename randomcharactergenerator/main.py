import io
from random import randint, uniform
import pygame as pg

import datetime

import json

from pygame import mixer
from os.path import join
import os
from os import walk
from sys import exit

# import tkinter
import ctypes
import pywinauto

import pyautogui

# from random import randint

import settings


class Player(pg.sprite.Sprite):
    def __init__(self, groups, parts):
        super().__init__(groups)
        self.parts = parts
        self.skin_colors = ["fair", "pale_brown"]
        self.races = ["human", "cat"]
        self.hairstyles = ["emo", "bubble_braid"]
        self.hair_colors = ["black", "blonde", "brown", "purple"]
        self.bottoms = ["shorts", "skirt"]
        self.chests = ["cropped_shirt", "bra"]
        self.tops = ["none", "jacket", "coat"]
        self.socks = ["none", "leggings", "thigh_highs_black"]
        
        # Index Defaults, used when not randomized
        self.skin_colors_idx = 0
        self.hairstyles_idx = 1
        self.hair_colors_idx = 0
        self.races_idx = 0
        self.tops_idx = 0
        self.bottoms_idx = 0
        self.socks_idx = 0
        self.chests_idx = 0
        
        self.change_appearance()
        self.rect = self.image.get_frect(topleft=(settings.W * .5, settings.H * -.045))



    def randomize_attributes(self):
        self.skin_colors_idx = randint(0, len(self.skin_colors) - 1)
        self.hairstyles_idx = randint(0, len(self.hairstyles) - 1)
        self.hair_colors_idx = randint(0, len(self.hair_colors) - 1)
        self.races_idx = randint(0, len(self.races) - 1)
        self.tops_idx = randint(0, len(self.tops) - 1)
        self.bottoms_idx = randint(0, len(self.bottoms) - 1)
        self.socks_idx = randint(0, len(self.socks) - 1)
        self.chests_idx = randint(0, len(self.chests) - 1)

    def change_appearance(self):

        self.randomize_attributes()

        # Draws character and updates self.image
        surf = pg.Surface((1766, 2513), pg.SRCALPHA)
        if self.tops[self.tops_idx] != 'none':
            surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back1'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_back'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'tail_cat_{self.hair_colors[self.hair_colors_idx]}'])
        if self.tops[self.tops_idx] != 'none':
            surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back2'])
        surf.blit(self.parts[f'body_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'socks_{self.socks[self.socks_idx]}'])
        surf.blit(self.parts[f'bottom_{self.bottoms[self.bottoms_idx]}'])
        surf.blit(self.parts[f'chest_{self.chests[self.chests_idx]}'])
        surf.blit(self.parts[f'arm_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_front'])
        surf.blit(self.parts[f'face_purple'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'catear_back_{self.hair_colors[self.hair_colors_idx]}'])
            surf.blit(self.parts[f'catear_under_hair_{self.hair_colors[self.hair_colors_idx]}'])
        else:
            surf.blit(self.parts[f'humanear_{self.skin_colors[self.skin_colors_idx]}'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_front'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'catear_front_{self.hair_colors[self.hair_colors_idx]}'])

        data = pg.image.tobytes(surf, "RGBA")
        final_surf = pg.image.frombytes(data, (1766, 2513), "RGBA")
        final_surf = pg.transform.scale_by(final_surf, .46)
        self.image = final_surf
        
    def return_image(self):
        # Draws character at max res and returns it
        surf = pg.Surface((1766, 2513), pg.SRCALPHA)
        if self.tops[self.tops_idx] != 'none':
            surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back1'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_back'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'tail_cat_{self.hair_colors[self.hair_colors_idx]}'])
        if self.tops[self.tops_idx] != 'none':
            surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_back2'])
        surf.blit(self.parts[f'body_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'socks_{self.socks[self.socks_idx]}'])
        surf.blit(self.parts[f'bottom_{self.bottoms[self.bottoms_idx]}'])
        surf.blit(self.parts[f'chest_{self.chests[self.chests_idx]}'])
        surf.blit(self.parts[f'arm_{self.skin_colors[self.skin_colors_idx]}'])
        surf.blit(self.parts[f'top_{self.tops[self.tops_idx]}_front'])
        surf.blit(self.parts[f'face_purple'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'catear_back_{self.hair_colors[self.hair_colors_idx]}'])
            surf.blit(self.parts[f'catear_under_hair_{self.hair_colors[self.hair_colors_idx]}'])
        else:
            surf.blit(self.parts[f'humanear_{self.skin_colors[self.skin_colors_idx]}'])
        if self.hairstyles[self.hairstyles_idx] != 'bald':
            surf.blit(self.parts[f'hair_{self.hairstyles[self.hairstyles_idx]}_{self.hair_colors[self.hair_colors_idx]}_front'])
        if self.races[self.races_idx] == "cat":
            surf.blit(self.parts[f'catear_front_{self.hair_colors[self.hair_colors_idx]}'])

        data = pg.image.tobytes(surf, "RGBA")
        final_surf = pg.image.frombytes(data, (1766, 2513), "RGBA")
        return final_surf

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

class Slider(pg.sprite.Sprite):
    def __init__(self, groups, surfs, pos, user_settings, name):
        super().__init__(groups)
        self.pos = pos
        self.surfs = surfs
        self.selected = False
        self.in_use = False
        self.image = self.surfs['unselected']
        self.rect = self.image.get_frect(center = self.pos)
        self.bounds = (self.rect.centerx - 600, self.rect.centerx)
        self.name = name
        self.user_settings = user_settings
        self.idx = int(self.user_settings[name])
        self.rect.centerx += (self.idx * 6) - 600
        
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
                mouse_x = pg.mouse.get_pos()[0]
                if mouse_x > self.bounds[0] and mouse_x < self.bounds[1]:
                    self.rect.center = (mouse_x, self.pos[1])
                self.idx = 100 - round((self.bounds[1] - self.rect.centerx) / 6)
            
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
            with open('user_settings.txt') as settings_file:
                self.user_settings = json.load(settings_file)
                print(self.user_settings)
        except: 
            print('could not load user settings')
        
        ctypes.windll.user32.SetProcessDPIAware()  # keeps Windows GUI scale settings from messing with resolution
        monitor_size = pg.display.list_modes()[0]
        self.fullscreen = self.user_settings['Fullscreen']
        if self.fullscreen:
            self.display = pg.display.set_mode((settings.W, settings.H), pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode((settings.W, settings.H))
        self.font = pg.font.Font(join('assets', 'motley_forces.ttf'), 90)
        self.playscreen_button_font = pg.font.Font(join('assets', 'motley_forces.ttf'), 80)
        pg.display.set_caption("Dress Up Game")
        if not self.fullscreen:  # These just slow down game launch if done in fullscreen
            os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centers window
            # app = pywinauto.Application().connect(title_re="Dress Up Game")
            # app.top_window().set_focus() # Activates window
        self.clock = pg.time.Clock()
        self.running = True

        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_location = os.path.join(current_dir, "assets")

        # Imports: Cursor
        cursor_surf = pg.image.load(join(asset_location, 'img', 'ui', 'mouse.png')).convert_alpha()
        cursor = pg.cursors.Cursor((0,0), cursor_surf)
        pg.mouse.set_cursor(cursor)

        # Imports: Player
        self.player_parts = {}
        for folder_path, sub_folders, file_names in walk(join(asset_location, "img", "player_pieces")):
            if file_names:
                for file_name in file_names:
                    path = join(folder_path, file_name)
                    surf = pg.image.load(path).convert_alpha()
                    self.player_parts[file_name.split('.')[0]] = surf

        # Imports: Buttons and Sliders
        self.button_surfs = {
                             'selected': pg.image.load(join('assets', 'img', 'ui', 'button_selected.png')).convert_alpha(),
                             'unselected': pg.image.load(join('assets', 'img', 'ui', 'button_unselected.png')).convert_alpha()
        }
        
        self.return_button_surfs = {
                                    'selected': pg.image.load(join('assets', 'img', 'ui', 'return_button_selected.png')).convert_alpha(),
                                    'unselected': pg.image.load(join('assets', 'img', 'ui', 'return_button_unselected.png')).convert_alpha()                                    
        }
        
        self.slider_surfs = {
                             'unselected': pg.image.load(join('assets', 'img', 'ui', 'slider_knob_unselected.png')).convert_alpha(),
                             'selected': pg.image.load(join('assets', 'img', 'ui', 'slider_knob_selected.png')).convert_alpha()
        }
        
        self.checkbox_surfs = {
                               'unselected': pg.image.load(join('assets', 'img', 'ui', 'checkbox_unchecked.png')).convert_alpha(),
                               'unselected_hover': pg.image.load(join('assets', 'img', 'ui', 'checkbox_unchecked_hover.png')).convert_alpha(),
                               'selected': pg.image.load(join('assets', 'img', 'ui', 'checkbox_checked.png')).convert_alpha(),
                               'selected_hover': pg.image.load(join('assets', 'img', 'ui', 'checkbox_checked_hover.png')).convert_alpha()
        }
        
        self.randomize_button_surfs = {
                                       'unselected': pg.image.load(join('assets', 'img', 'ui', 'randomize_unselected.png')).convert_alpha(),
                                       'selected': pg.image.load(join('assets', 'img', 'ui', 'randomize_selected.png')).convert_alpha(),
                                       'pressed': pg.image.load(join('assets', 'img', 'ui', 'randomize_pressed.png')).convert_alpha()
        }
        
        self.save_image_button_surfs = {
                                        'unselected': pg.image.load(join('assets', 'img', 'ui', 'save_image_unselected.png')).convert_alpha(), 
                                        'selected': pg.image.load(join('assets', 'img', 'ui', 'save_image_selected.png')).convert_alpha(),
                                        'pressed': pg.image.load(join('assets', 'img', 'ui', 'save_image_pressed.png')).convert_alpha()
        }
        
        self.back_button_surfs = {
                                  'unselected': pg.image.load(join('assets', 'img', 'ui', 'back_button_unselected.png')).convert_alpha(),
                                  'selected': pg.image.load(join('assets', 'img', 'ui', 'back_button_selected.png')).convert_alpha()
        }
        
        # Imports: Background Hearts
        self.heart_surf = pg.image.load(join(asset_location, 'img', 'ui', 'heart.png')).convert_alpha()
        
        # Imports: Audio
        
        pg.mixer.music.load(join('assets', 'audio', '90s_Bodybuilding_Music_by_Aries_Beats.mp3'))

        # Sprite groups
        self.start_sprites = pg.sprite.Group()
        self.play_sprites = pg.sprite.Group()
        self.about_sprites = pg.sprite.Group()
        self.options_sprites = pg.sprite.Group()
        
        # Play music
        
        music_volume = (self.user_settings['Master Volume'] / 100) * (self.user_settings['Music Volume'] / 100)
        pg.mixer.music.set_volume(music_volume)
        pg.mixer.music.play(loops = -1)
        

    def start(self):

        self.display.fill('black')

        # Sprites
        start_button = Button(self.start_sprites, 'start', self.button_surfs, (1495, 290), self.font, 'light')
        options_button = Button(self.start_sprites, 'options', self.button_surfs, (1495, 475), self.font, 'light')
        about_button = Button(self.start_sprites, 'about', self.button_surfs, (1495, 660), self.font, 'light')
        close_button = Button(self.start_sprites, 'close', self.button_surfs, (1495, 845), self.font, 'light')

        menu_box = pg.image.load(join('assets', 'img', 'ui', 'start_menu_box.png')).convert_alpha()

        # Custom heart event
        self.background_hearts = pg.sprite.Group()
        heart_event = pg.event.custom_type()
        pg.time.set_timer(heart_event, 1000)
        
        for i in range(0, 2):
            x, y = randint(265, settings.W - 265), 0
            Heart(self.heart_surf, (x, y), self.background_hearts)

        # Loop
        while self.running:
            self.dt = self.clock.tick() / 1000
            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == heart_event:
                    x, y = randint(0, settings.W), randint(-300, -221)
                    Heart(self.heart_surf, (x, y), self.background_hearts)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_button.check_for_input():
                        for sprite in self.start_sprites:
                            sprite.kill()
                        self.play()
                    elif options_button.check_for_input():
                        for sprite in self.start_sprites:
                            sprite.kill()
                        self.options()
                    elif close_button.check_for_input():
                        self.running = False

            # Render
            self.display.fill('#ffe3f8')
            self.background_hearts.update(self.dt)
            self.background_hearts.draw(self.display)
            self.display.blit(menu_box)
            self.start_sprites.draw(self.display)
            self.start_sprites.update(self.display)
            pg.display.flip()
        pg.quit()
        exit()

    def options(self):
        
        self.display.fill('black')
        
        # Sprites
        options_bg = pg.image.load(join('assets', 'img', 'ui', 'options_background.png')).convert_alpha()
        
        return_button = Button(self.options_sprites, 'return to main menu', self.return_button_surfs, (settings.W / 2, 965), self.font, 'dark')
        
        fullscreen_checkbox = Checkbox(self.options_sprites, self.checkbox_surfs, (1480, 260), self.user_settings, "Fullscreen")
        master_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 430), self.user_settings, "Master Volume")
        music_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 610), self.user_settings, "Music Volume")
        sfx_volume_slider = Slider(self.options_sprites, self.slider_surfs, (1750, 790), self.user_settings, "SFX Volume")
                
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
                        with open('user_settings.txt', 'w') as settings_file:
                            json.dump(self.user_settings, settings_file)
                        for sprite in self.options_sprites:
                            sprite.kill()
                        self.start()
                if event.type == pg.MOUSEBUTTONUP:
                        self.fullscreen = self.user_settings['Fullscreen']
                        if self.fullscreen:
                            self.display = pg.display.set_mode((settings.W, settings.H), pg.FULLSCREEN)
                        else:
                            self.display = pg.display.set_mode((settings.W, settings.H))

            
            # Update User Settings
            self.user_settings['Fullscreen'] = fullscreen_checkbox.give_state()
            self.user_settings['Master Volume'] = master_volume_slider.give_idx()
            self.user_settings['Music Volume'] = music_volume_slider.give_idx()
            self.user_settings['SFX Volume'] = sfx_volume_slider.give_idx()
            music_volume = (self.user_settings['Master Volume'] / 100) * (self.user_settings['Music Volume'] / 100)
            pg.mixer.music.set_volume(music_volume)
            print(self.user_settings)


            # Render
            self.display.blit(options_bg)
            self.options_sprites.draw(self.display)
            self.options_sprites.update(self.display)
            pg.display.flip()
        pg.quit()
        exit()

    def play(self):

        self.display.fill('black')

        # Sprites
        self.player = Player(self.play_sprites, self.player_parts)
        play_bg = pg.image.load(join('assets', 'img', 'ui', 'halftone_bg.png')).convert_alpha()
        randomize_button = Button(self.play_sprites, 'randomize', self.randomize_button_surfs, (470, 260), self.playscreen_button_font, 'light')
        save_image_button = Button(self.play_sprites, 'save image', self.save_image_button_surfs, (495, 465), self.playscreen_button_font, 'light')
        back_button = Button(self.play_sprites, 'main menu', self.back_button_surfs, (312, 955), self.playscreen_button_font, 'light')

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
                    if randomize_button.check_for_input():
                        self.player.change_appearance()
                    elif save_image_button.check_for_input():
                        now = str(datetime.datetime.now())
                        print(f'original = {now}')
                        now_formatted = now.replace(' ', '.').replace(':', '.').replace('-', '.')
                        print('new = ', now_formatted)
                        pg.image.save(self.player.return_image(), join('your images', f'{now_formatted}.png'))
                    elif back_button.check_for_input():
                        for sprite in self.play_sprites:
                            sprite.kill()
                        self.start()
                        
            # Render
            self.display.blit(play_bg)
            self.play_sprites.draw(self.display)
            self.play_sprites.update(self.display)
            pg.display.flip()

        pg.quit()
        exit()


if __name__ == "__main__":
    game = Game()    
    game.start()