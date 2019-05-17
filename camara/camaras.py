# -*- coding: utf-8 -*-
#!/usr/bin/python2.7.13

import os
import vlc
from variables import var as vg



class cam():


	def camara_1(self):
		global player
		vg.sreboot = 0
		vg.f_tiempo_camara = True
		vg.f_mostrar_ventana_esperar = True
		#os.system("cvlc -f --no-osd  $(cat /home/pi/s_domotica/configuraciones/camara1.txt)")
		player=vlc.MediaPlayer('rtsp://admin:martin1422@192.168.1.10:554/h264/ch1/main/av_stream')
		player.play()
		#os.system("omxplayer --avdict rtsp_transport:tcp  $(cat /home/pi/s_domotica/configuraciones/camara1.txt)")

	def camara_2(self):
		vg.sreboot = 0
		vg.f_tiempo_camara = True
		vg.f_mostrar_ventana_esperar = True
		os.system("cvlc -f --xlib --no-osd  $(cat /home/pi/s_domotica/configuraciones/camara2.txt)")
		#os.system("omxplayer --avdict rtsp_transport:tcp  $(cat /home/pi/s_domotica/configuraciones/camara2.txt)")

	def camara_3(self):
		vg.sreboot = 0
		vg.f_tiempo_camara = True
		vg.f_mostrar_ventana_esperar = True
		os.system("cvlc -f --xlib --no-osd  $(cat /home/pi/s_domotica/configuraciones/camara3.txt)")
		#os.system("omxplayer --avdict rtsp_transport:tcp  $(cat /home/pi/s_domotica/configuraciones/camara3.txt)")

	def camara_4(self):
		vg.sreboot = 0
		vg.f_tiempo_camara = True
		vg.f_mostrar_ventana_esperar = True
		os.system("cvlc -f --xlib --no-osd  $(cat /home/pi/s_domotica/configuraciones/camara4.txt)")
		#os.system("omxplayer --avdict rtsp_transport:tcp  $(cat /home/pi/s_domotica/configuraciones/camara4.txt)")

	def stop_vlc(self):
		player=vlc.MediaPlayer('rtsp://admin:martin1422@192.168.1.10:554/h264/ch1/main/av_stream')
		player.stop()