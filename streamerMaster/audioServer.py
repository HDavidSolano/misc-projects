import queue
import socket
import wave

import pyaudio

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "server_output.wav"
WIDTH = 2

HOST = '192.168.10.103'        # Algun ip de persona
PORT = 1414              # Algun puerto de persona

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

conn, addr = server_socket.accept()
print ('Got connection from', addr)

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
while len(data) > 0:
    q.put(data)
    if not q.empty():
        stream.write(q.get())

    # stream.write(data)
    data = conn.recv(CHUNK)
    print(len(data))
    frames.append(data)

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