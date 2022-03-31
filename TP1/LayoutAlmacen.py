
from random import randint

# Estas son para la parte grafica
import pygame
import time
import _thread # para hacer multihilos

class Almacen():
    col = 6
    row = 3

    estanterias_X_size = 2
    estanterias_Y_size = 3
    pasillos = 1

    def __init__(self,col=None,row=None,estantesX=None,estantesY=None,pasillos=None,plot=False):
        if col == None:
            self.col = Almacen.col
        else:
            self.col = col
        if row == None:
            self.row = Almacen.row
        else:
            self.row = row

        if estantesX == None:
            self.estanterias_X_size = Almacen.estanterias_X_size
        else:
            self.estanterias_X_size = estantesX
        self.estanterias_X = list(range(1,self.estanterias_X_size+1))
        if estantesY==None:
            self.estanterias_Y_size = Almacen.estanterias_Y_size
        else:
            self.estanterias_Y_size = estantesY
        self.estanterias_Y = list(range(1,self.estanterias_Y_size+1))
        if pasillos == None:
            self.pasillos = Almacen.pasillos
        else:
            self.pasillos = pasillos

        self.limits_x = [0,self.col*(self.estanterias_X_size+self.pasillos)+1]
        self.limits_y = [0,self.row*(self.estanterias_Y_size+self.pasillos)+1]
        self.limits = [self.limits_x,self.limits_y]
        
        self.matriz_deposito = []
        self.estanterias = [] #Guardo los objetos estanterias
        self.obstaculos = [] #guardo posiciones [X,Y]

        _id = 1
        _almacen_id = 1

        # Llenar la matriz del almacen (se comento el mapa)
        for y in range(self.limits[1][1]): #limite en Y
            
            for x in range(self.limits[0][1]): #limite en X
                xx = x%(self.estanterias_X_size+self.pasillos)
                yy = y%(self.estanterias_Y_size+self.pasillos)
                
                if (xx in self.estanterias_X) and (yy in self.estanterias_Y):
                    elemento = {"id":_id,
                                "pos":[x,y],
                                "x":x,
                                "y":y,
                                "almacen":True,
                                "almacen_id":_almacen_id, #id de almacen
                                "producto":_almacen_id-1
                                }
                    if plot:
                        #print(_almacen_id,end=" ")
                        print("#",end=" ") #Almacen
                    _almacen_id += 1
                    self.estanterias.append(elemento)
                    self.obstaculos.append([x,y])

                else:
                    elemento = {"id":_id,
                                "pos":[x,y],
                                "x":x,
                                "y":y,
                                "almacen":False
                                }
                    if plot:
                        print(".",end=" ") #Camino
                
                self.matriz_deposito.append(elemento)
                _id += 1

            if plot:
                print()


    def inicioAleatorio(self):
        # Genero el nodo inicial que tambien es el final ================================================
        # Elegir al azar algun nodo de inicio (no puede ser almacen)
        ID_start = randint(1,len(self.matriz_deposito))

        while self.matriz_deposito[ID_start-1]["almacen"] == True:
            ID_start = randint(1,len(self.matriz_deposito)) #cambiar la eleccion
        
        return self.getPosicion(ID_start)

    def getPosicion(self,ID_):
        return self.matriz_deposito[ID_-1]["pos"]

    def finalAleatorio(self):
        id_end = randint(1,len(self.estanterias))
        #ID_end = self.getPosicionEstante(id_end)
        return self.getPosicionEstante(id_end)

    def getPosicionEstante(self,id_estante):
        if id_estante+1<len(self.estanterias):
            posicionFinal = self.estanterias[id_estante+1]["pos"]
            return posicionFinal
        else:
            print("el estante",id_estante,"esta fuera de rango")
            return False
        
    def getPosicionProducto(self,producto):
        for estanteria in self.estanterias:
            if estanteria["producto"]==producto:
                posicion = estanteria["pos"]
                return posicion
        else:
            print(f"No se encontro el producto {producto}")
            return None

    def getproducto(self,posicion):
        for estanteria in self.estanterias:
            if estanteria["pos"]==posicion:
                producto = estanteria["producto"]
                return producto
        else:
            print(f"No se encontro la posicion {posicion}")
            return None

    def cargarProductos(self,layout):
        i=0
        for prod in layout:
            self.estanterias[i]["producto"]=prod
            i+=1

# #######################################################################################################
# Almacen(plot = True)
# #######################################################################################################

#SCREENRECT = pygame.Rect(0, 0, 640, 480)

pasada = 0
estanteria = 1
inicio = 2
final = 3
recorrido = 4
estante = 5

