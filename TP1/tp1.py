
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from generadores import distribucion_uniforme
from generadores import distribucion_exponencial
from generadores import distribucion_normal
from generadores import generador_congruente
from graficos import graficar_histograma

class AplicacionSimulacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Variables Aleatorias")

        # Tamaño de muestra
        ttk.Label(root, text="Tamaño de Muestra:").grid(row=0, column=0, padx=10, pady=5)
        self.entrada_muestra = ttk.Entry(root)
        self.entrada_muestra.grid(row=0, column=1, padx=10, pady=5)

        # Selección de distribución
        ttk.Label(root, text="Distribución:").grid(row=1, column=0, padx=10, pady=5)
        self.opciones_distribucion = ["Uniforme", "Exponencial", "Normal"]
        self.combo_distribucion = ttk.Combobox(root, values=self.opciones_distribucion, state="readonly")
        self.combo_distribucion.grid(row=1, column=1, padx=10, pady=5)
        self.combo_distribucion.bind("<<ComboboxSelected>>", self.mostrar_parametros)

        # Parámetros de distribución
        self.frame_parametros = ttk.Frame(root)
        self.frame_parametros.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para generar números
        self.boton_generar = ttk.Button(root, text="Generar Números", command=self.iniciar_generacion_numeros)
        self.boton_generar.grid(row=3, column=0, columnspan=2, pady=10)

        # Selección de intervalos del histograma
        ttk.Label(root, text="Intervalos:").grid(row=4, column=0, padx=10, pady=5)
        self.combo_intervalos = ttk.Combobox(root, values=[10, 15, 20, 30], state="readonly")
        self.combo_intervalos.grid(row=4, column=1, padx=10, pady=5)

        # Botón para graficar histograma
        self.boton_graficar = ttk.Button(root, text="Graficar Histograma", command=self.graficar)
        self.boton_graficar.config(state="disabled")
        self.boton_graficar.grid(row=5, column=0, columnspan=2, pady=10)

        self.datos_generados = []

    def mostrar_parametros(self, event):
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()

        seleccion = self.combo_distribucion.get()
        
        if seleccion == "Uniforme":
            ttk.Label(self.frame_parametros, text="a:").grid(row=0, column=0)
            self.entrada_a = ttk.Entry(self.frame_parametros)
            self.entrada_a.grid(row=0, column=1)

            ttk.Label(self.frame_parametros, text="b:").grid(row=1, column=0)
            self.entrada_b = ttk.Entry(self.frame_parametros)
            self.entrada_b.grid(row=1, column=1)

        elif seleccion == "Exponencial":
            ttk.Label(self.frame_parametros, text="Lambda:").grid(row=0, column=0)
            self.entrada_lambda = ttk.Entry(self.frame_parametros)
            self.entrada_lambda.grid(row=0, column=1)

        elif seleccion == "Normal":
            ttk.Label(self.frame_parametros, text="Media:").grid(row=0, column=0)
            self.entrada_media = ttk.Entry(self.frame_parametros)
            self.entrada_media.grid(row=0, column=1)

            ttk.Label(self.frame_parametros, text="Desviación:").grid(row=1, column=0)
            self.entrada_desviacion = ttk.Entry(self.frame_parametros)
            self.entrada_desviacion.grid(row=1, column=1)

    def iniciar_generacion_numeros(self):
        # Disable the "Graficar Histograma" button while generating numbers
        self.boton_graficar.config(state="disabled")
        self.generar_numeros()

    def generar_numeros(self):
        print('generar_numeros()')
        try:
            tamano_muestra = int(self.entrada_muestra.get())
            if tamano_muestra > 1000000:
                messagebox.showerror("Error", "El tamaño máximo es 1,000,000.")
                return

            seleccion = self.combo_distribucion.get()
            self.datos_generados = []
            if seleccion == 'Normal':
                self.generar_distribucion_normal(tamano_muestra)
            elif seleccion == 'Uniforme':
                pass
            elif seleccion == 'Exponencial':
                pass

            # for _ in range(tamano_muestra):
            #     r = np.random.rand()

            #     if seleccion == "Uniforme":
            #         a = float(self.entrada_a.get())
            #         b = float(self.entrada_b.get())
            #         self.datos_generados.append(distribucion_uniforme(a, b, r))

            #     elif seleccion == "Exponencial":
            #         lamb = float(self.entrada_lambda.get())
            #         self.datos_generados.append(distribucion_exponencial(lamb, r))

            #     elif seleccion == "Normal":
            #         r2 = np.random.rand()
            #         media = float(self.entrada_media.get())
            #         desviacion = float(self.entrada_desviacion.get())
            #         self.datos_generados.append(distribucion_normal(media, desviacion, r, r2))

            # Once the numbers are generated, enable the "Graficar Histograma" button
            self.boton_graficar.config(state="normal")

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos.")

    def generar_distribucion_normal(self, tamano_muestra):
        media = float(self.entrada_media.get())
        desviacion = float(self.entrada_desviacion.get())
        intervalo =  int(self.combo_intervalos.get())

        for i in range(tamano_muestra):
            r1 = generador_congruente(1, 50, i)
            r2 = generador_congruente(1, 50, i)
            x = distribucion_normal(media, desviacion, r1, r2)
            self.datos_generados.append(x)

    def graficar(self):
        graficar_histograma(self.datos_generados, int(self.combo_intervalos.get()))

root = tk.Tk()
app = AplicacionSimulacion(root)
root.mainloop()

