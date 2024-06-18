#Viñales Facundo, Meyer Iván, Paolo Landó, Escallier Alejandro

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

import os
import sys
from scipy.integrate import solve_ivp

sys.setrecursionlimit(200000000)  # ojo con esto que despues se rompe el programa, ajustar segun lo adecuado
flag = 0

class Ecuacion:
    def __init__(self, tiempo, theta, dtheta):
        self.tiempo = tiempo
        self.theta = theta
        self.dtheta = dtheta

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def agregar(self, tiempo, theta, dtheta):
        nueva_ecuacion = Ecuacion(tiempo, theta, dtheta)
        nuevo_nodo = Nodo(nueva_ecuacion)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def mostrar(self):
        actual = self.cabeza
        datos = []
        while actual is not None:
            ecuacion = actual.dato
            datos.append(f"Tiempo: {ecuacion.tiempo}, Theta: {ecuacion.theta}, dTheta: {ecuacion.dtheta}")
            actual = actual.siguiente
        return datos

#Definimos la ecuacion diferencial
def eq_diff(t, y, c, k):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -c * omega - k * theta
    return [dtheta_dt, domega_dt]

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

# por defecto es 1, que extiende la grafica hasta que T = 10s, si es 10, llega a t = 100s
largo_grafica = 1 

# parámetros de la ecuación diferencial
C = 0.1
k = 1.0

# parámetros para el método de Euler
tiempo_inicial = 0.0
theta_inicial = 1.0 # probar con 20
dtheta_inicial = 0.0
dt = 0.01 #probar con 0.1
pasos = 1000 * largo_grafica

# resolución de la ecuación diferencial usando solve_ivp  
t_span = (tiempo_inicial, tiempo_inicial + dt * pasos)
y0 = [theta_inicial, dtheta_inicial]
t_eval = np.linspace(*t_span, pasos)

sol = solve_ivp(eq_diff, t_span, y0, args=(C, k), t_eval=t_eval)

tiempos = sol.t
thetas = sol.y[0]
dthetas = sol.y[1]

lista_datos = ListaEnlazada()
for t, theta, dtheta in zip(tiempos, thetas, dthetas):
    lista_datos.agregar(t, theta, dtheta)

def graficar_en_tiempo_real(tiempos, thetas, theta_analitica=None):
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))
    linea_numerica, = ax.plot(tiempos, thetas, 'b-', label='Solución Numérica (Euler)')
    plt.title(r'Solución de $\frac{d^2\theta}{dt^2} + c\frac{d\theta}{dt} + k\theta = 0$')
    plt.grid(True)
    plt.xlabel('t')
    plt.ylabel(r'$\theta(t)$')
    
    if theta_analitica is not None:
        linea_analitica, = ax.plot(tiempos, theta_analitica, 'r--', label='Solución Analítica')
    if flag == 1:
        ax.set_title('Comparación de Soluciones')
    elif flag == 2:
        plt.title(r'Solución de $\frac{d^2\theta}{dt^2} + c\frac{d\theta}{dt} + k\theta = 0$')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Theta')
    
    ax.legend()
    
    for i in range(len(tiempos)):
        linea_numerica.set_xdata(tiempos[:i+1])
        linea_numerica.set_ydata(thetas[:i+1])
        if theta_analitica is not None:
            linea_analitica.set_xdata(tiempos[:i+1])
            linea_analitica.set_ydata(theta_analitica[:i+1])
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()
        plt.pause(0.01)
    
    plt.ioff()
    plt.show()

