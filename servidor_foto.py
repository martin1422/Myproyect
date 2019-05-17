#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
import socket


ver = open ('/home/pi/s_domotica/configuraciones/version.txt','r')
version = str(ver.read(5))
print(version)
ver.close()

# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock = socket.socket(socket.SOL_SOCKET, socket.SOCK_STREAM)

# Enlace de socket y puerto
server_address = ('', 10005)
#print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
	
# Escuchando conexiones entrantes
sock.listen(1)


while True:
	 
    # Esperando conexion
	print 'Esperando foto...'
	connection, client_address = sock.accept()
	try:
			print client_address
			# Recibe los datos en trozos y reetransmite
			f = open("/home/pi/s_domotica/historial/foto.jpg", "wb")
			while True:
				data = connection.recv(10)
				if data:
					#print 'recibido "%s"' % data
					f.write(data)
				else:
					print 'recibido DATO para salir..... "%s"' % data
					f.close()
					c = open ('/home/pi/s_domotica/' + version + '/comunicacion','w')
					c.write("1")
					c.close()
					break
			
	finally:
			#Cerrando conexion
			connection.close()