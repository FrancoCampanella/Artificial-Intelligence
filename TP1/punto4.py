
#Implementar un algoritmo genético para resolver el problema de optimizar la ubicación de los
#productos en el almacén, de manera de optimizar el picking de los mismos. Considere que

from cache import Cache
from simulated_anneling import ley_enfriamiento
from LayoutAlmacen import Almacen
from genetic import genetic
from leerOrdenes import getOrdenes

import numpy as np
import matplotlib.pyplot as plt
import os



#Lee las ordenes de un archivo
path, _ = os.path.split(os.path.abspath(__file__))
list_order=getOrdenes("orders.txt")


#Parametros del modelo
len_enfria=400  #Longitud de la ley de enfriamiento
coef_exp=1.1    #Coef de caida exponelcia de la temperatura
tem_max=5000    #Temperatur maxima
T=ley_enfriamiento(tem_max,len_enfria,coef_exp)

almacen2 = Almacen(plot=True)
cache = Cache(almacen2)
cant_poblacion = 20 #Numeros de individuos de una poblacion

#Se realiza el algoritmo genetico
alg_genetic=genetic(cache,almacen2,T)
best_individuo,list_fit=alg_genetic.process(cant_poblacion,list_order)

#--------------------------------------------------------------------------------------
#                   Se imprime el mejor individuo y se grafica los fitness
#--------------------------------------------------------------------------------------
cache.guardar()

print(best_individuo)
print(list_fit)

plt.figure(1)
plt.xlabel("it")
plt.ylabel("Fitness")
plt.plot(np.linspace(0,(len(list_fit)-1),len(list_fit)),list_fit)

