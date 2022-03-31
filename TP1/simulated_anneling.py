import random
import math


class anneling(): 

    def __init__(self,cache,_T):
        
        self.cache = cache
        self.T=_T
        self.t=len(_T)
        self.it=0

    def next_state(self):

        aux=self.actual_state.copy()
        index=random.sample(range(self.d2),2)
        aux[index[0]],aux[index[1]] = self.actual_state[index[1]],self.actual_state[index[0]]
        
        return aux

    #Devuelve la energia del conjunto de ordenes o el camino
    def energy(self,state,camino_total=False):

        # Tengo un estado (conjunto de posiciones a unir)
        # Si camino total = False, solo calculo la distancia
        # Sino devuelvo toda la solucion
        list_way=[]
        way=0

        state.append(self.end)
        state.insert(0,self.start)

        for i in range(self.d2+1):

            if camino_total==True:

                list_way.extend(self.cache.camino(state[i+1],state[i]))

            else:

                way+=self.cache.distanciaEntre(state[i+1],state[i])
        
        if camino_total==True:

            return list_way
        else:

            return way

    def probability(self,delta_energy,Temp):
        return math.exp(delta_energy/Temp)

    def search(self,order,inicio,fin,caminoTotal=False):

        it=0
        self.actual_state=order
        self.start=inicio
        self.end=fin
        self.list_energy=[]
        self.next_stateaux=[]
        self.d2=len(order)
        self.E1=self.energy(self.actual_state.copy())

        for i in range(self.t):

            it+=1

            if abs(self.T[i])==0 or it==self.it :

                if caminoTotal:

                    return self.energy(self.actual_state.copy(),camino_total=True),self.actual_state,self.list_energy
                    
                else:

                    return self.list_energy
                        
            self.next_stateaux=self.next_state()
            E2=self.energy(self.next_stateaux.copy())
            deltaenergy=self.E1-E2

            if deltaenergy>0:

                it=0
                self.actual_state=self.next_stateaux
                self.E1=E2

            else:

                prob=self.probability(deltaenergy,self.T[i])
                choise=random.choices([0,1],[1-prob,prob])

                if (choise[0]==1): 

                    self.actual_state=self.next_stateaux
                    self.E1=E2

            self.list_energy.append(self.E1)


def ley_enfriamiento(tem_max,len_enfria,coef_exp):

    T=[tem_max]

    for i in range(len_enfria):

        T.append(T[-1]/coef_exp)

    T[-1]=0

    return T


    



    