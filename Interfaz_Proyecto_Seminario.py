import func_finan
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import math

# Definiciones de funciones 
def verificar_paridad_put_call(S, K, r, T, precio_call, precio_put):
    lado_izquierdo = precio_call - precio_put
    lado_derecho = S - K * np.exp(-r * T)
    return abs(lado_izquierdo - lado_derecho)

def ejecutar_modelo():
    tipo = tipo_opcion_europea_americana_var.get().upper()
    modelo = modelo_var.get()
    tipo_nombre, S, K, r, T, tipo_opcion = solicitar_datos_entrada()
    lista = []

    if modelo == '1':
        sigma = float(sigma_var.get()) / 100
        precio_opcion = func_finan.black_scholes(tipo_nombre, S, K, T, r, sigma)
        valores_x = range(100)
        valores_y = [precio_opcion] * len(valores_x)

        # Genera el gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(valores_x, valores_y, label=f'Precio de la opción usando BS = {precio_opcion:.6f}')
        plt.xlabel('Número de pasos temporales', fontsize=12)
        plt.ylabel('Precio de la opción', fontsize=12)
        plt.title('Gráfico del modelo de BS', fontsize=16)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

        print(f"El precio de la opción según Black-Scholes es: {precio_opcion:.6f}")

        precio_call = func_finan.black_scholes(1, S, K, T, r, sigma)  # Precio de la opción de compra
        precio_put = func_finan.black_scholes(-1, S, K, T, r, sigma)  # Precio de la opción de venta
        
        # Verificar la paridad put-call
        diferencia = verificar_paridad_put_call(S, K, r, T, precio_call, precio_put)
        print(f"Diferencia en la paridad put-call: {diferencia:.6f}")

        un_umbral_aceptable=0.01

        if diferencia < un_umbral_aceptable:  # Define un umbral aceptable, por ejemplo, 0.01
            print("La paridad put-call se cumple dentro del umbral aceptable.")
        else:
            print("La paridad put-call no se cumple dentro del umbral aceptable.")

    elif modelo == '2' or modelo == '3':
        n = int(n_var.get())

        if modelo == '2':
            sigma = float(sigma_var.get()) / 100
            #n = int(input("n: Ingrese el número de pasos temporales en el árbol binomial: "))
            #sigma = float(input("sigma: Ingrese el valor de sigma (desviación estándar): "))/100
            
            if tipo =='E': #Europeas

                for i in range(1,n+1):
                    precio_opcion = func_finan.precio_opcion_europea_sigma(tipo_nombre, S, K, r, T,i, sigma)
                    lista.append(precio_opcion)
                ultimo_precio = lista[-1]
                tipo_nombre = 'Compra' if tipo_opcion == 'C' else 'Venta'
                print(f"Precio de Opción Europea de {tipo_nombre}: {ultimo_precio:.6f}")

            elif tipo == 'A':       #Americanas

                print("Hola")

                for i in range(1,n+1):
                    precio_opcion = func_finan.precio_opcion_americana_sigma(S, K, r, T,i,tipo_nombre,  sigma)
                    lista.append(precio_opcion)
                ultimo_precio = lista[-1]
                tipo_nombre = 'Compra' if tipo_opcion == 'C' else 'Venta'
                print(f"Precio de Opción Americana de {tipo_nombre}: {ultimo_precio:.6f}")

            else:
                print('La opción que ingresante es incorrecta')
            
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, n + 1), lista, marker='o', linestyle='-', color='b', label=f'Precio de la opción usando Binomial= {ultimo_precio:.6f}')
            plt.title('Evolución del precio de la acción', fontsize=16)
            plt.xlabel('Número de pasos temporales', fontsize=12)
            plt.ylabel('Precio de la opción', fontsize=12)
            plt.legend()
            plt.grid(True)



        else:
            u = float(u_var.get())
            d = float(d_var.get())

            if tipo =='E': #Europeas

                for i in range(1,n+1):
                    precio_opcion = func_finan.precio_opcion_europea(tipo_nombre, S, K, r, T,i,u,d)
                    lista.append(precio_opcion)
                ultimo_precio = lista[-1]
                tipo_nombre = 'Compra' if tipo_opcion == 'C' else 'Venta'
                print(f"Precio de Opción Europea de {tipo_nombre}: {ultimo_precio:.6f}")

            elif tipo == 'A':       #Americanas

                for i in range(1,n+1):
                    precio_opcion = func_finan.precio_opcion_americana(S, K, r, T,i,u,d,tipo_nombre)
                    lista.append(precio_opcion)
                ultimo_precio = lista[-1]
                tipo_nombre = 'Compra' if tipo_opcion == 'C' else 'Venta'
                print(f"Precio de Opción Americana de {tipo_nombre}: {ultimo_precio:.6f}")

            else:
                print('La opción que ingresante es incorrecta')
            
            plt.figure(figsize=(10, 6))
            plt.plot(range(1, n + 1), lista, marker='o', linestyle='-', color='b',  label=f'Precio de la opción usando Binomial= {ultimo_precio:.6f}')
            plt.title('Evolución del precio de la acción', fontsize=16)
            plt.xlabel('Número de pasos temporales', fontsize=12)
            plt.ylabel('Precio de la opción', fontsize=12)
            plt.legend()
            plt.grid(True)

            #sigma = float(input("sigma: Ingrese el valor de sigma (desviación estándar): "))/100
            sigma = ((n/T)**(1/2))*math.log(u)
        # Generación y visualización de gráficos

        tipo_nombre = 1 if tipo_opcion == 'C' else -1

        tipo_nombre=int(tipo_nombre)

        #print(f"{tipo_nombre}, {S}, {K}, {T}, {r},{sigma}")


        precio_opcion = func_finan.black_scholes(tipo_nombre, S, K, T, r, sigma)
        # Crea una lista de valores x (por ejemplo, un rango de valores)

        #Ciclo para calcular la diferencia
        for i in range(n):
            diferencia=abs(precio_opcion-lista[i])
            if diferencia <= 0.01:
                print(f"El numero de pasos para obtener una diferencia  menor o igual a 0.01 es: {i+1}")
                print(f"El valor de la diferencia es de: {diferencia}")
                break


        #Bloque para calcular las diferencias
        valores_x = range(n)
        valores_y = [precio_opcion] * len(valores_x)

        print(f"El precio de la opción según Black-Scholes es: {precio_opcion:.6f}")
        plt.plot(valores_x, valores_y, label=f'Precio de la opción usando BS = {precio_opcion:.6f}')
        plt.legend()
        plt.show()

    else:
        messagebox.showerror("Error", "Opción de modelo incorrecta")

