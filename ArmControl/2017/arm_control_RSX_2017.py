#! /usr/bin/env python
# imports
import copy
import time
import openravepy
import numpy as np
import pygame
import math
#import socket
import httplib
import sys


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


def inverseKinematicsPositional(dhTable, homTransMatrix, rotationVector):
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
    updatedDHTable[3][3] = rotationVector[1]
    updatedDHTable[4][3] = rotationVector[0]
    updatedDHTable[5][3] = rotationVector[2]
    
    return updatedDHTable


def updateHomTransMatrix(homTransMatrix, DHTable, translationVector, rotationVector):
    updatedHomTransMatrix = copy.deepcopy( homTransMatrix )
    global k, t
    for ind in range(3):
        translationVector[ind] = k * translationVector[ind]
        rotationVector[ind] = t * rotationVector[ind]


    # ## TYPE0 fancy motions, relative to the camera
    # ## update movement in end effector camera frame
    # x0 = np.matrix( [1, 0, 0] ).transpose()
    # y0 = np.matrix( [0, 1, 0] ).transpose()
    # z0 = np.matrix( [0, 0, 1] ).transpose()
    # R06 = np.matrix( [ updatedHomTransMatrix[0][:3], updatedHomTransMatrix[1][:3], updatedHomTransMatrix[2][:3] ] )
    # # get z3
    # A1 = np.matrix( homogenousTransform(DHTable[0]) )
    # A2 = np.matrix( homogenousTransform(DHTable[1]) )
    # A3 = np.matrix( homogenousTransform(DHTable[2]) )
    # H03 = A1*A2*A3#*A4
    # R03 = H03[:3,:3]
    # z3 = R03 * z0
    
    # #z6 = R06 * z0
    # # get z4
    # A4 = np.matrix( homogenousTransform(DHTable[3]) )
    # #A5 = np.matrix( homogenousTransform(DHTable[4]) )
    # H04 = H03*A4
    # R04 = H04[:3,:3]
    # z4 = R04 * z0
    # # define the end effector camera frame
    # x0_tilda = z3.transpose().tolist()[0]
    # z0_tilda = z4.transpose().tolist()[0]#np.cross(x0_tilda, y0_tilda)
    # y0_tilda = np.cross(z0_tilda,x0_tilda)#(-z5.transpose()).tolist()[0]
    # y0_tildaNorm = np.linalg.norm(y0_tilda)
    # for i in range(len(z0_tilda)):
    #     y0_tilda[i] = y0_tilda[i]/y0_tildaNorm

    # #print(x0_tilda)
    # #print(y0_tilda)
    # #print(z0_tilda)

    # # construct R00_tilda
    # x0 = x0.transpose().tolist()[0]
    # y0 = y0.transpose().tolist()[0]
    # z0 = z0.transpose().tolist()[0]
    # R00_tilda = np.matrix( [ [np.dot(x0_tilda,x0), np.dot(y0_tilda,x0), np.dot(z0_tilda,x0)], 
    #                         [np.dot(x0_tilda,y0), np.dot(y0_tilda,y0), np.dot(z0_tilda,y0)], 
    #                         [np.dot(x0_tilda,z0), np.dot(y0_tilda,z0), np.dot(z0_tilda,z0)] ] )
    # # update translation
    # xMovement = R00_tilda * np.matrix( [translationVector[0], 0, 0] ).transpose()
    # yMovement = R00_tilda * np.matrix( [0, translationVector[1], 0] ).transpose()
    # zMovement = R00_tilda * np.matrix( [0, 0, translationVector[2]] ).transpose()
    # # update rotation
    # Rx = np.matrix( [ [1, 0, 0], 
    #                     [0, math.cos(rotationVector[0]), -math.sin(rotationVector[0])], 
    #                     [0, math.sin(rotationVector[0]), math.cos(rotationVector[0])] ] )
    # Ry = np.matrix( [ [math.cos(rotationVector[1]), 0, math.sin(rotationVector[1])], 
    #                     [0, 1, 0], 
    #                     [-math.sin(rotationVector[1]), 0, math.cos(rotationVector[1])] ] )
    # Rz = np.matrix( [ [math.cos(rotationVector[2]), -math.sin(rotationVector[2]), 0], 
    #                     [math.sin(rotationVector[2]), math.cos(rotationVector[2]), 0], 
    #                     [0, 0, 1] ] )
    # Rx0_tilda = R00_tilda * Rx * R00_tilda.transpose()
    # Ry0_tilda = R00_tilda * Ry * R00_tilda.transpose()
    # Rz0_tilda = R00_tilda * Rz * R00_tilda.transpose()
    # # update homogenous transform matrix
    # updatedHomTransMatrix[0][3] += (xMovement.tolist()[0][0] + yMovement.tolist()[0][0] + zMovement.tolist()[0][0])
    # updatedHomTransMatrix[1][3] += (xMovement.tolist()[1][0] + yMovement.tolist()[1][0] + zMovement.tolist()[1][0])
    # updatedHomTransMatrix[2][3] += (xMovement.tolist()[2][0] + yMovement.tolist()[2][0] + zMovement.tolist()[2][0])
    # #rotation is happening in the order: around z -> around y -> around x
    # R06_updated = (Rx0_tilda * Ry0_tilda * Rz0_tilda * R06).tolist()
    # for i in range(3):
    #     for j in range(3):
    #         updatedHomTransMatrix[i][j] = R06_updated[i][j] 


    ### TYPE 1 fancy motions
    # update translation (in the tip reference frame)
    R06 = np.matrix( [ updatedHomTransMatrix[0][:3], updatedHomTransMatrix[1][:3], updatedHomTransMatrix[2][:3] ] )
    # forward-backward movement update
    xMovement = R06 * np.matrix( [0, 0, translationVector[0]] ).transpose()
    updatedHomTransMatrix[0][3] += xMovement.tolist()[0][0]
    updatedHomTransMatrix[1][3] += xMovement.tolist()[1][0]
    updatedHomTransMatrix[2][3] += xMovement.tolist()[2][0]
    # left-right movement update
    yMovement = R06 * np.matrix( [0, -translationVector[1], 0] ).transpose() # put "-" for the right movement direction
    updatedHomTransMatrix[0][3] += yMovement.tolist()[0][0]
    updatedHomTransMatrix[1][3] += yMovement.tolist()[1][0]
    updatedHomTransMatrix[2][3] += yMovement.tolist()[2][0]
    # up-down movement update
    zMovement = R06 * np.matrix( [translationVector[2], 0, 0] ).transpose()
    updatedHomTransMatrix[0][3] += zMovement.tolist()[0][0]
    updatedHomTransMatrix[1][3] += zMovement.tolist()[1][0]
    updatedHomTransMatrix[2][3] += zMovement.tolist()[2][0]


    # update rotation (in the tip reference frame)
    # basic rotations
    Rx = np.matrix( [ [1, 0, 0], 
                        [0, math.cos(rotationVector[1]), -math.sin(rotationVector[1])], 
                        [0, math.sin(rotationVector[1]), math.cos(rotationVector[1])] ] )
    Ry = np.matrix( [ [math.cos(rotationVector[0]), 0, math.sin(rotationVector[0])], 
                        [0, 1, 0], 
                        [-math.sin(rotationVector[0]), 0, math.cos(rotationVector[0])] ] )
    Rz = np.matrix( [ [math.cos(rotationVector[2]), -math.sin(rotationVector[2]), 0], 
                        [math.sin(rotationVector[2]), math.cos(rotationVector[2]), 0], 
                        [0, 0, 1] ] )
    # update rotation matrix
    # rotation is happening in the order: around x -> around y -> around z
    R06_updated = (R06 * Rx * Ry * Rz).tolist()


    # # left-right movement
    # updatedHomTransMatrix[1][3] += translationVector[1]
    # # up-down movement
    # updatedHomTransMatrix[2][3] += translationVector[2]
    # 
    # # update rotation
    # # update rotation about z0
    # Rz0 = np.matrix( [ [math.cos(rotationVector[1]), -math.sin(rotationVector[1]), 0], 
    #                     [math.sin(rotationVector[1]), math.cos(rotationVector[1]), 0], 
    #                     [0, 0, 1] ] )
    # # update rotation about z6
    # Rz6 = np.matrix( [ [math.cos(rotationVector[2]), -math.sin(rotationVector[2]), 0], 
    #                     [math.sin(rotationVector[2]), math.cos(rotationVector[2]), 0], 
    #                     [0, 0, 1] ] )
    # # update rotation about y0_tilda, where y0_tilda = z6 x z0/||z6 x z0||
    # # basic rotation about y in 0_tilda frame
    # Ry = np.matrix( [ [math.cos(rotationVector[0]), 0, math.sin(rotationVector[0])], 
    #                     [0, 1, 0], 
    #                     [-math.sin(rotationVector[0]), 0, math.cos(rotationVector[0])] ] )
    # # construction of rotation matrix from 0 to 0_tilda frame
    # x0 = [1, 0, 0]
    # y0 = [0, 1, 0]
    # z0 = [0, 0, 1]
    # z6_temp = (R06 * np.matrix( z0 ).transpose()).tolist()
    # z6 = [ z6_temp[0][0], z6_temp[1][0], z6_temp[2][0] ]

    # z0_tilda = copy.deepcopy(z6)

    # y0_tilda = np.cross(z6, z0)
    # y0_tildaNorm = np.linalg.norm(y0_tilda)
    # for i in range(len(y0_tilda)):
    #     y0_tilda[i] = y0_tilda[i]/y0_tildaNorm
    # y0_tilda = y0_tilda.tolist()

    # x0_tilda = np.cross(y0_tilda,z0_tilda).tolist()

    # R00_tilda = np.matrix( [ [np.dot(x0_tilda,x0), np.dot(y0_tilda,x0), np.dot(z0_tilda,x0)], 
    #                         [np.dot(x0_tilda,y0), np.dot(y0_tilda,y0), np.dot(z0_tilda,y0)], 
    #                         [np.dot(x0_tilda,z0), np.dot(y0_tilda,z0), np.dot(z0_tilda,z0)] ] )
    # Ry0_tilda = R00_tilda * Ry * R00_tilda.transpose()

    # # update rotation matrix
    # R06_updated = (Rz0 * Ry0_tilda * R06 * Rz6).tolist()

    # update homTrans matrix
    for i in range(3):
        for j in range(3):
            updatedHomTransMatrix[i][j] = R06_updated[i][j] 
    
    return updatedHomTransMatrix


