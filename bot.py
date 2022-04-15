import cv2
import pyautogui
import mss
import numpy as np
import time
from random import uniform

sunflower = cv2.imread('sunflower.png')
hole = cv2.imread('hole.png')

#ZOOM 67%


def screenshot():
    with mss.mss() as sct:
        img = sct.grab({'top': 0, 'left': -1920, 'width': 1920, 'height': 1080})
        mss.tools.to_png(img.rgb, img.size, output='print.png')
        screen = cv2.imread('print.png')
    return screen

def match(img, threshold):
    screen = screenshot()
    res = cv2.matchTemplate(screen, img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    locs = zip(*loc[::-1])
    xO = 21435122
    yO = 21435122

    for pt in locs:
        x, y = pt
        if x < xO-5 or x > xO+5:
            pyautogui.dragTo(-1920+x+12, y+17)
            time.sleep(uniform(1,2))
            pyautogui.click()
            time.sleep(uniform(0.5,1))
            pyautogui.click()
            xO = x
            yO = y
            extras()

    pyautogui.dragTo(-960,628)
    pyautogui.click()
    time.sleep(2)
    
    return locs

def extras():
    screen = screenshot()
    chest = cv2.imread('chest.png')
    chestres = cv2.matchTemplate(screen, chest, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(chestres)
    if max_val >= 0.99:
        x, y = max_loc
        pyautogui.dragTo(-1920+x, y)
        pyautogui.click()

        time.sleep(uniform(0.5,1))
        pyautogui.dragTo(-960,628)
        pyautogui.click()

while True:
    
    print("Planting")
    match(hole, 0.85)
    print("Waiting")
    time.sleep(10)
    print("Harvesting")
    match(sunflower,0.75)
