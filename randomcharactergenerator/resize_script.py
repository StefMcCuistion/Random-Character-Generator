from PIL import Image
import os, sys
from os.path import join

path = join('assets', 'img', 'character_parts/')
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((1766,2514), Image.LANCZOS)
            imResize.save(f + e)

if __name__ == "__main__":
    resize()