def updateHomTransMatrixPositional(homTransMatrix, DHTable, translationVector, rotationVector):
    updatedHomTransMatrix = copy.deepcopy( homTransMatrix )
    global k, t
    for ind in range(3):
        translationVector[ind] = k * translationVector[ind]
        rotationVector[ind] = t * rotationVector[ind]
        # update translational part
        updatedHomTransMatrix[ind][3] += translationVector[ind] 
    
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
    initAngles = [0,0,-math.pi/2,0,0,0]

    setupAngles = []
    for i in range(len(initAngles)):
        setupAngles.append( copySavedJointAngles[i]+initAngles[i] )
        
    robot.SetActiveDOFValues(setupAngles)
    #print( robot.GetActiveDOFValues() )


def getJoystickButtons():
    pygame.event.pump()
    
    buttons = []
    for i in range(0, joystick.get_numbuttons()):
        button = joystick.get_button(i)
        buttons.append(button)
    #print(buttons)
    return buttons


# TODO MAYBE IMPLEMENT DIFFERENTLY
def sendAngleValues(qVect, start = 0):

    # stepper steps per 2*pi rotation
    q1Steps = 1000
    q2Steps = 1000
    q3Steps = 1000
    q4Steps = 1000
    q5Steps = 1000
    q6Steps = 1000
    # gripperRange = 0 - 1023
    # generate messages from qVect here q1String etc correspond to order in message, not exactly in qVect
    q1String = str( int(qVect[4] * q5Steps/(2*math.pi) ) )
    q2String = str( int(qVect[5] * q6Steps/(2*math.pi) ) )
    q3String = str( int(qVect[3] * q4Steps/(2*math.pi) ) )
    q4String = str( int(qVect[2] * q3Steps/(2*math.pi) ) )
    q5String = str( int(qVect[1] * q2Steps/(2*math.pi) ) )
    q6String = str( int(qVect[0] * q1Steps/(2*math.pi) ) )

    command = 'p'
    if start == 1:
	   command = 'g'
    message = command+"%20"+q1String+"%20"+q2String+"%20"+q3String+"%20"+q4String+"%20"+q5String+"%20"+q6String

    sendMessage(message)


    # current implementation of servo control
    buttons = getJoystickButtons()
    if buttons[22] == 1:
        message = 'o'

        sendMessage(message)
    if buttons[25] == 1:
        message = 'k'

        sendMessage(message)
    # miscellaneous buttons
    if buttons[23] == 1:
        message = 'b'

        sendMessage(message)
    if buttons[17] == 1:
        message = 'c'

        sendMessage(message)
    if buttons[18] == 1:
        message = 'd'

        sendMessage(message)
    if buttons[21] == 1:
        message = 'e'

        sendMessage(message)
    if buttons[19] == 1:
        message = 'f'

        sendMessage(message)
    if buttons[20] == 1:
        message = 'g'

        sendMessage(message)

    

