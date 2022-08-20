#main
import time

#buttons
import keyboard

#fishing
import pyautogui
from PIL import ImageGrab
import numpy as np

#map
import pygame
from ctypes import windll

#idicators
import winsound  

#timer
from tkinter import *
from datetime import datetime, timedelta


def print_img(x, y, dir):
    SetWindowPos = windll.user32.SetWindowPos

    pygame.display.init()
    img = pygame.image.load(dir)
    screen = pygame.display.set_mode(img.get_size())

    run = True
    while run:
        pygame.time.delay(100)
        SetWindowPos(pygame.display.get_wm_info()['window'], -1, x, y, 0, 0, 0x0001)
        screen.blit(img, (0, 0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                 
    pygame.quit()

def fishing():
    coords = [1000,550,1010,555]
    pyautogui.press('e')
    time.sleep(0.1)
    while (keyboard.is_pressed('alt') and keyboard.is_pressed('f')) == False:
        screen = np.array(ImageGrab.grab(bbox=coords))
        ind = False
        for line in screen:
            for pix in line:
                if pix[0] > 180 and pix[1] < 55 and pix[2] < 55:
                    ind = True
        print(pix, ind)
        if ind:
            pyautogui.press('e')
            time.sleep(1)
            pyautogui.press('e')
            
        time.sleep(0.1)


def time_text(i):
    time_zero = datetime(2000, 1, 1)
    timer = timers[i][1]
    time_stop = timers[i][2]
    
    if time_stop != 0:
        t_delta = time_stop - datetime.now()
        
    else:
        t_delta = timedelta(0, 0, 0, 0, timer/60, 0, 0)
    
    return (time_zero + t_delta).strftime("%H:%M:%S")


def button_text(i):
    return timers[i][0].ljust(max_len) + ': ' + time_text(i)


def max_name():
    max = 0
    
    for timer in timers:
        len_t = len(timer[0])
        if len_t > max:
            max = len_t
    return max
    
    
def color_button(i):
    time_stop = timers[i][2]
    if time_stop == 0:
        return '#eee'
    
    t_delta = time_stop - datetime.now()
    
    if t_delta < time_red:
        return '#FC5362'
    if t_delta < time_orange:
        return '#FF8F33'
    if time_stop != 0:
        return '#77c66e'
    
    return '#77c66e'    
    

def check_time():
    ind = False
    time_zero = timedelta(0, 0, 0, 0, 0, 0, 0)
    for i in range(num_timer):
        time_stop = timers[i][2]
        if time_stop != 0:
            t_delta = time_stop - datetime.now()
            if t_delta < time_zero:
                check_list[i] = 'wait1'
                timers[i][2] = 0
                
            elif t_delta < time_orange and check_list[i] == 'wait1':
                check_list[i] = 'wait2'
                ind = True
                
            elif t_delta < time_red and check_list[i] == 'wait2':
                check_list[i] = 'wait3'
                ind = True
    
    return ind
 
    
def timer():
    def update():
        global timers
        check_time()
        for i in range(num_timer):
            buttons[i].config(text=button_text(i), bg=color_button(i))
        root.after(500, update)
    
    def start_timer(i):
        timers[i][2] = datetime.now() + timedelta(0, 0, 0, 0, timers[i][1]/60, 0, 0)
    
    root = Tk()
    root.attributes("-topmost",True)
    root.title("Timer")
    width_win = len(button_text(0)) * 12
    height_win = num_timer * 28
    root.geometry(str(width_win) + 'x' + str(height_win) + '+250+-30')
    root.configure(bg='white')
    
    buttons = []
    for i in range(num_timer):
        timer = timers[i]

        buttons.append(Button(text=button_text(i), font=("Courier", 11), bg=color_button(i), command= lambda i=i:start_timer(i)))
        buttons[i].place(relx=0.5, rely=(0.5 / num_timer) + (1 / num_timer) * i, anchor='c', height=25, width=width_win-10)
    
    root.after(500, update)
    root.after(5000, root.destroy)
    
    
    root.mainloop()


minute_time = 7

timers = [['Мемориальный район', minute_time*60, 0],
          ['Район Арены', minute_time*60, 0],
          ['Дендрарий', minute_time*60, 0],
          ['Храмовый район', minute_time*60, 0],
          ['Район Знати', minute_time*60, 0],
          ['Район Эльфийские сады', minute_time*60, 0]]

max_len = max_name()
num_timer = len(timers)

time_orange = timedelta(0, 0, 0, 0, 1/2, 0, 0) # 30 sec
time_red = timedelta(0, 0, 0, 0, 1/12, 0, 0) # 5 sec

# wait1 - t > 30 sec
# wait2 - 30 > t > 5 sec
# wait3 - 5 > t > 0 sec
check_list = ['wait1']*num_timer

print(check_list)

#main
while True:
    print('stop')
    keyboard.wait('*')
    winsound.Beep(700, 500)
    
    time.sleep(0.1)
    print('play')
    while keyboard.is_pressed('*') == False:
        ind = check_time()
        
        if keyboard.is_pressed('alt') and keyboard.is_pressed('m'):
            print('map')
            print_img(-8, -36, 'map2.png')
            
        elif keyboard.is_pressed('alt') and keyboard.is_pressed('f'):
            print('fishing')
            winsound.Beep(800, 300)
            winsound.Beep(800, 300)
            fishing()
            winsound.Beep(600, 300)
            winsound.Beep(600, 300)
            
        elif (keyboard.is_pressed('alt') and keyboard.is_pressed('t')) or ind:
            print('timer start')
            timer()
            time.sleep(0.3)
            print('timer end')
        
        
        time.sleep(0.05)
        
    winsound.Beep(500, 500)

input('Nu vse - pizdec!')





