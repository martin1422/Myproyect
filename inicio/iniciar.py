# -*- coding: utf-8 -*-
#!/usr/bin/python2.7.13

import os
import time
from variables import var as vg


class ini():

    def __init__(self):
		#-----------------------------------------------------------------#
		ver = open ('/home/pi/s_domotica/configuraciones/version.txt','r')
		vg.version = str(ver.read(5))
		print(vg.version)
		ver.close()

		n_cli = open ('/home/pi/s_domotica/configuraciones/num_cliente.txt','r')
		vg.ncliente = str(n_cli.read(12)) #Cliente: 000
		print(vg.ncliente)
		n_cli.close()

		tc = open ('/home/pi/s_domotica/configuraciones/tiempo_camara.txt','r')
		vg.tiempo_cam_on = int(tc.read(3))
		print(vg.tiempo_cam_on)
		tc.close()

		tf = open ('/home/pi/s_domotica/configuraciones/tiempo_foto.txt','r')
		vg.tiempo_foto_on = int(tf.read(3))
		print(vg.tiempo_foto_on)
		tf.close()

		h = open ('/home/pi/s_domotica/configuraciones/host.txt','r')
		vg.HOST = str(h.read(26)) #192.168.1.160 casitavenezuela.dyndns.org
		print(vg.HOST)
		h.close()


		p = open ('/home/pi/s_domotica/configuraciones/port.txt','r')
		vg.PORT = int(p.read(5))
		print(vg.PORT)
		p.close()

		blt = open ('/home/pi/s_domotica/configuraciones/timelcdon.txt','r')
		vg.TLCD = int(blt.read(3))
		vg.tiempolcdon = vg.TLCD
		print(vg.tiempolcdon)
		blt.close()

		vol = open ('/home/pi/s_domotica/configuraciones/volumen.txt','r')
		vg.volumen = int(vol.read(3))
		print(vg.volumen)
		vol.close()

		ini = open ('/home/pi/s_domotica/conectividad_log.txt','a')
		ini.write("Sistema inicio: %s - %s - INICIO\n" %(vg.HOST ,time.strftime("%c")))
		ini.close()

		c1 = open("/home/pi/s_domotica/configuraciones/camara1.txt", "r")
		char = str(c1.read(1))
		while char != '#':
			vg.camara1 = vg.camara1 + char
			char = str(c1.read(1))
		c1.close()
		print vg.camara1

		c2 = open("/home/pi/s_domotica/configuraciones/camara2.txt", "r")
		char = str(c2.read(1))
		while char != '#':
			vg.camara2 = vg.camara2 + char
			char = str(c2.read(1))
		c2.close()
		print vg.camara2

		c3 = open("/home/pi/s_domotica/configuraciones/camara3.txt", "r")
		char = str(c3.read(1))
		while char != '#':
			vg.camara3 = vg.camara3 + char
			char = str(c3.read(1))
		c3.close()
		print vg.camara3

		c4 = open("/home/pi/s_domotica/configuraciones/camara4.txt", "r")
		char = str(c4.read(1))
		while char != '#':
			vg.camara4 = vg.camara4 + char
			char = str(c4.read(1))
		c4.close()
		print vg.camara4

    def verficacionMAC(self):

		mac1 = open ('/home/pi/.mac_.txt','r+')
		nmac = str(mac1.read(17)) #b8:27:eb:27:5b:fa
		mac1.close()
		print(nmac)
		v_mac = os.popen("cat /sys/class/net/eth0/address").read()
		print(v_mac)
		if nmac == "11:22:33:44:55:66":
			print "Memoria viregen"
			print(v_mac)
			mac = open ('/home/pi/.mac_.txt','w+')
			mac.write(str(v_mac))
			mac.close()
		else:
			mac1 = open ('/home/pi/.mac_.txt','r+')
			nmac = str(mac1.read(18)) #b8:27:eb:27:5b:fa
			mac1.close()

		print "No Virgen"
		if nmac == v_mac:
			print "Memoria Correcta"
		else:
			print "Memoria Invalida"
			os.system("sudo pkill python")
			exit()