def getJoystickAxes():
    out = [0,0,0,0,0,0]
    it = 0 # iterator
    pygame.event.pump()
    #Read input from the joystick       
    for i in range(0, joystick.get_numaxes()):
        out[i] = joystick.get_axis(i)
    return out


def getJoystickDirection():
    global modeOfMovement
    global savedJointAngles
    global modeOfOperation

    joystickValues = getJoystickAxes()
    print(joystickValues)

    if modeOfMovement == 0:
        print("All DOFs mode")
        # mode for all joints being controlled at once
        beforeDirectionVector = copy.deepcopy(joystickValues)
        #print(beforeDirectionVector)
        directionVector = [0,0,0,0,0,0] #beforeDirectionVector
        index = -1
        for thing in beforeDirectionVector:
            index += 1
            if abs(thing) > 0.05: # sensitivity "gap", to avoid random movements
                directionVector[index] = thing
        #print(directionVector)
    elif modeOfMovement == 1:
        print("One DOF mode")
        # mode for only one joint at once rotation
        # determine direction
        directionVector = [0,0,0,0,0,0]
        storedVal = 0
        storedInd = 0
        ind = -1
        absJoystickValues = np.absolute(np.matrix(joystickValues))
        storedInd = np.argmax(absJoystickValues)
        storedVal = joystickValues[storedInd]
        # introduce some "sensitivity gap" to avoid random movement
        if abs(storedVal) > 0.05:
            # if storedInd == 3 and modeOfOperation == 3:
            #     if savedJointAngles[5] > 0:
            #         directionVector[storedInd] = storedVal
            #     else:
            #         directionVector[storedInd] = -storedVal
            # else:
            directionVector[storedInd] = storedVal
        #print(directionVector)
        
    # needed specifically to make thigs coincide with our arm
    for i in range( len(directionVector) ):
        directionVector[i] = -directionVector[i]
    #xyz > yxz > zxy
    # swap x with y
    tempval = copy.deepcopy( directionVector[0] )
    directionVector[0] = copy.deepcopy( directionVector[1] )
    directionVector[1] = tempval
    # in new translation swap z and y
    tempval2 = copy.deepcopy( directionVector[2] )
    directionVector[2] = copy.deepcopy( directionVector[0] )
    directionVector[0] = tempval2
    # swap the z direction
    directionVector[0] = -directionVector[0]
    # rotations swaps. Remember for positionalIK mode it's rotations above yxz order
    directionVector[3] = -directionVector[3]
    directionVector[4] = directionVector[4]
    directionVector[5] = -directionVector[5]
    return directionVector


