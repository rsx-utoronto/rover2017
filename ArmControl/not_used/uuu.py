#! /usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

qVect = [ 0.1234, 5.2234, 0.3234, 0.4234, 0.5234, 0.6234 ]

arduino1IP = '192.168.0.101'
arduino1Port = 45
arduino2IP = '192.168.0.182'
arduino2Port = 6000

# stepper steps per 2*pi rotation
q1Steps = 21973
q2Steps = 191102
q3Steps = 6484
q4Steps = 5493
q5Steps = 5493
q6Steps = 5493
# gripperRange = 0 - 1024
# generate messages from qVect
q1String = str( '%10d' %(int(qVect[4] * q1Steps)) ).replace(' ','0')
q2String = str( '%10d' %(int(qVect[5] * q2Steps)) ).replace(' ','0')
q3String = str( '%10d' %(int(qVect[3] * q3Steps)) ).replace(' ','0')
q4String = str( '%10d' %(int(qVect[0] * q4Steps)) ).replace(' ','0')
q5String = str( '%10d' %(int(qVect[2] * q5Steps)) ).replace(' ','0')
q6String = str( '%10d' %(int(qVect[1] * q6Steps)) ).replace(' ','0')
q7String = '0000000999'
message1 = q1String+q2String+q3String+q4String+'p'
message2 = q5String+q6String+q7String+'p'
print(message1)
print(message2)

s.connect( (arduino1IP, arduino1Port) )
s.send(message1)

#s.connect( (arduino2IP, arduino2Port) )
#s.send(message2)

s.close()
