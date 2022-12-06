import tkinter as tk
import numpy as np
import matplotlib as mpl
from tkinter import ttk
from matplotlib import pyplot as plt
from funciones_modelo import *
import struct as st

mpl.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from PIL import ImageTk, Image

#---------------------------------------------------------------- Interfaz ----------------------------------------------------------------
# crear ventana:
window = tk.Tk()

# Definir tamaño de ventana:
window.geometry("800x600")
window.title("Simulación - Modelo Hodkin-Huxley")

#Variables de texto
tiempoSimulacion1Var = tk.StringVar()
tiempoInicioEstimulacion1Var = tk.StringVar()
tiempoFinEstimulacion1Var = tk.StringVar()
ValorEstimulacion1Var = tk.StringVar()
Ek1Var = tk.StringVar()
ENa1Var = tk.StringVar()
El1Var = tk.StringVar()
gk1Var = tk.StringVar()
gNa1Var = tk.StringVar()


label = tk.Label(window, background= "#8ea7ba", text="Modelo de Hodgkin-Huxley", font=('math', 15, 'bold italic'),height=1 ,width=800).pack()

# grafica
fig = Figure(figsize=(6, 5), dpi=50)
ax = fig.add_subplot()
ax.set_xlabel("time (ms)")
ax.set_ylabel("voltage (mV)")
canvas = FigureCanvasTkAgg(fig, window)
canvas.get_tk_widget().place(x=50, y=50)

#Imagen
img = ImageTk.PhotoImage(Image.open("assets/images/Imagen_circuito.png"))
lab = tk.Label(image=img)
lab.place(x=440,y=50)

img2 = ImageTk.PhotoImage(Image.open("assets/images/Imagen_tabla.png"))
lab = tk.Label(image=img2)
lab.place(x=440,y=445)

# Metodos de Solucion
checkRungeKutta2V = tk.IntVar()
checkRungeKutta4V = tk.IntVar()
checkEulerAdelanteV = tk.IntVar()
checkEulerAtrasV = tk.IntVar()
checkEulerModificadoV = tk.IntVar()

metodo = tk.Label(window, text="Método de solución:", font=('math', 9, 'bold italic')).place(x=20, y=320)
checkRungeKutta2 = tk.Checkbutton(window, text="Runge-Kutta 2",font=('math', 9, 'italic'), height=1, width=14, variable=checkRungeKutta2V).place(x=15, y=360)
checkRungeKutta4 = tk.Checkbutton(window, text="Runge-Kutta 4",font=('math', 9, 'italic'), height=1, width=14, variable=checkRungeKutta4V).place(x=15, y=400)
checkEulerAdelante= tk.Checkbutton(window, text="Euler Adelante",font=('math', 9, 'italic'), height=1, width=14, variable=checkEulerAdelanteV).place(x=15, y=440)
checkEulerModificado = tk.Checkbutton(window, text="Euler Modificado",font=('math', 9, 'italic'), height=1, width=15, variable=checkEulerAtrasV).place(x=15, y=480)
checkEulerAtrás = tk.Checkbutton(window, text="Euler Atrás",font=('math', 9, 'italic'), height=1, width=11, variable=checkEulerModificadoV).place(x=15, y=520)

# Variables
check6V = tk.IntVar()
check7V = tk.IntVar()
check8V = tk.IntVar()

variable = tk.Label(window, text="Variables:", font=('math', 9, 'bold italic')).place(x=150, y=320)
check6 = tk.Checkbutton(window, text="V(t)",font=('math', 9, 'italic'), height=1, width=4, variable=check6V).place(x=150, y=350)
check7 = tk.Checkbutton(window, text="gk(t)",font=('math', 9, 'italic'), height=1, width=4, variable=check7V).place(x=245, y=350)
check8 = tk.Checkbutton(window, text="gNa(t)",font=('math', 9, 'italic'), height=1, width=4, variable=check8V).place(x=340, y=350)

# Parametros
parametros = tk.Label(window, text="Parámetros:", font=('math', 9, 'bold italic')).place(x=150, y=380)
Ek = tk.Label(window, text="Ek",font=('math', 9, 'italic')).place(x=155, y=410)
Ek1 = tk.Entry(window, width=8, textvariable= Ek1Var).place(x=185, y=410)
Ek11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=410)
ENa = tk.Label(window, text="ENa",font=('math', 9, 'italic')).place(x=155, y=465)
ENa1 = tk.Entry(window, width=8, textvariable=ENa1Var).place(x=185, y=465)
ENa11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=465)
El = tk.Label(window, text="El",font=('math', 9, 'italic')).place(x=155, y=520)
El1 = tk.Entry(window, width=8, textvariable=El1Var).place(x=185, y=520)
El11 = tk.Label(window, text="mV",font=('math', 9, 'italic')).place(x=230, y=520)
gk = tk.Label(window, text="/gk",font=('math', 9, 'italic')).place(x=260, y=430)
gk1 = tk.Entry(window, width=8, textvariable=gk1Var).place(x=295, y=430)
gk11 = tk.Label(window, text="mS/cm^3",font=('math', 9, 'italic')).place(x=340, y=430)
gNa = tk.Label(window, text="/gNa",font=('math', 9, 'italic')).place(x=260, y=490)
gNa1 = tk.Entry(window, width=8, textvariable=gNa1Var).place(x=295, y=490)
gNa11 = tk.Label(window, text="mS/cm^3",font=('math', 9, 'italic')).place(x=340, y=490)

