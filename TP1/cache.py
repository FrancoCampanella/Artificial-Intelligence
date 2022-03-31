
from A_estrella import A_star
import os
import json

class Cache():
    
    def __init__(self,almacen):

        self.almacen = almacen
        self.X = self.almacen.limits_x
        self.Y = self.almacen.limits_y
        self.A_object=A_star(2,1,self.almacen.obstaculos)

        self.path, _ = os.path.split(os.path.abspath(__file__))

        tf = open(self.path+"/cache.json", "r")
        self.tabla = json.load(tf)
        tf.close()

    def crear(self):
        # =================================== Se crea una vez la cache ====================
        
        # =================================================================================
        self.tabla = {}

        for j in range(self.Y[0],self.Y[1]):

            for i in range(self.X[0],self.X[1]):
                
                dct = {}
                From = [i,j]

                for J in range(self.Y[0],self.Y[1]):

                    for I in range(self.X[0],self.X[1]):

                        To = [I,J]
                        D = -1
                        dct.update({f"{str(To)}":D})

                self.tabla.update({f"{str(From)}":dct})

        tf = open(self.path+"/cache.json", "w")
        json.dump(self.tabla,tf)
        tf.close()

    def camino(self,state1,state):

        return self.A_object.buscar_camino(state1,state,camino_total=True)

    def guardar(self):

        tf = open(self.path+"/cache.json", "w")
        json.dump(self.tabla,tf)
        tf.close()

    def distanciaEntre(self,A,B):

        From = str(A)
        To = str(B)
        d = self.tabla[From][To]

        if d<0:

            d = self.A_object.buscar_camino(A,B)
            self.tabla[From][To] = d
            self.tabla[To][From] = d

            return d
            
        else:

            return d
        