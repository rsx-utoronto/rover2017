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

    Rd = np.matrix( [ homTransMatrix[0][:3], homTransMatrix[1][:3], homTransMatrix[2][:3] ] )
    od = np.matrix( [ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ] ).transpose()

    arD6 = np.matrix( [ 0,0,d6] ).transpose()
    #print(arD6)
    #print(arD6.transpose())
    #print(Rd)
    oc = od - Rd * arD6
    #print(np.dot(Rd,arD6))
    #print(np.dot(Rd,arD6.transpose()))
    print(oc.tolist()[0][0])

    

    xc = oc[0]
    yc = oc[1]
    zc = oc[2]

    q1 = math.atan2(yc, xc)
    
    Dtemp = ( xc**2 + yc**2 + (zc-d1)**2 - a2**2 - d4**2 )/( 2*a2*d4 )
    if abs(Dtemp) > 1:
        print( 'Can not reach {}, {}, {}'.format( homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ) )
        return dhTable
    
    q3 = math.atan2( Dtemp, math.sqrt(1 - Dtemp**2) ) # assumes we chose to always have 'elbow up' solution
    
    q2 = math.atan2( zc - d1, math.sqrt(xc**2 + yc**2) ) - math.atan2( d4*math.sin(q3-math.pi/2), a2+d4*math.cos(q3-math.pi/2) )
    
    H01 = np.matrix( homogenousTransform(dhTable[0]) )
    H12 = np.matrix( homogenousTransform(dhTable[1]) )
    H23 = np.matrix( homogenousTransform(dhTable[2]) )
    H03 = (H01 * H12 * H23).tolist()
    R03 = np.matrix( [H03[0][:3], H03[1][:3], H03[2][:3]] )
    #print(R03)
    #print(R03.transpose())
    R36 = np.dot(R03.transpose(), Rd)
    #print( np.dot(R03, Rd) )
    #print( np.dot(R03.transpose(), Rd) )

    q4 = math.atan2( R36[1][2], R36[0][2] )
    q5 = math.atan2( math.sqrt(1 - R36[2][2]**2), R36[2][2] )
    q6 = math.atan2( R36[2][1], -R36[2][0] )

    # updating DH table
    updatedDHTable = copy.deepcopy(dhTable)
    updatedDHTable[0][3] = q1
    updatedDHTable[1][3] = q2
    updatedDHTable[2][3] = q3
    updatedDHTable[3][3] = q4
    updatedDHTable[4][3] = q5
    updatedDHTable[5][3] = q6
    
    return updatedDHTable


#TODO IMPLEMENT
def updateHomTransMatrix(homTransMatrix, DHTable, translationVector, rotationVector):
    updatedHomTransMatrix = copy.deepcopy( homTransMatrix )
    # update translation part
    k = 1 # amplification coefficient translational motion
    t = 1 # amplification coefficient rotational motion
    for ind in range(3):
        translationVector[ind] = k * translationVector[ind]
        rotationVector[ind] = t * rotationVector[ind]
    
    # update translational part
    for i in range(3):
        updatedHomTransMatrix[i][3] += translationVector[i] 
    # TODO update rotational part
    
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
    return directionVector
    

# TODO IMPLEMENT
def visualizeArm(jointAngles):
    copyJointAngles = copy.deepcopy(jointAngles)
    global robot
    global initAngles
    # invert signs of q4 and q6. Needed specifically for visualizer
    copyJointAngles[3] = -copyJointAngles[3]
    copyJointAngles[5] = -copyJointAngles[5]
    
    for i in range(len(copyJointAngles)):
        copyJointAngles[i] += initAngles[i]
    robot.SetActiveDOFValues(copyJointAngles)
    

# TODO IMPLEMENT
def setJointAngles(qVector):
    # SET JOINT ANGLES
    return


# TODO IMPLEMENT gets them from the arm
def getJointAngles():
    #global currentJointAngles

    #initialJointAngles = [0,0,0,0,0,0]
    #if justStarted:
    #    currentJointAngles = initialJointAngles
    #    justStarted = False
    jointAngles = [0.1,0.1,0.1,0.1,0.1,0.1] # IMPLEMENT GETTING THEM CORRECTLY
    visualizeArm(jointAngles)
    return jointAngles


# TODO IMPLEMENT
def setJointAngles(qVector):
    jointAngles = qVector
    # DO IT SOMEHOW
    visualizeArm(jointAngles)
    


# TODO IMPLEMENT
def manual():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print(joystickDirection)
    # get the current joint angles of the arm
    jointAngles = getJointAngles()
    #print(jointAngles)
    
    # depending on the direction vector
    return None


# TODO IMPLEMENT
def positionalIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    #print(joystickDirection)
    # get the current joint angles of the arm
    jointAngles = getJointAngles()
    #print(jointAngles)
    
    return None
    

# TODO IMPLEMENT
def fullIK():
    # get the direction value to move in
    joystickDirection = getJoystickDirection()
    print("Current joystick direction:")
    print(joystickDirection)
    # get the current joint angles of the arm
    #jointAngles = getJointAngles() # TODO TEMPORARY REPLACED
    global savedJointAngles
    jointAngles = copy.deepcopy(savedJointAngles) # TODO TEMPORARY REPLACEMENT?
    print("Current joint angles: ")
    print(jointAngles)
    
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
    print("Current position: ")
    print([ homTransMatrix[0][3], homTransMatrix[1][3], homTransMatrix[2][3] ])
    visualizeArm(jointAngles)

    # update homogenous transformation matrix based on joystick input
    translationVector = joystickDirection[:3]
    rotationVector = joystickDirection[3:]
    
    copyHomTransMatrix = copy.deepcopy(homTransMatrix)
    DHTableCopy2 = copy.deepcopy(DHTable)
    updatedHomTransMatrix = updateHomTransMatrix(copyHomTransMatrix, DHTableCopy2, translationVector, rotationVector)
    print("Updated position: ")
    print([ updatedHomTransMatrix[0][3], updatedHomTransMatrix[1][3], updatedHomTransMatrix[2][3] ])

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
        jointAngles = [uq1,uq2,uq3,uq4,uq5,uq6]
        savedJointAngles = copy.deepcopy(jointAngles)
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        visualizeArm(jointAngles)
    except:
        print("Exception encountered")
        jointAngles = [q1,q2,q3,q4,q5,q6]
        savedJointAngles = copy.deepcopy(jointAngles)
        # MOVE THE ARM TO THE NEW PLACE!!!!!!!!!!
        visualizeArm(jointAngles)
        


def main():
    # TODO GET THE MODE OF OPERATION
    # modes: '1'-manual, '2'-positional IK (first 3 joints), '3'-full IK
    modeOfOperation = 3#GET THE MODE OF OPERATION FROM SOMEWHERE
    if modeOfOperation == 1:
        manual()
    elif modeOfOperation == 2:
        positionalIK()
    elif modeOfOperation == 3:
        fullIK()
        #time.sleep(1)

    

if __name__ == "__main__":
    # global variables are:
    # joystick
    # savedJointAngles
    # initAngles
    # robot

    # note for the future, for correct visualization q4 there should be
    # given with the opposite side
    global savedJointAngles
    savedJointAngles = [0,0,0,0,0,0]
    setupVisualEnv()
    initializeJoystick()
    
    #time.sleep(1)
    
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
    print("Shutting the operations down")
    