def solucion_analitica(t, theta_0, dtheta_0, C, k):
    omega0 = np.sqrt(k)
    zeta = C / (2 * np.sqrt(k))
    omega_d = omega0 * np.sqrt(1 - zeta**2)
    
    A = theta_0
    B = (dtheta_0 + zeta * omega0 * theta_0) / omega_d
    
    theta_t = np.exp(-zeta * omega0 * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    return theta_t

def calcular_error(tiempo, valor_imagen, lista_datos):
    actual = lista_datos.cabeza
    while actual is not None:
        if actual.dato.tiempo >= tiempo:
            break
        actual = actual.siguiente
    if actual is None:
        return float('inf')
    error = abs(actual.dato.theta - valor_imagen)
    return error

def graficar_punto(tiempos, thetas, tiempo, valor_imagen):
    fig, ax = plt.subplots()
    ax.plot(tiempos, thetas, 'b-')
    ax.plot(tiempo, valor_imagen, 'ro')
    plt.show()

def buscar_tiempo(tiempo, lista_datos):
    actual = lista_datos.cabeza
    while actual is not None:
        if actual.dato.tiempo < tiempo:
            actual = actual.siguiente
        if actual.dato.tiempo >= tiempo:
            return f"Tiempo: {actual.dato.tiempo}, Theta: {actual.dato.theta}, dTheta: {actual.dato.dtheta}"
    return "Tiempo no encontrado en la lista."

def buscar_valor(valor, lista_datos):
    actual = lista_datos.cabeza
    nodo_mas_cercano = actual
    diferencia_minima = abs(actual.dato.theta - valor)
    actual = actual.siguiente
    
    while actual is not None:
        diferencia_actual = abs(actual.dato.theta - valor)
        if diferencia_actual < diferencia_minima:
            nodo_mas_cercano = actual
            diferencia_minima = diferencia_actual
        actual = actual.siguiente
    
    return f"Valor más cercano encontrado: Tiempo: {nodo_mas_cercano.dato.tiempo}, Theta: {nodo_mas_cercano.dato.theta}, dTheta: {nodo_mas_cercano.dato.dtheta}"

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_interactivo():
    historial_errores = []

    def mostrar_grafica():
        global flag 
        flag = 2
        graficar_en_tiempo_real(tiempos, thetas)

    
    def mostrar_datos():
        datos = lista_datos.mostrar()
        file = open("datos_log.txt", "w")
        for i in range(len(datos)):
            file.write(datos[i] + "\n")
        os.startfile("datos_log.txt")
    
    def ingresar_coordenada():
        tiempo = simpledialog.askfloat("Input", "Ingrese el tiempo:")
        valor_imagen = simpledialog.askfloat("Input", "Ingrese el valor de la imagen:")
        if tiempo is not None and valor_imagen is not None:
            error = calcular_error(tiempo, valor_imagen, lista_datos)
            if error < float('inf'):
                graficar_punto(tiempos, thetas, tiempo, valor_imagen)
                messagebox.showinfo("Error", f"Error: {error:.4f}")
                historial_errores.append((tiempo, valor_imagen, error))
            else:
                messagebox.showwarning("Advertencia", "Tiempo no encontrado en la lista.")
    
    def mostrar_historial():
        if not historial_errores:
            messagebox.showinfo("Historial de Errores", "No hay búsquedas recientes.")
        else:
            historial = [f"Tiempo: {coord[0]}, Valor Imagen: {coord[1]}, Error: {coord[2]}" for coord in historial_errores]
            messagebox.showinfo("Historial de Errores", "\n".join(historial))
    
    def buscar_por_tiempo():
        tiempo = simpledialog.askfloat("Input", "Ingrese el tiempo a buscar:")
        if tiempo is not None:
            resultado = buscar_tiempo(tiempo, lista_datos)
            messagebox.showinfo("Resultado de búsqueda", resultado)
    
    def buscar_por_valor():
        valor = simpledialog.askfloat("Input", "Ingrese el valor a buscar:")
        if valor is not None:
            resultado = buscar_valor(valor, lista_datos)
            messagebox.showinfo("Resultado de búsqueda", resultado)
    
    def graficar_comparacion():
        global flag 
        flag = 1
        theta_analitica = [solucion_analitica(t, theta_inicial, dtheta_inicial, C, k) for t in tiempos]
        graficar_en_tiempo_real(tiempos, thetas, theta_analitica)

    
    def salir():
        root.destroy()

    root = tk.Tk()
    root.title("Simulación Diferencial")
    root.geometry("700x500")
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    menu = tk.Menu(root)
    root.config(menu=menu)

    archivo_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Salir", command=salir)

    acciones_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Acciones", menu=acciones_menu)
    acciones_menu.add_command(label="Mostrar Grafica en tiempo real", command=mostrar_grafica)
    acciones_menu.add_command(label="Mostrar Datos", command=mostrar_datos)
    acciones_menu.add_command(label="Ingresar Coordenada", command=ingresar_coordenada)
    acciones_menu.add_command(label="Mostrar Historial", command=mostrar_historial)
    acciones_menu.add_command(label="Buscar por Tiempo", command=buscar_por_tiempo)
    acciones_menu.add_command(label="Buscar por Valor", command=buscar_por_valor)
    acciones_menu.add_command(label="Graficar Comparación", command=graficar_comparacion)

    tk.Label(root, text="Simulación de Ecuaciones Diferenciales", font=("Helvetica", 16)).pack(pady=10)
    ttk.Button(root, text="Mostrar Grafica en tiempo real", command=mostrar_grafica).pack(pady=5)
    ttk.Button(root, text="Mostrar Datos", command=mostrar_datos).pack(pady=5)
    ttk.Button(root, text="Ingresar Coordenada", command=ingresar_coordenada).pack(pady=5)
    ttk.Button(root, text="Mostrar Historial", command=mostrar_historial).pack(pady=5)
    ttk.Button(root, text="Buscar Dato por Tiempo", command=buscar_por_tiempo).pack(pady=5)
    ttk.Button(root, text="Buscar Dato por Valor", command=buscar_por_valor).pack(pady=5)
    ttk.Button(root, text="Graficar Comparación", command=graficar_comparacion).pack(pady=5)
    ttk.Button(root, text="Salir", command=salir).pack(pady=5)

    root.mainloop()
    


if __name__ == "__main__":
    menu_interactivo()