def updateServo(savedServo):
    buttons = getJoystickButtons()

    # servo moves in the range 0 -1023
    updatedServo = savedServo
    speed = 1
    if buttons[22] == 1:
        if updatedServo+speed <= 1023:
            updatedServo += speed
        else:
            print("Servo completely open")
    elif buttons[25] == 1:
        if updatedServo-speed >= 0:
            updatedServo -= speed
        else:
            print("Servo completely closed")

    return updatedServo
    

def visualizeArm(jointAngles):
    copyJointAngles = copy.deepcopy(jointAngles)
    #print("Values on visualization: {}".format(copyJointAngles))
    global robot
    global initAngles
    
    for i in range(len(copyJointAngles)):
        copyJointAngles[i] += initAngles[i]
    robot.SetActiveDOFValues(copyJointAngles)
    #print("Initial angles: {}".format(initAngles))


def resetArm():

    message = 'x'

    sendMessage(message)


def sendMessage(message):
    
    global conn

    # conn.request("PUT","/arm/"+message+"/")

    # r1 = conn.getresponse()
    # print r1.status, r1.reason
    # data1 = r1.read()
    # print data1

    # conn.request("GET", "/arm")
    # r2 = conn.getresponse()
    # print r2.status, r2.reason
    # data2 = r2.read()
    # print data2

    # conn.close()
    
