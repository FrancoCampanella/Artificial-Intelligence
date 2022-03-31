def getOrdenes(path):
    f = open(path)
    ordenes = []
    orden = []
    orden = 1
    it = 0
    orden = []
    for linea in f:
        if linea.startswith("Order"):
            
            #meter la orden anterior al la lista de ordenes
            if it == 0:
                pass
            else:
                ordenes.append(orden)
            #armar orden nueva
            orden = []
            
        elif linea == "\n":
            pass
        else:
            orden.append(int(linea.replace("P","").replace("\n","")))

        it+=1

    ordenes.append(orden)
    f.close()
    # print(ordenes)
    return ordenes
