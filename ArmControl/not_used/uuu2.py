#! /usr/bin/env python

import socket

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#qVect = [ 0.1234, 5.2234, 0.3234, 0.4234, 0.5234, 0.6234 ]

#arduino1IP = '192.168.0.181'
#arduino1Port = 6000
#arduino2IP = '192.168.0.182'
#arduino2Port = 6000

TCP_IP = '172.16.92.2'
TCP_PORT = 6000
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()

s.close()
