#! /usr/bin/env python
# imports
import copy
import time
import openravepy
import numpy as np
#if not __openravepy_build_doc__:
#    from openravepy import *
#    from numpy import *
import pygame
import math
import socket


def homogenousTransform(dhVector):
    a = dhVector[0]
    alpha = dhVector[1]
    d = dhVector[2]
    theta = dhVector[3]
    homTransMatrix = [ [math.cos(theta), -math.sin(theta)*math.cos(alpha), math.sin(theta)*math.sin(alpha), a*math.cos(theta)],
                       [math.sin(theta), math.cos(theta)*math.cos(alpha), -math.cos(theta)*math.sin(alpha), a*math.sin(theta)],
                       [0, math.sin(alpha), math.cos(alpha), d],
                       [0, 0, 0, 1] ]
    return homTransMatrix


def forwardKinematics(dhTable):
    A1 = np.matrix( homogenousTransform(dhTable[0]) )
    A2 = np.matrix( homogenousTransform(dhTable[1]) )
    A3 = np.matrix( homogenousTransform(dhTable[2]) )
    A4 = np.matrix( homogenousTransform(dhTable[3]) )
    A5 = np.matrix( homogenousTransform(dhTable[4]) )
    A6 = np.matrix( homogenousTransform(dhTable[5]) )
    fullHomTransMatrix = A1*A2*A3*A4*A5*A6
    #print( fullHomTransMatrix.tolist() )
    return fullHomTransMatrix.tolist()


def inverseKinematics(dhTable, homTransMatrix):
    d1 = dhTable[0][2]
    a2 = dhTable[1][0]
    d4 = dhTable[3][2]
    d6 = dhTable[5][2]

    #print("HomTransMatrix: ")
    #print(homTransMatrix)
    
    Rd = np.matrix( [ homTransMatrix[0][:3], homTransMatrix[1][:3], homTransMatrix[2][:3] ] )
    #print("Rd: ")
    #print(Rd)
    od = np.matrix( [ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ] ).transpose()
    #print("od: ")
    #print(od)

    arD6 = np.matrix( [ 0,0,d6] ).transpose()
    #print("arD6: ")
    #print(arD6)
    #print(arD6.transpose())
    #print(Rd)
    oc = od - Rd * arD6
    #print(np.dot(Rd,arD6))
    #print(np.dot(Rd,arD6.transpose()))
    #print("oc: ")
    #print(oc)

    xc = oc.tolist()[0][0]
    yc = oc.tolist()[1][0]
    zc = oc.tolist()[2][0]

    q1 = math.atan2(yc, xc)
    
    Dtemp = ( xc**2 + yc**2 + (zc-d1)**2 - a2**2 - d4**2 )/( 2*a2*d4 )
    if abs(Dtemp) > 1:
        print( 'Can not reach {}, {}, {}'.format( homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ) )
        return dhTable
    
    q3 = math.atan2( Dtemp, math.sqrt(1 - Dtemp**2) ) # assumes we chose to always have 'elbow up' solution
    
    q2 = math.atan2( zc - d1, math.sqrt(xc**2 + yc**2) ) - math.atan2( d4*math.sin(q3-math.pi/2), a2+d4*math.cos(q3-math.pi/2) )

    # start updating dhTable. Update with first 3 joints
    updatedDHTable = copy.deepcopy(dhTable)
    updatedDHTable[0][3] = q1
    updatedDHTable[1][3] = q2
    updatedDHTable[2][3] = q3
    
    H01 = np.matrix( homogenousTransform(updatedDHTable[0]) )
    H12 = np.matrix( homogenousTransform(updatedDHTable[1]) )
    H23 = np.matrix( homogenousTransform(updatedDHTable[2]) )
    H03 = (H01 * H12 * H23).tolist()
    R03 = np.matrix( [H03[0][:3], H03[1][:3], H03[2][:3]] )
    #print("R03: ")
    #print(R03)
    #print(R03)
    #print(R03.transpose())
    R36 = R03.transpose() * Rd
    #print("R36: ")
    #print(R36)
    #print( np.dot(R03, Rd) )
    #print( np.dot(R03.transpose(), Rd) )

    q4 = math.atan2( R36.tolist()[1][2], R36.tolist()[0][2] )
    q5 = math.atan2( math.sqrt(1 - R36.tolist()[2][2]**2), R36.tolist()[2][2] )
    q6 = math.atan2( R36.tolist()[2][1], -R36.tolist()[2][0] )

    # updating DH table with the wrist stuff
    updatedDHTable[3][3] = q4
    updatedDHTable[4][3] = q5
    updatedDHTable[5][3] = q6
    
    return updatedDHTable


