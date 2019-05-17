# -*- coding: utf-8 -*-
#!/usr/bin/python2.7.13

import os
import sys
import socket
import time
import tkFont
import pygame
import serial
import Tkinter as tk
from Tkinter import *
from threading import Thread
import tkMessageBox
import RPi.GPIO as GPIO
import Tkinter
import Image, ImageTk
import pexpect
import alsaaudio
#from camara import camaras
from variables import var as vg
from inicio import iniciar
from tarea  import tareas
import gc
import vlc



backlight = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(backlight, GPIO.OUT)
GPIO.output(backlight, GPIO.HIGH)


#uart = serial.Serial(port='/dev/ttyAMA0', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1)


n_foto = 0
c_f = 1

f_boton_estado = False
p1 = False
p2 = False
clicks = 0


def motion(event):
	global p1,p2,clicks

	vg.tiempolcdon = vg.TLCD
	GPIO.output(backlight, GPIO.HIGH)
	x, y = event.x, event.y
	#print('{}, {}'.format(x, y))
	#clicks += 1
	#print clicks
	if(x > 105 and x < 205 and y < 50):
		p1 = True
		#print "p1=True"
	if(x > 950 and y < 50 and p1 == True):
		p2 = True
		#print "p2=True"
	if(x > 100 and x < 205 and y > 530 and p2 == True):
		salir()
	if(clicks > 40):
		p1 = p2 = False
		clicks = 0



#	if(x > 950 and y > 530):
#		sreboot += 1
#
#	if(sreboot > 20):
#		os.system("sudo reboot")



class boton_press(tk.Frame):

	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.button = tk.Button(self, text="Hablar",width=10, height=5)
		self.button.grid(row=10, column=2, sticky="w")

		self.button.bind("<ButtonPress>", self.presionado)
		self.button.bind("<ButtonRelease>", self.suelto)

	def suelto(self, event):
		global  f_habilitar_handi

		print "boton liberado"
		if vg.f_habilitar_handi == True:
			GPIO.output(talk_handi, GPIO.LOW)
			##Mando al porton que se Soloto TALK.
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((vg.HOST, vg.PORT))
			s.sendall('4')
			time.sleep(2)
			data = s.recv(32)
			s.close()

	def presionado(self, event):

		print "boton presionado"
		if vg.f_habilitar_handi == True:
			GPIO.output(talk_handi, GPIO.HIGH)
			##Mando al porton que se Soloto TALK.
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((vg.HOST, vg.PORT))
			s.sendall('5')
			time.sleep(2)
			data = s.recv(32)
			s.close()



def estado_porton():
	global porton

	if vg.f_estado_porton == True:
		porton.config(bg = 'red')
		porton.config(text = 'Porton Abierto')
	else:
		porton.config(bg = 'green')
		porton.config(text = 'Porton Cerrado')





def reboot():
	vg.sreboot += 1
	if(vg.sreboot > 6):
		os.system("sudo reboot")
	#salir()



def estado_conexion():
	global b_conexion

	if vg.f_estado_conexion == True:
		b_conexion.config(text = 'Conectado')
		b_conexion.config(bg = 'green')
	else:
		b_conexion.config(text = 'Desconectado')
		b_conexion.config(bg = 'red')




