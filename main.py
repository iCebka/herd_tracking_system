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

def simulation(n):
    pygame.init()

    WIN = pygame.display.set_mode(size)
    pygame.display.set_caption("Herd Tracking System V1")
    clock = pygame.time.Clock()
    fps = 60

    scale = 40
    Distance = 5
    speed = 0.0005
    FONT = pygame.font.SysFont("times new roman", 12)

    cadena1 = "Hola, mundo!"

    ruta = f"hola.csv"


    archivo_csv = open(ruta, mode = 'w', newline = '')
    escritor_csv = csv.writer(archivo_csv, delimiter = ' ')

    run = True
    showUI = False
    clock = pygame.time.Clock()
    deceso = False

    last_operation_time = pygame.time.get_ticks()

    signal = False
    sheeps = []

    N = n
    lives = [0 for _ in range(N)]
    #for i in range(len(last_pos)):
    #   for j in range(len(last_pos[i])):
    #       ffvf( last_pos[i][j], end = " ")
    #   print()
    pos_counter = 0
    pos_buffer = 2
    last_pos =  [[None for _ in range(pos_buffer)] for _ in range(N)]
    etiq = False
    dead_counter = 1
    interval = 5000
    clicked = False
    deathStr = ""

    for i in range(N):
        j = random.randint(100,999)
        sheeps.append( Sheep(random.randint(LEFT, RIGHT), random.randint(TOP, BOTTOM), f"{j}ah") )

    while run:
        clock.tick(fps)
        WIN.fill((0,0,0))
        scale = sliderScale.value
        pygame.draw.rect(WIN, DARK_GREY, (LEFT, TOP, RIGHT, BOTTOM))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    showUI = not showUI
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = True

        if decesoButton.state == True:
            dead_counter = 0

        if clicked:
            etiq = not toggleEtiquetas.state

        while dead_counter < 1:
            l = random.randint(0, len(sheeps)-1)
            sheeps[l].death()
            #print(sheeps[l].iden, " ha muerto")
            dead_counter += 1
            #print(dead_counter)
        tString = ""
        current_time = pygame.time.get_ticks()
        if (current_time - last_operation_time >= interval):
            outStr = ""
            sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)
            signal = True
            now = datetime.now()
            print("\n\n=================================================\n\nDate and actual time:", now.strftime("%Y-%m-%d %H:%M:%S"))
            tString = tString + now.strftime("%Y-%m-%d %H:%M:%S") + ","
            last_operation_time = current_time

        if (pos_counter == pos_buffer):
            
            #print("Resumen de ultimos 10 movimientos:")
            #for m in range(len(last_pos)):
                #print(f"Individuo {sheeps[m].iden}: ", end =" ")
            #   for n in range(len(last_pos[m])):
            #       pos = last_pos[m][n]
                    #print(pos)
            #       pygame.draw.circle(WIN, (255,255,255), (pos[0],pos[1]), 6)
                    #print( "(",pos[0],pos[1],")",  end = " ")
                #print()
            #   pos_counter = 0
            '''
            for m in range(len(last_pos)):
                dTemp = 0
                #print(lives[m])
                for n in range(len(last_pos[m])-1):
                    pos = last_pos[m][n]
                    dTemp +=  (last_pos[m][n][0] - last_pos[m][n+1][0])**2 + (last_pos[m][n][1] - last_pos[m][n+1][1])**2
                if (dTemp == 0):
                    lives[m] += 1
                else:
                    if (lives[m] == -1):
                        continue
                    else:
                        lives[m] = 0
                if (lives[m] == 2):
                    print(f"ADVERTENCIA! Individuo {sheeps[m].iden} lleva mucho tiempo inmóvil")
                if (lives[m] >= 3):
                    lives[m] = -1
                    #print(f"{sheeps[m].iden} esta muerto")
                    sheeps[m].death()
                    deathStr = deathStr + " " + sheeps[m].iden + " "
            pos_counter = 0
            '''

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


        i = 0
        for sheep in sheeps:
            sheep.radius = scale
            if (signal):
                last_pos[i][pos_counter] = (sheep.position.x,sheep.position.y)
                #print("* Meto esta posicion (", last_pos[i][pos_counter][0], ",", last_pos[i][pos_counter][1], ") en ", i, ", ", pos_counter )
                tString = tString + sheep.iden +":("+str(sheep.position.x)+";"+str(sheep.position.y)+")" + ","
                if (sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                    sheep.alert = True
                    outStr = outStr+ " "+ sheep.iden+ " "
                else:
                    sheep.alert = False
            if (sheep.alive):
                    #if pos_counter < pos_buffer:
                    #   last_pos[i][pos_counter] =  sheep.position 
                sheep.behaviour(sheeps)
                sheep.limits(0, WIDTH, 0, HEIGHT)#(LEFT, RIGHT, TOP, BOTTOM)
                sheep.update()
                sheep.hue += speed
            #print("ID:", sheep.iden, " speed ", sheep.velocity.magnitude())
            sheep.draw(WIN, Distance, etiq, scale)
            i += 1

        if (signal):
            tString = tString[:-1]
            #print(tString)
            escritor_csv.writerow(tString)
            print("Out of protected area ", "[",outStr, "]")
            outStr = ""
            signal = False
            print("Detected deaths: ", "[", deathStr, "]")
            pos_counter += 1

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


def run():
    try:
        n = int(prompt_entry.get("1.0", "end-1c"))
        #os.system(f"core.py {n}")
        simulation(n)
    except ValueError:
        tkinter.messagebox.showerror("Error", "Input value must be a non negative integer")
        return
    #user_prompt = prompt_entry.get("0.0", tkinter.END)
    #user_prompt += " en modo: " + style_dropdown.get()

    #n = int(number_slider.get())
    #user_prompt += f" con {n} ovejas"
    #os.system(f"main.py {n}")
    #print(user_prompt)

root = ctk.CTk()
root.title("Mis Ovejas")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

prompt_label = ctk.CTkLabel(input_frame, text="Sheep Number (non zero integer) ")
prompt_label.grid(row=0, column = 0, padx = 10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column = 1, padx = 10, pady=10)    

'''
style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1, column = 0, padx = 10, pady=10)

style_dropdown = ctk.CTkComboBox(input_frame, values=["Uno","Dos","Tres","Cuatro"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

number_label = ctk.CTkLabel(input_frame, text="# Ovejas")
number_label.grid(row=2, column = 0, padx = 10, pady=10)
number_slider = ctk.CTkSlider(input_frame, from_= 1, to = 100, number_of_steps=9)
number_slider.grid(row=2,column=1)

number_label_slider = ctk.CTkLabel(input_frame, text=str(number_slider.get()))
number_label_slider.grid(row=3,column=2)
'''

generate_button = ctk.CTkButton(input_frame, text="Run simulation", command=run)
generate_button.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)
'''
#canvas = tkinter.Canvas(root, width=700,height=700)
#canvas.pack(side="left")

#embeded_tk_window=tk.Frame(root, width = 700, height = 700)
'''

root.mainloop()


