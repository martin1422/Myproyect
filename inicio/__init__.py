
#-----------------------------------------------------------------#
tc = open ('/home/pi/s_domotica/configuraciones/tiempo_camara.txt','r')
tiempo_cam_on = int(tc.read(3))
print(tiempo_cam_on)
tc.close()

tf = open ('/home/pi/s_domotica/configuraciones/tiempo_foto.txt','r')
tiempo_foto_on = int(tf.read(3))
print(tiempo_foto_on)
tf.close()

h = open ('/home/pi/s_domotica/configuraciones/host.txt','r')
HOST = str(h.read(13)) #192.168.1.160
print(HOST) 
h.close()


p = open ('/home/pi/s_domotica/configuraciones/port.txt','r')
PORT = int(p.read(5))
print(PORT)
p.close()

blt = open ('/home/pi/s_domotica/configuraciones/timelcdon.txt','r')
TLCD = int(blt.read(3))
tiempolcdon = TLCD
print(TLCD)
blt.close()