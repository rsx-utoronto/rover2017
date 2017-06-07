#! /usr/bin/env python

import sys

if len(sys.argv)==2 and sys.argv[1] == 'import':
    angleFile = open('savedJointAngles.txt','r')
    angles = angleFile.read()
    angleFile.close()
    angles = angles.strip()
    angles = angles.strip('[]')
    angles = angles.split(',')
    for i in range( len(angles) ):
        angles[i] = float(angles[i])
    print( angles )
    savedJointAngles = angles
    # send angles with the special start command
else:
    print('Wrong input')