class mapa():
    # Colores
    BLUE = (20, 34, 238)
    GREEN = (20, 240, 50)
    RED = (230, 0, 20)
    BLACK = (0, 0, 0)
    WHITE = (250,250,250)
    YELLOW = (240,240,20)
    GRAY = (30,30,30)
    VIOLET = (250,0,250)
          # camino,estant,inicio,fin,recorr,estant.
    Color = [WHITE,GRAY,GREEN,RED,BLUE,YELLOW,VIOLET]
    sizeSquare = 40

    def __init__(self,almacen):
        self.Layout = almacen
        # Distribucion del almacen
        self.estanterias_X_pos = self.Layout.estanterias_X
        self.estanterias_X_size = self.Layout.estanterias_X_size
        self.estanterias_Y_pos = self.Layout.estanterias_Y
        self.estanterias_Y_size = self.Layout.estanterias_Y_size

        # Crear mapa
        self.cantCol = self.Layout.limits_x[1]
        self.cantRow = self.Layout.limits_y[1]
        self.pasillos = self.Layout.pasillos

        pygame.init()
        self.size = [mapa.sizeSquare*self.cantCol, mapa.sizeSquare*self.cantRow]
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Almacen on PYGAME")
        self.clock = pygame.time.Clock()
        self.gameOver = False

        self.matrix = []

        for i in range(self.cantCol):
            subM = []

            for j in range(self.cantRow):
                xx = i%(self.estanterias_X_size+self.pasillos)
                yy = j%(self.estanterias_Y_size+self.pasillos)
                if (xx in self.estanterias_X_pos) and (yy in self.estanterias_Y_pos):
                    subM.append(estanteria)
                else:
                    subM.append(pasada)
            
            self.matrix.append(subM)

        self.font_size = 18
        self.font = pygame.font.Font(None, self.font_size)
        #self.font.set_bold(0)
        self.font_color = pygame.Color("white")

    def start(self):
        _thread.start_new_thread( self.mostrarMapa,() )

    # Muestra el mapa completo y lo va actualizando =======================================================
    def mostrarMapa(self):
        while not self.gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            self.screen.fill(mapa.BLACK)
            for elemento in self.Layout.matriz_deposito:
                i,j = elemento["x"],elemento["y"]
                X,Y = i*self.sizeSquare,j*self.sizeSquare
                
                if elemento["almacen"]==True:

                    color = self.matrix[i][j]
                    pygame.draw.rect(self.screen, mapa.Color[color], [X, Y, self.sizeSquare-2, self.sizeSquare-2], 0)
                    
                    # Numero de estanteria
                    self.txt = self.font.render(f"E{elemento['almacen_id']}", 0, self.font_color)
                    self.txtRect = self.txt.get_rect().move(X,Y)
                    self.screen.blit(self.txt, self.txtRect)

                    # Producto que hay cargado
                    self.txt = self.font.render(f"P{elemento['producto']}", 0, self.font_color)
                    self.txtRect = self.txt.get_rect().move(X,Y+self.sizeSquare-self.font_size)
                    self.screen.blit(self.txt, self.txtRect)
                    
                else:
                    color = self.matrix[i][j]
                    pygame.draw.rect(self.screen, mapa.Color[color], [X, Y, self.sizeSquare-2, self.sizeSquare-2], 0)

            pygame.display.flip()
            #self.clock.tick(5)
        pygame.quit()
    
    def resetMapa(self):
        for i in range(self.cantCol):
            subM = []
            for j in range(self.cantRow):
                xx = i%(self.estanterias_X_size+self.pasillos)
                yy = j%(self.estanterias_Y_size+self.pasillos)
                if (xx in self.estanterias_X_pos) and (yy in self.estanterias_Y_pos):
                    self.matrix[i][j]=estanteria
                else:
                    self.matrix[i][j]=pasada

    def printCaminos(self,caminos,marcarPuntos=0,animar=0,hilo=True,reset=False):
        if hilo:
            _thread.start_new_thread( self.animarCaminos,(caminos,marcarPuntos,animar,False,reset) )
        else:
            self.animarCaminos(caminos,marcarPuntos=marcarPuntos,animar=animar,hilo=False,reset=reset)

    def animarCaminos(self,caminos,marcarPuntos=0,animar=0,hilo=False,reset=False):
        inicio = caminos[0][0]
        final = caminos[-1][-1]
        #intermedios = []
        ultimos = []
        for c in caminos[0:-1]:
            #intermedios.append(c[0])
            ultimos.append(c[-1])
        
        if marcarPuntos>0:
            self.mostrarInicio(inicio)
            self.mostrarFinal(final)
            for i in range(len(ultimos)):
                self.mostrarEstante(ultimos[i])
            time.sleep(marcarPuntos)
        
        for c in caminos:
            if reset:
                self.resetMapa()
            self.printCamino(c,animar,hilo)

    def printCamino(self,camino_,animar=0,hilo=True):
        if hilo:
            _thread.start_new_thread( self.animar,(camino_,animar) )
        else:
            self.animar(camino_,animar)

    def animar(self,camino_,animar=0):
        camino = camino_.copy()
        q_0 = camino.pop(0)
        q_f = camino.pop(-1)
        self.mostrarInicio(q_0)
        time.sleep(animar)

        for q in camino:
            self.mostrarCamino(q,6)
            time.sleep(animar)
            self.mostrarCamino(q)
        
        self.mostrarFinal(q_f)
        time.sleep(animar)

    # Sirven para animar cada celda del mapa del almacen ==================================================
    def mostrarCamino(self,pos,state=recorrido):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    def borrarCamino(self,pos,state=pasada):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est
    
    def mostrarEstante(self,pos,state=estante):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    def borrarEstante(self,pos,state=estanteria):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    def mostrarInicio(self,pos,state=inicio):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    def borrarInicio(self,pos,state=pasada):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est
    
    def mostrarFinal(self,pos,state=final):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    def borrarFinal(self,pos,state=pasada):
        X = pos[0]
        Y = pos[1]
        est = self.matrix[X][Y]
        self.matrix[X][Y] = state
        return est

    # Para cerrar el ploteo y terminar ====================================================================
    def close(self):
        self.gameOver = True
        time.sleep(2)
        pygame.quit()