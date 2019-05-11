from matplotlib import mlab as mlab
from rtlsdr import RtlSdr
import numpy as np
from PIL import Image
import time
import pygame

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

sdr = RtlSdr()
# configure device
sdr.sample_rate = 2.4e6  # Hz
sdr.center_freq = 94.7e6  # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'


image = []


def get_data():
    samples = sdr.read_samples(16*1024)
    power, _ = mlab.psd(samples, NFFT=1024, Fs=sdr.sample_rate /
                        1e6)

    max_pow = 0
    min_pow = 10

    # search whole data set for maximum and minimum value
    for dat in power:
        if dat > max_pow:
            max_pow = dat
        elif dat < min_pow:
            min_pow = dat

    # update image data
    imagelist = []
    for dat in power:
        imagelist.append(mymap(dat, min_pow, max_pow, 0, 255))
    image.append(np.array(imagelist, np.ubyte))
    print(image)
    print(len(image))
    print("LIVE")


def mymap(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(f"DIY SDR")
clock = pygame.time.Clock()
background = pygame.Surface(gameDisplay.get_size())
background = background.convert()
background.fill((0, 0, 0))

game_quit = False

while not game_quit:

    gameDisplay.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_quit = True

    pass

    pygame.display.update()
    clock.tick(60)

pygame.quit()

try:
    get_data()

    #im = Image.fromarray(largearray, mode='L')
    #t = time.time()
    # im.save(f"sdr/images/waterfall{t}.jpg")
    # im.save(f"sdr/images/waterfall{t}.bmp")


except KeyboardInterrupt:
    pass
finally:
    sdr.close()
