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



def validar_enteros_flotantes(texto):
    texto = texto.replace(',', '.')  # permite coma como separador decimal
    pattern = r'^[+-]?(\d+(\.\d*)?|\.\d+)$'
    return bool(re.match(pattern, texto))

#Permite valores positivos , negativos y con decimales separados por punto ( ejemplo: 1.2)
def validar_parametro(texto):
    # Permitir campo vacío
    if texto == "":
        return True

    # Permitir solo el signo como entrada válida
    if texto == '-':
        return True
    #pattern = r'^-?(\d+(\.\d*)?|\.\d+)$'
    pattern = r'^-?(?:\d+(?:\.\d+)?|\.\d+)$'
    return bool(re.match(pattern, texto))


def validar_naturales_flotantes(texto):
    texto = texto.replace(',', '.')  # permite coma como separador decimal
    pattern = r'^[+-]?(\d+(\.\d*)?|\.\d+)$'
    return bool(re.fullmatch(pattern, texto))

def validar_naturales(text):
    # Esta función permite solo la entrada de números (enteros)
    pattern = r'^[0-9]*$'
    return re.match(pattern, text) is not None

# Sub Métodos para generar los aleatorios de cada una de la distribuciones
def uniforme(a:int, b:int, rnd:float) -> float:
    return round(a + rnd * (b-a), 4)

def exponencial(lamb:float, rnd:float) -> float:
    return round((-1 / lamb) * math.log(1 - rnd), 4)

def normal_convolucion(k:int, media:float, desv:float)->float:
    x = 0
    for _ in range(k):
        x += random.random()
    return round((((x - k/2) / math.sqrt(k/12)) * desv + media), 4)

# Método para generar los aletorios rnd [0,1]
def generar_numeros_aleatorios(n: int) -> list:
    numeros_aleatorios = []
    for _ in range(n):
        numero = random.random()
        numeros_aleatorios.append(numero)
    return numeros_aleatorios

#Esta función se encarga de generar la distribución de acuerdo a los parámetros ingresados por el usuario.
def generar_distribucion():
    if entry_tamaño_muestra.get() != "" and int(entry_tamaño_muestra.get()) > 0 and int(entry_tamaño_muestra.get()) <= 1000000:
        datos = []
        distribucion = combo_distribucion.get() #Busca el dato seleccionado en el combo (Uniforme, exponenecial, normal)
        tamaño_muestra = int(entry_tamaño_muestra.get())  #Busca el dato tamaño de muestra solicitado y devuelve un entero
        intervalos = int(combo_intervalos.get()) #Busca el dato cantidad de intervalos solicitado yb devuelve un entero
    
        genera_distribucion = False
        if distribucion == "Uniforme":
            if (entry_a.get() and entry_b.get()) != "" and (entry_a.get() and entry_b.get() != "-"):

                aleatorios = generar_numeros_aleatorios(tamaño_muestra)

                a = float(entry_a.get()) 
                b = float(entry_b.get())
                
                
                if a < b:
                    for rnd in aleatorios:
                        x = uniforme(a, b, rnd)
                        datos.append(x)
                    genera_distribucion = True
                else:
                    messagebox.showinfo(title="Parámetros dist. uniforme", message="El parametro A debe ser menor al parametro B")

            else:
                messagebox.showinfo(title="Parámetros dist. uniforme", message="Debe ingresar valores en los parámetros de la distribución")
        elif distribucion == "Exponencial":
            if entry_λ.get() != "":
                aleatorios = generar_numeros_aleatorios(tamaño_muestra)
                λ = float(entry_λ.get())
                if λ > 0:
                    for rnd in aleatorios:
                        x = exponencial(λ, rnd)
                        datos.append(x)
                    genera_distribucion = True
                else:
                    messagebox.showinfo(title="Parámetros dist. exponencial", message="El parametro λ debe ser mayor a 0")
                    
            else:
                messagebox.showinfo(title="Parámetros dist. exponencial", message="Debe ingresar valores en los parámetros de la distribución")
        elif distribucion == "Normal":
            if (entry_μ.get() and entry_σ.get()) != "":
                μ = float(entry_μ.get())
                σ = float(entry_σ.get())

                for _ in range(tamaño_muestra):
                    x = normal_convolucion(12, μ, σ)
                    datos.append(x)
                genera_distribucion = True
            else:
                messagebox.showinfo(title="Parámetros dist. Normal", message="Debe ingresar valores en los parámetros de la distribución")
        if genera_distribucion:
            histograma_frecuencias(datos, intervalos)
    else:
        messagebox.showinfo(title="Tamaño de muestra", message="Debe ingresar un tamaño de muestra entre 1 y 1,000,000")

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
ventana.geometry('500x500')
ventana.update_idletasks()
ventana.title("Generador de Distribuciones")

# Definir la función de validación para numeros positivos
validar_enteros_flotantes = ventana.register(validar_enteros_flotantes)

# Definir la funcion de validación para numeros positivos y negativos
validar_naturales_flotantes = ventana.register(validar_naturales_flotantes)

# Definir la funcion de validación para numeros enteros
validar_naturales = ventana.register(validar_naturales)

# Definir la funcion de validación para numeros negativos de mu
validar_parametro = ventana.register(validar_parametro)

# Crear widgets
lbl_tamaño_muestra = tk.Label(ventana, text="Tamaño de muestra:")
entry_tamaño_muestra = tk.Entry(ventana, validate="key", validatecommand=(validar_naturales, '%S'))

lbl_intervalos = tk.Label(ventana, text="Número de intervalos:")
combo_intervalos = ttk.Combobox(ventana, values=[10, 15, 20,30], validate="key", validatecommand=(validar_naturales, '%S'), state="readonly")
#Seteo valor por defecto al combo 
combo_intervalos.set(10)

lbl_distribucion = tk.Label(ventana, text="Distribución:")
combo_distribucion = ttk.Combobox(ventana, validate="key", values=["Uniforme", "Exponencial", "Normal"], state=["readonly"])
#Seteo valor por defecto al combo 
combo_distribucion.set("Uniforme")


lbl_a = tk.Label(ventana, text="Valor de a:")
entry_a = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_parametro, '%P'))
lbl_b = tk.Label(ventana, text="Valor de b:")
entry_b = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_parametro, '%P'))

lbl_λ = tk.Label(ventana, text="Valor de λ:")
entry_λ = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_enteros_flotantes, '%S'))

lbl_μ = tk.Label(ventana, text="Valor de μ:")
entry_μ = tk.Entry(ventana, state="disabled", validate="key", validatecommand=(validar_parametro, '%P'))
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
btn_generar.grid(row=8, column=1, columnspan=2, padx=5, pady=5)
btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
btn_cerrar.grid(row=9, column=1, columnspan=2, padx=5, pady=5)


# Iniciar la ventana
ventana.mainloop()