
from cache import Cache
from simulated_anneling import anneling, ley_enfriamiento
from LayoutAlmacen import Almacen,mapa
from leerOrdenes import getOrdenes

import numpy as np

import matplotlib.pyplot as plt
import time
import os


#Lee las ordenes de un archivo
path, _ = os.path.split(os.path.abspath(__file__))
list_order=getOrdenes("orders.txt")

best_individuo=[19, 37, 21, 64, 104, 40, 17, 54, 26, 53, 11, 68, 47, 50, 99, 3, 107, 32, 80, 30, 66, 35, 29, 6, 88, 77, 36, 72, 91, 20, 76, 55, 73, 52, 101, 61, 106, 22, 86, 93, 41, 95, 38, 12, 75, 78, 79, 7, 65, 57, 1, 63, 105, 10, 46, 98, 39, 45, 44, 5, 14, 23, 84, 92, 83, 94, 69, 60, 90, 96, 15, 67, 89, 34, 0, 2, 25, 59, 42, 103, 24, 70, 28, 18, 9, 43, 100, 62, 16, 33, 4, 48, 81, 56, 87, 102, 8, 82, 71, 85, 97, 74, 27, 51, 58, 13, 49, 31]

almacen2 = Almacen(plot=True)
cache = Cache(almacen2)

#Parametros del modelo
len_enfria=2000  #Longitud de la ley de enfriamiento
coef_exp=1.01    #Coef de caida exponelcia de la temperatura
tem_max=5000    #Temperatur maxima

T=ley_enfriamiento(tem_max,len_enfria,coef_exp)
empiezaEN = [0, 0] #Punto de salida
terminaEN = [0, 0]

#Array para almacenar E2 promedio
E2=np.zeros((len_enfria))
list_E2=[]
time_ini=time.time()

#===========================================================================================
#                                       Orden del almacen por defecto
#===========================================================================================

temple=anneling(cache,T)
for order in list_order:

    #Se busca las coordenadas de estos puntos en el layout
    ordenesPosiciones = list(map(lambda x:almacen2.getPosicionProducto(x),order))

    #Se realiza el temple
    
    E=temple.search(ordenesPosiciones,empiezaEN,terminaEN)
    
    tim=time.time()-time_ini
    print(tim)

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
    order2.append(almacen2.getproducto(i))
    
print(f"El mejor camino para realizar las ordenes {order} es: {order2} \n\n")





input("Presione entre para continuar\n")


E2=E2/len(list_order)

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
indices=[i for i in range(len(list_order))]
plt.bar(indices,abs(aux),label='it')
plt.title("Desviacion con respecto a la E promedio en %")
plt.xlabel("it")
plt.ylabel("desE%")

#===========================================================================================
#                      Orden del almacen siguiendo el mejor individuo obtenido
#===========================================================================================

almacen2.cargarProductos(best_individuo)
E2=np.zeros((len_enfria))
list_E2=[]
#Se realiza el temple orden por orden
temple=anneling(cache,T)
for order in list_order:

    #Se busca las coordenadas de estos puntos en el layout
    ordenesPosiciones = list(map(lambda x:almacen2.getPosicionProducto(x),order))

    #Se realiza el temple
    E=temple.search(ordenesPosiciones,empiezaEN,terminaEN)
    
    tim=time.time()-time_ini
    print(tim)

    #Lista de energias finales
    list_E2.append(E[-1])

    #Energia promedio
    E2+=np.array(E)

    plt.figure(5)
    plt.plot(np.linspace(0,(len(E)-1),len(E)),np.array(E))
    plt.title("Energia de las soluciones")
    plt.xlabel("it")
    plt.ylabel("E")

[way,resultado,E]=temple.search(ordenesPosiciones,empiezaEN,terminaEN,caminoTotal=True)


cache.guardar()
order2=[]
for i in resultado:
    order2.append(almacen2.getproducto(i))
    
print(f"El mejor camino para realizar las ordenes {order} es: {order2} \n\n")

#Grafica el ultimo camino obtenido

layout=mapa(almacen2)
layout.start()
layout.printCamino(way,animar=0.1)

input("Presione entre para continuar\n")

E2=E2/len(list_order)

plt.figure(6)
plt.xlabel("E pormedio")
plt.ylabel("it")
plt.plot(np.linspace(0,(len(E2)-1),len(E2)),E2)


plt.figure(7)
plt.title("Agenda de temperatura")
plt.xlabel("it")
plt.ylabel("T")
plt.plot(np.linspace(0,(len(T)-1),len(T)),T)


print(f"Lista de energia finales:{list_E2}")
print(f"Promedio:{E2[-1]}")
E2array=np.array(list_E2)
des=np.std(E2array)
print(f"Desviacion estandar: {des}")

plt.figure(8)
aux=E2array-E2[-1]*np.ones((len(E2array)))
aux=aux/E2[-1]*100
indices=[i for i in range(len(list_order))]
plt.bar(indices,abs(aux),label='it')
plt.title("Desviacion con respecto a la E promedio en %")
plt.xlabel("it")
plt.ylabel("desE%")




plt.show()
