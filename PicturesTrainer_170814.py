# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 03:24:21 2017

@author: JanFreixa

THIS TRAINER IS BASED ON Pictures_Trainer_170725
+ uses a trained model to filter the creations.

"""

import math
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from keras.models import load_model

import tkinter as tk

#------------------------------Picture Creator---------------------------------
def RandomPic():
    
    while True:    

        w = list(range(1,100))
        canvas = np.zeros((100,100),dtype=int)
    
        lines = 10  # 
        for i in range(lines):     
            
            phi = random.uniform(0,1.57079633) # radianes
            m = math.tan(phi)
            n = random.uniform(10,70)
            
            # simple corrección del (0,0) de ejes cartesianos a numpy array            
            def D(o):
                return (100-o)
            
            # pinta la linea en el bitmap       
            for x in w:
                y = int(m*x + n) 
                previous_y = int(m*(x-1) + n)
                half_y = int(((y - previous_y)/2) + previous_y) 
                
                if previous_y == y:         
                    if y == 0:
                        y = 1 
                    canvas [ D (y) , x  ] = 1    
                else:               
                    if half_y > 100:
                        canvas [ D (100) : D (previous_y) , x-1] = 1
                        break
                    else:
                        if y > 100: 
                            canvas [ D (100)    : D (half_y)     , x   ] = 1
                            canvas [ D (half_y) : D (previous_y) , x-1 ] = 1                
                            break
                        else:
                            canvas [ D (y)      : D (half_y)     , x   ] = 1
                            canvas [ D (half_y) : D (previous_y) , x-1 ] = 1
        
            # simetrias
            ruleta = random.randint(0,3)
            if ruleta == 0: canvas = np.flipud(canvas)
            if ruleta == 1: canvas = np.fliplr(canvas)
            if ruleta == 2:
                canvas = np.flipud(canvas)
                canvas = np.fliplr(canvas)
            else: pass
            
            # borrar partes aleatorias de la linea 
            vert = [random.randint(0,99),random.randint(0,99)]  # eje vertical
            vert = sorted(vert)
            hori = [random.randint(0,99),random.randint(0,99)]  # eje horizontal
            hori = sorted(hori)
            canvas [0:vert[0], 0:hori[0]] = 0
            canvas [vert[1]:99, hori[1]:99] = 0

        # marconegro    
        canvas[0,:]=0
        canvas[99,:]=0
        canvas[:,0]=0
        canvas[:,99]=0
        
        # FILTERS 
        # restriccion de densidad - cantidad de puntos 
        #if np.count_nonzero(canvas) > 300:
            #break
        # trained model
        pred = model.predict(np.expand_dims(np.expand_dims(canvas, axis=0),axis=3))
                
        if np.count_nonzero(canvas) > 300 and pred >= 0.8:
            print (pred)            
            break
    
    return (canvas)
#-----------------------------------Actions------------------------------------

#pictures = np.load ('pictures.npy')  #load numpy array where pictures are stored
#target = np.load ('target.npy') 
# Check number of pictures I have stored
#n = np.load('pictures.npy').shape[0]


def kandinsky0 ():
    
    global pic
    global pictures
    global target
    global W
    
    if W == True:
        pic = pic_wait
        W = False
    
    pic = pic.flatten()
    pictures = np.vstack ([pictures, pic])
    np.save('pictures.npy', pictures)
    
    val=0
    target = np.append(target, val)
    np.save('target.npy', target)
    
    pic = RandomPic()
    DisplayPic(pic)
    

def kandinsky1 ():

    global pic
    global pictures
    global target
    global W
    
    if W == True:
        pic = pic_wait
        W = False
    
    pic = pic.flatten()
    pictures = np.vstack ([pictures, pic])
    np.save('pictures.npy', pictures)
    
    val=1
    target = np.append(target, val)
    np.save('target.npy', target)
    
    pic = RandomPic()
    DisplayPic(pic)

def kandinskyPASS ():
    
    global pic
    global pic_wait
    global W
    
    W = False    
    
    pic_wait=pic
    pic = RandomPic()
    DisplayPic(pic)
    
def kandinskyWAIT ():
    
    global pic
    global pic_wait
    global W
    
    DisplayPic(pic_wait)
    W = True        

def DisplayPic (img):
    
    plt.imsave( 'kdsk.png' , img, cmap=cm.gray)
    photo = tk.PhotoImage(file='kdsk.png')
    photo = photo.zoom(3, 3)
    
    photo_label.configure(image=photo)

    photo_label.pack()             
    photo_label.image = photo
    
##############################   M A I N    ###################################

'''
pictures = np.zeros(shape=(1,10000),dtype=int)
np.save('pictures.npy', pictures)

target = np.array((0),dtype=int)
np.save('target.npy', target)
'''

pictures  =  np.load('pictures.npy')
target    =  np.load('target.npy'  )
W = False

# trained model
model = load_model('C:/Users/Administrator/Desktop/kandinsky/predictive model - only copied data/my_model.h5')

#  GUI
main = tk.Tk()
main.title("Kandinsky's strings")
main.geometry('300x370')

photo = tk.PhotoImage(file='kdsk.png')
photo = photo.zoom(3, 3)
photo_label = tk.Label(image=photo)
photo_label.pack()     

pic = RandomPic()
plt.imsave( 'kdsk.png' , pic, cmap=cm.gray)
DisplayPic(pic)

# BUTTONS
button = tk.Button(main, text="DISTURBING", command = kandinsky0)
button.place(x=72, y=310, in_= main)

button2 = tk.Button( main, text="APPEALING", command = kandinsky1 )
button2.place(x=150, y=310, in_= main)

button3 = tk.Button( main, text="PASS", command = kandinskyPASS )
button3.place(x=128, y=336, in_= main)

button4 = tk.Button( main, text="<-", command = kandinskyWAIT )
button4.place(x=104, y=336, in_= main)

main.mainloop()