def makeDHTable(jointAngles):
    #global savedServo
    #print("Current joint angles: {}".format(jointAngles))
    #print(jointAngles)
    

	# DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = [ [0, math.pi/2, 5.5, jointAngles[0]],
                [36, 0, 0, jointAngles[1]],
                [0, math.pi/2, 0, jointAngles[2]],
                [0, -math.pi/2, 32, jointAngles[3]],
                [0, math.pi/2, 0, jointAngles[4]],
                [0, 0, 15, jointAngles[5]] ]
    return DHTable

def updateAngles(DHTable, updatedDHTable):
    global k
    global modeOfOperation
    global qlim
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)

    if modeOfOperation == 1:
        #Manual mode
        uq1 = DHTable[0][3] + 0.002 * 2*math.pi * joystickDirection[1]#sr
        uq2 = DHTable[1][3] + 0.0006 * 2*math.pi * joystickDirection[2]#sp
        uq3 = DHTable[2][3] + 0.001 * 2*math.pi * joystickDirection[0]#eb
        uq4 = DHTable[3][3] + 0.005 * 2*math.pi * joystickDirection[4]#w3
        uq5 = DHTable[4][3] + 0.005 * 2*math.pi * joystickDirection[3]#w1
        uq6 = DHTable[5][3] + 0.005 * 2*math.pi * joystickDirection[5]#w2
    elif modeOfOperation == 2:
        #Positional IK mode
        uq1 = updatedDHTable[0][3]
        uq2 = updatedDHTable[1][3]
        uq3 = updatedDHTable[2][3]
        uq4 = DHTable[3][3] + updatedDHTable[3][3]
        uq5 = DHTable[4][3] + updatedDHTable[4][3]
        uq6 = DHTable[5][3] + updatedDHTable[5][3]
    elif modeOfOperation == 3:
        #Full IK mode
        uq1 = updatedDHTable[0][3]
        uq2 = updatedDHTable[1][3]
        uq3 = updatedDHTable[2][3]
        uq4 = updatedDHTable[3][3]
        uq5 = updatedDHTable[4][3]
        uq6 = updatedDHTable[5][3]
    elif modeOfOperation == 4:
        #Manual no memory mode
        uq1 = DHTable[0][3] + 0.002 * 2*math.pi * joystickDirection[1] * k / 0.6#sr
        uq2 = DHTable[1][3] + 0.0006 * 2*math.pi * joystickDirection[2] * k / 0.3#sp
        uq3 = DHTable[2][3] + 0.001 * 2*math.pi * joystickDirection[0] * k / 0.3#eb
        uq4 = DHTable[3][3] + 0.005 * 2*math.pi * joystickDirection[4] * k / 0.3#w3
        uq5 = DHTable[4][3] + 0.005 * 2*math.pi * joystickDirection[3] * k / 0.3#w1
        uq6 = DHTable[5][3] + 0.005 * 2*math.pi * joystickDirection[5] * k / 0.3#w2
    uq = [uq1, uq2, uq3, uq4, uq5, uq6]
    maxRot = 2*math.pi*10/360
    update = 1
    for i in range(6):
        if(uq[i] <= qlim[i][0] or uq[i] >= qlim[i][1] or abs(uq[i] - DHTable[i][3]) > maxRot):
            update = 0
            break
    if(update == 0):
        for i in range(6):
            uq[i] = DHTable[i][3]       #Do not change angle if it exceeds the limits.


    return uq

