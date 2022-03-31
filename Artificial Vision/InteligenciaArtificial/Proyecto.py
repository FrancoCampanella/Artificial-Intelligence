import numpy as np
import matplotlib.pyplot as plt
import cv2
import fnmatch
import os
import math
import random
import imutils
from gtts import gTTS

class VisionArtificial:
	def __init__(self, frutas):
		self.Data = []
		self.nombres = []
		self.imagenes = []
		self.nro_img = []
		self.matriz = []
		self.frutas = frutas 
		self.fruta = None
		self.nro_frutas = 7

	def tratamiento_img(self,imagen):
		imagen = self.escalado(imagen)

		img_RGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
		gray_image = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)

		#SEGMENTACION DE IMAGEN: Umbrales 
		gaussian = cv2.GaussianBlur(gray_image, (3,3), 0.0)

		#Forma del objeto de interes
		ret, mask = cv2.threshold(gaussian, 255, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		kernel = np.ones((13,13), np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

		#Extraigo el fondo
		result = img_RGB.copy()
		result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
		result[:, :, 3] = mask
		H,S,R,G,B = self.color(result)

		#Dibujo de contornos
		contours,im = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
		with_contours = cv2.drawContours(imagen,contours,-1,(255,0,0),5) 
		with_contours = cv2.cvtColor(with_contours, cv2.COLOR_BGR2RGB)
		
		#Calculo de coeficientes de interes
		cnt = contours[0]
		M = cv2.moments(cnt)
		moments = cv2.HuMoments(M).flatten()

		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		im = img_RGB.copy()
		im = cv2.drawContours(im,[box],0,(0,0,255),2)
		x0=[box[0][0],box[0][1]]
		x1=[box[3][0],box[3][1]]
		y1=[box[1][0],box[1][1]]
		base=self.dist_euclidian(x0,x1)
		altura=self.dist_euclidian(x0,y1)
		if base<altura:
			aux=base
			base=altura
			altura=aux
		if base>=(altura-30)*2:
			base=base*2
			altura=altura*2

		#Centroide
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		with_contours = cv2.circle(with_contours,(cx,cy),20,(255,0,255),-1)
		x,y,w,h = cv2.boundingRect(cnt)
		ARec=w*h
		perimetro = float(cv2.arcLength(cnt,True))
		
		self.names = ['Original','Grises','Desenfoque','Mascara','S_Fondo','Bordes']
		self.imagenes = [img_RGB,gray_image,gaussian,mask,result,with_contours]

		#Vectorizado de la informacion 
		self.Data = [H/100]#,perimetro,w,h
		for i in range(0,4):
			if i==1:
				a=10
			elif i==2:
				a=10
			elif i==3:
				a=10**2
			else:
				a=1
			self.Data.append(float(moments[i])*a)
		
	def graficar(self, imagen=[]):
		if imagen==[]:
			cont=0
			for i in range(len(self.matriz)):
				for j in range(len(self.matriz[i])):
					plt.subplot(len(self.matriz),len(self.matriz[i]),cont+1)
					plt.imshow(self.matriz[i][j],'gray')
					if i==0: plt.title(self.names[j])
					plt.xticks([]),plt.yticks([])
					cont=cont+1
			self.matriz = []
		else:
			self.tratamiento_img(imagen)
			for j in range(len(self.imagenes)):
				plt.subplot(1,len(self.imagenes),j+1)
				plt.imshow(self.imagenes[j],'gray')
				plt.title(self.names[j])
				plt.xticks([]),plt.yticks([])
		plt.show()

	def Base_datos(self):
		if os.path.exists("Base_datos.txt"): os.remove('Base_datos.txt')
		archivo=open('Base_datos.txt','a') 
		nro = []
		for fruta in self.frutas:
			cont = 0
			path=os.getcwd()+'/'+fruta 
			archivo.write(f"{fruta}\n")
			for file in os.listdir(path):
				if fnmatch.fnmatch(file, '*.jpg'):
					direc=path + '/' + file
					imagen = cv2.imread(direc)
					self.tratamiento_img(imagen)
					self.matriz.append(self.imagenes)
					archivo.write(f"{self.Data}\n")
					cont = cont + 1
			nro.append(cont)
			self.graficar()
		archivo.write(f"END\n")
		archivo.close()
		print(f"\nSe analizaron:\n1-{self.frutas[0]}: {nro[0]}\n2-{self.frutas[1]}: {nro[1]}\n3-{self.frutas[2]}: {nro[2]}\n4-{self.frutas[3]}: {nro[3]}\n")

	
	def audio(self):
		if self.fruta == 'Naranja' or self.fruta == 'naranja':
			fruta = 'una naranja'
		elif self.fruta == 'Banana' or self.fruta == 'banana':
			fruta = 'una banana'
		elif self.fruta == 'Tomate' or self.fruta == 'tomate':
			fruta = 'un tomate'
		elif self.fruta == 'Limon' or self.fruta == 'limon':
			fruta = 'un limón'
		tts = gTTS('Veo '+fruta, lang='es',tld="com")

		with open("Sonido.mp3", "wb") as archivo:
			tts.write_to_fp(archivo)
		os.system('mpg123 -q Sonido.mp3')

		path = os.getcwd()+'/'+self.fruta
		im = random.choice(os.listdir(path))
		direc = path + '/' + im
		imagen=cv2.imread(direc)
		imagen=cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
		plt.imshow(imagen)
		plt.title(self.fruta)
		plt.show()


	def color(self,result):  #La funcion recibe una imagen enmascarada de la figura en estudio
		u = []
		for i in range(result.shape[0]):
			for j in range(result.shape[1]):
				if result[i][j][3]!=0:
					u.append(result[i][j])
		R=0
		G=0
		B=0
		for i in range(len(u)):
			R=R+u[i][0]
			G=G+u[i][1]
			B=B+u[i][2]
		R=R/len(u)
		G=G/len(u)
		B=B/len(u)
		color = np.array([R,G,B])
		min = random.choice(color)
		max = random.choice(color)
		for i in range(len(color)):
			valor = color[i]
			if valor < min:
				min = valor
			elif valor > max:
				max = valor
		if max==R and G>=B:
			H = 60*((G-B)/(max-min))
		elif max==R and G<B:
			H = 60*((G-B)/(max-min)) + 360
		elif max==G:
			H = 60*((B-R)/(max-min)) + 120
		elif max==B:
			H = 60*((R-G)/(max-min)) + 240
		if max==0:
			S=0
		else:
			S=1-(min/max)
		V=max
		return H,S,R,G,B


	def escalado(self,imagen):
		img_RGB = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
		gray_image = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
		#Extracción de la forma del objeto de interes
		ret,thresh_trunc = cv2.threshold(gray_image,254,255,cv2.THRESH_TRUNC)
	
		#Extracción de la máscara  
		ret, mask = cv2.threshold(thresh_trunc, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		kernel = np.ones((15,15), np.uint8)
		mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

		#Extracción de contornos del objeto
		contours,im = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
		cnt = contours[0]

		#Rectangulo recto
		x,y,w,h = cv2.boundingRect(cnt)

		#Recorte de la imagen según dimensiones del rectángulo
		im=img_RGB[y-18:y+h+18,x-18:x+w+18]

		#Escalado de la imagen en 300xX
		imageOut = imutils.resize(im,width=300)
		imageOut = cv2.cvtColor(imageOut, cv2.COLOR_BGR2RGB)
		return imageOut

	def k_means(self,imagen,k):
		try:
			archivo=open('Base_datos.txt','r')
			lines=archivo.readlines()
			archivo.close()

			#Se cuenta la cantidad de ejemplares muestra
			self.nro_ejemplares(lines) 

			#Selecciono un centroide de cada clase
			A=[0,0,0,0]
			c = []
			c.append(self.vec_tofloat(lines[random.randint(1,self.nro_img[0]-1)]))
			c.append(self.vec_tofloat(lines[random.randint(self.nro_img[0]+1,self.nro_img[1]-1)]))
			c.append(self.vec_tofloat(lines[random.randint(self.nro_img[1]+1,self.nro_img[2]-1)]))
			c.append(self.vec_tofloat(lines[random.randint(self.nro_img[2]+1,self.nro_img[3]-1)]))	
			
			self.tratamiento_img(imagen)
			err=10
			while err>math.pow(10,-3):
				vect = []
				posiciones = []
				for v in c:
					dist = []
					for i in range(len(lines)):
						if lines[i][:-1]!=self.frutas[0] and lines[i][:-1]!=self.frutas[1] and lines[i][:-1]!=self.frutas[2] and lines[i][:-1]!=self.frutas[3] and lines[i][:-1]!='END':
							w = self.vec_tofloat(lines[i])
							d = self.dist_euclidian(v,w)
							if d!=0:
								dist.append(float(d))
							if v==c[3]:
								vect.append(w)
					posiciones.append(self.menor(dist,7))
				
				err = [0,0,0,0]
				for j in range(len(posiciones)):
					v = posiciones[j]
					aux = []
					for i in range(len(v)):
						#Armado de cada una de las clases
						aux.append(vect[v[i]])
					w = self.media(aux)
					err[j] = self.dist_euclidian(w,c[j])
					c[j] = w
	
				#GRAFICO DE DISPERSION
				for j in range(len(posiciones)):
					v = posiciones[j]
					for i in range(len(v)):
						if j==0:
							marker='yo'
							if i==6: ax.plot(float(vect[v[i]][0]),float(vect[v[i]][1]),marker,label=self.frutas[j])
						elif j==1:
							marker='bp'
							if i==6: ax.plot(float(vect[v[i]][0]),float(vect[v[i]][1]),marker,label=self.frutas[j])
						elif j==2:
							marker='rx'
							if i==6: ax.plot(float(vect[v[i]][0]),float(vect[v[i]][1]),marker,label=self.frutas[j])
						elif j==3:
							marker='g1'
							if i==6: ax.plot(float(vect[v[i]][0]),float(vect[v[i]][1]),marker,label=self.frutas[j])
						if i!=6:
							ax=plt.gca()
							ax.plot(float(vect[v[i]][0]),float(vect[v[i]][1]),marker)
					ax.plot(float(c[j][0]),float(c[j][1]),'kD')
				ax.plot(float(self.Data[0]),float(self.Data[1]),'rD')
				plt.title("H vs Hu_mom[0]")
				plt.xlabel("Color")
				plt.ylabel("Primer mto de Hu")
				plt.legend()
				plt.show()

				#HISTOGRAMA
				for j in range(len(posiciones)):
					v = posiciones[j]
					f = []
					for i in range(len(v)):
						if v[i]<=6:
							f.append(self.frutas[0])
						elif v[i]>=7 and v[i]<14:
							f.append(self.frutas[1])
						elif v[i]>=14 and v[i]<21:
							f.append(self.frutas[2])
						elif v[i]>=21 and v[i]<28:
							f.append(self.frutas[3])
					plt.subplot(1,len(self.frutas),j+1)
					plt.hist(f,4,[0,4])
					plt.title(self.frutas[j])
				plt.show()

				err = sum(err)/len(err)
				
			dist_c = []
			for v in c:
				dist_c.append(self.dist_euclidian(v,self.Data))
			pos = self.menor(dist_c,k=1)
			self.fruta = self.frutas[pos[0]]

		except FileNotFoundError:
			print("Error: Base de datos inexistente\n")

	def k_nn(self,imagen,k):
		self.tratamiento_img(imagen)
		d = []
		try:
			self.archivo=open('Base_datos.txt','r')
			lines=self.archivo.readlines()
			self.archivo.close()
			#Distancia euclidiana del vector de interes a los vectores de la base de datos
			vect = []
			for i in range(len(lines)):
				if lines[i][:-1]!=self.frutas[0] and lines[i][:-1]!=self.frutas[1] and lines[i][:-1]!=self.frutas[2] and lines[i][:-1]!=self.frutas[3] and lines[i][:-1]!='END':
					w = self.vec_tofloat(lines[i])
					dist = self.dist_euclidian(self.Data,w)
					d.append(dist)
					vect.append(w)
			#Calculo de las k menores distancias del vector objetivo respecto a la base 
			posiciones = self.menor(d,k)
			pos_max = random.choice(posiciones)
			for valor in posiciones:
				if valor > pos_max:
			    		pos_max = valor
			#GRAFICO DE CLASES
			for i in range(len(vect)):
				if i <= 6:
					marker='yo'
					if i==6: ax.plot(float(vect[i][0]),float(vect[i][1]),marker,label=self.frutas[0])
				elif i >= 7 and i < 14:
					marker='bp'
					if i==13: ax.plot(float(vect[i][0]),float(vect[i][1]),marker,label=self.frutas[1])
				elif i >= 14 and i < 21:
					marker='rx'
					if i==20: ax.plot(float(vect[i][0]),float(vect[i][1]),marker,label=self.frutas[2])
				elif i >= 21 and i < 28:
					marker='g1'
					if i==27: ax.plot(float(vect[i][0]),float(vect[i][1]),marker,label=self.frutas[3])
				if i!=6 and i!=13 and i!=20 and i!=27:
					ax=plt.gca()
					ax.plot(float(vect[i][0]),float(vect[i][1]),marker)
			ax.plot(float(self.Data[0]),float(self.Data[1]),'kD')
			plt.title("H vs Hu_mom[0]")
			plt.xlabel("Color")
			plt.ylabel("Primer mto de Hu")
			plt.legend()
			plt.show()

			
			#Identificacion de la fruta en estudio
			n=0
			b=0
			t=0
			l=0
			#HISTOGRAMA  
			f = []
			for i in range(len(posiciones)):
				if posiciones[i] <= 6:
					n=n+1
					f.append(self.frutas[0])
				if posiciones[i] >= 7 and posiciones[i] < 14:
					b=b+1
					f.append(self.frutas[1])
				if posiciones[i] >= 14 and posiciones[i] < 21:
					t=t+1
					f.append(self.frutas[2])
				if posiciones[i] >= 21 and posiciones[i] < 28:
					l=l+1
					f.append(self.frutas[3])
			plt.hist(f,4,[0,4])

			ide = [n,b,t,l]
			M=random.choice(ide)
			for valor in ide:
				if valor > M:
			    		M = valor
			i=0
			while ide[i] != M:
				i=i+1
			self.fruta = self.frutas[i]
			plt.title(self.fruta)
			plt.show()

		except FileNotFoundError:
			print("Error: Base de datos inexistente\n")
						
	def menor(self,lista,k):
		it=0
		posiciones = []
		while it<k:
			menor = random.choice(lista)
			for valor in lista:
				if valor < menor:
			    		menor = valor
			i=0
			while lista[i] != menor:
				i=i+1
			posiciones.append(i)
			lista.pop(i)
			lista.insert(i,500)
			it=it+1
		return posiciones

	def dist_euclidian(self,v,w):
		sum=0
		for i in range(len(w)):
			sum = sum + math.pow((float(v[i])-float(w[i])),2)
		return math.sqrt(sum)

	def vec_tofloat(self,w):
		w=w.split(',')
		w[0]=w[0][1:]
		w[len(w)-1]=w[len(w)-1][:-2]
		return w
	
	def nro_ejemplares(self, b_datos):
		for i in range(len(b_datos)):
			if b_datos[i][:-1]==self.frutas[0]:
				cont = 0
			elif b_datos[i][:-1]==self.frutas[1] or b_datos[i][:-1]==self.frutas[2] or b_datos[i][:-1]==self.frutas[3] or b_datos[i][:-1]=='END':
				cont = cont + 1
				self.nro_img.append(cont)
			else:
				cont = cont + 1

	def media(self,matriz):
		data = []
		for j in range(len(matriz[0])):
			sum = 0
			for i in range(len(matriz)):
				sum = sum + float(matriz[i][j])
			media = sum/len(matriz)
			data.append(media)
		return data
