import math
from A_estrella import A_star,nodos,nodo_inicial
import os
import json
from LayoutAlmacen import Almacen,mapa
from cache import Cache

almacen = Almacen()

X = [0,2]
Y = [0,2]

cache = Cache(almacen)

for j in range(Y[0],Y[1]):
                for i in range(X[0],X[1]):
                    # from i,j
                    dct = {}
                    From = [i,j]
                    for J in range(Y[0],Y[1]):
                        for I in range(X[0],X[1]):
                            # to I,J
                            To = [I,J]  
                            cache.distanciaEntre(To,From,2,almacen.obstaculos)

cache.guardar()