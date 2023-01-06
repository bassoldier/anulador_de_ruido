from tkinter import *
from tkinter import filedialog
import pyaudio
import glob
import os
import wave
import threading
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as waves
import matplotlib
import time as timelib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from detector_agresividad import DetectorAgr

class Ventana:
	raiz=Tk()
	
	grabando=False
	reproduciendo=False
	CHUNK=1024
	data=""
	stream=""
	f=""
	contador=0
	contador1=0
	contador2=0

	flag=False

	btnIniciar=0
	btnDir=0
	btnAbrir=0
	btnParar=0
	time=0
	frame=0
	frameCenter=0
	resultado=0
	selectModel=0
	variable=0

	textoAgresivo=0
	textoNoAgresivo=0
	textoClase=0

	archivo="/Users/diego/Desktop/ILOGICA/ESTUDIO/detector_agresividad/DetectorDeAgresividadEnVoz/"

	def crearVentana(self):
		self.raiz.title('DETECTOR DE AGRESIVIDAD EN VOZ')

		self.raiz.resizable(0,0)

		self.raiz.geometry("850x600")

		self.mostrarInicio()

		self.raiz.mainloop()


	def mostrarInicio(self):
		self.crearFrameUp()
		self.crearFrameCenter()
		self.crearFrameDown()


	def crearFrameCenter(self):
		global frameCenter
		frameCenter=Frame()
		frameCenter.pack()
		frameCenter.config(bg="white")
		frameCenter.config(width="800",height="450")

		frameCenter.config(bd="5")
		frameCenter.config(relief="groove")


	def crearFrameDown(self):
		global textoClase
		global textoNoAgresivo
		global textoAgresivo
		desp=280
		desp2=598

		frameDown=Frame()
		frameDown.pack()
		frameDown.config(width="800",height="95")

		labelAgresivo=Label(frameDown, text="% Prec. Agresivo:", height=2)
		labelAgresivo.config(fg="black", font=("Verdana"))
		labelAgresivo.place(x=-4, y=15)

		textoAgresivo=Entry(frameDown)
		textoAgresivo.place(x=145, y=28)
		


		labelNoAgresivo=Label(frameDown, text="% Prec. No Agresivo:", height=2)
		labelNoAgresivo.config(fg="black", font=("Verdana"))
		labelNoAgresivo.place(x=5 + desp, y=15)

		textoNoAgresivo=Entry(frameDown)
		textoNoAgresivo.place(x=183 + desp, y=28)

		labelClase=Label(frameDown, text="Clase:", height=2)
		labelClase.config(fg="black", font=("Verdana"))
		labelClase.place(x=10 + desp2, y=15)

		textoClase=Entry(frameDown)
		textoClase.place(x=65 + desp2, y=28)


	def clear_contador(self):
	    global contador,contador1,contador2
	    contador=0
	    contador1=0
	    contador2=0



	def formato(self, c):
	    if c<10:
	        c="0"+str(c)
	    return c
	  

	def cuenta(self):
	    global proceso
	    global contador,contador1,contador2
	    time['text'] = str(self.formato(contador1))+":"+str(self.formato(contador2))+":"+str(self.formato(contador))
	    contador+=1
	    if contador==60:
	        contador=0
	        contador2+=1
	    if contador2==60:
	        contador2=0
	        contador1+=1
	    proceso=time.after(1000, self.cuenta)

	def iniciar(self):
	    global grabando
	    global proceso
	    global act_proceso
	    global btnParar

	    btnParar.config(state='active')
	    self.clear_contador()
	    audio=pyaudio.PyAudio()
	    self.bloqueo('disabled')
	    grabando=True
	    FORMAT=pyaudio.paInt16
	    CHANNELS=1
	    RATE=44100
	    act_proceso=True
	    t1=threading.Thread(target=self.grabacion, args=(FORMAT,CHANNELS,RATE,self.CHUNK,audio,self.archivo+"grabacion.wav"))
	    t=threading.Thread(target=self.cuenta)
	    t1.start()
	    t.start()

	def abrir(self):
	    global data
	    global stream
	    global f
	    global reproduciendo
	    self.clear_contador()
	    audio=pyaudio.PyAudio()
	    open_archive=filedialog.askopenfilename(initialdir = "/",
	                 title = "Seleccione archivo",filetypes = (("wav files","*.wav"),
	                 ("all files","*.*")))
	    if open_archive!="":
	        reproduciendo=True
	        f = wave.open(open_archive,"rb")
	        stream = audio.open(format = audio.get_format_from_width(f.getsampwidth()),  
	                    channels = f.getnchannels(),  
	                    rate = f.getframerate(),
	                    output = True)
	        data = f.readframes(self.CHUNK)
	        self.bloqueo('disabled')



	        t=threading.Thread(target=self.cuenta)
	        t.start()
	        t2=threading.Thread(target=self.reproduce)
	        t2.start()

	def reproducir(self):
	    global data
	    global stream
	    global f
	    global reproduciendo

	    self.clear_contador()
	    audio=pyaudio.PyAudio()
	    if self.archivo + "grabacion.wav" !="":
	        reproduciendo=True
	        f = wave.open(self.archivo + "grabacion.wav","rb")
	        stream = audio.open(format = audio.get_format_from_width(f.getsampwidth()),  
	                    channels = f.getnchannels(),  
	                    rate = f.getframerate(),
	                    output = True)
	        data = f.readframes(self.CHUNK)
	        self.bloqueo('disabled')



	        t=threading.Thread(target=self.cuenta)
	        t.start()
	        t2=threading.Thread(target=self.reproduce)
	        t2.start()

	def grabacion(self, FORMAT,CHANNELS,RATE,CHUNK,audio,archivo):
	    global resultado
	    global textoClase
	    global textoNoAgresivo
	    global textoAgresivo
	    global variable
	    stream=audio.open(format=FORMAT,channels=CHANNELS,
	                          rate=RATE, input=True,
	                          frames_per_buffer=CHUNK)

	    frames=[]

	    while grabando==True:
	        data=stream.read(CHUNK)
	        frames.append(data)

	    #DETENEMOS GRABACIÓN
	    stream.stop_stream()
	    stream.close()
	    audio.terminate()

	    #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
	    waveFile = wave.open(archivo, 'wb')
	    waveFile.setnchannels(CHANNELS)
	    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	    waveFile.setframerate(RATE)
	    waveFile.writeframes(b''.join(frames))
	    waveFile.close()

	    self.insertarGrafico()
	    detector=DetectorAgr()

	    resultado=detector.procesar(self.archivo + "grabacion.wav", variable.get())

	    textoAgresivo.delete(0,END)
	    textoNoAgresivo.delete(0,END)
	    textoClase.delete(0,END)

	    textoAgresivo.insert(0,str(resultado[1][0]))
	    textoNoAgresivo.insert(0,str(resultado[1][1]))

	    if resultado[0]==0.0:
	        sentimiento="AGRESIVO"
	    else:
	       sentimiento="NO AGRESIVO"

	    textoClase.insert(0,sentimiento)


	def reproduce(self):
	    global data
	    global stream
	    global f
	    audio=pyaudio.PyAudio() 
	    while data and reproduciendo==True:  
	        stream.write(data)  
	        data = f.readframes(self.CHUNK)  
	 
	    stream.stop_stream()  
	    stream.close()  
	 
	    audio.terminate()
	    time.after_cancel(proceso)
	    self.bloqueo('normal')


	def bloqueo(self, s):
	    btnIniciar.config(state=s)
	    btnDir.config(state=s)
	    selectModel.config(state=s)


	    
	def parar(self):
	    global grabando
	    global reproduciendo
	    if grabando==True:
	        grabando=False
	        time.after_cancel(proceso)
	        self.clear_contador()
	    elif reproduciendo==True:
	        reproduciendo=False
	    self.bloqueo('normal')


	def direc(self):
	    directorio=filedialog.askdirectory()
	    if directorio!="":
	        os.chdir(directorio)


	def insertarGrafico(self):
		muestreo, sonido = waves.read(self.archivo + "grabacion.wav")

		# canales: monofónico o estéreo
		tamano = np.shape(sonido)
		muestras = tamano[0]
		m = len(tamano)
		canales = 1  # monofónico
		if (m>1):  # estéreo
		    canales = tamano[1]
		# experimento con un canal
		if (canales>1):
		    canal = 0
		    uncanal = sonido[:,canal] 
		else:
		    uncanal = sonido


		fig , ax1 = plt.subplots(figsize=(8, 4), dpi=100)
		ax1.set_title("Grabación") #titulo
		ax1.set_xlabel('Tiempo (Segundos)') #nombre del eje x
		ax1.set_ylabel('Amplitud') #nombre del eje y

		ax1.plot(uncanal) #genero el boxplot


		formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: timelib.strftime('%M:%S', timelib.gmtime(ms // 1000)))
		ax1.xaxis.set_major_formatter(formatter)


		
		#ELIMINAMOS TODO LO QUE TENGA EL FRAME
		for child in frameCenter.winfo_children(): child.destroy() 
			

		canvas = FigureCanvasTkAgg(fig, master=frameCenter)  # CREAR AREA DE DIBUJO DE TKINTER.
		

		#-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
		toolbar = NavigationToolbar2Tk(canvas, frameCenter)# barra de iconos
		toolbar.update()
		canvas.get_tk_widget().pack(expand=1)



	def crearFrameUp(self):
		global btnIniciar
		global btnDir
		global btnAbrir
		global btnParar
		global time
		global frame
		global selectModel
		global variable

		time = Label(self.raiz, fg='green', width=20, text="00:00:00", bg="black", font=("","30"))
		time.pack()
		frame=Frame(self.raiz)

		variable = StringVar(frame)
		variable.set('Corpus Híbrido')
		opciones=['Corpus Híbrido', 'Corpus Chileno', 'Corpus Británico (SAVEE)']
		selectModel=OptionMenu(frame,variable, *opciones)
		selectModel.config(width=20)
		selectModel.grid(row=1, column=0)

		btnIniciar=Button(frame, fg='red',width=16, text='Grabar', command=self.iniciar)
		btnIniciar.grid(row=1, column=2)

		btnParar=Button(frame, fg='blue', width=16, text='Parar', command=self.parar)
		btnParar.grid(row=1, column=3)

		btnDir=Button(frame, fg='green',text="Reproducir",width=16, command=self.reproducir)
		btnDir.grid(row=1,column=1)

		btnDir.config(state='disabled')
		btnParar.config(state='disabled')
		frame.pack()