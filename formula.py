import numpy as np
import matplotlib.pyplot as plt

class Ecuacion():

    coef_c = 1.0     # coeficiente al lado de la primera derivada
    coef_k = 1.0     # coeficiente al lado de theta
    theta_0 = 1.0
    dtheta_dt_0 = 0.0  # Valor inicial de dtheta/dt

    def __init__(self, h_local = 0.01, t_max_local = 10):
        self.h = h_local   # tamaño del paso (reducir num para mayor precision)
        self.t_max = t_max_local  # tiempo maximo (aumentar para mayor extensión grafica)
        self.n_pasos = int(self.t_max / self.h)

    def mostrar_datos(self) -> None:
# Inicialización de arrays
        t = np.linspace(0, self.t_max, self.n_pasos)
        theta = np.zeros(self.n_pasos)
        dtheta_dt = np.zeros(self.n_pasos)

# Condiciones iniciales
        theta[0] = self.theta_0
        dtheta_dt[0] = self.dtheta_dt_0

# Método de Euler
        for i in range(1, self.n_pasos):
            theta[i] = theta[i-1] + self.h * dtheta_dt[i-1]
            dtheta_dt[i] = dtheta_dt[i-1] + self.h * (-self.coef_c * dtheta_dt[i-1] - self.coef_k * theta[i-1])

# Plot
        plt.plot(t, theta, label='Theta (θ)')
        plt.plot(t, dtheta_dt, label='dTheta/dt (θ\')')
        plt.xlabel('Tiempo (t)')
        plt.ylabel('Valores')
        plt.title('Soluciones por medio de Euler')
        plt.legend()
        plt.grid()
        plt.show()

