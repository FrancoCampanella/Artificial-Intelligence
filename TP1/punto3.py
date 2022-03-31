#Dada una orden de pedido, que incluye una lista de productos del almacén anterior que deben
#ser despachados en su totalidad, determinar el orden óptimo para la operación de picking
#mediante Temple Simulado. ¿Qué otros algoritmos pueden utilizarse para esta tarea

import random
import numpy as np
import matplotlib.pyplot as plt

from simulated_anneling import anneling, ley_enfriamiento
from LayoutAlmacen import Almacen,mapa
from cache import Cache


#Parametros del modelo
len_enfria=3000  #Longitud de la ley de enfriamiento
coef_exp=1.01    #Coef de caida exponelcia de la temperatura
tem_max=5000    #Temperatur maxima
cant_ordenes=100  #Cantidad de ordenes
len_ordenes=20  #Longitud de ordenes

# Se crea el layout
almacen = Almacen()
cache = Cache(almacen)
empiezaEN = [0, 0] #Punto de salida
terminaEN = [0, 0]

#Array para almacenar E2 promedio
E2=np.zeros((len_enfria))
list_E2=[]


#Genera ordenes aleatorias
aux=random.sample(range(100),len_ordenes) 
list_order=[aux for i in range(cant_ordenes) ]

#Ley de enfriamiento
T=ley_enfriamiento(tem_max,len_enfria,coef_exp)


#Se realiza el temple orden por orden
temple=anneling(cache,T)
for order in list_order:

    #Se busca las coordenadas de estos puntos en el layout
    ordenesPosiciones = list(map(lambda x:almacen.getPosicionProducto(x),order))

    #Se realiza el temple
    
    E=temple.search(ordenesPosiciones,empiezaEN,terminaEN)

    #Lista de energias finales
    list_E2.append(E[-1])

    #Energia promedio
    E2+=np.array(E)

    plt.figure(1)
    plt.plot(np.linspace(0,(len(E)-1),len(E)),np.array(E))
    plt.title("Energia de las soluciones")
    plt.xlabel("it")
    plt.ylabel("E")

[way,resultado,E]=temple.search(ordenesPosiciones,empiezaEN,terminaEN,caminoTotal=True)
cache.guardar()

order2=[]
for i in resultado:
    order2.append(almacen.getproducto(i))
    
print(f"El mejor camino para realizar las ordenes {order} es: {order2} \n\n")

#Grafica el ultimo camino obtenido
layout=mapa(almacen)
layout.start()
layout.printCamino(way,animar=0.1)

input("Presione entre para continuar\n")

E2=E2/cant_ordenes

plt.figure(2)
plt.xlabel("E pormedio")
plt.ylabel("it")
plt.plot(np.linspace(0,(len(E2)-1),len(E2)),E2)


plt.figure(3)
plt.title("Agenda de temperatura")
plt.xlabel("it")
plt.ylabel("T")
plt.plot(np.linspace(0,(len(T)-1),len(T)),T)


print(f"Lista de energia finales:{list_E2}")
print(f"Promedio:{E2[-1]}")
E2array=np.array(list_E2)
des=np.std(E2array)
print(f"Desviacion estandar: {des}")

plt.figure(4)
aux=E2array-E2[-1]*np.ones((len(E2array)))
aux=aux/E2[-1]*100
indices=[i for i in range(cant_ordenes)]
plt.bar(indices,abs(aux),label='it')
plt.title("Desviacion con respecto a la E promedio en %")
plt.xlabel("it")
plt.ylabel("desE%")

plt.show()
