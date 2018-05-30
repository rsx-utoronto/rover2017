#! /usr/bin/env python
# imports
import copy
import time
import openravepy
import numpy as np
import pygame
import math
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


    ## TYPE0 fancy motions, relative to the camera reference frame
    ## update movement in the end effector camera frame
    x0 = np.matrix( [1, 0, 0] ).transpose()
    y0 = np.matrix( [0, 1, 0] ).transpose()
    z0 = np.matrix( [0, 0, 1] ).transpose()

    # get z4
    A1 = np.matrix( homogenousTransform(DHTable[0]) )
    A2 = np.matrix( homogenousTransform(DHTable[1]) )
    A3 = np.matrix( homogenousTransform(DHTable[2]) )
    A4 = np.matrix( homogenousTransform(DHTable[3]) )
    H04 = A1*A2*A3*A4
    R04 = H04[:3,:3]
    z4 = R04 * z0
    
    #get z6
    R06 = np.matrix( [ updatedHomTransMatrix[0][:3], updatedHomTransMatrix[1][:3], updatedHomTransMatrix[2][:3] ] )
    z6 = R06 * z0

    # define the end effector camera frame
    z0_tilda = z6.transpose().tolist()[0]
    y0_tilda = z4.transpose().tolist()[0]
    x0_tilda = np.cross(y0_tilda,z0_tilda)
    x0_tildaNorm = np.linalg.norm(x0_tilda)
    for i in range(len(z0_tilda)):
        x0_tilda[i] = x0_tilda[i]/x0_tildaNorm

    #print(x0_tilda)
    #print(y0_tilda)
    #print(z0_tilda)

    # construct R00_tilda
    x0 = x0.transpose().tolist()[0]
    y0 = y0.transpose().tolist()[0]
    z0 = z0.transpose().tolist()[0]
    R00_tilda = np.matrix( [ [np.dot(x0_tilda,x0), np.dot(y0_tilda,x0), np.dot(z0_tilda,x0)], 
                            [np.dot(x0_tilda,y0), np.dot(y0_tilda,y0), np.dot(z0_tilda,y0)], 
                            [np.dot(x0_tilda,z0), np.dot(y0_tilda,z0), np.dot(z0_tilda,z0)] ] )
    # update translation
    xMovement = R00_tilda * np.matrix( [translationVector[2], 0, 0] ).transpose()
    yMovement = R00_tilda * np.matrix( [0, -translationVector[1], 0] ).transpose()
    zMovement = R00_tilda * np.matrix( [0, 0, translationVector[0]] ).transpose()
    # update rotation
    Rx = np.matrix( [ [1, 0, 0], 
                        [0, math.cos(rotationVector[1]), -math.sin(rotationVector[1])], 
                        [0, math.sin(rotationVector[1]), math.cos(rotationVector[1])] ] )
    Ry = np.matrix( [ [math.cos(rotationVector[0]), 0, math.sin(rotationVector[0])], 
                        [0, 1, 0], 
                        [-math.sin(rotationVector[0]), 0, math.cos(rotationVector[0])] ] )
    Rz = np.matrix( [ [math.cos(rotationVector[2]), -math.sin(rotationVector[2]), 0], 
                        [math.sin(rotationVector[2]), math.cos(rotationVector[2]), 0], 
                        [0, 0, 1] ] )
    Rx0_tilda = R00_tilda * Rx * R00_tilda.transpose()
    Ry0_tilda = R00_tilda * Ry * R00_tilda.transpose()
    Rz0_tilda = R00_tilda * Rz * R00_tilda.transpose()
    # update homogenous transform matrix
    updatedHomTransMatrix[0][3] += (xMovement.tolist()[0][0] + yMovement.tolist()[0][0] + zMovement.tolist()[0][0])
    updatedHomTransMatrix[1][3] += (xMovement.tolist()[1][0] + yMovement.tolist()[1][0] + zMovement.tolist()[1][0])
    updatedHomTransMatrix[2][3] += (xMovement.tolist()[2][0] + yMovement.tolist()[2][0] + zMovement.tolist()[2][0])
    #rotation is happening in the order: around z -> around y -> around x
    R06_updated = (Rx0_tilda * Ry0_tilda * Rz0_tilda * R06).tolist()
    #print R06_updated


    # ### TYPE 1 fancy motions
    # # update translation (in the tip reference frame)
    # R06 = np.matrix( [ updatedHomTransMatrix[0][:3], updatedHomTransMatrix[1][:3], updatedHomTransMatrix[2][:3] ] )
    # # forward-backward movement update
    # xMovement = R06 * np.matrix( [0, 0, translationVector[0]] ).transpose()
    # updatedHomTransMatrix[0][3] += xMovement.tolist()[0][0]
    # updatedH        momTransMatrix[1][3] += xMovement.tolist()[1][0]
    # updatedHomTransMatrix[2][3] += xMovement.tolist()[2][0]
    # # left-right movement update
    # yMovement = R06 * np.matrix( [0, -translationVector[1], 0] ).transpose() # put "-" for the right movement direction
    # updatedHomTransMatrix[0][3] += yMovement.tolist()[0][0]
    # updatedHomTransMatrix[1][3] += yMovement.tolist()[1][0]
    # updatedHomTransMatrix[2][3] += yMovement.tolist()[2][0]
    # # up-down movement update
    # zMovement = R06 * np.matrix( [translationVector[2], 0, 0] ).transpose()
    # updatedHomTransMatrix[0][3] += zMovement.tolist()[0][0]
    # updatedHomTransMatrix[1][3] += zMovement.tolist()[1][0]
    # updatedHomTransMatrix[2][3] += zMovement.tolist()[2][0]


    # # update rotation (in the tip reference frame)
    # # basic rotations
    # Rx = np.matrix( [ [1, 0, 0], 
    #                     [0, math.cos(rotationVector[1]), -math.sin(rotationVector[1])], 
    #                     [0, math.sin(rotationVector[1]), math.cos(rotationVector[1])] ] )
    # Ry = np.matrix( [ [math.cos(rotationVector[0]), 0, math.sin(rotationVector[0])], 
    #                     [0, 1, 0], 
    #                     [-math.sin(rotationVector[0]), 0, math.cos(rotationVector[0])] ] )
    # Rz = np.matrix( [ [math.cos(rotationVector[2]), -math.sin(rotationVector[2]), 0], 
    #                     [math.sin(rotationVector[2]), math.cos(rotationVector[2]), 0], 
    #                     [0, 0, 1] ] )
    # # update rotation matrix
    # # rotation is happening in the order: around x -> around y -> around z
    # R06_updated = (R06 * Rx * Ry * Rz).tolist()
    # #print R06_updated


    ###!!! move the end effector to the specific predAll DOFs modeefined orientation, based on the predefined rotation matrices
    buttons = getJoystickButtons()
    #print buttons

    # turn to "Down" orientation
    if buttons[21] == 1:
        R06_updated = np.matrix( [ [1, 0, 0],
                                    [0, -1, 0],
                                    [0, 0, -1] ] ).tolist()
    # # turn to "Forward" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [0, 0, 1],
    #                                 [0, -1, 0],
    #                                 [1, 0, 0] ] ).tolist()
    # # turn to "Left" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [0, -1, 0],
    #                                 [0, 0, -1],
    #                                 [1, 0, 0] ] ).tolist()
    # # turn to "Right" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [0, 1, 0],
    #                                 [0, 0, 1],
    #                                 [1, 0, 0] ] ).tolist()
    # # turn to "Left-Forward" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [0, -1/math.sqrt(2), 1/math.sqrt(2)],
    #                                 [0, -1/math.sqrt(2), -1/math.sqrt(2)],
    #                                 [1, 0, 0] ] ).tolist()
    # # turn to "Right-Forward" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [0, 1/math.sqrt(2), 1/math.sqrt(2)],
    #                                 [0, -1/math.sqrt(2), 1/math.sqrt(2)],
    #                                 [1, 0, 0] ] ).tolist()
    # # turn to "Forward-Down" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [1/math.sqrt(2), 0, 1/math.sqrt(2)],
    #                                 [0, -1, 0],
    #                                 [1/math.sqrt(2), 0, -1/math.sqrt(2)] ] ).tolist()
    # # turn to "Forward-Up" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1/math.sqrt(2), 0, 1/math.sqrt(2)],
    #                                 [0, -1, 0],
    #                                 [1/math.sqrt(2), 0, 1/math.sqrt(2)] ] ).tolist()
    # # turn to "Left-Down" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [1, 0, 0],
    #                                 [0, -1/math.sqrt(2), -1/math.sqrt(2)],
    #                                 [0, 1/math.sqrt(2), -1/math.sqrt(2)] ] ).tolist()
    # # turn to "Right-Down" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [1, 0, 0],
    #                                 [0, -1/math.sqrt(2), 1/math.sqrt(2)],
    #                                 [0, -1/math.sqrt(2), -1/math.sqrt(2)] ] ).tolist()
    # # turn to "Forward-Up-Left" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), -1/math.sqrt(3), -1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)] ] ).tolist()
    # # turn to "Forward-Up-Right" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)] ] ).tolist()
    # # turn to "Forward-Down-Left" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [-1/math.sqrt(3), -1/math.sqrt(3), -1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), 1/math.sqrt(3), -1/math.sqrt(3)] ] ).tolist()
    # # turn to "Forward-Down-Right" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [1/math.sqrt(3), 1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), -1/math.sqrt(3), 1/math.sqrt(3)],
    #                                 [1/math.sqrt(3), 1/math.sqrt(3), -1/math.sqrt(3)] ] ).tolist()
    # # turn to "Up" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1, 0, 0],
    #                                 [0, -1, 0],
    #                                 [0, 0, 1] ] ).tolist()
    # # turn to "Left-Up" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1, 0, 0],
    #                                 [0, -1/math.sqrt(2), -1/math.sqrt(2)],
    #                                 [0, -1/math.sqrt(2), 1/math.sqrt(2)] ] ).tolist()
    # # turn to "Right-Up" orientation
    # elif buttons[21] == 1:
    #     R06_updated = np.matrix( [ [-1, 0, 0],
    #                                 [0, -1/math.sqrt(2), 1/math.sqrt(2)],
    #                                 [0, 1/math.sqrt(2), 1/math.sqrt(2)] ] ).tolist()
   
    #print R06_updated
    # update homTrans matrix
    for i in range(3):
        for j in range(3):
            updatedHomTransMatrix[i][j] = R06_updated[i][j] 
    #print updatedHomTransMatrix
    
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

    # encoder steps per 2*pi rotation
    q1Steps = 1680.0 * 60/24
    q2Steps = 2048*4
    q3Steps = 2048*4
    q4Steps = 1680
    q5Steps = 1680
    q6Steps = 1680
    q7Steps = 1#26.9*64 # gripper
    # generate messages from qVect here q1String etc correspond to order in message, not exactly in qVect
    q1String = str( int(qVect[0] * q1Steps/(2*math.pi) ) )
    q2String = str( int(qVect[1] * q2Steps/(2*math.pi) ) )
    q3String = str( int(qVect[2] * q3Steps/(2*math.pi) ) )
    q4String = str( int(qVect[3] * q4Steps/(2*math.pi) ) )
    q5String = str( int(qVect[4] * q5Steps/(2*math.pi) ) )
    q6String = str( int(qVect[5] * q6Steps/(2*math.pi) ) )
    q7String = str( int(qVect[6] * q7Steps ) ) # gripper

    command = 'p'
    #if start == 1:
	#   command = 'g'
    message = command+"%20"+q1String+"%20"+q2String+"%20"+q3String+"%20"+q4String+"%20"+q5String+"%20"+q6String+"%20"+q7String

    sendMessage(message)


    # # current implementation of servo control
    # buttons = getJoystickButtons()
    # if buttons[22] == 1:
    #     message = 'o'
    #     sendMessage(message)
    # if buttons[25] == 1:
    #     message = 'k'
    #     sendMessage(message)
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
    print("Joystick direction values: {}".format(joystickValues))

    if modeOfMovement == 0:
        print("     All DOFs mode")
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
        print("     One DOF mode")
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