def inverseKinematicsPositional(dhTable, homTransMatrix):
    d1 = dhTable[0][2]
    a2 = dhTable[1][0]
    d4 = dhTable[3][2]
    d6 = dhTable[5][2]

    #print("HomTransMatrix: ")
    #print(homTransMatrix)
    
    Rd = np.matrix( [ homTransMatrix[0][:3], homTransMatrix[1][:3], homTransMatrix[2][:3] ] )
    #print("Rd: ")
    #print(Rd)
    od = np.matrix( [ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ] ).transpose()
    #print("od: ")
    #print(od)

    arD6 = np.matrix( [ 0,0,d6] ).transpose()
    #print("arD6: ")
    #print(arD6)
    #print(arD6.transpose())
    #print(Rd)
    oc = od - Rd * arD6
    #print(np.dot(Rd,arD6))
    #print(np.dot(Rd,arD6.transpose()))
    #print("oc: ")
    #print(oc)

    xc = oc.tolist()[0][0]
    yc = oc.tolist()[1][0]
    zc = oc.tolist()[2][0]

    q1 = math.atan2(yc, xc)
    
    Dtemp = ( xc**2 + yc**2 + (zc-d1)**2 - a2**2 - d4**2 )/( 2*a2*d4 )
    if abs(Dtemp) > 1:
        print( 'Can not reach {}, {}, {}'.format( homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ) )
        return dhTable
    
    q3 = math.atan2( Dtemp, math.sqrt(1 - Dtemp**2) ) # assumes we chose to always have 'elbow up' solution
    
    q2 = math.atan2( zc - d1, math.sqrt(xc**2 + yc**2) ) - math.atan2( d4*math.sin(q3-math.pi/2), a2+d4*math.cos(q3-math.pi/2) )

    # start updating dhTable. Update with first 3 joints
    updatedDHTable = copy.deepcopy(dhTable)
    updatedDHTable[0][3] = q1
    updatedDHTable[1][3] = q2
    updatedDHTable[2][3] = q3
    
    return updatedDHTable


def updateHomTransMatrix(homTransMatrix, DHTable, translationVector, rotationVector):
    updatedHomTransMatrix = copy.deepcopy( homTransMatrix )
    # update translation part
    k = 1 # amplification coefficient translational motion
    t = 0.05 # amplification coefficient rotational motion
    for ind in range(3):
        translationVector[ind] = k * translationVector[ind]
        rotationVector[ind] = t * rotationVector[ind]

    # update rotation
    H01 = homogenousTransform(DHTable[0])
    R01 = np.matrix( [ H01[0][:3], H01[1][:3], H01[2][:3] ] )
    H12 = homogenousTransform(DHTable[1])
    R12 = np.matrix( [ H12[0][:3], H12[1][:3], H12[2][:3] ] )
    H23 = homogenousTransform(DHTable[2])
    R23 = np.matrix( [ H23[0][:3], H23[1][:3], H23[2][:3] ] )
    R03 = R01 * R12 * R23
    
    DHTable[3][3] += rotationVector[1]
    DHTable[4][3] += rotationVector[0]
    DHTable[5][3] += rotationVector[2]
    H34 = homogenousTransform(DHTable[3])
    R34 = np.matrix( [ H34[0][:3], H34[1][:3], H34[2][:3] ] )
    H45 = homogenousTransform(DHTable[4])
    R45 = np.matrix( [ H45[0][:3], H45[1][:3], H45[2][:3] ] )
    H56 = homogenousTransform(DHTable[5])
    R56 = np.matrix( [ H56[0][:3], H56[1][:3], H56[2][:3] ] )
    R36 = R34 * R45 * R56
    
    #R06 = R03 * R36
    #for i in range(3):
    #    for j in range(3):
    #        updatedHomTransMatrix[i][j] = R06[i,j]

    # update translation
    #updatedHomTransMatrix[0][3] += translationVector[0]
    #updatedHomTransMatrix[1][3] += translationVector[1]
    #updatedHomTransMatrix[2][3] += translationVector[2]

    H06 = (np.matrix(H01) * np.matrix(H12) * np.matrix(H23) * np.matrix(H34) * np.matrix(H45) * np.matrix(H56)).tolist()
    H06[0][3] += translationVector[0]
    H06[1][3] += translationVector[1]
    H06[2][3] += translationVector[2]
    
    return H06


