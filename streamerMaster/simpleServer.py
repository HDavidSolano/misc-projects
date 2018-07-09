import socket
import _thread
from time import sleep
import signal
import cv2
import struct
import numpy as np
from CamRunnable import camVideoStream

#cam_holder = camVideoStream(0,30,320,240)

#cam_holder.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5005))
server_socket.listen(5)
# Establish connection with client.
c, addr = server_socket.accept()  
print ('Got connection from', addr) 
while True:
    #my_frame, t = cam_holder.read()
    my_frame = cv2.imread('newplot.png')
    data = cv2.imencode('.jpg', my_frame)[1].tostring()
    #print('len:', len(data))
    len_str = struct.pack('!i', len(data))
    sleep(0.1)
    # send first the size of the image
    c.send(len_str)
    # send the encoded image  
    c.send(data)
    sleep(0.1)
    len_str = c.recv(4)
    
    size = struct.unpack('!i', len_str)[0]
    #print('size:', size)
    if size > 0:

        data = c.recv(size)
    
        nparr = np.fromstring(data, np.uint8)
        
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        cv2.imshow('received Server',img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Close the connection with the client
c.close()

cv2.waitKey(0)
# close the connection
cv2.destroyAllWindows()