def updateGripperAngle(localSavedGripperAngle):
    buttons = getJoystickButtons()


    # servo moves in the range 0 -1023
    updatedGripperAngle = localSavedGripperAngle
    step = 100
    if buttons[22] == 1:
        if updatedGripperAngle+step <= 21000:
            updatedGripperAngle += step
        else:
            print("Gripper completely open")
    elif buttons[25] == 1:
        if updatedGripperAngle-step >= 0:
            updatedGripperAngle -= step
        else:
            print("Gripper completely closed")

    return updatedGripperAngle
    

def visualizeArm(jointAngles):
    copyJointAngles = copy.deepcopy(jointAngles)
    #print("Values on visualization: {}".format(copyJointAngles))
    global robot
    global initAngles
    
    for i in range(len(copyJointAngles)):
        copyJointAngles[i] += initAngles[i]
    robot.SetActiveDOFValues(copyJointAngles)
    #print("Initial angles: {}".format(initAngles))


# def resetArm():

#     message = 'x'
#     sendMessage(message)


def sendMessage(message):
    
    global conn

    conn.request("PUT","/arm/"+message+"/")

    # r1 = conn.getresponse()
    # print r1.status, r1.reason
    # data1 = r1.read()
    # print data1

    # conn.request("GET", "/arm")
    # r2 = conn.getresponse()
    # print r2.status, r2.reason
    # data2 = r2.read()
    # print data2

    conn.close()
    