def updateHomTransMatrixPositional(homTransMatrix, DHTable, translationVector, rotationVector):
    updatedHomTransMatrix = copy.deepcopy( homTransMatrix )
    # update translation part
    k = 1 # amplification coefficient translational motion
    t = 0.05 # amplification coefficient rotational motion
    for ind in range(3):
        translationVector[ind] = k * translationVector[ind]
        rotationVector[ind] = t * rotationVector[ind]
    
    # update translational part
    for i in range(3):
        updatedHomTransMatrix[i][3] += translationVector[i] 
    
    return updatedHomTransMatrix


def initializeJoystick():
    pygame.init()
    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print('Initialized joystick: %s' % joystick.get_name())


def setupVisualEnv():
    env = openravepy.Environment()
    env.Load('environment.xml')
    env.SetViewer('qtcoin')
    viewer = env.GetViewer()
    global robot
    robot = env.GetRobots()[0]
    global initAngles
    # if want to modify q4 and q6, reverse the sign from "angle" to "-angle"
    # needed specifically for visualizer
    global savedJointAngles
    copySavedJointAngles = savedJointAngles[:]
    copySavedJointAngles[3] = -copySavedJointAngles[3]
    copySavedJointAngles[5] = -copySavedJointAngles[5]
    initAngles = [0,0,-math.pi/2,0,0,0]

    setupAngles = []
    for i in range(len(initAngles)):
        setupAngles.append( copySavedJointAngles[i]+initAngles[i] )
        
    robot.SetActiveDOFValues(setupAngles)
    #print( robot.GetActiveDOFValues() )


# TODO IMPLEMENT
def sendAngleValues(qVect):
    #global s
    
    arduino1IP = '192.168.0.181'
    arduino1Port = 6000
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
    #print(message1)
    #print(message2)

    s.connect( (arduino1IP, arduino1Port) )
    s.send(message1)

    s.connect( (arduino2IP, arduino2Port) )
    s.send(message2)

    #s.close() # ??????????? HERE OR AT THE END ??????


    
# TODO IMPLEMENT
def getAngleValues():
    global s

    arduino1IP = '127.0.0.1'
    arduino1Port = 6000
    arduino2IP = '127.0.0.1'
    arduino2Port = 6000
    BUFFER_SIZE = 1024

    #s.connect( (arduino1IP, arduino1Port) )
    #message1 = s.recv(BUFFER_SIZE)
    #s.connect( (arduino2IP, arduino2Port) )
    #message2 = s.recv(BUFFER_SIZE)

    #s.close() # ????????? HERE OR AT THE END ???????
    
    return [message1,message2]


def getJoystickAxes():
    out = [0,0,0,0,0,0]
    it = 0 # iterator
    pygame.event.pump()
    #Read input from the joystick       
    for i in range(0, joystick.get_numaxes()):
        out[i] = joystick.get_axis(i)
    return out


