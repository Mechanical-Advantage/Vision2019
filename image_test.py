import cv2
import numpy
import math

pointsFile = "points.csv"

amodel_points = [
    # Left target
    (-5.938, 2.938, 0.0), # top left
    (-4.063, 2.375, 0.0), # top right
    (-7.375, -2.500, 0.0), # bottom left
    (-5.438, -2.938, 0.0), # bottom right


    # Right target
    (3.938, 2.375, 0.0), # top left
    (5.875, 2.875, 0.0), # top right
    (5.375, -2.938, 0.0), # bottom left
    (7.313, -2.500, 0.0), # bottom right
]


model_points = numpy.array(amodel_points)

#Read from csv
inputPoints = open(pointsFile, "r")
inputPoints = inputPoints.read()
inputPoints = inputPoints.split("\n\n") #Splits by set
for i in range(len(inputPoints)):
    inputPoints[i] = inputPoints[i].split("\n") #Splits by coordinate pair
    if len(inputPoints[i]) == 9: #Removes extra coordinate pair (b/c of extra newline)
        inputPoints[i] = inputPoints[i][:-1]
    for f in range(len(inputPoints[i])): #Splits coordinate pair
        inputPoints[i][f] = inputPoints[i][f].split(",")
        for n in range(len(inputPoints[i][f])):
            inputPoints[i][f][n] = float(inputPoints[i][f][n])

#Iterate through sets
for setNumber in range(len(inputPoints)):
    
    aimage_points = inputPoints[setNumber]
    image_points = numpy.array(aimage_points)

    #camera_matrix =numpy.array([[329.49123792544623, 0.0, 168.96618562196542],
    #                            [0.00, 329.49123792544623, 156.180131529639],
    #                            [0.0000, 0.0000, 1.000)]]
    camera_matrix = numpy.array([[512.0486676110471, 0.0, 305.52035364138726], [0.0, 515.3532387199512, 262.41020845383434], [0.0, 0.0, 1.0]])
    #print(camera_matrix)

    dist_coeffs = numpy.array([0.08454318371194253, -0.24818779001569383, 0.002509250787445395, 0.0033838430868377263, 0.12424667264216427])

    #print(model_points)
    #print(image_points)
    image_size = (640,480)
    (ret, rvec, tvec) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
    #print(tvec[2])
    x = tvec[0][0]
    z = tvec[2][0]
    # distance in the horizontal plane between camera and target
    distance = math.sqrt(x**2 + z**2)
    # horizontal angle between camera center line and target
    angle1 = math.atan2(x, z)
    rot, _ = cv2.Rodrigues(rvec)
    rot_inv = rot.transpose()
    pzero_world = numpy.matmul(rot_inv, -tvec)
    angle2 = math.atan2(pzero_world[0][0], pzero_world[2][0])
    #print(pzero_world[0][0], pzero_world[2][0])
    print("Distance: ", distance, "Angle1: ", numpy.degrees(angle1), "Angle 2: ", numpy.degrees(angle2),"\r\nX Offset: ", x, "Z Offset: ", z, "\n")
