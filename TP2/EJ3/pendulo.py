import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

from punto3 import controlador

CONSTANTE_M = 2 # Masa del carro
CONSTANTE_m = 1 # Masa de la pertiga
CONSTANTE_l = 1 # Longitud dela pertiga

# Simula el modelo del carro-pendulo.
# Parametros:
#   t_max: tiempo maximo (inicia en 0)
#   delta_t: incremento de tiempo en cada iteracion
#   theta_0: Angulo inicial (grados)
#   v_0: Velocidad angular inicial (radianes/s)
#   a_0: Aceleracion angular inicial (radianes/s2)

def simular(t_max, delta_t, theta_0, v_0, a_0):
  con=controlador()

  theta = (theta_0 * np.pi) / 180
  v = v_0
  a = a_0

  # Simular
  y = []
  y2=[]
  y3=[]
  f2=[]
  x = np.arange(0, t_max, delta_t)
  
  for t in x:
    F=con.motordeinferencias(theta, v)
    a = calcula_aceleracion(theta, v,F)
    v = v + a * delta_t
    theta = theta + v * delta_t + a * np.power(delta_t, 2) / 2 
    y.append(theta)
    y2.append(v)
    y3.append(a)
    f2.append(F)

  fig, ax = plt.subplots()
  fig2, ay = plt.subplots()
  fig2, a = plt.subplots()
  fig2, a3 = plt.subplots()
  ax.plot(x, y)
  ax.set_title('Theta')
  ay.plot(x, y2)
  ay.set_title('Velocidad')
  a.plot(x,y3)
  a.set_title('Aceleracion')
  a3.plot(x,f2)
  a3.set_title('Fuerza')
  ax.set(xlabel='time (s)', ylabel='theta', title='Delta t = ' + str(delta_t) + " s")
  ax.grid()
  
  plt.show()


# Calcula la aceleracion en el siguiente instante de tiempo dado el angulo y la velocidad angular actual, y la fuerza ejercida
def calcula_aceleracion(theta, v, f):
    numerador = constants.g * np.sin(theta) + np.cos(theta) * ((-f - CONSTANTE_m * CONSTANTE_l * np.power(v, 2) * np.sin(theta)) / (CONSTANTE_M + CONSTANTE_m))
    denominador = CONSTANTE_l * (4/3 - (CONSTANTE_m * np.power(np.cos(theta), 2) / (CONSTANTE_M + CONSTANTE_m)))
    return numerador / denominador



simular(10, 0.0001, 45, 0, 0)