def manual_no_memory():
    
    # get the current joint angles of the arm
    global tempAngles
    jointAngles = copy.deepcopy(tempAngles)
    # joint variables limits (in degrees), format [min, max]

    DHTable = makeDHTable(jointAngles)
    
    uq = updateAngles(DHTable, 0)

    # update servo value
    #servoValueNew = updateServo(savedServo)
    try:
        jointAngles = copy.deepcopy( uq )

        #savedServo = servoValueNew

        tempAngles = copy.deepcopy( jointAngles )
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(tempAngles)

        visualizeArm(tempAngles)
        print(tempAngles)
        
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )

        #savedServo = savedServo

        tempAngles = copy.deepcopy( jointAngles )
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(tempAngles)

        visualizeArm(tempAngles)
        print(tempAngles)


def manual():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of the arm
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles)
    # joint variables limits (in degrees), format [min, max]

    DHTable = makeDHTable(jointAngles)
    # do forward kinematics
    DHTableCopy = copy.deepcopy(DHTable)
    #homTransMatrix = forwardKinematics(DHTableCopy)
    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)
    
    uq = updateAngles(DHTable, 0)

    # update servo value
    #servoValueNew = updateServo(savedServo)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)
        savedJointAngles = copy.deepcopy(jointAngles)

        #savedServo = servoValueNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles)) 
        savedJointAngles = copy.deepcopy(jointAngles)

        #savedServo = savedServo
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        print(savedJointAngles)


def positionalIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of  the arm
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles)
    # joint variables limits (in degrees), format [min, max]


    # DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = makeDHTable(jointAngles)

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
    updatedDHTable = inverseKinematicsPositional(DHTableCopy3, copyUpdatedHomTransMatrix, rotationVector)

    uq = updateAngles(DHTable, updatedDHTable)
    # update servo value
    #servoValueNew = updateServo(savedServo)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)

        #savedServo = servoValueNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))

        #savedServo = savedServo
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        print(savedJointAngles)
    

def fullIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction: {}".format(joystickDirection))
    # get the current joint angles of the arm
    global savedJointAngles          
    jointAngles = copy.deepcopy(savedJointAngles)
    # joint variables limits (in degrees), format [min, max]

    DHTable = makeDHTable(jointAngles)

    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)

    # update homogenous transformation matrix based on joystick input
    translationVector = joystickDirection[:3]
    rotationVector = joystickDirection[3:]

    DHTableCopy = copy.deepcopy(DHTable)
    homTransMatrix = forwardKinematics(DHTableCopy)
    copyHomTransMatrix = copy.deepcopy(homTransMatrix)
    updatedHomTransMatrix = updateHomTransMatrix(copyHomTransMatrix, DHTableCopy, translationVector, rotationVector)
    #print("Updated position: ")
    #print([ updatedHomTransMatrix[0][3], updatedHomTransMatrix[1][3], updatedHomTransMatrix[2][3] ])

    # solve IK based on the new homTransMatrix
    DHTableCopy2 = copy.deepcopy(DHTable)
    copyUpdatedHomTransMatrix = copy.deepcopy(updatedHomTransMatrix)
    updatedDHTable = inverseKinematics(DHTableCopy2, copyUpdatedHomTransMatrix)
    
    uq = updateAngles(DHTable, updatedDHTable)
    # update servo value
    #servoValueNew = updateServo(savedServo)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        
        savedJointAngles = copy.deepcopy(jointAngles)

        #savedServo = servoValueNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        print(savedJointAngles)
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))
        savedJointAngles = copy.deepcopy(jointAngles)

        #savedServo = savedServo
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!! or just do nothing?
        sendAngleValues(savedJointAngles)
        
        visualizeArm(savedJointAngles)
        #print("Joint angles and servo are {}, {}".format(savedJointAngles, savedServo) )
        #print(savedJointAngles)


