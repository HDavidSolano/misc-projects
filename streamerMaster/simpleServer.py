import socket
import _thread
from time import sleep
import signal
import cv2
import struct
from CamRunnable import camVideoStream

cam_holder = camVideoStream(0,30,640,480)

cam_holder.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5005))
server_socket.listen(5)
# Establish connection with client.
c, addr = server_socket.accept()  
print ('Got connection from', addr) 
while True:
    my_frame, t = cam_holder.read()
    data = cv2.imencode('.jpg', my_frame)[1].tostring()
    #print('len:', len(data))
    len_str = struct.pack('!i', len(data))
    # send first the size of the image
    c.send(len_str)
    # send the encoded image
    c.send(data)
# Close the connection with the client
c.close()