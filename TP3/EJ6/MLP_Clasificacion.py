import numpy as np
import matplotlib.pyplot as plt
from random import randint


# Generador basado en ejemplo del curso CS231 de Stanford: 
# CS231n Convolutional Neural Networks for Visual Recognition
# (https://cs231n.github.io/neural-networks-case-study/)

def generar_datos_clasificacion(cantidad_ejemplos, cantidad_clases):
    FACTOR_ANGULO = 0.79
    AMPLITUD_ALEATORIEDAD = 0.1

    # Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
    # una (clases balanceadas)
    n = int(cantidad_ejemplos / cantidad_clases)

    # Entradas: 2 columnas (x1 y x2)
    x = np.zeros((cantidad_ejemplos, 2))
    # Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero)
    t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target")

    randomgen = np.random.default_rng()

    # Por cada clase (que va de 0 a cantidad_clases)...
    for clase in range(cantidad_clases):
        # Tomando la ecuacion parametrica del circulo (x = r * cos(t), y = r * sin(t)), generamos 
        # radios distribuidos uniformemente entre 0 y 1 para la clase actual, y agregamos un poco de
        # aleatoriedad
        radios = np.linspace(0, 1, n) + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)

        # ... y angulos distribuidos tambien uniformemente, con un desfasaje por cada clase
        angulos = np.linspace(clase * np.pi * FACTOR_ANGULO, (clase + 1) * np.pi * FACTOR_ANGULO, n)

        # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
        # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
        # la segunda clase estan en [n, (2 * n) - 1], etc.
        indices = range(clase * n, (clase + 1) * n)

        # Generamos las "entradas", los valores de las variables independientes. Las variables:
        # radios, angulos e indices tienen n elementos cada una, por lo que le estamos agregando
        # tambien n elementos a la variable x (que incorpora ambas entradas, x1 y x2)
        x1 = radios * np.sin(angulos)
        x2 = radios * np.cos(angulos)
        x[indices] = np.c_[x1, x2]

        # Guardamos el valor de la clase que le vamos a asociar a las entradas x1 y x2 que acabamos
        # de generar
        t[indices] = clase

    return x, t

def generar_datos_clasificacion2(cantidad_ejemplos, cantidad_clases):
    FACTOR_ANGULO = 1
    AMPLITUD_ALEATORIEDAD = 0.1

    # Calculamos la cantidad de puntos por cada clase, asumiendo la misma cantidad para cada 
    # una (clases balanceadas)
    n = int(cantidad_ejemplos / cantidad_clases)

    # Entradas: 2 columnas (x1 y x2)
    x = np.zeros((cantidad_ejemplos, 2))
    # Salida deseada ("target"): 1 columna que contendra la clase correspondiente (codificada como un entero)
    t = np.zeros(cantidad_ejemplos, dtype="uint8")  # 1 columna: la clase correspondiente (t -> "target")

    randomgen = np.random.default_rng()
    
    r = np.linspace(0, 1, cantidad_clases)

    # Por cada clase (que va de 0 a cantidad_clases)...
    for clase in range(cantidad_clases):
        # Tomando la ecuacion parametrica del circulo (x = r * cos(t), y = r * sin(t)), generamos 
        # radios distribuidos uniformemente entre 0 y 1 para la clase actual, y agregamos un poco de
        # aleatoriedad
        radios = r[clase] + AMPLITUD_ALEATORIEDAD * randomgen.standard_normal(size=n)

        # ... y angulos distribuidos tambien uniformemente, con un desfasaje por cada clase
        angulos = np.linspace( - np.pi * FACTOR_ANGULO, np.pi * FACTOR_ANGULO, n)

        # Generamos un rango con los subindices de cada punto de esta clase. Este rango se va
        # desplazando para cada clase: para la primera clase los indices estan en [0, n-1], para
        # la segunda clase estan en [n, (2 * n) - 1], etc.
        indices = range(clase * n, (clase + 1) * n)

        # Generamos las "entradas", los valores de las variables independientes. Las variables:
        # radios, angulos e indices tienen n elementos cada una, por lo que le estamos agregando
        # tambien n elementos a la variable x (que incorpora ambas entradas, x1 y x2)
        x1 = radios * np.sin(angulos)
        x2 = radios * np.cos(angulos)
        x[indices] = np.c_[x1, x2]

        # Guardamos el valor de la clase que le vamos a asociar a las entradas x1 y x2 que acabamos
        # de generar
        t[indices] = clase

    return x, t


def inicializar_pesos(n_entrada, n_capa_2, n_capa_3):
    randomgen = np.random.default_rng()

    w1 = 0.1 * randomgen.standard_normal((n_entrada, n_capa_2))
    # Genera valores aleatorios con distribucion normal estandar (media 0 y desviacion estandar 1)
    b1 = 0.1 * randomgen.standard_normal((1, n_capa_2))

    w2 = 0.1 * randomgen.standard_normal((n_capa_2, n_capa_3))
    b2 = 0.1 * randomgen.standard_normal((1,n_capa_3))

    return {"w1": w1, "b1": b1, "w2": w2, "b2": b2}


