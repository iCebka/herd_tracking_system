import customtkinter as ctk
import tkinter
import pygame
import math
import random
import os
import sys
import csv
from constants import *
from tools import Vector
from sheep import Sheep
from uiParameters import *
from datetime import datetime

#To be called after first screen display
def simulation(N):
    
    pygame.init()

    #To write positions in a csv
    ruta = f"data.csv"
    archivo_csv = open(ruta, mode = 'w', newline = '')
    escritor_csv = csv.writer(archivo_csv, delimiter = ' ')

    #pygame management parameters
    WIN = pygame.display.set_mode(size)
    pygame.display.set_caption("Herd Tracking System V1")
    clock = pygame.time.Clock()
    fps = 60
    scale = 40
    Distance = 5
    speed = 0.0005
    FONT = pygame.font.SysFont("times new roman", 12)
    run = True
    showUI = False
    clock = pygame.time.Clock()
    
    #Simulation parameters and auxiliars
    last_operation_time = pygame.time.get_ticks()
    signal = False
    sheeps = []
    deceso = False
    lives = [0 for _ in range(N)]
    pos_counter = 0
    pos_buffer = 2 #Pulses of intervals to verify if a sheep is not moving
    last_pos =  [[None for _ in range(pos_buffer)] for _ in range(N)]
    etiq = False
    dead_counter = 1
    interval = 5000
    clicked = False
    deathStr = ""

    for i in range(N):
        j = random.randint(100,999)
        sheeps.append( Sheep(random.randint(LEFT, RIGHT), random.randint(TOP, BOTTOM), f"{j}ah") )#ah is just an example of posible characters tag for each sheep

    while run:
        clock.tick(fps)
        WIN.fill((1,50,32))
        scale = sliderScale.value
        pygame.draw.rect(WIN, GREEN, (LEFT, TOP, RIGHT, BOTTOM))

        #Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    showUI = not showUI
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True

        #Deaths button
        if decesoButton.state == True:
            dead_counter = 0
        #Tags button
        if clicked:
            etiq = not toggleEtiquetas.state
        #Provoking deaths
        while dead_counter < 1:
            l = random.randint(0, len(sheeps)-1)
            sheeps[l].death()
            #print(sheeps[l].iden, " ha muerto")
            dead_counter += 1

        #Building position messages each interval seconds
        tString = "" # to write in csv
        current_time = pygame.time.get_ticks()
        if (current_time - last_operation_time >= interval):
            outStr = ""
            sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)
            signal = True
            now = datetime.now()
            print("\n\n=================================================\n\nDate and actual time:", now.strftime("%Y-%m-%d %H:%M:%S"))
            tString = tString + now.strftime("%Y-%m-%d %H:%M:%S") + ","
            last_operation_time = current_time

        #When the number of positions recorded is the same of pos_buffer, the program verifies if a sheep has been immobile
        if (pos_counter == pos_buffer):
            for m in range(len(last_pos)):
                dTemp = 0
                if (lives[m] != -1):
                    for n in range(len(last_pos[m])-1):
                        pos = last_pos[m][n]
                        dTemp += (last_pos[m][n][0] - last_pos[m][n+1][0])**2 + (last_pos[m][n][1] - last_pos[m][n+1][1])**2
                        if (dTemp == 0):
                            lives[m] += 1
                        else:
                            lives[m] = 0
                        if lives[m] == 2:
                            print(f"Warning! Individual {sheeps[m].iden} has been immobile for a long time")
                            sheeps[m].alert = True
                        if lives[m] >= 3:
                            lives[m] = -1
                            sheeps[m].death()
                            deathStr = deathStr + " " + sheeps[m].iden + " "
            pos_counter = 0

        #Sheep drawing and position update
        i = 0
        for sheep in sheeps:
            sheep.radius = scale
            if (signal):
                last_pos[i][pos_counter] = (sheep.position.x,sheep.position.y)
                tString = tString + sheep.iden +":("+str(sheep.position.x)+";"+str(sheep.position.y)+")" + ","
                if (sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                    sheep.alert = True
                    outStr = outStr+ " "+ sheep.iden+ " "
                else:
                    sheep.alert = False
            if (sheep.alive):
                sheep.behaviour(sheeps)
                sheep.limits(0, WIDTH, 0, HEIGHT)#(LEFT, RIGHT, TOP, BOTTOM)
                sheep.update()
                sheep.hue += speed
            sheep.draw(WIN, Distance, etiq, scale)
            i += 1

        #Printing individuals out of protected area or deaths
        if (signal):
            tString = tString[:-1]
            #print(tString)
            escritor_csv.writerow(tString)
            print("Out of protected area ", "[",outStr, "]")
            outStr = ""
            signal = False
            print("Detected deaths: ", "[", deathStr, "]")
            pos_counter += 1

        #GUI display
        if showUI == True:
            panel.Render(WIN)
            ScaleText.Render(WIN)
            sliderScale.Render(WIN)
            decesoButton.Render(WIN)
            Etiquetas.Render(WIN)
            toggleEtiquetas.Render(WIN, clicked)
        else:
            UItoggle.Render(WIN)
        clicked = False
        pygame.display.update()

    pygame.quit()
    archivo_csv.close()

#To be called after first screen
def run():
    try:
        n = int(prompt_entry.get("1.0", "end-1c"))
        #os.system(f"core.py {n}")
        simulation(n)
    except ValueError:
        tkinter.messagebox.showerror("Error", "Input value must be a non negative integer")
        return

#First Screen
root = ctk.CTk()
root.title("My sheep")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(input_frame, text="Sheep Number (non zero integer) ")
prompt_label.grid(row=0, column = 0, padx = 10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column = 1, padx = 10, pady=10)    

generate_button = ctk.CTkButton(input_frame, text="Run simulation", command=run)
generate_button.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)

root.mainloop()


