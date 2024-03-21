import customtkinter as ctk
import tkinter
import pygame
import math
import random
import os

def run():
    try:
        n = int(prompt_entry.get("1.0", "end-1c"))
        os.system(f"core.py {n}")
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
