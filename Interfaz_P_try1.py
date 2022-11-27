#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

matplotlib.use("TkAgg")

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk ,Image

#Estilos para fuentes y demás



window = tk.Tk()                # Definimos la ventana con nombre window
window.geometry('900x700')      # Tamaño de la ventana
window.title('Diferentes funciones - Programación Científica')
#window.config(cursor="heart", bg='teal')
etiqueta=tk.Label(window,text="Modelo de Hodgkin y Huxley",font=('math', 15, 'bold italic'))#, borderwidth = 3,width = 8)
etiqueta.pack(side=tk.TOP)

frame1 = tk.Frame(master=window)
frame1.place(x=25, y=400)
frame1.config(bg="#83D6B7", width=850, height=300, relief=tk.GROOVE, bd=8)

img = ImageTk.PhotoImage(Image.open("assets/images/Imagen_circuito.png"))
lab = tk.Label(image=img)
lab.place(x=470,y=50)

figure1 = plt.figure(figsize=(4.5, 3.5), dpi=100)
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (mV)')
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, window)
widget = bar1.get_tk_widget()
widget.place(x=10, y=50)


def CerrarAplicacion():
    MsgBox = tk.messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
    if MsgBox == 'yes':
       window.destroy()
    else:
        tk.messagebox.showinfo('Retornar','Será retornado a la aplicación')


Style = ttk.Style()      
Style.configure('2.TButton', font =('Times', 10, 'bold', 'underline'), foreground = '#000000')
Style.configure('titulo', font =('Times', 20, 'bold', 'underline'), foreground = '#E88A18')


Style.map("1.TButton",
          foreground=[('pressed', 'orange'), ('active', '#000000')],
          background=[('pressed', '!disabled', 'yellow'), ('active', 'yellow')])

Style.map("titulo",
           foreground=[('pressed', 'yellow'), ('active', '#34495E')],
           background=[('pressed', '!disabled', 'black'), ('active', 'white')])


Boton2 = ttk.Button(master=window, text="Simular", style="2.TButton", command = CerrarAplicacion).place(x=750,y=650)
Boton3 = ttk.Button(master=window, text="Importar", style="2.TButton", command = CerrarAplicacion).place(x=650,y=650)
Boton4 = ttk.Button(master=window, text="Exportar", style="2.TButton", command = CerrarAplicacion).place(x=550,y=650)

#Textos en la interfaz

lbl_titulo = tk.Label(master=frame1, bg="#83D6B7", font=('TIMES', 15, 'bold'), text="Método solución").place(x=5,y=5)

#Checkbox
c1 = tk.Checkbutton(master=frame1, bg="#83D6B7", font=('TIMES', 11, 'bold italic'),text="Runge-Kutta 2",variable=1, onvalue=1, offvalue=0, command=0).place(x=20,y=50)
c2 = tk.Checkbutton(master=frame1, bg="#83D6B7", font=('TIMES', 11, 'bold italic'),text="Runge-Kutta 4",variable=2, onvalue=1, offvalue=0, command=0).place(x=20,y=80)
c3 = tk.Checkbutton(master=frame1, bg="#83D6B7", font=('TIMES', 11, 'bold italic'),text="Euler Adelante",variable=3, onvalue=1, offvalue=0, command=0).place(x=20,y=110)
c4 = tk.Checkbutton(master=frame1, bg="#83D6B7", font=('TIMES', 11, 'bold italic'),text="Euler Modificado",variable=4, onvalue=1, offvalue=0, command=0).place(x=20,y=140)
c5 = tk.Checkbutton(master=frame1, bg="#83D6B7", font=('TIMES', 11, 'bold italic'),text="Euler Atrás",variable=5, onvalue=1, offvalue=0, command=0).place(x=20,y=170)

#c1.pack()
#lbl_x = tk.Label(master=frame1,font=('math', 15, 'bold italic'),bg="#F4D03F",text="x =",relief = tk.RIDGE, borderwidth = 3,width = 8).place(x=200, y=100)



window.mainloop()
# %%
