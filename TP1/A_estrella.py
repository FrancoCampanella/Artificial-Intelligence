import numpy as np

class nodos():

    punto_final=[]
    numNodos=1

    def __init__(self,_ubicacion,_nodo_anterior):
        
        self.ubicacion = _ubicacion
        self.camino_recorridoant=_nodo_anterior.camino_recorrido
        self.camino_recorrido = self.camino_recorridoant + self.dis_euc(self.ubicacion,_nodo_anterior.ubicacion)
        self.dist_puntofinal = self.dis_euc(self.ubicacion,nodos.punto_final)
        self.F = self.camino_recorrido + self.dist_puntofinal
        self.numAnt = _nodo_anterior.num
        self.num=nodos.numNodos
        nodos.numNodos += 1

    def dis_euc(self,vec1,vec2):
        return (np.sum(abs(np.array(vec1)-np.array(vec2))**2))**0.5

class nodo_inicial():

    def __init__(self,ubicacion):
        self.ubicacion = ubicacion
        self.camino_recorridoant=0
        self.camino_recorrido = 0
        self.heuristica = 0
        self.F = 0
        self.numAnt = -1
        self.num=0


class A_star():


    def __init__(self,_dim,_paso,_obstaculos):

        self.dim=_dim
        self.paso=_paso
        self.obstaculos=_obstaculos

    def neighbors(self,ubicacion,it=0):

        if self.dim>it:

            for i in range(self.dim-it):
                vec_der=ubicacion.copy()
                vec_izq=ubicacion.copy()
                vec_der[i+it]=ubicacion[i+it]+self.paso
                vec_izq[i+it]=ubicacion[i+it]-self.paso
                
                self.lista_abierta.append(nodos(vec_der,self.nodo_explorar))
                self.Fun_busqueda.append(self.lista_abierta[-1].F)

                self.lista_abierta.append(nodos(vec_izq,self.nodo_explorar))
                self.Fun_busqueda.append(self.lista_abierta[-1].F)

                self.neighbors(vec_izq,it+1+i)
                self.neighbors(vec_der,it+1+i)
    
    def isobstaculo(self,nodo_aux,ff):

        if (nodo_aux.ubicacion in self.obstaculos): 

            self.Fun_busqueda[ff]=10e38
            return False
        
        return True

    def isinlistcerrada(self,nodo_aux,ff):

        if (nodo_aux.ubicacion in self.lista_cerrada) :

            self.Fun_busqueda[ff]=10e38
            return False

        return True

    def together(self,nodo_aux,ff):

        if self.nodo_explorar.numAnt==-1:

            if nodo_aux.ubicacion==self.punto_final:

                self.Fun_busqueda[ff]=10e38
                return False

        return True

    def end_point(self,nodo_aux,camino_total):

            camino_nodos=[nodo_aux.ubicacion]

            if camino_total==True:

                while (nodo_aux.numAnt!=-1):
                    nodo_aux=self.lista_abierta[nodo_aux.numAnt]
                    camino_nodos.append(nodo_aux.ubicacion)
                return camino_nodos

            else:
                        
                return nodo_aux.camino_recorrido

    
    def buscar_camino(self,punto_incial,_punto_final,camino_total=False):

        self.Fun_busqueda=[]
        self.lista_abierta=[]
        self.lista_cerrada=[]
        nodos.punto_final=_punto_final
        nodos.numNodos=1
        self.punto_final=_punto_final
        self.nodo_explorar=nodo_inicial(punto_incial)
        self.lista_abierta.append(self.nodo_explorar)
        self.Fun_busqueda.append(self.nodo_explorar.F)
        self.lista_cerrada.append(self.nodo_explorar.ubicacion)

        iterar=True

        while (iterar):

            self.neighbors(self.nodo_explorar.ubicacion)

            it=True
            
            while(it):
                
                
                ff=self.Fun_busqueda.index(min(self.Fun_busqueda))
                nodo_aux=self.lista_abierta[ff]

                ent1=self.together(nodo_aux,ff)

                if (nodo_aux.ubicacion == self.punto_final) and ent1:
                    return self.end_point(nodo_aux,camino_total)

                ent2=self.isobstaculo(nodo_aux,ff)

                ent3=self.isinlistcerrada(nodo_aux,ff)

                if (ent1 and ent2 and ent3):

                    self.lista_cerrada.append(self.lista_abierta[ff].ubicacion)
                    self.nodo_explorar=self.lista_abierta[ff]
                    self.Fun_busqueda[ff]=10e38
                    it=False
                

