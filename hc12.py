# -*- coding: utf-8 -*-
#!/usr/bin/python2.7.13


import serial
import os
import sys
import time
import serial
import struct
import binascii
import RPi.GPIO as GPIO



		
uart = serial.Serial(port='/dev/ttyS0',baudrate = 9600,parity=serial.PARITY_NONE,
			    stopbits=serial.STOPBITS_ONE,
			    bytesize=serial.EIGHTBITS,
			    timeout=0.1)
				
datotx1 = 0
datotx2 = 0
timeout_master = 5e-3

set = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(set, GPIO.OUT)

a = GPIO.VERSION
print a


class HC_12(object):

	"This is my second class"

		
	def inicializo_hc12(self):
		GPIO.output(set, GPIO.LOW)
		time.sleep(0.5)
		#message = '\x41\x54\x0D'#.format(hex_cmd)
		message = 'AT+RX\r'
		write_uart(message)
		
		return

	def on(self, cmd):
		message = cmd
		write_uart(message)
		return	
		
	def off(self, cmd):
		message = cmd
		write_uart(message)
		return	
	############################################
	
		
		


			   
#uart = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=0.1)

def write_uart(message):
	char = ''
	for char in message:
		#time.sleep(timeout_master)
		uart.write(char)
	return
	




cadena = "test de prueba de HC-12".capitalize()
print cadena.center(70, "=")


dat = uart.read(10)

c = HC_12()
c.inicializo_hc12()

time.sleep(0.2)

datos = uart.read(50)
print datos

time.sleep(0.2)

GPIO.output(set, GPIO.HIGH)



dat = uart.read(30)
print dat

time.sleep(1)

print "Pendiendo Rele"
salir = 0
while datos != '4' and salir < 10:
	c.on('D')
	time.sleep(0.5)
	datos = uart.read(1)
	print datos
	salir += 1

print "Rele ON"	




time.sleep(2)

print "Apagando Rele"
salir = 0
while datos != '3' and salir < 10:
	c.off('C')
	time.sleep(0.5)
	datos = uart.read(1)
	print datos
	salir += 1
	
print "Rele OFF"	




# time.sleep(2)

# print "Prendo Rele Pileta"

# salir = 0

# while datos != '1' and salir < 10:
	# c.on('B')
	# time.sleep(0.5)
	# datos = uart.read(1)
	# print datos
	# salir += 1

# print "Filtro ON"	

# time.sleep(2)

# print "Apagando Rele Pileta"

# salir = 0

# while datos != '2' and salir < 10:
	# c.on('A')
	# time.sleep(0.5)
	# datos = uart.read(1)
	# print datos
	# salir += 1

# print "Filtro OFF"	





uart.close()