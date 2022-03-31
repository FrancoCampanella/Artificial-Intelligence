from csp import grafo_csp

def ac3(csp,it=3): #receive binary CSP (X,D,C)
    queue = csp.getArcos() # cola de arcos, inicialmente los arcos en el csp
            # []
    while len(queue)>0:
        i,j = queue.pop(0) # saco el primer elemento
        # son ids i,j
        if revise(csp,i,j):
            if len(csp.D[i]['Dominio'])==0:
                return False
            for k in csp.C[i]: #
                if k != j:
                    # buscar en restricciones todos los que tengan Xi, y sacar el otro
                    queue.append((i,k))
    return True

def revise(csp,Xi,Xj):
    I = Xi
    J = Xj
    revised = False
    aux1=csp.D[I]["Dominio"].copy()
    for x in aux1: # (m1,1)....,(m3,1)... para Xi
        
        # Existe algun y talque (x,y) satisfacen restricciones entre (Xi,Xj) ===========
        hay_y = False
        aux2=csp.D[J]["Dominio"].copy()
        for y in aux2: # (m3,1)....,(m4,1)... para Xj
            # si x,y satisfacen las restricciones de Xi, Xj
            restricciones = csp.C[Xi][Xj][str(x)]
            for solucion in restricciones:
                if str(y) == str(solucion): # si mi par x,y es alguno de los x,y posibles
                    hay_y = True # entonces hay un y que cumple
                    break
            if hay_y: # si ya encontre un "y", no busco otros
                break
        # ==============================================================================
        
        if hay_y==False: # if no value y in Dj...
            #delete x from Di
            csp.D[I]["Dominio"].remove(x)
            revised = True
            
    return revised
