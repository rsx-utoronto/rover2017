#! /usr/bin/env python

import httplib


qVect = [ 0.1234, 5.2234, 0.3234, 0.4234, 0.5234, 0.6234 ]

serverIP = '127.0.0.1'
serverHttpPort = '8080'
    
conn = httplib.HTTPConnection(serverIP+":"+serverHttpPort)
    
# stepper steps per 2*pi rotation
q1Steps = 21973
q2Steps = 191102
q3Steps = 6484
q4Steps = 5493
q5Steps = 5493
q6Steps = 5493
# gripperRange = 0 - 1024
# generate messages from qVect
q1String = str( int(qVect[4] * q1Steps) )#str( '%10d' %(int(qVect[4] * q1Steps)) ).replace(' ','0')
q2String = str( int(qVect[5] * q2Steps) )#str( '%10d' %(int(qVect[5] * q2Steps)) ).replace(' ','0')
q3String = str( int(qVect[3] * q3Steps) )#str( '%10d' %(int(qVect[3] * q3Steps)) ).replace(' ','0')
q4String = str( int(qVect[0] * q4Steps) )#str( '%10d' %(int(qVect[0] * q4Steps)) ).replace(' ','0')
q5String = str( int(qVect[2] * q5Steps) )#str( '%10d' %(int(qVect[2] * q5Steps)) ).replace(' ','0')
q6String = str( int(qVect[1] * q6Steps) )#str( '%10d' %(int(qVect[1] * q6Steps)) ).replace(' ','0')
q7String = '999'
command = 'p'
message = command+'_'+q1String+'_'+q2String+'_'+q3String+'_'+q4String+'_'+q5String+'_'+q6String+'_'+q7String

conn.request("PUT","/arm/"+message+"/")

r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
print data1

conn.request("GET", "/arm/")
r2 = conn.getresponse()
print r2.status, r2.reason
data2 = r2.read()
print data2
