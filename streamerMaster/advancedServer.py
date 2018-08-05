import socket
import _thread
from time import sleep
import signal
import cv2
import struct
import numpy as np
from CamRunnable import camVideoStream

clients=[]


cam_holder = camVideoStream(0,30,320,240)

cam_holder.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('192.168.10.106', 5005))
server_socket.listen(5)

<<<<<<< HEAD
num_users = 3 # this specifies the number of users connected to the server
=======
num_users = 2# this specifies the number of users connected to the server
>>>>>>> branch 'master' of https://github.com/HDavidSolano/misc-projects

connected_users = 0
<<<<<<< HEAD
time_delay = 0.1
=======
time_delay = 0.05
>>>>>>> branch 'master' of https://github.com/HDavidSolano/misc-projects
while connected_users  < num_users:
    c, addr = server_socket.accept()
    clients.append(c)
    print ('Got connection from', addr) 
    connected_users += 1
print("proceeding to send camera...")
sleep(4)

while True:
    my_frame, t = cam_holder.read()
    # First I prepare the image to be sent along with its size:
    data = cv2.imencode('.jpg', my_frame)[1].tostring()
    len_str = struct.pack('!i', len(data))
    #print("sending...")
    for a_client in clients:
        # send first the size of the image
        a_client.send(len_str)
        # send the encoded image  
        a_client.send(data)
    sleep(time_delay)