def ejecutar_adelante(x, pesos,sig):
    # Funcion de entrada (a.k.a. "regla de propagacion") para la primera capa oculta
    z = x.dot(pesos["w1"]) + pesos["b1"]

    # Funcion de activacion ReLU para la capa oculta (h -> "hidden")
    if sig:
        h=sigmoid(z)
    else:
        h = np.maximum(0, z)

    # Salida de la red (funcion de activacion lineal). Esto incluye la salida de todas
    # las neuronas y para todos los ejemplos proporcionados
    y = h.dot(pesos["w2"]) + pesos["b2"]

    return {"z": z, "h": h, "y": y}


def clasificar(x, pesos,sig):
    # Corremos la red "hacia adelante"
    resultados_feed_forward = ejecutar_adelante(x, pesos,sig)
    
    # Buscamos la(s) clase(s) con scores mas altos (en caso de que haya mas de una con 
    # el mismo score estas podrian ser varias). Dado que se puede ejecutar en batch (x 
    # podria contener varios ejemplos), buscamos los maximos a lo largo del axis=1 
    # (es decir, por filas)
    max_scores = np.argmax(resultados_feed_forward["y"], axis=1)

    # Tomamos el primero de los maximos (podria usarse otro criterio, como ser eleccion aleatoria)
    # Nuevamente, dado que max_scores puede contener varios renglones (uno por cada ejemplo),
    # retornamos la primera columna
    return max_scores#[:, 0]

# x: n entradas para cada uno de los m ejemplos(nxm)
# t: salida correcta (target) para cada uno de los m ejemplos (m x 1)
# pesos: pesos (W y b)

def train(x_train, t_train, x_test, t_test, x_validation, t_validation, pesos, learning_rate, epochs, detencion_temprana,sig):
    # Cantidad de filas (i.e. cantidad de ejemplos)
    m = np.size(x_train, 0)
    
    # Cantidad de epochs a las cuales hay que revisar con el conjunto de validacion
    # para hacer una detencion temprana del entrenamiento si ya no hay mejoras
    N = detencion_temprana
    
    prevAccuracy = None # precision minima de prediccion
    
    for i in range(epochs):
        # Ejecucion de la red hacia adelante
        resultados_feed_forward = ejecutar_adelante(x_train, pesos,sig)
        y = resultados_feed_forward["y"]
        h = resultados_feed_forward["h"]
        z = resultados_feed_forward["z"]

        # LOSS
        # a. Exponencial de todos los scores
        exp_scores = np.exp(y)

        # b. Suma de todos los exponenciales de los scores, fila por fila (ejemplo por ejemplo).
        #    Mantenemos las dimensiones (indicamos a NumPy que mantenga la segunda dimension del
        #    arreglo, aunque sea una sola columna, para permitir el broadcast correcto en operaciones
        #    subsiguientes)
        sum_exp_scores = np.sum(exp_scores, axis=1, keepdims=True)

        # c. "Probabilidades": normalizacion de las exponenciales del score de cada clase (dividiendo por 
        #    la suma de exponenciales de todos los scores), fila por fila
        p = exp_scores / sum_exp_scores

        # d. Calculo de la funcion de perdida global. Solo se usa la probabilidad de la clase correcta, 
        #    que tomamos del array t ("target")
        loss = (1 / m) * np.sum( -np.log( p[range(m), t_train] ))
        

        # Mostramos solo cada N epochs
        if i % N == 0:
            # print()
            
            # Training ========================================
            
            # print("Training Loss epoch", i, ":", loss)
            
            # ACCURACY
            # aciertos/ejemplos totales
            
            cant_ejemplos = np.size(y, 0)
            accuracy = 0
            
            neurona_ganadora = np.argmax(y, axis=1) # indices de la neurona ganadora
            
            for j in range(cant_ejemplos):
                if neurona_ganadora[j]==t_train[j]: # si fue correcta la clasificacion
                    accuracy+=1
            accuracy/=cant_ejemplos
            
            # print("Training Accuracy epoch",i,":",accuracy)
            
            # Validation ========================================
            
            mm = np.size(x_validation, 0)
            resultados = clasificar(x_validation, pesos,sig)
            
            accuracy_validation = 0
            
            for j in range(mm):
                if resultados[j]==t_validation[j]: # si fue correcta la clasificacion
                    accuracy_validation+=1
            accuracy_validation/=mm
            list_accuracy.append(accuracy_validation)
            list_epochs.append(i)
            # print("Validation Accuracy epoch ",i,":",accuracy_validation)
            
            if prevAccuracy==None:
                prevAccuracy = accuracy_validation
            elif accuracy_validation<=prevAccuracy:
                # empezo a empeorar
                # print("Empeoro!!")
                prob = randint(0, 100)/100
                
                # hacemos una parada temprana en base a una probabilidad
                if False:#prob<(i/epochs): # print(prob,i/epochs)
                    break
                else:
                    prevAccuracy = accuracy_validation
            else:
                prevAccuracy = accuracy_validation
            
            

        # Extraemos los pesos a variables locales
        w1 = pesos["w1"]
        b1 = pesos["b1"]
        w2 = pesos["w2"]
        b2 = pesos["b2"]

        # Ajustamos los pesos: Backpropagation
        dL_dy = p                # Para todas las salidas, L' = p (la probabilidad)...
        dL_dy[range(m), t_train] -= 1  # ... excepto para la clase correcta
        dL_dy /= m

        dL_dw2 = h.T.dot(dL_dy)                         # Ajuste para w2
        dL_db2 = np.sum(dL_dy, axis=0, keepdims=True)   # Ajuste para b2

        dL_dh = dL_dy.dot(w2.T)
        
        if sig:
            dL_dz = dL_dh *sigmoid(z)*(1-sigmoid(z))
        else:
            dL_dz = dL_dh       # El calculo dL/dz = dL/dh * dh/dz. La funcion "h" es la funcion de activacion de la capa oculta,
            dL_dz[z <= 0] = 0   # para la que usamos ReLU. La derivada de la funcion ReLU: 1(z > 0) (0 en otro caso)

        dL_dw1 = x_train.T.dot(dL_dz)                   # Ajuste para w1
        dL_db1 = np.sum(dL_dz, axis=0, keepdims=True)   # Ajuste para b1

        # Aplicamos el ajuste a los pesos
        w1 += -learning_rate * dL_dw1
        b1 += -learning_rate * dL_db1
        w2 += -learning_rate * dL_dw2
        b2 += -learning_rate * dL_db2

        # Actualizamos la estructura de pesos
        # Extraemos los pesos a variables locales
        pesos["w1"] = w1
        pesos["b1"] = b1
        pesos["w2"] = w2
        pesos["b2"] = b2
    
    # Termino el ciclo de entrenamiento
    # print()
    # print(f" * Termino el entrenamiento en {i} epochs")
    
    # Testing ========================================
    mm = np.size(x_test, 0)
    resultados = clasificar(x_test, pesos,sig)
    
    accuracy_test = 0
    
    for j in range(mm):
        if resultados[j]==t_test[j]: # si fue correcta la clasificacion
            accuracy_test+=1
    accuracy_test/=mm
            
    print(" * Testing Accuracy epoch ",i,":",accuracy_test)

