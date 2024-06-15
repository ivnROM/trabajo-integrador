import numpy as np
import matplotlib.pyplot as plt
from collections import deque

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

def euler(tiempo_inicial, theta_inicial, dtheta_inicial, dt, pasos, C, k):
    tiempos = []
    thetas = []
    dthetas = []
    
    lista_datos = ListaEnlazada()
    
    t = tiempo_inicial
    theta = theta_inicial
    dtheta = dtheta_inicial
    
    for _ in range(pasos):
        tiempos.append(t)
        thetas.append(theta)
        dthetas.append(dtheta)
        
        lista_datos.agregar(t, theta, dtheta)
        
        dtheta_new = dtheta - dt * (C * dtheta + k * theta)
        theta_new = theta + dt * dtheta
        
        theta = theta_new
        dtheta = dtheta_new
        t += dt
    
    return tiempos, thetas, dthetas, lista_datos

# Parámetros de la ecuación diferencial
C = 0.1
k = 1.0

# Parámetros para el método de Euler
tiempo_inicial = 0.0
theta_inicial = 1.0
dtheta_inicial = 0.0
dt = 0.01
pasos = 1000

# Resolución de la ecuación diferencial
tiempos, thetas, dthetas, lista_datos = euler(tiempo_inicial, theta_inicial, dtheta_inicial, dt, pasos, C, k)

# Mostrar los datos calculados
lista_datos.mostrar()


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



def menu_interactivo():
    historial_errores = []
    
    while True:
        print("\nMenú Interactivo")
        print("a. Mostrar grafica")
        #arreglar el print N° 1 
        print("1. Mostrar los datos calculados")
        print("b. Ingresar una coordenada para el cálculo de error")
        print("c. Mostrar historial de coordenadas ingresadas y sus respectivos cálculos de error")
        #Arreglar en la opcion "d" que la busqueda no sea tan precisa
        print("d. Buscar un dato en la lista ingresando el tiempo")
        print("e. Buscar un dato en la lista ingresando la variable dependiente o su valor más cercano")
        print("f. Limpiar la consola")
        print("g. Salir del programa")
        
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion == 'a':
            lista_datos.mostrar()   
        elif opcion == '1':
            graficar_en_tiempo_real(tiempos, thetas)
        elif opcion == 'b':
            tiempo = float(input("Ingrese el tiempo: "))
            valor_imagen = float(input("Ingrese el valor de la imagen: "))
            error = calcular_error(tiempo, valor_imagen, lista_datos)
            historial_errores.append((tiempo, valor_imagen, error))
            print(f"Error calculado: {error}")
            graficar_punto(tiempos, thetas, tiempo, valor_imagen)
        elif opcion == 'c':
            for coord in historial_errores:
                print(f"Tiempo: {coord[0]}, Valor Imagen: {coord[1]}, Error: {coord[2]}")
        elif opcion == 'd':
            tiempo = float(input("Ingrese el tiempo a buscar: "))
            buscar_tiempo(tiempo, lista_datos)
        elif opcion == 'e':
            valor = float(input("Ingrese el valor dependiente a buscar: "))
            buscar_valor(valor, lista_datos)
        elif opcion == 'f':
            limpiar_consola()
        elif opcion == 'g':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

def calcular_error(tiempo, valor_imagen, lista_datos):
    # Implementar la búsqueda binaria para encontrar el valor correspondiente en la lista y calcular el error
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

def solucion_analitica(t, theta_0, dtheta_0, C, k):
    # Aquí se calcularía la solución analítica dependiendo de C y k
    # Esto puede variar si es una ecuación subamortiguada, sobreamortiguada, o críticamente amortiguada
    # Para simplificar, asumamos el caso subamortiguado
    omega0 = np.sqrt(k)
    zeta = C / (2 * np.sqrt(k))
    omega_d = omega0 * np.sqrt(1 - zeta**2)
    
    A = theta_0
    B = (dtheta_0 + zeta * omega0 * theta_0) / omega_d
    
    theta_t = np.exp(zeta * omega0 * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    return theta_t

# Generar datos de la solución analítica
theta_analitica = [solucion_analitica(t, theta_inicial, dtheta_inicial, C, k) for t in tiempos]

# Graficar la comparación
plt.plot(tiempos, thetas, 'b-', label='Solución Numérica (Euler)')
plt.plot(tiempos, theta_analitica, 'r--', label='Solución Analítica')
plt.legend()
plt.show()
