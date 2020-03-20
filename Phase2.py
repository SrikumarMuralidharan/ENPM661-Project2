import math
import numpy as np
import cv2

"""
 Final Obstacle Map
"""
def obstacles(point):
    x = point[0]
    y = point[1]
    maze_h = 200 
    maze_w = 300
    BlankImage = 255 * np.ones(shape=[maze_h, maze_w, 3], dtype=np.uint8)
    # Window name in which image is displayed
    map = 'Final Map'
    BlackColor = (0, 0, 0)  # black color for the obstacle
    
    # Draw a circular obstacle on the map
    r = 25  # Radius of circular obstacle
    center = (225,150)
    for a in range(maze_h-center[1]-r,maze_h-center[1]+r+1):
        for b in range(center[0]-r,center[0]+r+1):
            i = a - 50
            j = b - 225
            if ((i ** 2 + j ** 2) <= r ** 2):
                BlankImage[a,b] = BlackColor

    # Draw an ellipse shaped obstacle on the map
    ElCenter = (150, 100)  # Center coordinates of the ellipse shaped obstacle
    ElMajor = 40  # Major axis length of the ellipse
    ElMinor = 20  # Minor axis length of the ellipse
    for a in range(ElCenter[1]-ElMinor,ElCenter[1]+ElMinor+1):
        for b in range(ElCenter[0]-ElMajor,ElCenter[0]+ElMajor+1):
            j = a - 100
            i = b - 150
            if (((i ** 2 / ElMajor ** 2) + (j ** 2 / ElMinor ** 2)) <= 1):
                BlankImage[a,b] = BlackColor

    # Draw the polygon obstacle on the map
    # Vertices of the polygon
    # polygon = np.array([[20, 80], [25, 15], [75, 15], [100, 50], [75, 80], [50, 50]], np.int32)
    for i in range(15, 81):
        for j in range(20, 101):
            if((i + (13)*j - 340 >= 0) and (i - (1.4)*j +20 >= 0) and (i + j - 100 <= 0)):
                BlankImage[i,j] = BlackColor
            if((i - (1.4)*j +20 <= 0) and (i - 15 >= 0) and (i - (1.4)*j + 90 >= 0) and (i + (1.2)*j - 170<=0) and (i - (1.2)*j +10 <= 0)):
                BlankImage[i,j] = BlackColor
            
    # Draw the diamond shaped obstacle on the map
    # Vertices of the diamond
    for i in range(160,191):
        for j in range(200,251):
            if((i - (0.6)*j - 25 >= 0) and (i + (0.6) * j - 325 <= 0) and (i - (0.6) * j - 55 <= 0) and
                     (i + (0.6) * j - 295 >= 0)):
                BlankImage[i,j] = BlackColor

    # The rectangular obstacle
    for i in range(123,171):
        for j in range(30, 101):
            if ((i - (0.577)*j - 115.15 <= 0) and (i + (1.73) * j - 184.55 >= 0) and (i - (0.577)*j - 103.60 >= 0) and (i + (1.73) * j - 334.35 <= 0)):
                BlankImage[i,j] = BlackColor

    # Displaying the final map with obstacles
    cv2.imshow(map, BlankImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


## changes done till here!


    # Checking if the robot is hitting an obstacle
    if (((x ** 2 + y ** 2) > r ** 2) and (((x ** 2 / ElMajor ** 2) + (y ** 2 / ElMinor ** 2)) > 1)):
        return True
    elif ((i - (0.6)*j - 145 > 0) and (i + (0.6) * j - 155 <= 0) and (i + (0.6) * j - 115 > 0) and
                     (i - (0.6) * j - 185 <= 0)):
        return False
    elif (((i + (13)*j - 140 > 0) and (i - 15 > 0) and (i - (1.4)*j + 90 > 0) and (i + (1.2)*j - 170 <= 0))):
        return False
    elif ((i - (1.2) * j + 10 > 0) and (i + j - 100 > 0)):
        return True
    elif ((y - (1.73) * x + 135 > 0) and (y + (0.58) * x - 96.35 <= 0) and (y - (1.73) * x - 15.54 <= 0) and (y +
          (0.58) * x - 84.81 >= 0)):
        return False
    return True

# Function call - (10,190) is not an obstacle and (10,10) is an obstacle
test = obstacles((10, 190))
print(test)