from settings import *
import numpy as np
from PIL import Image
# pour ramener le répertoire d'exécution à l'emplacement du script courant
from inspect import getsourcefile
import os

script_dir = os.path.dirname(getsourcefile(lambda: 0))
os.chdir(script_dir)
# fin changement dir
RES = WIDTH, HEIGHT = 255, 255
im = Image.new("RGB", RES)
for x in range(WIDTH):
    for y in range(HEIGHT):
        x0_1 = x / WIDTH
        y0_1 = y / HEIGHT
        px = get_color(x0_1, y0_1, *rgb_square_points)
        px = (255 - px[0], px[1], px[2])
        im.putpixel((x, y), px)

im.save('ressources/rgb_color1pick.png')
im.show()

