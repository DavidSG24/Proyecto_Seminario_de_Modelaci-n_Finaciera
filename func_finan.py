import numpy as np
import math
from scipy.stats import norm

def black_scholes(tipo_opcion: int, S: str, K: str, T:str, r: str, sigma: str) -> str:
    """
    Calcula el precio de la opción utilizando el modelo Black-Scholes.

    Parámetros:
    - tipo_opcion: 'call' para opción de compra, 'put' para opción de venta
    - S: Precio actual de la acción
    - K: Precio de ejercicio de la opción
    - T: Tiempo hasta el vencimiento (en años)
    - r: Tasa de interés libre de riesgo
    - sigma: Volatilidad de la acción subyacente

    Retorna:
    - Precio de la opción
    """

    d1 = (math.log(S / K) + (r + (sigma**2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if tipo_opcion == 1:
        precio_opcion = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif tipo_opcion == -1:
        precio_opcion = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Tipo de opción no válido. Use 'call' o 'put'.")

    return precio_opcion


def precio_opcion_americana(S:float, K:float, r:float, T:float, n:int, u:float, d:float, tipo_nombre:float)->float:

    """
    Esta es la funcion que pemite calcular el valor de una opcion americana, de acuerdo con la soicitu del usuario.


    Parámetros:
    - S: Precio actual de la acción
    - K: Precio de ejercicio de la opción
    - r: Tasa de interés libre de riesgo
    - T: Tiempo hasta el vencimiento (en años)
    - n: Número de pasos en el modelo binomial
    - u: Factor de subida en el modelo binomial
    - d: Factor de bajada en el modelo binomial
    - tipo_opcion: '1' para opción de compra, '-1' para opción de venta
    """
    
    dt = T / n
    p = (np.exp(r * dt) - d) / (u - d)

    # Inicializar la matriz de valores de la opción
    valores_opcion = np.zeros((n + 1, n + 1))

    # Calcular los valores de la opción al vencimiento
    for i in range(n + 1):
        if tipo_nombre == 1:
            valores_opcion[n, i] = max(0, S * (u ** i) * (d ** (n - i)) - K)
        else:
            valores_opcion[n, i] = max(0, K - S * (u ** i) * (d ** (n - i)))

    # Calcular los valores de la opción en cada nodo considerando el ejercicio temprano
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            if tipo_nombre == 1:
                valores_opcion[j, i] = max(
                    (S * (u ** i) * (d ** (j - i)) - K),
                    np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
                )
            else:
                valores_opcion[j, i] = max((K - S * (u ** i) * (d ** (j - i))),
                    np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
                )

    return valores_opcion[0, 0]


def precio_opcion_europea(tipo_opcion: int, S:float, K:float, r:float, T:float, n: int, u:float, d:float)->float:

    """Calcula el precio de una opción europea, ya sea de compra (call) o venta (put), dados varios parámetros financieros. 
    Los resultados se imprimen en una matriz que muestra los valores de la opción en diferentes pasos temporales. Luego, el precio final de la opción se imprime en la consola. 
    

    Parámetros:
    - tipo_opcion: '1' para opción de compra, '-1' para opción de venta
    - S: Precio actual de la acción
    - K: Precio de ejercicio de la opción
    - r: Tasa de interés libre de riesgo
    - T: Tiempo hasta el vencimiento (en años)
    - n: Número de pasos en el modelo binomial
    - u: Factor de subida en el modelo binomial
    - d: Factor de bajada en el modelo binomial
    """

    
    dt = T / n
    p = (np.exp(r * dt) - d) / (u - d)

    # Inicializar los valores de la opción en la madurez según el pago de la opción en cada nodo.
    valores_opcion = np.zeros((n + 1, n + 1))
    #print(valores_opcion)
    for i in range(n + 1):
        #print(valores_opcion[n, i])
        valores_opcion[n, i] = max(0, tipo_opcion * (S * (u ** i) * (d ** (n - i)) - K))
        #print(valores_opcion[n, i])

    
    #print(valores_opcion)

    # Calcular los valores de la opción en cada nodo del árbol, retrocediendo en el tiempo.
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            # Utilizar la tasa de interés libre de riesgo para descontar los valores futuros de la opción.
            valores_opcion[j, i] = np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
            #print(valores_opcion[j, i])
     # Imprimir la matriz de valores de la opción para visualizar la evolución de los valores en el árbol.
    #print(valores_opcion)

    #
    
    # Devolver el valor calculado de la opción en el nodo inicial (raíz del árbol).
    return valores_opcion[0, 0]


'''desciación  estandar'''

def precio_opcion_europea_sigma(tipo_opcion: int, S:float, K:float, r:float, T:float, n: int, sigma: float)->float:

    """Calcula el precio de una opción europea, ya sea de compra (call) o venta (put), dados varios parámetros financieros. 
    Los resultados se imprimen en una matriz que muestra los valores de la opción en diferentes pasos temporales. 
        
        Parámetros:
    - tipo_opcion: '1' para opción de compra, '-1' para opción de venta
    - S: Precio actual de la acción
    - K: Precio de ejercicio de la opción
    - r: Tasa de interés libre de riesgo
    - T: Tiempo hasta el vencimiento (en años)
    - n: Número de pasos en el modelo binomial
    - sigma: Valor de la desviación estándar

       """
    
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Inicializar los valores de la opción en la madurez según el pago de la opción en cada nodo.
    valores_opcion = np.zeros((n + 1, n + 1))
    #print(valores_opcion)
    for i in range(n + 1):
        #print(valores_opcion[n, i])
        valores_opcion[n, i] = max(0, tipo_opcion * (S * (u ** i) * (d ** (n - i)) - K))
        #print(valores_opcion[n, i])

    
    #print(valores_opcion)

    # Calcular los valores de la opción en cada nodo del árbol, retrocediendo en el tiempo.
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            # Utilizar la tasa de interés libre de riesgo para descontar los valores futuros de la opción.
            valores_opcion[j, i] = np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
            #print(valores_opcion[j, i])
     # Imprimir la matriz de valores de la opción para visualizar la evolución de los valores en el árbol.
    #print(valores_opcion)

    #
    '''print("Option Values Matrix:")
    for row in valores_opcion:
        print(row)'''
    
    # Devolver el valor calculado de la opción en el nodo inicial (raíz del árbol).
    return valores_opcion[0, 0]

def precio_opcion_americana_sigma(S:float, K:float, r:float, T:float, n:int, tipo_nombre:float, sigma: float)->float:
    

    """
    Esta es la funcion que pemite calcular el valor de una opcion americana, de acuerdo con la soicitud del usuario.

    Parámetros:
    - S: Precio actual de la acción
    - K: Precio de ejercicio de la opción
    - r: Tasa de interés libre de riesgo
    - T: Tiempo hasta el vencimiento (en años)
    - n: Número de pasos en el modelo binomial
    - tipo_nombre: '1' para opción de compra, '-1' para opción de venta
    - sigma: Valor de la desviación estándar
    """
    
    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Inicializar la matriz de valores de la opción
    valores_opcion = np.zeros((n + 1, n + 1))

    # Calcular los valores de la opción al vencimiento
    for i in range(n + 1):
        if tipo_nombre == 1:
            valores_opcion[n, i] = max(0, S * (u ** i) * (d ** (n - i)) - K)
        else:
            valores_opcion[n, i] = max(0, K - S * (u ** i) * (d ** (n - i)))

    # Calcular los valores de la opción en cada nodo considerando el ejercicio temprano
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            if tipo_nombre == 1:
                valores_opcion[j, i] = max(
                    (S * (u ** i) * (d ** (j - i)) - K),
                    np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
                )
            else:
                valores_opcion[j, i] = max(
                    (K - S * (u ** i) * (d ** (j - i))),
                    np.exp(-r * dt) * (p * valores_opcion[j + 1, i + 1] + (1 - p) * valores_opcion[j + 1, i])
                )

    return valores_opcion[0, 0]
