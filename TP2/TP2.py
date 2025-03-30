import random
import numpy as np
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter.filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

datos_pdf = []


def validar_naturales(text):
    # Esta función permite solo la entrada de números (naturales o flotantes)
    return re.match(r'-?\d+\.?\d*', text) is not None

def validar_enteros_flotantes(text):
    # Esta función permite solo la entrada de números (enteros o flotantes)
    return re.match(r'^[0-9]*\.?[0-9]*$', text) is not None

def uniforme(a:int, b:int, rnd:float)->float:
    return round(a + rnd * (b-a), 4)

def exponencial(lamb:float, rnd:float)->float:
    return round((-1 / lamb) * math.log(1 - rnd), 4)

def normal_convolucion(k:int, media:float, desv:float)->float:
    x = 0
    for i in range(k):
        x += random.random()
    return round((((x - k/2) / math.sqrt(k/12)) * desv + media), 4)


def generar_numeros_aleatorios(n, exp=False, media=0, desv=1):
    numeros_aleatorios = []
    for _ in range(n):
        if exp:
            numero = normal_convolucion(12, media, desv)
        else:
            numero = random.random()
        #numero = random.uniform(0, 1)
        numeros_aleatorios.append(numero)

    #print("rnd", numeros_aleatorios)
    return numeros_aleatorios

#Esta función se encarga de generar la distribución de acuerdo a los parámetros ingresados por el usuario.
def generar_distribucion(): 
    distribucion = combo_distribucion.get() #Busca el dato seleccionado en el combo (Uniforme, exponenecial, normal)
    tamaño_muestra = int(entry_tamaño_muestra.get()) #Busca el dato tamaño de muestra solicitado y devuelve un entero
    intervalos = int(combo_intervalos.get()) #Busca el dato cantidad de intervalos solicitado yb devuelve un entero
    global datos_pdf
    if tamaño_muestra > 0 and tamaño_muestra <= 1000000:
        if distribucion == "Uniforme":
            rnd = generar_numeros_aleatorios(tamaño_muestra)
            a = float(entry_a.get()) # Obtiene el valor ingresado por el usuario en un widget de entrada y lo combierte a float
            b = float(entry_b.get())

            datos = []

            for i in rnd:
                x = uniforme(a, b, i)
                datos.append(x)
            print("uniforme", datos)

        elif distribucion == "Exponencial":
            rnd = generar_numeros_aleatorios(tamaño_muestra)
            datos = []

            λ = float(entry_λ.get())

            for i in rnd:
                x = exponencial(λ, i)
                datos.append(x)
            print("EXPONENCIAL", datos)

        elif distribucion == "Normal":

            #rnd1 = generar_numeros_aleatorios(tamaño_muestra)
            #rnd2 = generar_numeros_aleatorios(tamaño_muestra)

            datos = []

            μ = float(entry_μ.get())
            σ = float(entry_σ.get())
            datos = generar_numeros_aleatorios(tamaño_muestra, True, μ, σ)

            print("NORMAL", datos)
            datos_pdf = datos
        histograma_frecuencias(datos, intervalos)
    else:
        messagebox.showinfo(title="Tamaño de muestra", message="Debe ingresar un tamaño de muestra mayor a 0 y menor a 1000000")

def histograma_frecuencias(datos, intervalos): # Define una función llamada histograma_frecuencias que calcula el histograma de frecuencias de los datos generados y muestra tanto el histograma como la tabla de frecuencias en una nueva ventana.
    mostrar_datos(datos)
    frecuencia, intervalo = np.histogram(datos, bins=intervalos)

# Crear una nueva ventana para mostrar el histograma y la tabla de frecuencias
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados")

# Mostrar el histograma
    fig, ax = plt.subplots()
    ax.hist(datos, bins=intervalos, edgecolor='black')
    ax.set_xlabel('Intervalos')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma de Frecuencias')

# Mostrar los intervalos limitantes en el eje x
    ax.set_xticks(intervalo)

# Mostrar la tabla de frecuencias
    tabla_frecuencias = "Tabla de frecuencias:\nIntervalo\tFrecuencia\n"
    for i in range(len(frecuencia)):
        tabla_frecuencias += f"{intervalo[i]:.2f} - {intervalo[i + 1]:.2f}\t{frecuencia[i]}\n"

    txt_tabla_frecuencias = tk.Text(ventana_resultados, height=20, width=40)
    txt_tabla_frecuencias.insert(tk.END, tabla_frecuencias)
    txt_tabla_frecuencias.grid(row=1, column=0)

    plt.show()

# Define una función llamada mostrar_datos que muestra los datos generados en una nueva ventana.
def mostrar_datos(datos): 
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Variables aleatorias según distribución")

    txt_datos = tk.Text(ventana_datos, height=40, width=50)
    txt_datos.pack()

# Insertar los datos en el widget Text
    for dato in datos:
        txt_datos.insert(tk.END, f"{dato}\n")

