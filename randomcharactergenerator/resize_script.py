from PIL import Image
import os, sys
from os.path import join

path = join('assets', 'img', 'character_pieces_high_res/')
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((883,1257), Image.LANCZOS)
            f.replace("high_res", "low_res")
            imResize.save(f + '.png',)


resize()