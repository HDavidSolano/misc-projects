import socket       
import struct        
import cv2
import numpy as np
from time import sleep
import math as m
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
        
        if m.fabs(size) < 50000:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('received',img)
        
            gray_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
        
            data = cv2.imencode('.jpg', gray_frame)[1].tostring()
            
            sleep(0.05)
            
            len_str = struct.pack('!i', len(data))
        
            s.send(len_str)
    
            s.send(data)
        else:
            not_good = -999999
            len_str = struct.pack('!i', not_good)
            s.send(len_str)
            print('received a bad image')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
# close the connection
cv2.destroyAllWindows()