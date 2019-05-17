#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa Servidor
# www.pythondiario.com
import os
import socket
import sys
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto
server_address = ('', 10090) #puerto del porton
sock.bind(server_address)
	
# Escuchando conexiones entrantes
sock.listen(1)



while True:

  # Esperando conexion
  print >>sys.stderr, 'Esperando para conectarse'
  connection, client_address = sock.accept()

  try:
	
   print >>sys.stderr, 'concexion desde', client_address
    # Recibe los datos en trozos y reetransmit
		
   while True:
            	
        data = connection.recv(10)
        print >>sys.stderr, 'recibido "%s"' % data
		
	if data:
			if data == "1":
					arch = open ('/home/pi/s_domotica/comunicacion','w')
					arch.write("1")
					arch.close()
					connection.sendall('ping')
					print data
					data = 0
	else:
				#print >>sys.stderr, 'no hay mas datos', client_address
				break				
	
  finally:
        # Cerrando conexion
		connection.close()