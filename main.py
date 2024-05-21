import customtkinter as ctk
from tkinter import filedialog
import tkinter
import pygame
import math
import random
import os
import sys
import csv
import re
from collections import defaultdict
from constants import *
from tools import Vector
from environment import Sheep
from environment import Hole
from environment import Wolf
from uiParameters import *
from datetime import datetime
from dataReadingFigures import parse_positions, readAndFigures

def run_load():
    try:
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=(("Text files", "*.csv"), ("All files", "*.*")))
        if file_path:
            print(file_path)
            sheeps = load_sheeps(file_path)
            loaded_simulation(sheeps)
    except ValueError:
        tkinter.messagebox.showerror("Error", "Failure while reading file. Please use a csv file in the right format.")
        return

def load_sheeps(file):
    # Inicializar diccionario para las posiciones de las ovejas
    sheep_positions = defaultdict(lambda: {'x': [], 'y': []})

    # Leer el archivo CSV
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # El primer campo es la fecha y hora, el resto contiene información de las ovejas
            timestamp = row[0]
            sheep_data = ' '.join(row[1:]).replace('"', '').replace(':', ' : ')
            
            # Parsear posiciones de las ovejas
            parsed_data = parse_positions(sheep_data)
            
            # Guardar posiciones en arreglos separados
            for sheep_id, x, y in parsed_data:
                sheep_positions[sheep_id]['x'].append(x)
                sheep_positions[sheep_id]['y'].append(y)

    # Mostrar los datos almacenados
    sheeps = []
    for sheep_id, positions in sheep_positions.items():
        print(f"Oveja {sheep_id}:")
        print(f"  x: {positions['x'][len(positions['x'])-1]}")
        print(f"  y: {positions['y'][len(positions['x'])-1]}")
        sheeps.append( Sheep(positions['x'][len(positions['x'])-1], positions['y'][len(positions['x'])-1],sheep_id ) )

    return sheeps

