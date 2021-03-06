import socket

import pyaudio

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

HOST = '192.168.10.103'    # Algun ip de persona
PORT = 5005            # Algun puerto de persona

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream.start_stream()

print("*_>recording")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:
        data = stream.read(CHUNK)
    except Exception as e:
        print(e)
        data = '\x00' * CHUNK

    print(len(data))
    s.sendall(data)

print("*_>done recording")

stream.stop_stream()
stream.close()
p.terminate()
s.close()

print("*_>closed")