#Función sigmoide estable

def sigmoid(x):

    sig = np.where(x < 0, np.exp(x)/(1 + np.exp(x)), 1/(1 + np.exp(-x)))
    return sig   
    
    

def iniciar(numero_clases, numero_ejemplos,learnign,neuronas, graficar_datos,sig=False):
    # Generamos datos
    x_train, t_train = generar_datos_clasificacion2(round(numero_ejemplos*0.8), numero_clases)
    x_validation, t_validation = generar_datos_clasificacion2(round(numero_ejemplos*0.2),numero_clases)
    x_test, t_test = generar_datos_clasificacion2(round(numero_ejemplos*0.2), numero_clases)

    # Graficamos los datos si es necesario
    if graficar_datos:
        # Parametro: "c": color (un color distinto para cada clase en t)
        plt.scatter(x_train[:, 0], x_train[:, 1], c=t_train)
        plt.title("Entrenamiento")
        plt.show()
        
        plt.scatter(x_validation[:, 0], x_validation[:, 1], c=t_validation)
        plt.title("Validacion")
        plt.show()
        
        plt.scatter(x_test[:, 0], x_test[:, 1], c=t_test)
        plt.title("Test")
        plt.show()


    # Inicializa pesos de la red
    NEURONAS_CAPA_OCULTA = neuronas
    NEURONAS_ENTRADA = 2
    DETENCION_TEMPRANA = 20
    pesos = inicializar_pesos(n_entrada=NEURONAS_ENTRADA, n_capa_2=NEURONAS_CAPA_OCULTA, n_capa_3=numero_clases)

    # Entrena
    LEARNING_RATE=learnign
    EPOCHS=2000
    train(x_train, t_train, x_test, t_test, x_validation, t_validation, pesos, LEARNING_RATE, EPOCHS, DETENCION_TEMPRANA,sig)
aux=[]
for i in range(5):
    aux.append(20*(i+1))
    list_accuracy=[]
    list_epochs=[]
    iniciar(numero_clases=3, numero_ejemplos=400,learnign=1,neuronas=aux[i], graficar_datos=False)
    s=f"Cant. Neuronas: {round(aux[i],2)}"
    plt.plot(list_epochs,list_accuracy,label=s)
    plt.title("Precisión vs Epochs")
    
    plt.legend()  

plt.show()
