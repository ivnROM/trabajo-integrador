import numpy as np
import matplotlib.pyplot as plt

import sys

sys.setrecursionlimit(200000000)  # Ajusta esto según sea necesario

class Nodo:
    def __init__(self, tiempo, theta, dtheta):
        self.tiempo = tiempo
        self.theta = theta
        self.dtheta = dtheta
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def agregar(self, tiempo, theta, dtheta):
        nuevo_nodo = Nodo(tiempo, theta, dtheta)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def mostrar(self):
        actual = self.cabeza
        while actual is not None:
            print(f"Tiempo: {actual.tiempo}, Theta: {actual.theta}, dTheta: {actual.dtheta}")
            actual = actual.siguiente

def euler(tiempo_inicial, theta_inicial, dtheta_inicial, dt, pasos, C, k, lista_datos=None, tiempos=None, thetas=None, dthetas=None):
    if pasos == 0:
        return tiempos, thetas, dthetas, lista_datos
    
    if lista_datos is None:
        lista_datos = ListaEnlazada()
        tiempos = []
        thetas = []
        dthetas = []

    t = tiempo_inicial
    theta = theta_inicial
    dtheta = dtheta_inicial
    
    tiempos.append(t)
    thetas.append(theta)
    dthetas.append(dtheta)
    
    lista_datos.agregar(t, theta, dtheta)
    
    dtheta_new = dtheta - dt * (C * dtheta + k * theta)
    theta_new = theta + dt * dtheta
    
    return euler(t + dt, theta_new, dtheta_new, dt, pasos - 1, C, k, lista_datos, tiempos, thetas, dthetas)

# Por defecto es 1, que extiende la grafica hasta que T = 10s, si es 10, llega a t = 100s
largo_grafica = 1

# Parámetros de la ecuación diferencial
C = 0.1
k = 1.0

# Parámetros para el método de Euler
tiempo_inicial = 0.0
theta_inicial = 1.0
dtheta_inicial = 0.0
dt = 0.01
pasos = 1000 * largo_grafica

# Resolución de la ecuación diferencial
tiempos, thetas, dthetas, lista_datos = euler(tiempo_inicial, theta_inicial, dtheta_inicial, dt, pasos, C, k)

# Mostrar los datos calculados


def graficar_en_tiempo_real(tiempos, thetas):
    plt.ion()
    fig, ax = plt.subplots()
    linea, = ax.plot(tiempos, thetas, 'b-')
    
    for i in range(len(tiempos)):
        linea.set_xdata(tiempos[:i+1])
        linea.set_ydata(thetas[:i+1])
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)
    
    plt.ioff()
    plt.show()

def solucion_analitica(t, theta_0, dtheta_0, C, k):
    # Aquí se calcularía la solución analítica dependiendo de C y k
    # Esto puede variar si es una ecuación subamortiguada, sobreamortiguada, o críticamente amortiguada
    # Para simplificar, asumamos el caso subamortiguado
    omega0 = np.sqrt(k)
    zeta = C / (2 * np.sqrt(k))
    omega_d = omega0 * np.sqrt(1 - zeta**2)
    
    A = theta_0
    B = (dtheta_0 + zeta * omega0 * theta_0) / omega_d
    
    theta_t = np.exp(-zeta * omega0 * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    return theta_t


def menu_interactivo():
    historial_errores = []
    
    while True:
        print("\nMenú Interactivo")
        print("a. Mostrar grafica")
        print("b. Mostrar los datos calculados")
        print("c. Ingresar una coordenada para el cálculo de error")
        print("d. Mostrar historial de coordenadas ingresadas y sus respectivos cálculos de error")
        print("e. Buscar un dato en la lista ingresando el tiempo")
        print("f. Buscar un dato en la lista ingresando la variable dependiente o su valor más cercano")
        print("g. Limpiar la consola")
        print("h. Graficar Comparación")
        print("i. Salir del programa")
        
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion == 'a':
            graficar_en_tiempo_real(tiempos, thetas)
        elif opcion == 'b':
            lista_datos.mostrar()   
        elif opcion == 'c':
            tiempo = float(input("Ingrese el tiempo: "))
            valor_imagen = float(input("Ingrese el valor de la imagen: "))
            error = calcular_error(tiempo, valor_imagen, lista_datos)
            historial_errores.append((tiempo, valor_imagen, error))
            print(f"Error calculado: {error}")
            graficar_punto(tiempos, thetas, tiempo, valor_imagen)
        elif opcion == 'd':
            for coord in historial_errores:
                print(f"Tiempo: {coord[0]}, Valor Imagen: {coord[1]}, Error: {coord[2]}")
        elif opcion == 'e':
            tiempo = float(input("Ingrese el tiempo a buscar: "))
            buscar_tiempo(tiempo, lista_datos)
        elif opcion == 'f':
            valor = float(input("Ingrese el valor dependiente a buscar: "))
            buscar_valor(valor, lista_datos)
        elif opcion == 'g':
            limpiar_consola()
        elif opcion == 'h':
            # Generar datos de la solución analítica
            theta_analitica = [solucion_analitica(t, theta_inicial, dtheta_inicial, C, k) for t in tiempos]
            # Graficar la comparación
            plt.plot(tiempos, thetas, 'b-', label='Solución Numérica (Euler)')
            plt.plot(tiempos, theta_analitica, 'r--', label='Solución Analítica')
            plt.legend()
            plt.show()
        elif opcion == 'i':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def calcular_error(tiempo, valor_imagen, lista_datos):
    actual = lista_datos.cabeza
    while actual is not None:
        if actual.tiempo >= tiempo:
            break
        actual = actual.siguiente
    if actual is None:
        return float('inf')
    error = abs(actual.theta - valor_imagen)
    return error

def graficar_punto(tiempos, thetas, tiempo, valor_imagen):
    plt.plot(tiempos, thetas, 'b-')
    plt.plot(tiempo, valor_imagen, 'ro')
    plt.show()

def buscar_tiempo(tiempo, lista_datos):
    actual = lista_datos.cabeza
    while actual is not None:
        if actual.tiempo < tiempo:
            actual = actual.siguiente
        if actual.tiempo >= tiempo:
            print(f"Tiempo: {actual.tiempo}, Theta: {actual.theta}, dTheta: {actual.dtheta}")
            return
    print("Tiempo no encontrado en la lista.")

def buscar_valor(valor, lista_datos):
    actual = lista_datos.cabeza
    nodo_mas_cercano = actual
    diferencia_minima = abs(actual.theta - valor)
    actual = actual.siguiente
    
    while actual is not None:
        diferencia_actual = abs(actual.theta - valor)
        if diferencia_actual < diferencia_minima:
            nodo_mas_cercano = actual
            diferencia_minima = diferencia_actual
        actual = actual.siguiente
    
    print(f"Valor más cercano encontrado: Tiempo: {nodo_mas_cercano.tiempo}, Theta: {nodo_mas_cercano.theta}, dTheta: {nodo_mas_cercano.dtheta}")

def limpiar_consola():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

menu_interactivo()
