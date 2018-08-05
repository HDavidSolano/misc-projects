import socket
from time import sleep
import cv2
import struct
import numpy as np
import math as m
from CamRunnable import camVideoStream

clients=[]


cam_holder = camVideoStream(0,30,320,240)

cam_holder.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('192.168.10.106', 5005))
server_socket.listen(5)

num_users = 1# this specifies the number of users connected to the server

connected_users = 0
time_delay = 0.05
while connected_users  < num_users:
    c, addr = server_socket.accept()
    clients.append(c)
    print ('Got connection from', addr) 
    connected_users += 1
sleep(4)
while True:
    my_frame, t = cam_holder.read()
    # First I prepare the image to be sent along with its size:
    data = cv2.imencode('.jpg', my_frame)[1].tostring()
    len_str = struct.pack('!i', len(data))
    #print("sending...")
    cli_count = 1
    for a_client in clients:
        # send first the size of the image
        a_client.send(len_str)
        # send the encoded image  
        a_client.send(data)
        
        sleep(0.05)
        # now receive from the client a modified file to watch
        len_str = a_client.recv(4)
       
        size = struct.unpack('!i', len_str)[0]
        
        if size > 0:
    
            data2 = a_client.recv(size)
       
            nparr = np.fromstring(data2, np.uint8)
            if m.fabs(size) < 50000:
                img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                cv2.imshow('received Server ' + str(cli_count),img)
        cli_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    sleep(time_delay)
