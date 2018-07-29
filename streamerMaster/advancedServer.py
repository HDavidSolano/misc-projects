import socket
import _thread
from time import sleep
import signal
import cv2
import struct
import numpy as np
from CamRunnable import camVideoStream

clients=[]


cam_holder = camVideoStream(0,30,320,240)

cam_holder.start()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5005))
server_socket.listen(5)

num_users = 1 # this specifies the number of users connected to the server

connected_users = 0
time_delay = 0.25
while connected_users  < num_users:
    c, addr = server_socket.accept()
    clients.append(c)
    print ('Got connection from', addr) 
    connected_users += 1
sleep(4)
while True:
    #my_frame = cv2.imread('newplot.png')
    my_frame, t = cam_holder.read()
    # First I prepare the image to be sent along with its size:
    data = cv2.imencode('.jpg', my_frame)[1].tostring()
    len_str = struct.pack('!i', len(data))
    #print("sending...")
    for a_client in clients:
        # send first the size of the image
        a_client.send(len_str)
        # send the encoded image  
        a_client.send(data)
    sleep(time_delay)
"""
async def handle_client(client):
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 1024)).decode('utf8')
        response = request + ' me llego'
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()

async def run_server():
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5005))
server.listen(8)
server.setblocking(False)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run_server())
except KeyboardInterrupt:
    server.close() """

