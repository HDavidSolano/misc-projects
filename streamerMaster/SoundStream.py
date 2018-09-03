# Sound imports
import socket
import pyaudio
import queue
#Threading import
from threading import Thread

from time import sleep
class soundStream_sender:
    def __init__(self,HOST,PORT,CHUNK,RATE): # example: ('192.168.10.108',5005,8192,44100) 
        
        #Flag to stop the thread
        self.stopped = False
        # Preparing the SOUND socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT)) # Works for client only currently
        
        print('Got connection to the server')
        
        # Sound sending properties
        self.CHUNK = CHUNK
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = RATE
        # Sound runnable
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        self.stream.start_stream()
        
        print('Got stream working')
        
    def update(self):
        while not self.stopped:
            try:
                data = self.stream.read(self.CHUNK)
            except Exception as e:
                print(e)
                data = '\x00' * self.CHUNK
            self.s.sendall(data)
            
    def start(self):
        self.t = Thread(target=self.update, args=())
        self.t.start()
        return self
    
    def stop(self):
        self.stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.s.close()
        print("Stream closed")

class soundStream_receiver:
    def __init__(self,HOST,PORT,CHUNK,RATE): # example: ('192.168.10.108',5005,8192,44100) 
        #Flag to stop the thread
        self.stopped = False
        
        # Preparing connection:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        
        self.conn, self.addr = self.s.accept()
        
        print ('Got connection from', self.addr)
        
        # Sound properties
        self.CHUNK = CHUNK
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = RATE 
        self.WIDTH = 2
        
        # Prepare receiver for the sound
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK)
        self.q = queue.Queue()
        self.stream.start_stream()
        
        print('Got stream working')
        
    def update(self):
        data = self.conn.recv(self.CHUNK)
        while not self.stopped:
            self.q.put(data)
            if not self.q.empty():
                self.stream.write(self.q.get())
        
            data = self.conn.recv(self.CHUNK)
    
    def start(self):
        self.t = Thread(target=self.update, args=())
        self.t.start()
        return self
    
    def stop(self):
        self.stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.conn.close()
        print("Stream closed")
        
my_sound_sender = soundStream_sender('192.168.10.108',5005,8192,44100)
my_sound_sender.start()
for i in range(1,20):
    sleep(1)
    print(i)
    
my_sound_sender.stop()