# Entrada de texto
tiempoSimulacion = tk.Label(window, text="Tiempo de simulacion:",font=('math', 9, 'italic')).place(x=440, y=320)
tiempoSimulacion1 = tk.Entry(window, width=8, textvariable=tiempoSimulacion1Var).place(x=630, y=320)
tiempoSimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=320)
tiempoInicioEstimulacion = tk.Label(window, text="Tiempo de inicio estimulacion:",font=('math', 9, 'italic')).place(x=440, y=340)
tiempoInicioEstimulacion1 = tk.Entry(window, width=8, textvariable=tiempoInicioEstimulacion1Var).place(x=630, y=340)
tiempoInicioEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=340)
tiempoFinEstimulacion = tk.Label(window, text="Tiempo de fin estimulacion:",font=('math', 9, 'italic')).place(x=440, y=360)
tiempoFinEstimulacion1 = tk.Entry(window, width=8, textvariable=tiempoFinEstimulacion1Var).place(x=630, y=360)
tiempoFinEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=360)
ValorEstimulacion = tk.Label(window, text="Valor estimulacion:",font=('math', 9, 'italic')).place(x=440, y=380)
ValorEstimulacion1 = tk.Entry(window, width=8, textvariable=ValorEstimulacion1Var).place(x=630, y=380)
ValorEstimulacion11 = tk.Label(window, text="ms",font=('math', 9, 'italic')).place(x=680, y=380)

# Botones

# ------------------- Variables botones -------------------
def start_simulation():
    """
    Funcion que inicia la simulacion
    """

    print("Iniciando exportacion de datos...")

    # Solucion
    if checkRungeKutta2V.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Runge Kutta 2")

        # Solucion
        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "rungeKutta2" )
        solution_tuple = hh.Main()

        if check6V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[0], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check7V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[1], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check8V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[2], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

    if checkRungeKutta4V.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Runge Kutta 4")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "rungeKutta4")
        solution_tuple = hh.Main()

        if check6V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[0], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check7V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[1], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check8V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[2], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

    if checkEulerAdelanteV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler hacia adelante")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerFor")
        solution_tuple = hh.Main()

        if check6V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[0], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check7V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[1], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check8V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[2], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

    if checkEulerAtrasV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler hacia atras")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerBack")
        solution_tuple = hh.Main()

        if check6V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[0], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check7V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[1], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check8V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[2], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

    if checkEulerModificadoV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler modificado")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerMod")
        solution_tuple = hh.Main()


        if check6V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[0], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check7V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[1], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)

        elif check8V.get() == 1:
            fig = Figure(figsize=(6, 5), dpi=50)
            ax = fig.add_subplot()
            ax.plot(hh.t, solution_tuple[2], label="m")
            ax.set_xlabel("time (ms)")
            ax.set_ylabel("voltage (mV)")
            
            canvas = FigureCanvasTkAgg(fig, window)
            canvas.get_tk_widget().place(x=50, y=50)



def export_to_bin_file_double(V, t):
    """
    Parametros
    V: vector de voltajes
    t: vector de tiempos
    """
    # Exportar a binario
    if check6V.get() == 1:
        print("Exportar a binario")
        with open('pruebaV.bin', 'wb') as f:
            for i in range(len(V)):
                f.write(st.pack('d', V[i]))
        
        with open('pruebaT.bin', 'wb') as f:
            for i in range(len(t)):
                f.write(st.pack('d', t[i]))
    
    elif check7V.get() == 1:
        print("Exportar a binario")
        with open('pruebaGk.bin', 'wb') as f:
            for i in range(len(V)):
                f.write(st.pack('d', V[i]))
        
        with open('pruebaT.bin', 'wb') as f:
            for i in range(len(t)):
                f.write(st.pack('d', t[i]))

    elif check8V.get() == 1:
        print("Exportar a binario")
        with open('pruebaGna.bin', 'wb') as f:
            for i in range(len(V)):
                f.write(st.pack('d', V[i]))
        
        with open('pruebaT.bin', 'wb') as f:
            for i in range(len(t)):
                f.write(st.pack('d', t[i]))


