qVect = [ 0.1234, 500000.2234, 0.3234, 0.4234, 0.5234, 0.6234 ]

q1Steps = 21973
q2Steps = 191102
q3Steps = 6484
q4Steps = 5493
q5Steps = 5493
q6Steps = 5493
# gripperRange = 0 - 1024

q1String = str( '%10d' %(int(qVect[0] * q1Steps)) ).replace(' ','0')
q2String = str( '%10d' %(int(qVect[1] * q2Steps)) ).replace(' ','0')
q3String = str( '%10d' %(int(qVect[2] * q3Steps)) ).replace(' ','0')
q4String = str( '%10d' %(int(qVect[3] * q4Steps)) ).replace(' ','0')
q5String = str( '%10d' %(int(qVect[4] * q5Steps)) ).replace(' ','0')
q6String = str( '%10d' %(int(qVect[5] * q6Steps)) ).replace(' ','0')
q7String = '0000009990'
message1 = q1String+q2String+q3String+q4String+'p'
message2 = q5String+q6String+q7String+'p'
print(message1)
print(message2)



#q1String = qVect[0] * q1Steps
#q1String = qVect[0] * q1Steps
#q1String = qVect[0] * q1Steps
#q1String = qVect[0] * q1Steps
#q1String = qVect[0] * q1Steps
