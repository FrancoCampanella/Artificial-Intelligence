import random
import numpy as np
from simulated_anneling import anneling



class genetic():

    def __init__(self,cache,almacen,_T):
                    
        self.cache = cache
        self.almacen=almacen
        self.poblacion=[]                               #Poblacion inicial 
        self.list_fitbest=[]
        self.list_fit=[0]
        self.prob_mutacion=0.1
        self.T=_T   #Agenda de enfriamiento
        self.temple=anneling(self.cache,self.T)
        self.cant_iter=200
        

    def genoma(self):
        return random.sample(range(0,self.cant_pro),self.cant_pro)
    
    def set_poblacion(self):
        for i in range(self.cant_poblacion):
            self.poblacion.append(self.genoma())

    #La funcion de fitness hace uso del temple simulado para obtener una medida de idoneidad
    def fitness(self,individuo):

        fit=0
        #Carga cada individuo al almacen
        self.almacen.cargarProductos(individuo)

        #Se realiza el temple simulado orden por orden
        for order in self.list_ordenes :
            
            #Busca las posiciones de los productos en el almacen
            ordenesPosiciones = list(map(lambda x:self.almacen.getPosicionProducto(x),order))
            #Realiza el temple
            E=self.temple.search(ordenesPosiciones ,[0,0],[0,0])
            fit+=E[-1]

        #Devuelve el costo promedio de las ordenes historicas
        return  fit/len(self.list_ordenes)

    def probability(self):

        prob=self.list_fit/np.sum(np.array(self.list_fit))*100
        prob=np.ones(np.shape(prob))*100-prob

        return prob

    def fathers(self,prob):

        pares=[]
        for i in range(self.parespadres):
            equal=True

            while equal:

                ind=random.choices(range(len(self.poblacion_best)),prob[0:len(self.poblacion_best)],k=2)
                if ind[0]!=ind[1]:
                    equal=False

            pares.append([self.poblacion_best[ind[0]],self.poblacion_best[ind[1]]]) 
        
        return pares


    def cross_over(self):
        
        #Se calcula probabilidad de ser elegidos como padres
        prob=self.probability()

        self.poblacion=[]

        #Se seleccionan n pares de padres
        pares=self.fathers(prob)

        #Se realiza el crossover
        for ii in range(self.parespadres):
            
            padres=[pares[ii][0],pares[ii][1]]

            index=random.sample(range(len(padres[1])),2)
            index.sort()

            ind=[padres[1][index[0]:index[1]],padres[0][index[0]:index[1]]]

            for j in range(2):
                
                aa=0
                individuo=padres[j]
                aux1=ind[j].copy()
                aux2=padres[j][index[0]:index[1]]
                aux3=[]
                aux3=padres[j][index[1]:]
                aux3.extend(padres[j][0:index[j]])

                for i in aux3:
                    
                    if i in aux1:

                        pass

                    elif (len(aux1)+index[0])>=len(individuo):

                        aux1.insert(aa,i)
                        aa+=1
                        
                    else:

                        aux1.append(i)

                    if aux3.index(i)==len(aux3)-1:

                        if len(aux1)<len(individuo):

                            bb=len(aux1)
                            for i2 in range((len(individuo)-bb)):

                                index2=0
                                aux5=aux2[index2]

                                while aux5 in aux1:

                                    index2+=1
                                    aux5=aux2[index2]

                                if (len(aux1)+index[0])>=len(individuo):

                                    aux1.insert(aa,aux5)
                                    aa+=1
                                    
                                else:

                                    aux1.append(aux5)

                self.poblacion.append(aux1) 

        if len(self.poblacion)<self.cant_poblacion:

            self.poblacion.append(self.poblacion_best[0])

    def get_best(self):

        self.list_fit=[]                 #Lista de fitness
        self.poblacion_best=[]           #Lista con los mejores

        it=0
        dictor={}

        #Se calcula el fitness individuo por individuo 
        for invididuo in self.poblacion:

            self.list_fit.append(self.fitness(invididuo))
            dictor[self.list_fit[-1]]=it


        #Ordena los fitness de menor a mayor
        self.list_fit.sort()
        
        #Devuelve los k mejores individuos(Los que tienen el menor fitness)
        for i in range(self.k):

            index=dictor[self.list_fit[i]]
            self.poblacion_best.append(self.poblacion[index])
             
    def mutacion(self):
        
        for i in self.poblacion:

            aux=random.choice(range(0,101))/100

            if aux<self.prob_mutacion:
                
                index=random.sample(range(len(i)),2)
                aux1=i[index[0]]
                aux2=i[index[1]]
                i[index[0]]=aux2
                i[index[1]]=aux1

    def process(self,_cant_poblacion,_list_ordenes,_cant_prod=108):
        
        it=0
        iterar=True
        self.cant_poblacion = _cant_poblacion           #Numeros de individuos de una poblacion
        self.list_ordenes=_list_ordenes
        self.cant_pro=_cant_prod                        #Cantidad de productos
        self.parespadres=round(self.cant_poblacion/2)
        self.set_poblacion()
        self.k=round(self.cant_poblacion*0.4)

        while iterar:

            #Se guarda el ultimo mejor fitness
            fit_plob_ant=self.list_fit[0]
            #Obtiene los mejores individuos
            self.get_best()
            #Se guarda el mejor fitness de cada iteracion
            self.list_fitbest.append(self.list_fit[0])
            #Se realiza un crossover "Cruce de orden"
            self.cross_over()
            #Se realiza la mutacion
            self.mutacion()


            #Se verifica si se cumplio el numero max de it
            if it>=self.cant_iter:
                iterar=False

            #Se verifica si hay una convergencia en los fitness
            if abs(fit_plob_ant-self.list_fit[0])<0.001:
                iterar=False

        return self.poblacion_best[0],self.list_fitbest
        
        
