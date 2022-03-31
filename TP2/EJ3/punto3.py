
class controlador():

    def __init__(self):
        #=======================Variables de entrada ========================================
        #Variable linguistica theta(angulo): dict={conjuntos borrosos,universo del discurso(Por comprension)}.
        self.theta={'NG':(-0.5,-0.25),'NP':(-0.5,0),'Z':(-0.25,0.25),'PP':(0,0.5),'PG':(0.25,0.75)}

        #Variable linguistica dtheta(Velocidad angular): dict={conjuntos borrosos,universo del discurso(Por comprension)}.
        self.dtheta={'NG':(-3,-1),'NP':(-2,0),'Z':(-1,1),'PP':(0,2),'PG':(1,3)}
    
        #===================================================================================

        #=======================Variables de salida ========================================
        #Variable linguistica F(Fuerza): dict={conjuntos borrosos,universo del discurso(Por comprension)}.
        self.F={'NG':(-150,-50),'NP':(-100,0),'Z':(-50,50),'PP':(0,100),'PG':(50,150)}
        #===================================================================================

        #Lista de conjuntos borrosos
        self.conjuntos_borrosos=['NG','NP','Z','PP','PG']

        #Diccionaria que contiene los valores borrosos de las variables de entrada
        self.xtheta_borrosa={}
        self.dxtheta_borrosa={}

        #FAM: (theta,dtheta,F) Base de conocimientos
        self.FAM=[('NG','NG','PG'),('NG','NP','PG'),('NG','Z','PG'),('NG','PP','PP'),('NG','PG','PP'),
        ('NP','NG','PG'),('NP','NP','PG'),('NP','Z','PP'),('NP','PP','PP'),('NP','PG','NP'),
        ('Z','NG','PG'),('Z','NP','PP'),('Z','Z','Z'),('Z','PP','NP'),('Z','PG','NG'),
        ('PP','NG','PG'),('PP','NP','PP'),('PP','Z','NP'),('PP','PP','NP'),('PP','PG','NG'),
        ('PG','NG','PP'),('PG','NP','NP'),('PG','Z','NP'),('PG','PP','NG'),('PG','PG','NG')
        ]

        #Busca reglas en la BK que tengan el mismo consecuente
        self.dict_FAM={}
        for j in self.conjuntos_borrosos:
            FAM_C=[]
            for i in self.FAM:
                if i[2]==j:
                    FAM_C.append(i[:2])
            self.dict_FAM[j]=FAM_C

    def borrosificador(self,xtheta,xdtheta):

        for i in self.conjuntos_borrosos:
            self.xtheta_borrosa[i]=self.membership(self.theta[i][0],self.theta[i][1],xtheta,i)
            self.dxtheta_borrosa[i]=self.membership(self.dtheta[i][0],self.dtheta[i][1],xdtheta,i)

    dict_FAM2={}

    def motordeinferencias(self,xtheta,xdtheta):

        self.borrosificador(xtheta,xdtheta)

        for j in self.conjuntos_borrosos:
            list_aux=[]
            for i in self.dict_FAM[j]:
                aux1=self.xtheta_borrosa[i[0]]
                aux2=self.dxtheta_borrosa[i[1]]
                list_aux.append(min(aux1,aux2))
            self.dict_FAM2[j]=max(list_aux)
        return self.desborrificador()

    # Media de centros
    def desborrificador(self): 
        valornitido=0
        denominador=0
        for j in self.conjuntos_borrosos:
            a=(self.F[j][0]+self.F[j][1])/2
            valornitido+=self.dict_FAM2[j]*a
            denominador+=self.dict_FAM2[j]
        if denominador!=0:
            valornitido=-valornitido/denominador
            return valornitido
        else:
            return 0 

    def membership(self,a1,a3,X,i): #Me indica el grado de pertenencia de una variable a un conjunto borroso. Funcion triangular.
        a2=(a3+a1)/2

        if i=='NG':
            if X<=a2:
                return 1
        if i=='PG':
            if X>=a2:
                return 1
        if X>=a2:
            aux1=(1)/(a2-a3)*(X-a2)+1
            if aux1>0:
                return aux1
            else:
                return 0
        if X<a2:
            aux2=(1)/(a2-a1)*(X-a2)+1
            if aux2>0:
                return aux2
            else:
                return 0
