# Import socket module
import socket       
import struct        
import cv2
import numpy as np
from time import sleep
# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 5005  
s.connect(('127.0.0.1', port))            
while True:
# connect to the server on local computer
    # receive data from the server
    len_str = s.recv(4)
    size = struct.unpack('!i', len_str)[0]
    if size > 0:
        data = s.recv(size)
        
        nparr = np.fromstring(data, np.uint8)
        
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        cv2.imshow('received',img)
        #s.flush()
        
        gray_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
        
        data = cv2.imencode('.jpg', gray_frame)[1].tostring()
        sleep(0.10)
        len_str = struct.pack('!i', len(data))
        
        s.send(len_str)
    
        s.send(data)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
# close the connection
cv2.destroyAllWindows()