def cartel_info(msj):
	Botones  = tkFont.Font(family = 'Helvetica', size = 15, weight = 'bold')

	v_info = Tkinter.Toplevel(root)
	v_info.title('Espere por favor...')
	v_info.overrideredirect(1)
	v_info.geometry("200x120+380+250")    #Ancho alto y posicion WxH, X,Y
	v_info.focus_set()

	v = StringVar()
	Label(v_info, font = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold'), textvariable=v).pack()
	v.set(msj)

	cerrar_v_info = Button(v_info, text="Salir", font = Botones, width=8, height=3,anchor = "center", background= "gray",bd = 2, command=v_info.destroy)
	cerrar_v_info.pack()




##
##def fondo_y_logo():
##	# abrimos una imagen Del barrio
##	img1 = Image.open('/home/pi/s_domotica/fondo_sistema.png')
##	tkimage1 = ImageTk.PhotoImage(img1)
##	# Ponemos la imagen en un Lable dentro de la ventana
##	imagen1 = Tkinter.Label(root, relief=RAISED,image=tkimage1) #, width=imagenAnchuraMaxima, height=imagenAlturaMaxima)
##	imagen1.place(x=0, y=0, relwidth=1, relheight=1) #pack() #grid(row=1, column = 3, columnspan = 3, sticky=NW)#.pack()




def conexion():
	global player

	print "run 5 SEGUNDOS"
	if vg.f_servidor_una_vez:
		os.system("python /home/pi/s_domotica/" + vg.version + "/servidor_cliente.py &")
		os.system("python /home/pi/s_domotica/" + vg.version + "/servidor_foto.py &")
		vg.f_servidor_una_vez = False

	if vg.f_tiempo_foto == True:
		vg.cont_foto = vg.cont_foto + 1
		print "cont_foto:" , str(vg.cont_foto)
		print "tiempo default fotos" , str(vg.tiempo_foto_on)
		#print vg.cont_foto

	if (vg.cont_foto >= vg.tiempo_foto_on):
		player.stop()
		print "Mato VLC foto"
		vg.cont_foto = 0
		vg.f_tiempo_foto = False

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((vg.HOST, vg.PORT))
		s.sendall('1')
		c_data = s.recv(32)
		s.close()
	except:
		c_data = "error"
		print "No conectado"

	print 'Recibo:', str(c_data)

    ##Chequeo Conexion
	if c_data[0] == "p":

		vg.f_estado_conexion = True
		estado_conexion()
		if vg.f_conectado == False:
			con = open ('/home/pi/s_domotica/conectividad_log.txt','a')
			con.write("Ping: %s - %s - CONECTADO\n" %(vg.HOST ,time.strftime("%c")))
			con.close()
			vg.f_conectado = True
	else:
		vg.f_estado_conexion = False
		estado_conexion()
		if vg.f_conectado:
			con = open ('/home/pi/s_domotica/conectividad_log.txt','a')
			con.write("Ping: %s - %s - DESCONECTADO\n" %(vg.HOST ,time.strftime("%c")))
			con.close()
			vg.f_conectado = False

	##Chequeo PORTON
	if c_data[1] == "a":
		vg.f_estado_porton = True
	else:
		vg.f_estado_porton = False

	return False




#def horayfecha():
#	hs = Label(root, text = time.strftime("%b %d %Y %H:%M:%S"), bd = 0, justify = LEFT,relief=RAISED, width=120, height=1)
#	hs.grid(row=12, column=3)
#	print  time.strftime("%b %d %Y %H:%M:%S")

def habilitar_botnes(status):
	global cam1, cam2, cam3, cam4,porton

	cam1.config(state = status)
	cam2.config(state = status)
	cam3.config(state = status)
	cam4.config(state = status)
	porton.config(state = status)


def actualizacion():
	global n_foto, player, h_actual,hs



	if vg.f_mostrar_ventana_esperar == True:
		#esperar_info()
		#tkMessageBox.showinfo("Title", "a Tk MessageBox")
		vg.f_mostrar_ventana_esperar = False

	vg.tiempolcdon -= 1
	if vg.tiempolcdon <= 0:
		GPIO.output(backlight, GPIO.LOW)
		vg.tiempolcdon = 0

	if vg.f_tiempo_camara == True:
		vg.cont_camara += 1


	if vg.f_muestro_foto == True:
		#os.system("cvlc -f --xlib --no-osd /home/pi/s_domotica/historial/foto.jpg &")
		player=vlc.MediaPlayer('/home/pi/s_domotica/historial/foto.jpg')#'rtsp://admin:martin1422@192.168.1.10:554/h264/ch1/main/av_stream')
		player.set_fullscreen(True)
		player.play()
		vg.f_muestro_foto = False


	vg.cont_boton_porton +=1
	if vg.cont_boton_porton >= 10:
		vg.f_boton_abrir_porton = True
		vg.cont_boton_porton = 10
		print "Habilito boton PORTON"

	print "corriendo 1seg"
	print vg.f_tiempo_camara
	if vg.cont_camara >= vg.tiempo_cam_on:
		player.stop()
		print "Kill VLC Camara"
		vg.cont_camara = 0
		vg.f_tiempo_camara = False
		habilitar_botnes('normal')
		vg.f_boton_presionado_porton = True



	c = open ('/home/pi/s_domotica/' + vg.version + '/comunicacion','r')
	vg.c_dato = str(c.read(1))
	c.close()

	if vg.c_dato == "1":
		c = open ('/home/pi/s_domotica/' + vg.version + '/comunicacion','w')
		c.write("0")
		c.close()

		print "Reproduccion mp3..."
		player.stop()
		vg.tiempolcdon = vg.TLCD
		GPIO.output(backlight, GPIO.HIGH)
		m = alsaaudio.Mixer('PCM')
		current_volume = m.getvolume() # Get the current Volume
		m.setvolume(vg.volumen) # Set the volume to 70%.
		player=vlc.MediaPlayer('/home/pi/s_domotica/V1.08/Sonidos/nohaynadie.mp3')
		player.play()


		vg.cont_foto = 0
		vg.f_tiempo_foto = True
		#vg.f_tiempo_camara = True
		#vg.cont_camara = 0
		n_foto = n_foto + 1
		cadena = "mv foto.jpg foto" + str(n_foto) + ".jpg"
		print cadena
		vg.f_muestro_foto = True

	estado_porton()
	h_actual.set(time.strftime("%b %d %Y %H:%M:%S"))
	return False





def abrir_porton():
	global player


	#esperar_info()
	vg.f_boton_abrir_porton = False
	vg.cont_boton_porton = 0

	if vg.f_boton_presionado_porton == True:
		vg.f_boton_presionado_porton = False
		habilitar_botnes('disable')

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((vg.HOST, vg.PORT))
			s.sendall('2')
			data = s.recv(32)
			print data
			s.close()
		except:
			data = "error"
			print "Esperando respuesta porton"

		if data == 'pulso':
			cartel_info("Porton en movimiento")
			#ca.camara_1()
			#tkMessageBox.showinfo("Informacion", "Porton en movimiento")
		else:
			cartel_info("Porton ocupado")
			#ca.camara_1()
		player=vlc.MediaPlayer(vg.camara1)#'rtsp://admin:martin1422@192.168.1.10:554/h264/ch1/main/av_stream')
		player.set_fullscreen(True)
		player.play()
		vg.f_tiempo_camara = True


		##Guardo cada vez que le doy abrir_porton
		print "Guardando estado PORTON"
		con = open ('/home/pi/s_domotica/conectividad_log.txt','a')
		con.write("Abrio/Cerro: %s - %s - PORTON\n" %(vg.HOST ,time.strftime("%c")))
		con.close()




def salir():
	os.system("sudo pkill python")
	os.system("sudo pkill python")
	os.system("sudo pkill python")
	os.system("sudo pkill python")
	exit()
	return





def hablar():
	# global v_contestar, f_boton_estado, f_habilitar_handi

	# if f_habilitar_handi == True:
		# if f_boton_estado == True:
			# v_contestar.set("Hablar")
			# GPIO.output(talk_handi, GPIO.HIGH)
			# f_boton_estado = False
			# #button.configure(bg = "red")
		# else:
			# v_contestar.set("No hablar")
			# GPIO.output(talk_handi, GPIO.LOW)
			# f_boton_estado = True
			#button.configure(bg = "blue")
	return

def mostrar_foto():

	return

def rechazar():
	# global f_habilitar_handi
	# GPIO.output(power_handi, GPIO.LOW) #Apago el handi
	# GPIO.output(talk_handi, GPIO.LOW)

	# ##Mandar Cortar
	# if f_habilitar_handi == True:
		# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# s.connect((HOST, PORT))
		# s.sendall('0') #Cortar comunicacion
		# #time.sleep(2)
		# data = s.recv(32)
		# s.close()
	# f_habilitar_handi = False
	return

def camara_1():
	global player
	vg.sreboot = 0
	vg.f_tiempo_camara = True
	vg.f_mostrar_ventana_esperar = True
	player=vlc.MediaPlayer(vg.camara1)
	player.set_fullscreen(True)
	player.play()
	habilitar_botnes('disable')

def camara_2():
	global player
	vg.sreboot = 0
	vg.f_tiempo_camara = True
	vg.f_mostrar_ventana_esperar = True
	player=vlc.MediaPlayer(vg.camara2)#'rtsp://admin:martin1422@192.168.1.10:554/h264/ch2/main/av_stream')
	player.set_fullscreen(True)
	player.play()
	habilitar_botnes('disable')

def camara_3():
	global player
	vg.sreboot = 0
	vg.f_tiempo_camara = True
	vg.f_mostrar_ventana_esperar = True
	player=vlc.MediaPlayer(vg.camara3)#'rtsp://admin:martin1422@192.168.1.10:554/h264/ch3/main/av_stream')
	player.set_fullscreen(True)
	player.play()
	habilitar_botnes('disable')

def camara_4():
	global player
	vg.sreboot = 0
	vg.f_tiempo_camara = True
	vg.f_mostrar_ventana_esperar = True
	player=vlc.MediaPlayer(vg.camara4)#'rtsp://admin:martin1422@192.168.1.10:554/h264/ch4/main/av_stream')
	player.set_fullscreen(True)
	player.play()
	habilitar_botnes('disable')





#class ventana:


#	def __init__(self, root):
#		root.attributes('-fullscreen', True)


#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
root = Tk()
root.attributes('-fullscreen', True)




v = StringVar()
v_contestar = StringVar()
ruta_fondo = StringVar()
root.bind('<Motion>', motion)

i = iniciar.ini()

# abrimos una imagen Del barrio
img1 = Image.open('/home/pi/s_domotica/fondo_sistema.png')
img1.thumbnail((vg.imagenAnchuraMaxima1, vg.imagenAlturaMaxima1), Image.ANTIALIAS)
# Convertimos la imagen a un objeto PhotoImage de Tkinter
tkimage1 = ImageTk.PhotoImage(img1)
# Ponemos la imagen en un Lable dentro de la ventana
imagen1 = Tkinter.Label(root, image=tkimage1) #, width=imagenAnchuraMaxima, height=imagenAlturaMaxima)
imagen1.place(x=0, y=0, relwidth=1, relheight=1) #pack() #grid(row=1, column = 3, columnspan = 3, sticky=NW)#.pack()




#c = camaras.cam()
#i = iniciar.ini()
#i.incializar_variables()
i.verficacionMAC()


player=vlc.MediaPlayer(vg.camara1)
player.stop()

estado = StringVar()
estado = 'normal'

h_actual = StringVar()
h_actual.set( time.strftime("%b %d %Y %H:%M:%S"))

cam1 = Button(root,state = estado, text="Camara 1", width=10, height=3, command = camara_1)
cam1.grid(row=2, column=2, sticky="w")

cam2 = Button(root,state = estado, text="Camara 2", width=10, height=3, command = camara_2)
cam2.grid(row=3, column=2, sticky="w")

cam3 = Button(root,state = estado, text="Camara 3", width=10, height=3, command = camara_3)
cam3.grid(row=4, column=2, sticky="w")

cam4 = Button(root,state = estado, text="Camara 4", width=10, height=3, command = camara_4)
cam4.grid(row=5, column=2, sticky="w")


porton = Button(root,state = 'normal', text="Porton Abierto", bg= "red", width=10, height=3, command = abrir_porton)
porton.grid(row=6, column=2, sticky="w")

boton_press(root).grid(row=7, column=2, sticky="w")

rechazar = Button(root, text="Rechazar", width=10, height=3, command = rechazar)
rechazar.grid(row=8, column=2, sticky="w")

historial = Button(root, text="Historial", width=10, height=3, command = mostrar_foto)
historial.grid(row=9, column=2, sticky="w")


b_conexion = Button(root, text="Desconectado", bg= "red", width=10, height=2, anchor="center", command = reboot)
b_conexion.grid(row=10, column=2, sticky="se")

estado_font = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')
ver = Label(root, text = vg.version, bd = 0, relief=RAISED, font= estado_font, width=12, height=2)
ver.grid(row=11, column=2)

cli = Label(root, text = vg.ncliente, bd = 0, relief=RAISED, font= estado_font, width=12, height=2)
cli.grid(row=12, column=2)


hs = Label(root, textvariable = h_actual, bd = 0, justify = LEFT,relief=RAISED, width=120, height=1)
hs.grid(row=12, column=3)


#time.strftime("%H:%M:%S")

#h = tareas.Timer(horayfecha) ##Timer cada 1seg
#h.start()


t = tareas.Timer(actualizacion) ##Timer cada 1seg
t.start()

c = tareas.Timer1(conexion) ##Timer cada 5seg
c.start()




#if __name__ == '__main__':
#	root = Tk()
#	aplicacion = ventana(root)
#	root.mainloop()

root.mainloop()
