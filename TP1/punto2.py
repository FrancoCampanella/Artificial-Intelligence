
import random
from A_estrella import A_star
from LayoutAlmacen import Almacen,mapa


# Se crea el layout
almacen = Almacen()
layout=mapa(almacen)
layout.start()

#Se elige un producto inicial y final al azar
pro_inicial=random.sample(range(1,100),1)
pro_final=random.sample(range(1,100),1)

#Se busca las coordenadas de estos puntos en el layout
punto_inicial_coord = almacen.getPosicionProducto(pro_inicial[0])
punto_final_coord = almacen.getPosicionProducto(pro_final[0])

#Se realiza la busqueda con el algoritmo A*
posicion=A_star(2,1,almacen.obstaculos)
posicion_int=posicion.buscar_camino(punto_final_coord ,punto_inicial_coord,camino_total=True)

#Se acondicionan los datos para ser mostrados

print(f"El mejor camino del producto {pro_inicial[0]} que se encuentra en la posicion {punto_inicial_coord} al {pro_final[0]} que se encuentra en la posicion {punto_final_coord} es: \n{posicion_int}")

layout.printCamino(posicion_int,animar=0.1)

input("Presione entre para terminar\n")
