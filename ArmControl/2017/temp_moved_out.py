# update matrix values
    # global reference frame values
    tempH06 = copy.deepcopy( H06.tolist() )
    R06 = np.matrix( [tempH06[0][:3], tempH06[1][:3], tempH06[2][:3]] )
    angleXglobal = math.atan2( R06[2,1], R06[2,2] )
    angleYglobal = math.atan2( -R06[2,0], math.sqrt( R06[2,1]**2 + R06[2,2]**2 ) )
    angleZglobal = math.atan2( R06[1,0], R06[0,0] )
    angleXglobal += rotationVector[1]
    angleYglobal += rotationVector[0]
    angleZglobal += rotationVector[2]
    X = np.matrix( [ [1, 0, 0], [0, math.cos(angleXglobal), -math.sin(angleXglobal)], [0, math.sin(angleXglobal), math.cos(angleXglobal)] ] )
    Y = np.matrix( [ [math.cos(angleYglobal), 0, math.sin(angleYglobal)], [0, 1, 0], [-math.sin(angleYglobal), 0, math.cos(angleYglobal)] ] )
    Z = np.matrix( [ [math.cos(angleZglobal), -math.sin(angleZglobal), 0], [math.sin(angleZglobal), math.cos(angleZglobal), 0], [0, 0, 1] ] )
    R06new = Z * Y * X
    # end effector reference frame values
    tempH56 = copy.deepcopy( H56.tolist() )
    R56 = np.matrix( [tempH56[0][:3], tempH56[1][:3], tempH56[2][:3]] )
    # Euler angles determination
    angleXlocal = math.atan2( R56[2,1], R56[2,2] )
    angleYlocal = math.atan2( -R56[2,0], math.sqrt( R56[2,1]**2 + R56[2,2]**2 ) )
    angleZlocal = math.atan2( R56[1,0], R56[0,0] )
    angleXlocal += rotationVector[1]
    angleYlocal += rotationVector[0]
    angleZlocal += rotationVector[2]
    Xlocal = np.matrix( [ [1, 0, 0], [0, math.cos(angleXlocal), -math.sin(angleXlocal)], [0, math.sin(angleXlocal), math.cos(angleXlocal)] ] )
    Ylocal = np.matrix( [ [math.cos(angleYlocal), 0, math.sin(angleYlocal)], [0, 1, 0], [-math.sin(angleYlocal), 0, math.cos(angleYlocal)] ] )
    Zlocal = np.matrix( [ [math.cos(angleZlocal), -math.sin(angleZlocal), 0], [math.sin(angleZlocal), math.cos(angleZlocal), 0], [0, 0, 1] ] )
    R56new = Zlocal * Ylocal * Xlocal

    
    for i in range(3):
        for j in range(3):
            H06[i,j] = R06new[i,j]
    
    H06[0,3] += translationVector[0]
    H06[1,3] += translationVector[1]
    H06[2,3] += translationVector[2]

    #R06 = (R03*R36).tolist()
    #for i in range(3):
    #    for j in range(3):
    #        updatedHomTransMatrix[i][j] = R06[i][j]
