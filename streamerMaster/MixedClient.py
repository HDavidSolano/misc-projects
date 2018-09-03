# The idea behind this file is to create the client that sends both
# sound and video. The server will limit itself to just receiving.

# Sound imports
import socket
import pyaudio

# Video imports
from time import sleep
import cv2
import struct
import numpy as np
import math as m
from CamRunnable import camVideoStream


# Sound sending properties
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 120
'''
# Video sending properties
HEIGHT = 240
WIDTH =  320
FPS = 30
DELAY = 0
'''
# Preparing the SOUND socket
HOST = '192.168.10.108'    # Algun ip de persona
PORT = 5005            # Algun puerto de persona
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

'''
# Preparing the VIDEO socket
PORT = 5555          # Algun puerto de persona
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT))
'''
'''
# Video runnnable
cam_holder = camVideoStream(0,FPS,HEIGHT,WIDTH)
cam_holder.start()
sleep(5)
'''

# Sound runnable
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
stream.start_stream()

print("*_>recording")

while True:
    try:
        data = stream.read(CHUNK)
    except Exception as e:
        print(e)
        data = '\x00' * CHUNK

    print(len(data))
    s.send(data) # Send sound FIRST    
    '''
    my_frame, t = cam_holder.read()
    # First I prepare the image to be sent along with its size:
    data2 = cv2.imencode('.jpg', my_frame)[1].tostring()
    len_str = struct.pack('!i', len(data2))
    
    s2.send(len_str) # Send image size to decode first
    sleep(DELAY)
    s2.send(data2)    # Send the encoded image
    sleep(DELAY)
    '''
print("*_>done recording")

stream.stop_stream()
stream.close()
p.terminate()
s.close()

print("*_>closed")