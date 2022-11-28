import tkinter as tk
import numpy as np
import matplotlib as mpl
from tkinter import ttk

mpl.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from PIL import ImageTk, Image

# crear ventana:
window = tk.Tk()

# Definir tamaño de ventana:
window.geometry("800x600")
window.title("Simulación")


label = tk.Label(window, background= "#8ea7ba", text="Modelo de Hodgkin-Huxley", font=('math', 15, 'bold italic'),height=1 ,width=800).pack()

# grafica
fig = Figure(figsize=(6, 5), dpi=50)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")
canvas = FigureCanvasTkAgg(fig, window)
canvas.get_tk_widget().place(x=50, y=50)

#Imagen
img = ImageTk.PhotoImage(Image.open("assets/images/Imagen_circuito.png"))
lab = tk.Label(image=img)
lab.place(x=440,y=50)

# Metodos de Solucion
metodo = tk.Label(window, text="Método de solución:", font=('math', 9, 'bold italic')).place(x=20, y=320)
checkRungeKutta2 = tk.Checkbutton(window, text="Runge-Kutta 2",font=('math', 9, 'italic'), height=1, width=14).place(x=15, y=360)
checkRungeKutta4 = tk.Checkbutton(window, text="Runge-Kutta 4",font=('math', 9, 'italic'), height=1, width=14).place(x=15, y=400)
checkEulerAdelante= tk.Checkbutton(window, text="Euler Adelante",font=('math', 9, 'italic'), height=1, width=14).place(x=15, y=440)
checkEulerModificado = tk.Checkbutton(window, text="Euler Modificado",font=('math', 9, 'italic'), height=1, width=15).place(x=15, y=480)
checkEulerAtrás = tk.Checkbutton(window, text="Euler Atrás",font=('math', 9, 'italic'), height=1, width=11).place(x=15, y=520)

# Variables
variable = tk.Label(window, text="Variables:", font=('math', 9, 'bold italic')).place(x=150, y=320)
check6 = tk.Checkbutton(window, text="V(t)",font=('math', 9, 'italic'), height=1, width=4).place(x=150, y=350)
check7 = tk.Checkbutton(window, text="gk(t)",font=('math', 9, 'italic'), height=1, width=4).place(x=245, y=350)
check7 = tk.Checkbutton(window, text="gNa(t)",font=('math', 9, 'italic'), height=1, width=4).place(x=340, y=350)

# Parametros
parametros = tk.Label(window, text="Parámetros:", font=('math', 9, 'bold italic')).place(x=150, y=380)
Ek = tk.Label(window, text="Ek",font=('math', 9, 'italic')).place(x=155, y=410)
Ek1 = tk.Entry(window, width=8).place(x=185, y=410)
Ek11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=410)
ENa = tk.Label(window, text="ENa",font=('math', 9, 'italic')).place(x=155, y=465)
ENa1 = tk.Entry(window, width=8).place(x=185, y=465)
ENa11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=465)
El = tk.Label(window, text="El",font=('math', 9, 'italic')).place(x=155, y=520)
El1 = tk.Entry(window, width=8).place(x=185, y=520)
El11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=520)
gk = tk.Label(window, text="/gk",font=('math', 9, 'italic')).place(x=260, y=430)
gk1 = tk.Entry(window, width=8).place(x=295, y=430)
gk11 = tk.Label(window, text="mS/cm^3",font=('math', 9, 'italic')).place(x=340, y=430)
gNa = tk.Label(window, text="/gNa",font=('math', 9, 'italic')).place(x=260, y=490)
gNa1 = tk.Entry(window, width=8).place(x=295, y=490)
gNa11 = tk.Label(window, text="mS/cm^3",font=('math', 9, 'italic')).place(x=340, y=490)

# Botones
simular = tk.Button(window,background= "#8ea7ba", text="Simular",font=('math', 9, 'bold italic'), width=13).place(x=450, y=550)
importar = tk.Button(window,background= "#8ea7ba", text="Importar",font=('math', 9, 'bold italic'), width=13).place(x=560, y=550)
exportar = tk.Button(window,background= "#8ea7ba", text="Exportar",font=('math', 9, 'bold italic'), width=13).place(x=670, y=550)
cargar = tk.Button(window,background= "#8ea7ba", text="Cargar",font=('math', 9, 'bold italic'), width=13).place(x=670, y=410)

# Entrada de texto
tiempoSimulacion = tk.Label(window, text="Tiempo de simulacion:",font=('math', 9, 'italic')).place(x=440, y=320)
tiempoSimulacion1 = tk.Entry(window, width=8).place(x=630, y=320)
tiempoSimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=320)
tiempoInicioEstimulacion = tk.Label(window, text="Tiempo de inicio estimulacion:",font=('math', 9, 'italic')).place(x=440, y=340)
tiempoInicioEstimulacion1 = tk.Entry(window, width=8).place(x=630, y=340)
tiempoInicioEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=340)
tiempoFinEstimulacion = tk.Label(window, text="Tiempo de fin estimulacion:",font=('math', 9, 'italic')).place(x=440, y=360)
tiempoFinEstimulacion1 = tk.Entry(window, width=8).place(x=630, y=360)
tiempoFinEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=360)
ValorEstimulacion = tk.Label(window, text="Valor estimulacion:",font=('math', 9, 'italic')).place(x=440, y=380)
ValorEstimulacion1 = tk.Entry(window, width=8).place(x=630, y=380)
ValorEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=380)

window.mainloop()