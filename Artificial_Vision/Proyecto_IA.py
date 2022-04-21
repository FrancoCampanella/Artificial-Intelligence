from Proyecto import VisionArtificial
import numpy as np
import matplotlib.pyplot as plt
import cv2
import fnmatch
import os
import math
import random
from gtts import gTTS
from cmd import Cmd 


class CLI(Cmd):
	doc_header = "                   Ayuda de comandos documentados                   "
	undoc_header = "                   Ayuda de comandos no documentados                   "
	frutas = None
	ojo_artif = None
	imagen = None

	def do_iniciar(self, args):
		"""Inicializa el sistema y carga las frutas que se reconocerán"""
		if self.ojo_artif == None:
			self.frutas = ['Banana','Naranja','Tomate','Limon']
			self.ojo_artif = VisionArtificial(self.frutas)
		else:
			print("Error: el sistema ya ha sido inicializado")

	def do_basedatos(self, args):
		"""Actualiza la base de datos del sistema. Crea un archivo .txt en el host"""
		try:
			self.ojo_artif.Base_datos()
		except NameError:
			print("Error: inicialice el sistema previamente\n")
		except AttributeError:
			print("Error: inicialice el sistema previamente\n")

	def do_fruta(self,args):
		"""Actualiza la fruta en analisis"""
		fruta=input("Introduzca el nombre de la fruta que desea analizar:\n")
		fruta=fruta + ".jpg"
		self.imagen = cv2.imread(fruta)

	def do_knn(self, args): #k=5
		"""Ejecución del algoritmo supervisado knn"""
		try:
			if np.all(self.imagen)!=None:
				k=int(input("Ingrese k:\n"))
				self.ojo_artif.k_nn(self.imagen,k)
				self.ojo_artif.audio()
			else:
				fruta=input("Introduzca el nombre de la fruta que desea analizar:\n")
				fruta=fruta + ".jpg"
				self.imagen = cv2.imread(fruta)
				k=int(input("Ingrese k:\n"))
				self.ojo_artif.k_nn(self.imagen,k)
				self.ojo_artif.audio()
			i=int(input("Desea ejecutar el algoritmo kmeans?\n1-Si\n2-No\n"))
			if i==1:
				self.do_kmeans("\n")
		except NameError:
			print("Error: inicialice el sistema previamente\n")

	def do_kmeans(self, args):
		"""Ejecución del algoritmo no supervisado kmeans"""
		try:
			if np.all(self.imagen)!=None:
				self.ojo_artif.k_means(self.imagen,len(self.frutas))
				self.ojo_artif.audio()
			else:
				fruta=input("Introduzca el nombre de la fruta que desea analizar:\n")
				fruta=fruta + ".jpg"
				self.imagen = cv2.imread(fruta)
				self.ojo_artif.k_means(self.imagen,len(self.frutas))
				self.ojo_artif.audio()
			i=int(input("Desea ejecutar el algoritmo knn?\n1-Si\n2-No\n"))
			if i==1:
				self.do_knn("\n")
		except NameError:
			print("Error: inicialice el sistema previamente\n")

	def do_graficar(self, args):
		"""Grafica los elementos que conforman la base de conocimiento del sistema"""
		try:
			if np.all(self.imagen)!=None:
				self.ojo_artif.graficar(self.imagen)
			else:
				fruta=input("Introduzca el nombre de la fruta que desea analizar:\n")
				fruta=fruta + ".jpg"
				self.imagen = cv2.imread(fruta)
				self.ojo_artif.graficar(self.imagen)
		except NameError:
			print("Error: inicialice el sistema previamente\n")

	def do_quit(self, args):
		print("Ejecucion terminada")
		raise SystemExit

	def default(self, args):
		print("Error. El comando \'" + args + "\' no esta disponible")

	def precmd(self, args):
		args = args.lower()
		return(args) 

uncli = CLI()
uncli.prompt = '- '
uncli.cmdloop('Iniciando entrada de comandos...')
