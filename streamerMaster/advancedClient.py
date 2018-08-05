import socket       
import struct        
import cv2
import math as m
import numpy as np
from time import sleep
# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 5005  
s.connect(('192.168.10.106', port))            
while True:
# connect to the server on local computer
    # receive data from the server
    len_str = s.recv(4)
    
    size = struct.unpack('!i', len_str)[0]
    #print(size)
    #print(' ')
    sleep(0.05)
    if size > 0:
        data = s.recv(size)
        nparr = np.fromstring(data, np.uint8)
        #print(len(data))
        if m.fabs(size) < 50000:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('received',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
# close the connection
cv2.destroyAllWindows()