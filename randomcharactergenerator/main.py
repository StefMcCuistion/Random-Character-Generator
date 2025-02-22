import io
from random import randint, uniform
import pygame as pg

# from pygame import mixer
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
        self.hairstyles = ["bald", "emo", "bubble_braid"]
        self.hair_colors = ["black", "blonde", "brown", "purple"]
        self.bottoms = ["shorts", "skirt"]
        self.chests = ["cropped_shirt", "bra"]
        self.tops = ["none", "anime_jacket", "jacket", "coat", 'cropped_hoodie']
        self.socks = ["none", "leggings", "thigh_highs_black", "thigh_highs_cream"]
        
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
    def __init__(self, groups, name, surfs, pos, font):
        super().__init__(groups)
        self.selected = False
        self.surfs = surfs
        self.image = self.surfs['unselected']
        self.pos = pos
        self.rect = self.image.get_frect(center = self.pos)
        self.font = font
        self.selected_color = '#ffe8f9'
        self.unselected_color = '#ffb5ed'
        self.font_color = self.unselected_color
        self.name = name
        self.text = self.font.render(self.name, True, self.font_color)
        self.text_rect = self.text.get_frect(center = (self.rect.center[0], self.rect.center[1] + 22))


    def update(self, display):
        if self.check_for_input():
            self.selected = True
            self.font_color = self.selected_color
        else:
            self.selected = False
            self.font_color = self.unselected_color
        self.text = self.font.render(self.name, True, self.font_color)
        if self.selected:
            self.image = self.surfs['selected']
            self.rect = self.image.get_frect(center = self.pos)
        else:
            self.image = self.surfs['unselected']
            self.rect = self.image.get_frect(center = self.pos)
        display.blit(self.text, self.text_rect)



    def check_for_input(self):
        pos = (pg.mouse.get_pos())
        if pos[0] in (range(int(self.rect.left), int(self.rect.right))) and pos[1] in range(int(self.rect.top), int(self.rect.bottom)):
            return 1




class Game:

    def __init__(self):

        # Setup
        pg.init()
        pg.font.init()
        ctypes.windll.user32.SetProcessDPIAware()  # keeps Windows GUI scale settings from messing with resolution
        monitor_size = pg.display.list_modes()[0]
        self.display = pg.display.set_mode((settings.W, settings.H))
        self.fullscreen = False
        self.font = pg.font.Font(join('assets', 'motley_forces.ttf'), 80)
        pg.display.set_caption("Dress Up Game")
        if not self.fullscreen:  # These just slow down game launch if done in fullscreen
            os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centers window
            # app = pywinauto.Application().connect(title_re="Dress Up Game")
            # app.top_window().set_focus() # Activates window
        self.clock = pg.time.Clock()
        self.running = True

        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_location = os.path.join(current_dir, "assets")

        # Imports
        cursor_surf = pg.image.load(join(asset_location, 'img', 'ui', 'mouse.png')).convert_alpha()
        cursor = pg.cursors.Cursor((0,0), cursor_surf)
        pg.mouse.set_cursor(cursor)


        self.player_parts = {}
        for folder_path, sub_folders, file_names in walk(join(asset_location, "img", "player_pieces")):
            if file_names:
                for file_name in file_names:
                    path = join(folder_path, file_name)
                    surf = pg.image.load(path).convert_alpha()
                    self.player_parts[file_name.split('.')[0]] = surf

        self.button_surfs = {
                             'selected': pg.image.load(join('assets', 'img', 'ui', 'button_selected.png')).convert_alpha(),
                             'unselected': pg.image.load(join('assets', 'img', 'ui', 'button_unselected.png')).convert_alpha()
        }

        self.heart_surf = pg.image.load(join(asset_location, 'img', 'ui', 'heart.png')).convert_alpha()

        # Sprite groups
        self.start_sprites = pg.sprite.Group()
        self.play_sprites = pg.sprite.Group()
        self.options_sprites = pg.sprite.Group()

    def start(self):

        self.display.fill('black')

        # Sprites
        start_button = Button(self.start_sprites, 'start', self.button_surfs, (1495, 345), self.font)
        options_button = Button(self.start_sprites, 'options', self.button_surfs, (1495, 575), self.font)
        close_button = Button(self.start_sprites, 'close', self.button_surfs, (1495, 805), self.font)

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
                    if event.key == pg.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.display = pg.display.set_mode((settings.W, settings.H), pg.FULLSCREEN)
                        else:
                            self.display = pg.display.set_mode((settings.W, settings.H))
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_button.check_for_input():
                        for sprite in self.start_sprites:
                            sprite.kill()
                        self.play()
                    elif options_button.check_for_input():
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

    def options(self):
        print('options')

    def play(self):

        self.display.fill('black')

        # Sprites
        self.player = Player(self.play_sprites, self.player_parts)
        bg = pg.image.load(join('assets', 'img', 'test_bg.png')).convert_alpha()

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
                    if event.key == pg.K_f:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.display = pg.display.set_mode((settings.W, settings.H), pg.FULLSCREEN)
                        else:
                            self.display = pg.display.set_mode((settings.W, settings.H))
                    if event.key == pg.K_s:
                        for sprite in self.play_sprites:
                            sprite.kill()
                        self.start()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.player.change_appearance()
            # Render
            self.display.blit(bg)
            self.play_sprites.draw(self.display)
            pg.display.flip()

        pg.quit()
        exit()


if __name__ == "__main__":
    game = Game()    
    game.start()