def solicitar_datos_entrada():
    tipo_opcion = tipo_opcion_var.get().upper()
    tipo_nombre = 1 if tipo_opcion == 'C' else -1
    S = float(precio_accion_var.get())
    K = float(precio_ejercicio_var.get())
    r = float(tasa_interes_var.get()) / 100
    T = float(tiempo_var.get()) / 12
    return tipo_nombre, S, K, r, T, tipo_opcion

# Creación de la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Opciones Financieras")

# Variables para almacenar los datos de entrada
tipo_opcion_var = tk.StringVar()
precio_accion_var = tk.StringVar()
precio_ejercicio_var = tk.StringVar()
tasa_interes_var = tk.StringVar()
tiempo_var = tk.StringVar()
tipo_opcion_europea_americana_var = tk.StringVar()
modelo_var = tk.StringVar()
sigma_var = tk.StringVar()
n_var = tk.StringVar()
u_var = tk.StringVar()
d_var = tk.StringVar()


# Widgets para la entrada de datos y etiquetas

# Modelo a utilizar
ttk.Label(ventana, text="Modelo (1: Black-Scholes, 2: Binomial con volatilidad, 3: Binomial sin volatilidad):").grid(column=0, row=0)
ttk.Entry(ventana, textvariable=modelo_var).grid(column=1, row=0)

# Tipo de opción (Europea/Americana)
ttk.Label(ventana, text="Tipo de opción (E/A):").grid(column=0, row=1)
ttk.Entry(ventana, textvariable=tipo_opcion_europea_americana_var).grid(column=1, row=1)

# Tipo de opción (Compra/Venta)
ttk.Label(ventana, text="Tipo de Opción (C/P):").grid(column=0, row=2)
ttk.Entry(ventana, textvariable=tipo_opcion_var).grid(column=1, row=2)

# Precio actual de la acción
ttk.Label(ventana, text="Precio actual de la acción:").grid(column=0, row=3)
ttk.Entry(ventana, textvariable=precio_accion_var).grid(column=1, row=3)

# Precio de ejercicio de la opción
ttk.Label(ventana, text="Precio de ejercicio de la opción:").grid(column=0, row=4)
ttk.Entry(ventana, textvariable=precio_ejercicio_var).grid(column=1, row=4)

# Tasa de interés libre de riesgo
ttk.Label(ventana, text="Tasa de interés libre de riesgo (%):").grid(column=0, row=5)
ttk.Entry(ventana, textvariable=tasa_interes_var).grid(column=1, row=5)

# Tiempo hasta el vencimiento
ttk.Label(ventana, text="Tiempo hasta el vencimiento (meses):").grid(column=0, row=6)
ttk.Entry(ventana, textvariable=tiempo_var).grid(column=1, row=6)


# Parámetros adicionales para modelos específicos (si se requieren)
# Sigma (desviación estándar)
ttk.Label(ventana, text="Sigma (desviación estándar) (%):").grid(column=0, row=7)
ttk.Entry(ventana, textvariable=sigma_var).grid(column=1, row=7)

# Número de pasos para el modelo Binomial
ttk.Label(ventana, text="Número de pasos (modelo Binomial):").grid(column=0, row=8)
ttk.Entry(ventana, textvariable=n_var).grid(column=1, row=8)

# Factores de aumento y disminución para el modelo Binomial sin volatilidad conocida
ttk.Label(ventana, text="Factor de aumento (u) (modelo Binomial):").grid(column=0, row=9)
ttk.Entry(ventana, textvariable=u_var).grid(column=1, row=9)

ttk.Label(ventana, text="Factor de disminución (d) (modelo Binomial):").grid(column=0, row=10)
ttk.Entry(ventana, textvariable=d_var).grid(column=1, row=10)


# Botón para ejecutar el modelo
ttk.Button(ventana, text="Calcular", command=ejecutar_modelo).grid(column=1, row=11)

# Inicializar la ventana
ventana.mainloop()

