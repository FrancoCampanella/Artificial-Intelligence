from ac3 import ac3

def backtrack(csp,assigment,cant_tareas): # rellena las variables

    if iscomplete(assigment,csp):
        return assigment

    var=select_unassignedvariable(csp) # selecciona las variables no asignadas
    assigment['variables'].append(var) # las carga en assignment
    valuelist=csp.D[var]#order_domain_values(var,csp) # 

    for value in valuelist["Dominio"]:
        
        if isconsistent(value,csp,assigment):
            
            assigment['values'].append(value)
            bool_inference=inference(csp,assigment)

            if bool_inference:

                result=backtrack(csp,assigment,cant_tareas)

                if result!=None:
                
                    return result

            assigment['values'].pop(-1)
            inf = assigment['inferences'].pop(-1)
            auxX=inf["X"]
            auxD=inf["Dominio"]
            csp.X=auxX.copy()
            csp.D=auxD.copy()

    assigment['variables'].pop(-1)

    return None


def iscomplete(assigment,csp):

    if len(assigment['variables'])==len(csp.C.keys()): # verifica que se hayan asignado todas las variables

        return True

    return False

#Heuristicas globales
def select_unassignedvariable(csp):

    #En primer lugar elegimos la heuristica MRV, ordena las variables mas restringidas primero
    aux=10e4
    variableMRV=[]
    aux2=0
    for dom in csp.D:

        if dom['Tarea'] in csp.C.keys():
            if len(dom['Dominio'])>1:
                if len(dom['Dominio'])<aux:

                    aux=len(dom['Dominio'])
                    aux2=dom['Tarea']

    variableMRV.append(aux2)

    for dom in csp.D:
        if dom['Tarea'] in csp.C.keys():
            if len(dom['Dominio'])>1:
                if dom['Tarea']!=aux2:
                    if len(dom['Dominio'])==aux:
                        variableMRV.append(dom['Tarea'])
        
    #Si hay mas de dos variables MRV se desempata de acuerdo a la Variable más restrictiva
    if len(variableMRV)>0:

        cant_rest=[]
        for var in variableMRV:
            if var in csp.C.keys():
                cant_rest.append(len(csp.C[var]))

        if len(cant_rest)>0:
            ind=cant_rest.index(max(cant_rest))
            return variableMRV[ind]

    return variableMRV[0]

def order_domain_values(var,csp): # ordena primero el valor menos restrictivo

    aux=csp.D[var]['Dominio']

    aux1=0
    aux3=[]
    u=[]

    for x in aux:

        aux2=0

        for k in csp.C[var].keys():
                
            aux2+=len( csp.C[var][k][str(x)] )

        if aux2>aux1:
            aux1=aux2
            u.append(x)
        else:
            aux3.append(x)

    u.reverse()
    u.extend(aux3)

    return u

def isconsistent(value,csp,assigment):
    
    if value in csp.D[assigment['variables'][-1]]['Dominio']:
        return True

    return False

def inference(csp,assigment):
    
    assigment['inferences'].append( {"X":csp.copyX(), "Dominio":csp.copyD()} )

    csp.X[assigment['variables'][-1]]['PeriodoInicio']=assigment['values'][-1]['S']
    csp.X[assigment['variables'][-1]]['Maquina']=assigment['values'][-1]['M']
    csp.X[assigment['variables'][-1]]['PeriodoFin']=assigment['values'][-1]['S']+csp.X[assigment['variables'][-1]]['D']
    csp.D[assigment['variables'][-1]]['Dominio']=[assigment['values'][-1]]

    return ac3(csp)
    
