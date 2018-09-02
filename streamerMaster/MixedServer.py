# Sound imports
import queue
import socket
import wave
import pyaudio

# Video imports
import struct       
import cv2
import numpy as np
from time import sleep
import math as m

# Sound properties
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2
DELAY = 0.025

# SOUND Socket definition
HOST = '192.168.10.103'        # Algun ip de persona
PORT = 5005              # Algun puerto de persona
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# VIDEO Socket definition
HOST = '192.168.10.103'        # Algun ip de persona
PORT = 1414              # Algun puerto de persona
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket2.bind((HOST, PORT))
server_socket2.listen(5)

conn, addr = server_socket.accept()

conn2, addr2 = server_socket2.accept()

print ('Got connection from', addr)

# Prepare receiver for the sound
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
q = queue.Queue()

frames = []

stream.start_stream()
data = conn.recv(CHUNK)
while True > 0:
    q.put(data)
    if not q.empty():
        stream.write(q.get())

    data = conn.recv(CHUNK) # Receive sound file first
    frames.append(data)
        
    # receive data from the server
    len_str = conn2.recv(4)
    size = struct.unpack('!i', len_str)[0]
    print(size)
    if size > 0:
        data2 = conn2.recv(size)
       
        nparr = np.fromstring(data2, np.uint8)
       
        if m.fabs(size) < 150000:
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('received',img)
        else:
            print('received a bad image')
            
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.stop_stream()
stream.close()
p.terminate()
conn.close()