def import_from_bin_file_double():
    """
    Funcion que importa los datos de un archivo binario
    """
    if check6V.get() == 1:
        print("Importar de binario")
        with open('pruebaT.bin', 'rb') as f:
            t = []
            while True:
                data = f.read(8)
                if not data:
                    break
                t.append(st.unpack('d', data)[0])
        
        with open('pruebaV.bin', 'rb') as f:
            V = []
            while True:
                data = f.read(8)
                if not data:
                    break
                V.append(st.unpack('d', data)[0])

        fig = Figure(figsize=(6, 5), dpi=50)
        ax = fig.add_subplot()
        ax.plot(t, V, label="m")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("voltage (mV)")
        
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.get_tk_widget().place(x=50, y=50)

    elif check7V.get() == 1:
        print("Importar de binario")
        with open('pruebaT.bin', 'rb') as f:
            t = []
            while True:
                data = f.read(8)
                if not data:
                    break
                t.append(st.unpack('d', data)[0])
        
        with open('pruebaGk.bin', 'rb') as f:
            V = []
            while True:
                data = f.read(8)
                if not data:
                    break
                V.append(st.unpack('d', data)[0])

        fig = Figure(figsize=(6, 5), dpi=50)
        ax = fig.add_subplot()
        ax.plot(t, V, label="m")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("voltage (mV)")
        
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.get_tk_widget().place(x=50, y=50)

    elif check8V.get() == 1:
        print("Importar de binario")
        with open('pruebaT.bin', 'rb') as f:
            t = []
            while True:
                data = f.read(8)
                if not data:
                    break
                t.append(st.unpack('d', data)[0])
        
        with open('pruebaGna.bin', 'rb') as f:
            V = []
            while True:
                data = f.read(8)
                if not data:
                    break
                V.append(st.unpack('d', data)[0])

        fig = Figure(figsize=(6, 5), dpi=50)
        ax = fig.add_subplot()
        ax.plot(t, V, label="m")
        ax.set_xlabel("time (ms)")
        ax.set_ylabel("voltage (mV)")
        
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.get_tk_widget().place(x=50, y=50)
    
def export():
    """
    Funcion que exporta los datos a un archivo de texto
    """
    print("Iniciando exportacion de datos...")
    
    # Solucion
    if checkRungeKutta2V.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Runge Kutta 2")

        # Solucion
        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "rungeKutta2" )
        solution_tuple = hh.Main()

        
        # Exportar a binario
        if check6V.get() == 1:
            export_to_bin_file_double(solution_tuple[0], hh.t)
        
        elif check7V.get() == 1:
            export_to_bin_file_double(solution_tuple[1], hh.t)

        elif check8V.get() == 1:
            export_to_bin_file_double(solution_tuple[2], hh.t)

    if checkRungeKutta4V.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Runge Kutta 4")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "rungeKutta4")
        solution_tuple = hh.Main()

        # Exportar a binario
        export_to_bin_file_double(solution_tuple[0], hh.t)


    if checkEulerAdelanteV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler hacia adelante")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerFor")
        solution_tuple = hh.Main()
        
        # Exportar a binario
        export_to_bin_file_double(solution_tuple[0], hh.t)


    if checkEulerAtrasV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler hacia atras")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerBack")
        solution_tuple = hh.Main()

        # Exportar a binario
        export_to_bin_file_double(solution_tuple[0], hh.t)


    if checkEulerModificadoV.get() == 1:

        # Variables
        tiempoSimulacion = float(tiempoSimulacion1Var.get())
        tiempoInicioEstimulacion = float(tiempoInicioEstimulacion1Var.get())
        tiempoFinEstimulacion = float(tiempoFinEstimulacion1Var.get())
        valorEstimulacion = float(ValorEstimulacion1Var.get())
        h = 0.01
        cm = 1.0
        gl = 0.3

        # Parametros
        Ek = float(Ek1Var.get())
        ENa = float(ENa1Var.get())
        El = float(El1Var.get())
        gk = float(gk1Var.get())
        gNa = float(gNa1Var.get())
        print("Euler modificado")

        hh = HodgkinHuxley(cm, gNa, gk, gl, ENa, Ek, El, tiempoInicioEstimulacion, tiempoFinEstimulacion, h, "eulerMod")
        solution_tuple = hh.Main()

        # Exportar a binario
        export_to_bin_file_double(solution_tuple[0], hh.t)
    


simular = tk.Button(window,background= "#8ea7ba", text="Simular",font=('math', 9, 'bold italic'), width=13, command=lambda : start_simulation()).place(x=450, y=550)
importar = tk.Button(window,background= "#8ea7ba", text="Importar",font=('math', 9, 'bold italic'), width=13, command=lambda : import_from_bin_file_double()).place(x=560, y=550)
exportar = tk.Button(window,background= "#8ea7ba", text="Exportar",font=('math', 9, 'bold italic'), width=13, command=lambda : export()).place(x=670, y=550)
cargar = tk.Button(window,background= "#8ea7ba", text="Cargar",font=('math', 9, 'bold italic'), width=13).place(x=670, y=410)




window.mainloop()