import func_finan
import matplotlib.pyplot as plt
import numpy as np

def verificar_paridad_put_call(S, K, r, T, precio_call, precio_put):
    lado_izquierdo = precio_call - precio_put
    lado_derecho = S - K * np.exp(-r * T)
    return abs(lado_izquierdo - lado_derecho)

print("Ingrese '1' si desea usar el método de Black & Scholes\nIngrese '2' si desea desea usar el metodo binomial y conoce la volatilidad\nIngrese '3' si desea desea usar el metodo binomial y no conoce la volatilidad")
modelo = str(input("Ingrese la opción deseada: "))

def solicitar_datos_entrada():
    tipo_opcion = input("Ingrese 'C' para una opción de compra (call) o 'P' para una opción de venta (put): ").upper()
    tipo_nombre = 1 if tipo_opcion == 'C' else -1
    S = float(input("s0: Ingrese el precio actual de la acción: "))
    K = float(input("k: Ingrese el precio de ejercicio de la opción: "))
    r = float(input("r: Ingrese la tasa de interés libre de riesgo en términos porcentuales: ")) / 100
    T = float(input("T: Ingrese el tiempo hasta el vencimiento en meses: ")) / 12
    return tipo_nombre, S, K, r, T,tipo_opcion


tipo = input("Ingrese 'E' si desea calcular una opción de Europea o 'A' para una opción Americana: ").upper()

tipo_nombre, S, K, r, T,tipo_opcion = solicitar_datos_entrada()
lista=[]

if modelo=='1':

    sigma = float(input("sigma: Ingrese el valor de sigma (desviación estándar): "))/100

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


elif modelo=='2' or modelo=='3':
    
    if modelo == '2':
        print("")
        n = int(input("n: Ingrese el número de pasos temporales en el árbol binomial: "))
        sigma = float(input("sigma: Ingrese el valor de sigma (desviación estándar): "))/100
        
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
        print("")
        n = int(input("n: Ingrese el número de pasos temporales en el árbol binomial: "))
        u = float(input("u: Ingrese el factor de aumento: "))
        d = float(input("d: Ingrese el factor de disminución d: "))

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

        sigma = float(input("sigma: Ingrese el valor de sigma (desviación estándar): "))/100

    tipo_nombre = 1 if tipo_opcion == 'C' else -1

    tipo_nombre=int(tipo_nombre)

    #print(f"{tipo_nombre}, {S}, {K}, {T}, {r},{sigma}")


    precio_opcion = func_finan.black_scholes(tipo_nombre, S, K, T, r, sigma)
    # Crea una lista de valores x (por ejemplo, un rango de valores)
    valores_x = range(n)
    valores_y = [precio_opcion] * len(valores_x)

    print(f"El precio de la opción según Black-Scholes es: {precio_opcion:.6f}")
    plt.plot(valores_x, valores_y, label=f'Precio de la opción usando BS = {precio_opcion:.6f}')
    plt.legend()
    plt.show()

else:
    print("Ingresaste una opción incorrecta")