def updateOperationMode():
    global modeOfOperation
    global tempAngles
    global savedJointAngles

    buttons = getJoystickButtons()
    if buttons[28] == 1:
        if modeOfOperation == 4: # needed specifically to make manual without memory mode work
            sendMessage('v')
        modeOfOperation = 1
        print("Switched to manual mode")
        tempAngles = copy.deepcopy(savedJointAngles) # needed specifically to make manual without memory mode work
        return modeOfOperation
    elif buttons[27] == 1:
        if modeOfOperation == 4: # needed specifically to make manual without memory mode work
            sendMessage('v')
        modeOfOperation = 2
        print("Switched to positional IK mode")
        tempAngles = copy.deepcopy(savedJointAngles) # needed specifically to make manual without memory mode work
        return modeOfOperation
    elif buttons[26] == 1:
        if modeOfOperation == 4: # needed specifically to make manual without memory mode work
            sendMessage('v')
        modeOfOperation = 3
        print("Switched to full IK mode")
        tempAngles = copy.deepcopy(savedJointAngles) # needed specifically to make manual without memory mode work
        return modeOfOperation
    elif buttons[1] == 1:
        if modeOfOperation == 4: # needed specifically to make manual without memory mode work
            sendMessage('v')
        modeOfOperation = 4
        print("Switched to manual-no-memory mode")
        tempAngles = copy.deepcopy(savedJointAngles) # needed specifically to make manual without memory mode work
        sendMessage('q')
        return modeOfOperation


def updateModeOfMovement():
    global modeOfMovement

    buttons = getJoystickButtons()
    if buttons[24] == 1:
        modeOfMovement = 0
        print("Switched to all DOFs mode")
        return modeOfMovement
    elif buttons[0] == 1:
        modeOfMovement = 1
        print("Switched to one DOF mode")
        return modeOfMovement


def updateSpeed():
    global k, t
    buttons = getJoystickButtons()

    if buttons[29] == 1:
        k *= 1.5
        t *= 1.5
        print("Speed increased")
    if buttons[30] == 1:
        k /= 1.5
        t /= 1.5
        print("Speed decreased")
    while buttons[30] or buttons[29]:
        buttons = getJoystickButtons()
        continue


def main():
    # TODO GET THE MODE OF OPERATION
    # modes: '1'-manual, '2'-positional IK (first 3 joints), '3'-full IK
    global modeOfOperation
    global storageFile
    # resetting the IK model to zero position upon request 
    global savedJointAngles
    buttons = getJoystickButtons()
    if buttons[6] == 1: # reset servos and model to complete zero position
        savedJointAngles = [0,0,0,0,0,0]
        startTime = time.time()
        endTime = time.time()
        while endTime - startTime < 3:
            resetArm()
            endTime = time.time()
            time.sleep(0.02)

    updateOperationMode()
    updateModeOfMovement()
    updateSpeed()
    if modeOfOperation == 1:
        print("Manual mode")
        manual()
    elif modeOfOperation == 2:
        print("Positional IK mode")
        positionalIK()
    elif modeOfOperation == 3:
        print("Full IK mode")
        fullIK()
    elif modeOfOperation == 4:
        print("Manual no memory mode")
        manual_no_memory()

    # saving the current arm status just in case
    storageFile = open('savedJointAngles.txt', 'w')
    storageFile.write( str(savedJointAngles) )
    storageFile.close()
        
    # frequency in Hz
    frequency = 50
    timeDelay =  1.0/frequency
    #print(timeDelay)
    time.sleep(timeDelay)


if __name__ == "__main__":
    global savedJointAngles
    global savedServo
    global modeOfOperation
    global storageFile
    global tempAngles
    global modeOfMovement # either motion in every DOF at once or only one DOF at once, "0" - all DOFs, "1" - one DOF
    global k, t # velocity coefficients for translational and rotational motions, correspondingly
    global qlim
    k = 0.6
    t = 0.03
    modeOfMovement = 0 # all DOFs mode by default
    modeOfOperation = 2 # positional IK mode by default

    serverIP = '192.168.0.123'
    serverHttpPort = '8080'
    global conn
    conn = httplib.HTTPConnection(serverIP+":"+serverHttpPort)

    # choose between import and non-import modes
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
        sendAngleValues(savedJointAngles, 1) # MAYBE IMPLEMENT DIFFERENTLY
    else:
        savedJointAngles = [0,0,0,0,0,0]
        resetArm()

    qlim = np.array([[-180, 180], [-45, 315], [-180, 180], [-175, 175], [-175, 175], [-180, 180]]) * math.pi/180
    #qlim = np.array([[-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000]]) * math.pi/180
    #In the order of q1lim to q6lim [min,max]
    #savedServo = 0
    setupVisualEnv()
    initializeJoystick()
    #resetArm()
    
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
                #continue
        else:
            continue
    
    print("Shut the operations down")
    
