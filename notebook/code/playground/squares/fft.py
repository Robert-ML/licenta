import cv2
import numpy as np

import pyglet
from pyglet import shapes
from pyglet.window import mouse

import os


def do_fft(img):
    f = np.fft.fft2(img)
    fshift= np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    return (fshift, magnitude_spectrum)

def do_ifft(fshift):
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back

def create_file_name(file, suffix):
    return file.split(".")[0] + suffix + "." + file.split(".")[-1]


working_p = "./"
in_p = working_p + "in/"
out_p = working_p + "out/"

files = [f for f in os.listdir(in_p)]
imgs = []
for f in files:
    imgs.append((f, cv2.imread(in_p + f, cv2.IMREAD_GRAYSCALE)))



for (file, img) in imgs:
    (fshift, magnitude_spectrum) = do_fft(img)

    rows, cols = img.shape
    crow,ccol = int(rows/2) , int(cols/2)
    band = 2
    fshift[(crow-band):(crow+band), (crow-band):(crow+band)] = 0

    cv2.imwrite(out_p + file, magnitude_spectrum)
    cv2.imwrite(out_p + create_file_name(file, "_band"), 20*np.log(np.abs(fshift)))

    cv2.imwrite(out_p + create_file_name(file, "_ifft"), do_ifft(fshift))



size = 500
window = pyglet.window.Window(size, size, "board")

dist_pressed = None
dist_released = None

(file, img) = imgs[0]
rows, cols = img.shape
(fshift_o, magnitude_spectrum_o) = do_fft(img)
cv2.imshow("Image", img)
cv2.imshow("Magnitude Spectrum Original", magnitude_spectrum_o)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global dist_pressed
    dist_pressed = np.sqrt((x - size/2)**2 + (y - size/2)**2)
    print("pressed", dist_pressed)

    try:
        cv2.destroyWindow("Magnitude Spectrum")
    except:
        pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    global dist_released
    dist_released = np.sqrt((x - size/2)**2 + (y - size/2)**2)
    print("released", dist_released)

    # scale dist_pressed and dist_released to the image size
    scale = rows / size
    dist_pressed *= scale
    dist_released *= scale

    disk_mid_radius = abs(int((dist_pressed + dist_released) / 2))
    fshift = fshift_o.copy()
    cv2.circle(fshift, (int(rows/2), int(cols/2)), int(disk_mid_radius), color=0, thickness= abs(dist_pressed - dist_released))
    cv2.imshow("Magnitude Spectrum", 20*np.log(np.abs(fshift)))

# key press event
@window.event
def on_key_press(symbol, modifier):

    # key "E" get press
    if symbol == pyglet.window.key.E:

        # close the window
        window.close()

# start running the application
pyglet.app.run()

cv2.destroyAllWindows()