def makeDHTable(jointAngles):
    #print("Current joint angles: {}".format(jointAngles))
    #print(jointAngles)
    
	# DH Table with entries in the format: [a, alpha, d, theta]
    # First links are first entries
    DHTable = [ [0, math.pi/2, 5.5, jointAngles[0]],
                [36, 0, 0, jointAngles[1]],
                [0, math.pi/2, 0, jointAngles[2]],
                [0, -math.pi/2, 35.683, jointAngles[3]],
                [0, math.pi/2, 0, jointAngles[4]],
                [0, 0, 18, jointAngles[5]] ]
    return DHTable

def updateAngles(DHTable, updatedDHTable, joystickDirection):
    global k
    global modeOfOperation
    global qlim
    global maxRot

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
    uq = [uq1, uq2, uq3, uq4, uq5, uq6]
    update = 1
    for i in range(6):
        if(uq[i] <= qlim[i][0] or uq[i] >= qlim[i][1] or abs(uq[i] - DHTable[i][3]) > maxRot):
            update = 0
            break
    if(update == 0):
        for i in range(6):
            uq[i] = DHTable[i][3]       #Do not change angle if it exceeds the limits.


    return uq


def manual():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of the arm
    global savedJointAngles
    global savedGripperAngle
    jointAngles = copy.deepcopy(savedJointAngles)

    DHTable = makeDHTable(jointAngles)
    # do forward kinematics
    DHTableCopy = copy.deepcopy(DHTable)
    #homTransMatrix = forwardKinematics(DHTableCopy)
    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)
    
    uq = updateAngles(DHTable, 0, joystickDirection)

    # update gripper value
    gripperAngleNew = updateGripperAngle(savedGripperAngle)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)
        savedJointAngles = copy.deepcopy(jointAngles)
        savedGripperAngle = gripperAngleNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles)) 
        savedJointAngles = copy.deepcopy(jointAngles)
        savedGripperAngle = savedGripperAngle
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )


def positionalIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction:")
    #print(joystickDirection)
    # get the current joint angles of  the arm
    global savedJointAngles
    global savedGripperAngle
    jointAngles = copy.deepcopy(savedJointAngles)

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

    uq = updateAngles(DHTable, updatedDHTable, joystickDirection)
    # update gripper value
    gripperAngleNew = updateGripperAngle(savedGripperAngle)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        #print(jointAngles)

        savedGripperAngle = gripperAngleNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))

        savedGripperAngle = savedGripperAngle
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        savedJointAngles = copy.deepcopy(jointAngles)
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )
    

def fullIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print("Current joystick direction: {}".format(joystickDirection))
    # get the current joint angles of the arm
    global savedJointAngles
    global savedGripperAngle          
    jointAngles = copy.deepcopy(savedJointAngles)

    DHTable = makeDHTable(jointAngles)

    #print("Current position: " )
    #print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)

    # update homogenous transformation matrix based on joystick input
    translationVector = joystickDirection[:3]
    rotationVector = joystickDirection[3:]

    DHTableCopy = copy.deepcopy(DHTable)
    homTransMatrix = forwardKinematics(DHTableCopy)
    #print homTransMatrix
    copyHomTransMatrix = copy.deepcopy(homTransMatrix)
    updatedHomTransMatrix = updateHomTransMatrix(copyHomTransMatrix, DHTableCopy, translationVector, rotationVector)
    #print("Updated position: ")
    #print updatedHomTransMatrix

    # solve IK based on the new homTransMatrix
    DHTableCopy2 = copy.deepcopy(DHTable)
    #print "DHTable: "
    #print DHTableCopy2
    copyUpdatedHomTransMatrix = copy.deepcopy(updatedHomTransMatrix)
    updatedDHTable = inverseKinematics(DHTableCopy2, copyUpdatedHomTransMatrix)
    #print "DHTable updated: "
    #print updatedDHTable
    
    uq = updateAngles(DHTable, updatedDHTable, joystickDirection)
    # update gripper value
    gripperAngleNew = updateGripperAngle(savedGripperAngle)
    try:
        jointAngles = copy.deepcopy( uq )
        #print("Updated joint angles: {}".format(jointAngles))
        
        savedJointAngles = copy.deepcopy(jointAngles)

        savedGripperAngle = gripperAngleNew
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )
    except:
        print("Exception encountered")
        jointAngles = copy.deepcopy( [q1,q2,q3,q4,q5,q6] )
        #print("Updated joint angles: {}".format(jointAngles))
        savedJointAngles = copy.deepcopy(jointAngles)

        savedGripperAngle = savedGripperAngle
        
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!! or just do nothing?
        sendAngles = [ savedJointAngles[0], savedJointAngles[1], savedJointAngles[2], savedJointAngles[3], savedJointAngles[4], savedJointAngles[5], savedGripperAngle ]
        sendAngleValues(sendAngles)
        
        visualizeArm(savedJointAngles)
        print("Joint angles and gripper: \n Shoulder Rotation(q1): {} \n Shoulder Pitch(q2): {} \n Elbow(q3): {} \n W1(q4): {} \n W2(q5): {} \n W3(q6): {} \n Gripper value: {} \n".format( savedJointAngles[0]*180/math.pi, savedJointAngles[1]*180/math.pi, savedJointAngles[2]*180/math.pi, savedJointAngles[3]*180/math.pi, savedJointAngles[4]*180/math.pi, savedJointAngles[5]*180/math.pi, savedGripperAngle ) )
        #print( np.array(savedJointAngles) * 180/math.pi )


