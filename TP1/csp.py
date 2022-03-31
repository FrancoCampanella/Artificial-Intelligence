
class grafo_csp():

    def __init__(self,tareas=None,DominioTs=None,maquinas=None):
        print("- Creando Grafo CSP")
        
        self.X=[]
        self.D=[]
        self.C={} # entro por id tareaA, luego id tareaB y ahi tengo la extension
        
        self.tareas=tareas
        self.maquinas=maquinas

        for i in range(len(tareas)):

            TSM={"Tarea":self.tareas[i]['id'],'Maquina':None,'PeriodoInicio':None,'PeriodoFin':None,'D':self.tareas[i]['D']}

            dom=[]
            
            for T in DominioTs:

                for M in self.maquinas:

                    if M['tipo']==self.tareas[i]['M']:
                        dom.append({'M':M['id'],'S':T})
            
            self.D.append({"Tarea":self.tareas[i]["id"],'Dominio':dom})
            
            self.X.append(TSM)
            
        self.constraint() # crear las restricciones
        

    def constraint(self):
        print("--- Creando restricciones")
        
        for i in range(len(self.X)): # recorro variables TSMi
            X1 = self.X[i]
            keyA = X1["Tarea"] # id de la tarea
            # diccionario vacio para agregar la sig tarea
            Bij={} 
            for j in range(len(self.X)): # para cada TSMi analizo TSMj
                if i!=j:
                    #print(f"Restricciones: {i}-{j}")
                    X2 = self.X[j]
                    keyB = X2["Tarea"] # id de la tarea
                     
                    if self.tareas[i]["M"]==self.tareas[j]["M"]:
                        try: # esto es muy importante
                            self.C[keyA].update({ keyB:{} }) # trata de agregar una restriccione
                        except: # pero si no estan creadas
                            self.C.update({ keyA:{   keyB:  {}    } }) # entonces las crea
                                                       #Cij
                        Cij = {}

                        Dominio1 = self.D[i]["Dominio"]
                        for valor1 in Dominio1:

                            restricciones = [] # empiezan vacias las restricciones

                            Dominio2 = self.D[j]["Dominio"]
                            for valor2 in Dominio2:
                                
                                if valor1["M"]==valor2["M"]: # usan distintas maquinas
                                    if valor1["S"]+self.tareas[i]["D"]<valor2["S"]:
                                        # agregar, es valido
                                        restricciones.append(valor2)
                                    elif valor2["S"]+self.tareas[j]["D"]<valor1["S"]:
                                        # agregar, es valido
                                        restricciones.append(valor2)
                                else:
                                    restricciones.append(valor2)
                                # sino, las maquinas son distintas, no estan restringidas

                            if len(restricciones)>0:
                                Cij.update({str(valor1):restricciones}) #agregar restricciones
                            # sino, no agregar nada para ese valor 1 porque no tiene valores para la otra tarea

                        if len(Cij)>0: # hay restricciones, agregar valores validos
                            Bij.update({keyB:Cij})
            if len(Bij)>0:               
                self.C.update({keyA:Bij}) # lista de valores posibles en la tarea B
    
    def getArcos(self):
        arcos = []
        for key1 in self.C:
            for key2 in self.C[key1]:
                arcos.append((key1,key2))
        return arcos
    
    #funcion que setea el dominio temporal entre tareas
    def copyX(self):
        x = []
        for elem in self.X:
            x.append(elem.copy())
        return x
    
    def copyD(self):
        d = []
        for elem in self.D:
            key = list(elem.keys())
            d.append({key[0]:elem[key[0]],key[1]:elem[key[1]].copy()})
        return d