def getJoystickDirection():
    joystickValues = getJoystickAxes()
    # determine direction
    directionVector = [0,0,0,0,0,0]
    storedVal = 0
    storedInd = 0
    ind = -1
    for value in joystickValues:
        ind += 1
        if abs(value) > abs(storedVal):
            storedVal = value
            storedInd = ind
    # introduce some "sensitivity gap" to avoid random movement
    if abs(storedVal) > 0.2:
        directionVector[storedInd] = storedVal
    # needed specifically to make thigs coincide with our arm
    for i in range( len(directionVector) ):
        directionVector[i] = -directionVector[i]
    tempval = directionVector[0]
    directionVector[0] = directionVector[1]
    directionVector[1] = tempval
    directionVector[3] = -directionVector[3]
    directionVector[4] = -directionVector[4]
    return directionVector
    

def visualizeArm(jointAngles):
    copyJointAngles = copy.deepcopy(jointAngles)
    #print("Values on visualization: {}".format(copyJointAngles))
    global robot
    global initAngles
    # invert signs of q4 and q6. Needed specifically for visualizer
    copyJointAngles[3] = -copyJointAngles[3]
    copyJointAngles[5] = -copyJointAngles[5]
    
    for i in range(len(copyJointAngles)):
        copyJointAngles[i] += initAngles[i]
    robot.SetActiveDOFValues(copyJointAngles)
    #print("Initial angles: {}".format(initAngles))
    

# TODO IMPLEMENT
def setJointAngles(qVector):
    jointAngles = qVector
    # DO IT SOMEHOW
    visualizeArm(jointAngles)


# TODO IMPLEMENT
def getJointAngles():
    # stepper steps per 2 PI rotation for each joint
    

    # get values
    
    
    return qVect
    

def getOperationMode():
    return None
    

def manual():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of the arm
    #jointAngles = getJointAngles() # TODO TEMPORARY REPLACED
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles) # TODO TEMPORARY REPLACEMENT?
    #print("Current joint angles: {}".format(jointAngles))
    #print(jointAngles)
    
    # joint values, pretty view
    q1 = jointAngles[0]
    q2 = jointAngles[1]
    q3 = jointAngles[2]
    q4 = jointAngles[3]
    q5 = jointAngles[4]
    q6 = jointAngles[5]
    # joint variables limits (in degrees), format [min, max]
    q1lim = np.array( [-160, 160] ) * math.pi/180
    q2lim = np.array( [-45, 225] ) * math.pi/180
    q3lim = np.array( [-225, 45] ) * math.pi/180
    q4lim = np.array( [-110, 170] ) * math.pi/180
    q5lim = np.array( [-100, 100] ) * math.pi/180
    q6lim = np.array( [-266, 266] ) * math.pi/180
    # DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = [ [0, math.pi/2, 5.5, q1],
                [36.5, 0, 0, q2],
                [0, math.pi/2, 0, q3],
                [0, -math.pi/2, 33, q4],
                [0, math.pi/2, 0, q5],
                [0, 0, 15, q6] ]

    # do forward kinematics
    DHTableCopy = copy.deepcopy(DHTable)
    homTransMatrix = forwardKinematics(DHTableCopy)
    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)
    
    k = 0.05
    uq1 = DHTable[0][3] + k * joystickDirection[0]#updatedDHTable[0][3]
    uq2 = DHTable[1][3] + k * joystickDirection[1]#updatedDHTable[1][3]
    uq3 = DHTable[2][3] + k * joystickDirection[2]#updatedDHTable[2][3]
    uq4 = DHTable[3][3] + k * joystickDirection[3]#updatedDHTable[3][3]
    uq5 = DHTable[4][3] + k * joystickDirection[4]#updatedDHTable[4][3]
    uq6 = DHTable[5][3] + k * joystickDirection[5]#updatedDHTable[5][3]
    try:
        jointAngles = copy.deepcopy( [uq1,uq2,uq3,uq4,uq5,uq6] )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)
        savedJointAngles = copy.deepcopy(jointAngles)
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        visualizeArm(jointAngles)
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles)) 
        savedJointAngles = copy.deepcopy(jointAngles)
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        visualizeArm(jointAngles)
        print(savedJointAngles)


def positionalIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of  the arm
    #jointAngles = getJointAngles() # TODO TEMPORARY REPLACED
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles) # TODO TEMPORARY REPLACEMENT ?
    #print("Current joint angles: {}".format(jointAngles))
    #print(jointAngles)
    
    # joint values, pretty view
    q1 = jointAngles[0]
    q2 = jointAngles[1]
    q3 = jointAngles[2]
    q4 = jointAngles[3]
    q5 = jointAngles[4]
    q6 = jointAngles[5]
    # joint variables limits (in degrees), format [min, max]
    q1lim = np.array( [-160, 160] ) * math.pi/180
    q2lim = np.array( [-45, 225] ) * math.pi/180
    q3lim = np.array( [-225, 45] ) * math.pi/180
    q4lim = np.array( [-110, 170] ) * math.pi/180
    q5lim = np.array( [-100, 100] ) * math.pi/180
    q6lim = np.array( [-266, 266] ) * math.pi/180
    # DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = [ [0, math.pi/2, 5.5, q1],
                [36.5, 0, 0, q2],
                [0, math.pi/2, 0, q3],
                [0, -math.pi/2, 33, q4],
                [0, math.pi/2, 0, q5],
                [0, 0, 15, q6] ]

    # do forward kinematics
    DHTableCopy = copy.deepcopy(DHTable)
    homTransMatrix = forwardKinematics(DHTableCopy)
    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)

    # update homogenous transformation matrix based on joystick input
    translationVector = joystickDirection[:3]
    rotationVector = joystickDirection[3:]
    
    copyHomTransMatrix = copy.deepcopy(homTransMatrix)
    DHTableCopy2 = copy.deepcopy(DHTable)
    updatedHomTransMatrix = updateHomTransMatrixPositional(copyHomTransMatrix, DHTableCopy2, translationVector, rotationVector)
    #print("Updated position: ")
    #print([ updatedHomTransMatrix[0][3], updatedHomTransMatrix[1][3], updatedHomTransMatrix[2][3] ])

    # solve IK based on the new homTransMatrix
    DHTableCopy3 = copy.deepcopy(DHTable)
    copyUpdatedHomTransMatrix = copy.deepcopy(updatedHomTransMatrix)
    updatedDHTable = inverseKinematicsPositional(DHTableCopy3, copyUpdatedHomTransMatrix)
    uq1 = updatedDHTable[0][3]
    uq2 = updatedDHTable[1][3]
    uq3 = updatedDHTable[2][3]
    uq4 = DHTable[3][3] + rotationVector[0]#updatedDHTable[3][3]
    uq5 = DHTable[4][3] + rotationVector[1]#updatedDHTable[4][3]
    uq6 = DHTable[5][3] + rotationVector[2]#updatedDHTable[5][3]
    try:
        jointAngles = copy.deepcopy( [uq1,uq2,uq3,uq4,uq5,uq6] )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(jointAngles)
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(jointAngles)
        print(savedJointAngles)
    

def fullIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of the arm
    #jointAngles = getJointAngles() # TODO TEMPORARY REPLACED
    #global savedQ6 # needed specifically because we want to ignore roll of the end effector in IK
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles)
    #print("Current joint angles: {}".format(jointAngles))
    #print(jointAngles)
    
    # joint values, pretty view
    q1 = jointAngles[0]
    q2 = jointAngles[1]
    q3 = jointAngles[2]
    q4 = jointAngles[3]
    q5 = jointAngles[4]
    q6 = jointAngles[5]
    # joint variables limits (in degrees), format [min, max]
    q1lim = np.array( [-160, 160] ) * math.pi/180
    q2lim = np.array( [-45, 225] ) * math.pi/180
    q3lim = np.array( [-225, 45] ) * math.pi/180
    q4lim = np.array( [-110, 170] ) * math.pi/180
    q5lim = np.array( [-100, 100] ) * math.pi/180
    q6lim = np.array( [-266, 266] ) * math.pi/180
    # DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = [ [0, math.pi/2, 5.5, q1],
                [36.5, 0, 0, q2],
                [0, math.pi/2, 0, q3],
                [0, -math.pi/2, 33, q4],
                [0, math.pi/2, 0, q5],
                [0, 0, 15, q6] ]

    # do forward kinematics
    DHTableCopy = copy.deepcopy(DHTable)
    homTransMatrix = forwardKinematics(DHTableCopy)
    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)

    # update homogenous transformation matrix based on joystick input
    translationVector = joystickDirection[:3]
    rotationVector = joystickDirection[3:]
    
    copyHomTransMatrix = copy.deepcopy(homTransMatrix)
    DHTableCopy2 = copy.deepcopy(DHTable)
    updatedHomTransMatrix = updateHomTransMatrix(copyHomTransMatrix, DHTableCopy2, translationVector, rotationVector)
    #print("Updated position: ")
    #print([ updatedHomTransMatrix[0][3], updatedHomTransMatrix[1][3], updatedHomTransMatrix[2][3] ])

    # solve IK based on the new homTransMatrix
    DHTableCopy3 = copy.deepcopy(DHTable)
    copyUpdatedHomTransMatrix = copy.deepcopy(updatedHomTransMatrix)
    updatedDHTable = inverseKinematics(DHTableCopy3, copyUpdatedHomTransMatrix)
    uq1 = updatedDHTable[0][3]
    uq2 = updatedDHTable[1][3]
    uq3 = updatedDHTable[2][3]
    uq4 = updatedDHTable[3][3]
    uq5 = updatedDHTable[4][3]
    uq6 = updatedDHTable[5][3]
    try:
        #savedQ6 += uq6 # needed specifically because we want to ignore roll of the end effector but being able to set end effector how necessary
        jointAngles = copy.deepcopy( [uq1,uq2,uq3,uq4,uq5,uq6] )
        #print("Updated joint angles: {}".format(jointAngles))
        
        #jointAngles[5] = 0
        savedJointAngles = copy.deepcopy(jointAngles)
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))
        savedJointAngles = copy.deepcopy(jointAngles)
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!! or just do nothing?
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        print(savedJointAngles)
        


def main():
    # TODO GET THE MODE OF OPERATION
    # modes: '1'-manual, '2'-positional IK (first 3 joints), '3'-full IK
    
    modeOfOperation = 3#getOperationMode()#GET THE MODE OF OPERATION FROM SOMEWHERE
    if modeOfOperation == 1:
        manual()
    elif modeOfOperation == 2:
        positionalIK()
    elif modeOfOperation == 3:
        fullIK()
        
    # frequency in Hz
    frequency = 100
    timeDelay =  1.0/frequency
    #print(timeDelay)
    time.sleep(timeDelay)

    

if __name__ == "__main__":
    # global variables are:
    # joystick
    # savedJointAngles
    # initAngles
    # robot
    #global savedQ6
    #savedQ6 = 0
    global savedJointAngles
    savedJointAngles = [0,0,0,0,0,0]
    setupVisualEnv()
    initializeJoystick()
    #global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    #time.sleep(0.5)
    
    while True:
        # TODO
        turnedOn = True #GET THE TURNED_ON MODE FROM SOMEWHERE
        # TODO
        breakTrigger = False #GET THE BREAK TRIGGER FROM SOMEWHERE
        if turnedOn:
            if breakTrigger:
                print("Break triggered")
                break
            else:
                main()
        else:
            continue

    s.close()
    
    print("Shutting the operations down")
    
