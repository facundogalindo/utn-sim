import numpy as np

def calcular_aleatorio(X, m, intervalo_cerrado=False):
    if intervalo_cerrado:
        return X/(m - 1)
    else:
        return X/m

def generador_congruente(a, m, x, entero_cerrado=False):
    """
    Genera un número pseudo-aleatorio utilizando un generador congruente.

    Parámetros:
    - a (int): Constante o multiplicador.
    - m (int): Módulo.
    - x (int): Semilla.

    Retorna:
    - int: El siguiente número pseudo-aleatorio en la secuencia.
    """
    X = (a*x) % m
    r = calcular_aleatorio(X, m, entero_cerrado)
    return r

def distribucion_exponencial(lamb, r):
    """
    Genera una variable aleatoria con distribución exponencial.

    Parámetros:
    - lamb (float): Tasa de ocurrencia de eventos.
    - r (float): Número aleatorio en el intervalo [0, 1).

    Retorna:
    - float: Variable aleatoria generada.
    """
    if lamb > 0:
        return -1 / lamb * np.log(1 - r)
    return None

def distribucion_normal(media, desviacion, r1, r2):
    """
    Genera una variable aleatoria con distribución normal.

    Parámetros:
    - media (float): Media de la distribución.
    - desviacion (float): Desviación estándar de la distribución.
    - r1, r2 (float): Números aleatorios en el intervalo [0, 1).

    Retorna:
    - float: Variable aleatoria generada.
    """
    if desviacion >= 0:
        z = np.sqrt(-2 * np.log(1 - r1)) * np.cos(2 * np.pi * r2)
        return float(media + z * desviacion)
    return None

def distribucion_uniforme(a, b, r):
    """
    Genera una variable aleatoria con distribución uniforme.

    Parámetros:
    - a (float): Límite inferior.
    - b (float): Límite superior.
    - r (float): Número aleatorio en el intervalo [0, 1).

    Retorna:
    - float: Variable aleatoria generada.
    """
    if b >= a:
        return a + r * (b - a)
    return None