def updateOperationMode():
    global modeOfOperation
    global tempAngles
    global savedJointAngles

    buttons = getJoystickButtons()
    if buttons[28] == 1:
        modeOfOperation = 1
        print("Switched to manual mode")
        return modeOfOperation
    elif buttons[27] == 1:
        modeOfOperation = 2
        print("Switched to positional IK mode")
        return modeOfOperation
    elif buttons[26] == 1:
        modeOfOperation = 3
        print("Switched to full IK mode")
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
    if buttons[11] == 1: # reset model to complete initial position
        init_q2 = 1956.0/(2048*4)*360
        init_q3 = 1263.0/(2048*4)*360
        savedJointAngles = np.array([0,init_q2,init_q3,0,0,0]) * math.pi/180 # degrees
        print("Arm reset to Zero pose")

    updateOperationMode()
    updateModeOfMovement()
    updateSpeed()
    if modeOfOperation == 1:
        print("     Manual mode")
        manual()
    elif modeOfOperation == 2:
        print("     Positional IK mode")
        positionalIK()
    elif modeOfOperation == 3:
        print("     Full IK mode")
        fullIK()
        


if __name__ == "__main__":
    global savedJointAngles
    global savedGripperAngle
    global modeOfOperation
    global storageFile
    global tempAngles
    global modeOfMovement # either motion in every DOF at once or only one DOF at once, "0" - all DOFs, "1" - one DOF
    global k, t # velocity coefficients for translational and rotational motions
    global qlim
    global maxRot # determines max rotation by a joint per turn
    maxRot = 2*math.pi*10000/360 
    k = 0.6
    t = 0.03
    modeOfMovement = 0 # all DOFs mode by default
    modeOfOperation = 2 # positional IK mode by default

    serverIP = '192.168.0.3'
    serverHttpPort = '8080'
    global conn
    conn = httplib.HTTPConnection(serverIP+":"+serverHttpPort)

    init_q2 = 1956.0/(2048*4)*360
    init_q3 = 1263.0/(2048*4)*360
    savedJointAngles = np.array([0,init_q2,init_q3,0,0,0]) * math.pi/180 # degrees

    #In the order of q1lim to q6lim [min,max]
    lim_q1_min = -1400.0/(1680.0 * 60/24) *360
    lim_q1_max = 3000.0/(1680.0 * 60/24) *360
    lim_q2_min = -2158.0/(2048*4) *360
    lim_q2_max = 1956.0/(2048*4) *360
    lim_q3_min = -1180.0/(2048*4) *360
    lim_q3_max = 1263.0/(2048*4) *360
    lim_q4_min = -840.0/(1680) *360
    lim_q4_max = 840.0/(1680) *360
    lim_q5_min = -550.0/(1680) *360
    lim_q5_max = 400/(1680) *360
    lim_q6_min = -10000000000.0/(1680) *360
    lim_q6_max = 10000000000.0/(1680) *360

    qlim = np.array([[lim_q1_min, lim_q1_max], [lim_q2_min, lim_q2_max], [lim_q3_min, lim_q3_max], [lim_q4_min, lim_q4_max], [lim_q5_min, lim_q5_max], [lim_q6_min, lim_q6_max]]) * math.pi/180 # degrees
    #qlim = np.array([[-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000], [-18000, 18000]]) * math.pi/180
    savedGripperAngle = 0
    setupVisualEnv()
    initializeJoystick()
    #resetArm()
    
    while True:

        # frequency of the loop in Hz
        frequency = 50
        timeDelay =  1.0/frequency
        #print(timeDelay)
        time.sleep(timeDelay)

        # TODO
        turnedOn = False #GET THE TURNED_ON MODE FROM SOMEWHERE
        axes = getJoystickAxes()
        buttons = getJoystickButtons()
        #print axes
        #print buttons
        absAxesSum = 0
        for axis in axes:
            absAxesSum += abs(axis)
        #print absAxesSum
        # if one of the buttons pressed or one of the axes moved, move on!
        if (absAxesSum > 0 or 1 in buttons):
            turnedOn = True
        #print turnedOn
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
    
