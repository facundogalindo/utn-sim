import matplotlib.pyplot as plt
import numpy as np

def graficar_histograma(datos, num_intervalos):
    """
    Genera un histograma de frecuencias para los datos generados.

    Parámetros:
    - datos (list): Lista de números generados.
    - num_intervalos (int): Número de intervalos para el histograma.

    Retorna:
    - None: Muestra el gráfico en pantalla.
    """
    plt.figure(figsize=(10, 5))
    
    # Crear histograma y obtener los valores de frecuencias y bordes de los bins
    n, bins, patches = plt.hist(datos, bins=num_intervalos, edgecolor='black', alpha=0.7)

    # Agregar etiquetas con los valores de frecuencia en cada barra
    for count, x in zip(n, bins[:-1]):  # bins[:-1] para excluir el último valor
        plt.text(x + (bins[1] - bins[0]) / 2, count, str(int(count)), 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de Frecuencias")

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# # Ejemplo de uso con datos aleatorios
# datos = np.random.randn(1000)
# graficar_histograma(datos, 15)
