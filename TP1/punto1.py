# Dado un punto en el espacio articular de un robot serie de 6 grados de libertad, 
# encontrar el camino más corto para llegar hasta otro punto utilizando el algoritmo A*. 
# Genere aleatoriamente los puntos de inicio y fin, 
# y genere también aleatoriamente obstáculos que el robot debe esquivar, siempre en el espacio articular. 



import random
from A_estrella import A_star



n=12    # Paso
m=6     # Cantidad de obstaculos
d=6     # Dimension espacial

#Limites articulares del robo IRB140

#R.qlim(1,1:2) = [-180,  180]*pi/180;
#R.qlim(2,1:2) = [-100,  100]*pi/180;
#R.qlim(3,1:2) = [-220,  60]*pi/180;
#R.qlim(4,1:2) = [-200, 200]*pi/180;
#R.qlim(5,1:2) = [-200, 200]*pi/180;
#R.qlim(6,1:2) = [-400, 400]*pi/180;
    
#Elegimos el punto inicial de manera aleatoria dentro de los limites articulares
punto_inicial=[]
punto_inicial.append(random.randrange(-180,  180,n))
punto_inicial.append(random.randrange(-100,  100,n))
punto_inicial.append(random.randrange(-220,  60,n))
punto_inicial.append(random.randrange(-200, 200,n))
punto_inicial.append(random.randrange(-200, 200,n))
punto_inicial.append(random.randrange(-400, 400,n))

#Elegimos el punto final de manera aleatoria dentro de los limites articulares
punto_final= []
punto_final.append(random.randrange(-180,  180,n))
punto_final.append(random.randrange(-100,  100,n))
punto_final.append(random.randrange(-220,  60,n))
punto_final.append(random.randrange(-200, 200,n))
punto_final.append(random.randrange(-200, 200,n))
punto_final.append(random.randrange(-400, 400,n))

#Creamos puntos de obstaculos aleatorios
obstaculos=[]
for i in range(m):
    obstaculos.append([random.randrange(0,360, n) for i in range(d)])

#Creamos un camino para la posicion y otro para la orientacion
camino_A=[]
camino_B=[]

#Buscamos el camino de la posicion para una discretizacion del espacio grande
posicion=A_star(3,n,obstaculos)
posicion_int=posicion.buscar_camino(punto_inicial[0:3],punto_final[0:3],camino_total=True)

#Buscamos el camino de la posicion para una discretizacion del espacio chica
for i in range(len(posicion_int)-1):
    
    camino_A.extend(posicion.buscar_camino(posicion_int[i+1],posicion_int[i],camino_total=True))

#Buscamos el camino de la orientacion para una discretizacion del espacio grande
orientacion=A_star(3,12,obstaculos)
posicion_int=orientacion.buscar_camino(punto_inicial[3:6],punto_final[3:6],camino_total=True)

#Buscamos el camino de la orientacion para una discretizacion del espacio chica
for i in range(len(posicion_int)-1):
    
    camino_B.extend(orientacion.buscar_camino(posicion_int[i+1],posicion_int[i],camino_total=True))

#Formateamos la respuesta
print(f"El mejor camino entre [{punto_inicial}, {punto_final}] es:\n")
print("qt = [")

while len(camino_A)>len(camino_B):
    camino_B.append(camino_B[-1])

while len(camino_B)>len(camino_A):
    camino_A.append(camino_A[-1])

for q in zip(camino_A,camino_B):
    print(f"       {q}".replace(","," ").replace("(","").replace(")","").replace("[","").replace("]",""),"")

print("];")