def loaded_simulation(loaded_sheeps):
    pygame.init()

    M = 0
    L = 0
    N = len(loaded_sheeps)
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
    sheeps = loaded_sheeps
    wolfs = []
    holes = []
    environment = loaded_sheeps
    deceso = False
    lives = [0 for _ in range(N)]
    pos_counter = 0
    pos_buffer = 2 #Pulses of intervals to verify if a sheep is not moving
    last_pos =  [[None for _ in range(pos_buffer)] for _ in range(N)]
    etiq = False
    dead_counter = 1
    wolfAppeared = 0
    interval = 1000
    clicked = False
    deathStr = ""

    '''
    for i in range(N):
        j = random.randint(100,999)
        tempoSheep = Sheep(random.randint(LEFT, RIGHT), random.randint(TOP, BOTTOM), f"{j}ah")
        sheeps.append( tempoSheep )#ah is just an example of posible characters tag for each sheep
        environment.append( tempoSheep )

    
    for m in range(M):
        tempoWolf = Wolf(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ) )
        wolfs.append( tempoWolf )
        environment.append( tempoWolf)
    

    for l in range(L):
        tempoHole = Hole(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ))
        holes.append( tempoHole )
        environment.append( tempoHole )
    '''

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
            #sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)
            signal = True
            now = datetime.now()
            
            randomIt = random.randint(1, 100)
            #print(f"random: {randomIt} y {randomIt%7}")
            if (randomIt % 7 == 1 and wolfAppeared < M):
                tempoWolf = Wolf(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ) )
                wolfs.append( tempoWolf )
                environment.append( tempoWolf)
                wolfAppeared += 1
                print("Wolf is generated")
                    
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
                        if lives[m] == 7:
                            print(f"Warning! Individual {sheeps[m].iden} has been immobile for a long time")
                            #sheeps[m].alert = True
                        if lives[m] >= 8:
                            lives[m] = -1
                            sheeps[m].death()
                            deathStr = deathStr + " " + sheeps[m].iden + " "
            pos_counter = 0
        for hole in holes:
            hole.radius = scale
            hole.draw(WIN, Distance, scale)
        #Sheep drawing and position update
        i = 0
        for sheep in sheeps:
            #sheep.radius = sheep.radius * scale/100
            if (signal):
                last_pos[i][pos_counter] = (sheep.position.x,sheep.position.y)
                tString = tString + sheep.iden +":("+str(sheep.position.x)+";"+str(sheep.position.y)+")" + ","
                if (sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                    sheep.alert = True
                    outStr = outStr+ " "+ sheep.iden+ " "
                else:
                    sheep.alert = False
            if (sheep.alive):
                sheep.behaviour(environment)
                #sheep.behaviour(wolfs)
                sheep.limits(0, WIDTH, 0, HEIGHT)#(LEFT, RIGHT, TOP, BOTTOM)
                sheep.update()
                sheep.hue += speed
            sheep.draw(WIN, Distance, etiq, scale)
            i += 1

        
        for wolf in wolfs[:]:
            if (wolf.eatCounter >= 2 and wolf.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                wolfs.remove(wolf)
                environment.remove(wolf)
            #wolf.radius = wolf.radius * scale/100
            wolf.behaviour(environment)
            wolf.limits(0,WIDTH, 0, HEIGHT)
            wolf.update()
            wolf.hue += speed
            wolf.draw(WIN, Distance, scale)
        


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

#To be called after first screen display
def simulation(N, M, L):
    
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
    wolfs = []
    holes = []
    environment = []
    deceso = False
    lives = [0 for _ in range(N)]
    pos_counter = 0
    pos_buffer = 2 #Pulses of intervals to verify if a sheep is not moving
    last_pos =  [[None for _ in range(pos_buffer)] for _ in range(N)]
    etiq = False
    dead_counter = 1
    wolfAppeared = 0
    interval = 1000
    clicked = False
    deathStr = ""
    
    for i in range(N):
        j = random.randint(100,999)
        tempoSheep = Sheep(random.randint(LEFT, RIGHT), random.randint(TOP, BOTTOM), f"{j}ah")
        sheeps.append( tempoSheep )#ah is just an example of posible characters tag for each sheep
        environment.append( tempoSheep )

    '''
    for m in range(M):
        tempoWolf = Wolf(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ) )
        wolfs.append( tempoWolf )
        environment.append( tempoWolf)
    '''

    for l in range(L):
        tempoHole = Hole(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ))
        holes.append( tempoHole )
        environment.append( tempoHole )

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
            #sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)
            signal = True
            now = datetime.now()
            
            randomIt = random.randint(1, 100)
            #print(f"random: {randomIt} y {randomIt%7}")
            if (randomIt % 7 == 1 and wolfAppeared < M):
                tempoWolf = Wolf(random.randint(LEFT, RIGHT), random.randint( TOP, BOTTOM ) )
                wolfs.append( tempoWolf )
                environment.append( tempoWolf)
                wolfAppeared += 1
                    
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
                        if lives[m] == 7:
                            print(f"Warning! Individual {sheeps[m].iden} has been immobile for a long time")
                            #sheeps[m].alert = True
                        if lives[m] >= 8:
                            lives[m] = -1
                            sheeps[m].death()
                            deathStr = deathStr + " " + sheeps[m].iden + " "
            pos_counter = 0
        for hole in holes:
            hole.radius = scale
            hole.draw(WIN, Distance, scale)
        #Sheep drawing and position update
        i = 0
        for sheep in sheeps:
            #sheep.radius = sheep.radius * scale/100
            if (signal):
                last_pos[i][pos_counter] = (sheep.position.x,sheep.position.y)
                tString = tString + sheep.iden +":("+str(sheep.position.x)+";"+str(sheep.position.y)+")" + ","
                if (sheep.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                    sheep.alert = True
                    outStr = outStr+ " "+ sheep.iden+ " "
                else:
                    sheep.alert = False
            if (sheep.alive):
                sheep.behaviour(environment)
                #sheep.behaviour(wolfs)
                sheep.limits(0, WIDTH, 0, HEIGHT)#(LEFT, RIGHT, TOP, BOTTOM)
                sheep.update()
                sheep.hue += speed
            sheep.draw(WIN, Distance, etiq, scale)
            i += 1

        
        for wolf in wolfs[:]:
            if (wolf.eatCounter >= 2 and wolf.is_in_place(LEFT, RIGHT, TOP, BOTTOM)):
                wolfs.remove(wolf)
                environment.remove(wolf)
            #wolf.radius = wolf.radius * scale/100
            wolf.behaviour(environment)
            wolf.limits(0,WIDTH, 0, HEIGHT)
            wolf.update()
            wolf.hue += speed
            wolf.draw(WIN, Distance, scale)
        


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
        n = int(sheep_entry.get("1.0", "end-1c"))
        m = int(wolf_entry.get("1.0", "end-1c"))
        l = int(hole_entry.get("1.0", "end-1c"))
        generate_images = generate_images_var.get()
        #os.system(f"core.py {n}")
        if (n <= 0):
            raise ValueError("Negative value not allowed")
        simulation(n, m, l)
        if generate_images:
            print("Wait for generating tracking images...")
            readAndFigures()
        else:
            print("Not generating tracking images")
    except ValueError:
        tkinter.messagebox.showerror("Error", "Input value must be a non negative integer")
        return

if __name__ == '__main__':
    
    #First Screen
    root = ctk.CTk()
    root.title("My sheep")

    ctk.set_appearance_mode("dark")

    input_frame = ctk.CTkFrame(root)
    input_frame.pack(side="left", expand=True, padx=20, pady=20)

    #Sheep Number TextBox
    sheep_label = ctk.CTkLabel(input_frame, text="Sheep Number (positive integer) ")
    sheep_label.grid(row=0, column = 0, padx = 10, pady=10)
    sheep_entry = ctk.CTkTextbox(input_frame, height=10)
    sheep_entry.grid(row=0, column = 1, padx = 10, pady=10)

    #Wolf Number TextBox
    wolf_label = ctk.CTkLabel(input_frame, text="Wolf Number (non negative integer) ")
    wolf_label.grid(row=1, column = 0, padx = 10, pady=10)
    wolf_entry = ctk.CTkTextbox(input_frame, height=10)
    wolf_entry.grid(row=1, column = 1, padx = 10, pady=10)    

    #Hole Number TextBox
    hole_label = ctk.CTkLabel(input_frame, text="Hola Number (non negative integer) ")
    hole_label.grid(row=2, column = 0, padx = 10, pady=10)
    hole_entry = ctk.CTkTextbox(input_frame, height=10)
    hole_entry.grid(row=2, column = 1, padx = 10, pady=10)

    # Checkbox to generate tracking images
    generate_images_var = ctk.BooleanVar()
    generate_images_checkbox = ctk.CTkCheckBox(input_frame, text="Generate Tracking Images", variable=generate_images_var)
    generate_images_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    generate_button = ctk.CTkButton(input_frame, text="Run simulation", command=run)
    generate_button.grid(row=4, column=0, columnspan=2, sticky="news", padx=10, pady=10)

    # Button to load state (beta)
    load_state_button = ctk.CTkButton(input_frame, text="Load State (Beta)", command=run_load)
    load_state_button.grid(row=7, column=0, columnspan=2, sticky="news", padx=10, pady=10)


    root.mainloop()