# Deshabilitar la edición del widget Text
    txt_datos.config(state=tk.DISABLED)

# Botón para guardar los datos en un archivo
    btn_guardar = tk.Button(ventana_datos, text="Guardar", command=lambda: guardar_datos(datos))
    btn_guardar.pack()

#Define una función llamada guardar_datos que permite al usuario guardar las variables generadas en un archivo.
def guardar_datos(datos): 
    archivo_datos = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if archivo_datos is None:
        return
    for dato in datos:
        archivo_datos.write(f"{dato}\n")
    archivo_datos.close()

def guardar_datos_pdf(datos):
    archivo_pdf = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".pdf")
    if archivo_pdf is None:
        return

    c = canvas.Canvas(archivo_pdf.name, pagesize=letter)
    c.drawString(100, 750, "Valores Generados:")
    y = 730
    for dato in datos:
        c.drawString(100, y, str(dato))
        y -= 15

    c.save()
    archivo_pdf.close()
    messagebox.showinfo("Guardado", "Los datos se han guardado en formato PDF correctamente.")

# Desabilita los campos de valores dependiendo que distribucion elija
def actualizar_campos(*args):
    distribucion = combo_distribucion.get()

    entry_a.config(state="disabled")
    entry_b.config(state="disabled")
    entry_λ.config(state="disabled")
    entry_μ.config(state="disabled")
    entry_σ.config(state="disabled")

    if distribucion == "Uniforme":
        entry_a.config(state="normal")
        entry_b.config(state="normal")
    elif distribucion == "Exponencial":
        entry_λ.config(state="normal")
    elif distribucion == "Normal":
        entry_μ.config(state="normal")
        entry_σ.config(state="normal")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Generador de Distribuciones")

# Definir la función de validación para numeros positivos
validar_enteros_flotantes = ventana.register(validar_enteros_flotantes)

# Definir la funcion de validación para numeros positivos y negativos
validar_naturales = ventana.register(validar_naturales)

# Crear widgets
lbl_tamaño_muestra = tk.Label(ventana, text="Tamaño de muestra:")
entry_tamaño_muestra = tk.Entry(ventana, validate="key", validatecommand=(validar_enteros_flotantes, '%S'))

lbl_intervalos = tk.Label(ventana, text="Número de intervalos:")
combo_intervalos = ttk.Combobox(ventana, values=[5, 10, 15], validate="key", validatecommand=(validar_naturales, '%S'))

lbl_distribucion = tk.Label(ventana, text="Distribución:")
combo_distribucion = ttk.Combobox(ventana, values=["Uniforme", "Exponencial", "Normal"], state="readonly")

lbl_a = tk.Label(ventana, text="Valor de a:")
entry_a = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_naturales, '%S'))
lbl_b = tk.Label(ventana, text="Valor de b:")
entry_b = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_naturales, '%S'))

lbl_λ = tk.Label(ventana, text="Valor de λ:")
entry_λ = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_naturales, '%S'))

lbl_μ = tk.Label(ventana, text="Valor de μ:")
entry_μ = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_naturales, '%S'))
lbl_σ = tk.Label(ventana, text="Valor de σ:")
entry_σ = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_enteros_flotantes, '%S'))

btn_generar = tk.Button(ventana, text="Generar Distribución", command=generar_distribucion)

# Asignar función para actualizar campos según selección
combo_distribucion.bind("<<ComboboxSelected>>", actualizar_campos)

# Ubicar widgets en la ventana
lbl_tamaño_muestra.grid(row=0, column=0, padx=5, pady=5)
entry_tamaño_muestra.grid(row=0, column=1, padx=5, pady=5)
lbl_intervalos.grid(row=1, column=0, padx=5, pady=5)
combo_intervalos.grid(row=1, column=1, padx=5, pady=5)
lbl_distribucion.grid(row=2, column=0, padx=5, pady=5)
combo_distribucion.grid(row=2, column=1, padx=5, pady=5)

lbl_a.grid(row=3, column=0, padx=5, pady=5)
entry_a.grid(row=3, column=1, padx=5, pady=5)
lbl_b.grid(row=4, column=0, padx=5, pady=5)
entry_b.grid(row=4, column=1, padx=5, pady=5)

lbl_λ.grid(row=5, column=0, padx=5, pady=5)
entry_λ.grid(row=5, column=1, padx=5, pady=5)

lbl_μ.grid(row=6, column=0, padx=5, pady=5)
entry_μ.grid(row=6, column=1, padx=5, pady=5)
lbl_σ.grid(row=7, column=0, padx=5, pady=5)
entry_σ.grid(row=7, column=1, padx=5, pady=5)

# Botones
btn_generar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
btn_cerrar.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Botón para guardar en PDF
btn_guardar_pdf = tk.Button(ventana, text="Guardar en PDF", command=lambda: guardar_datos_pdf(datos_pdf))
btn_guardar_pdf.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Iniciar la ventana
ventana.mainloop()
