import math
import numpy as np
import cv2

# """
#  Taking input from the user for the start and goal points
# """
# StartPoint = []
# print("Enter the x, y and theta_start values for the start point: ")
# for _ in range(3):
#     StartPoint.append(int(input()))
# GoalPoint = []
# # Considering the orientation of the robot at the goal point is absent
# print("Enter the x and y values for the goal point: ")
# for _ in range(2):
#     GoalPoint.append(int(input()))
#
# """
#  Taking in the robot parameters
# """
# print("Enter the robot parameters: ")
# RobotRadius = int(input())
# RobotClearance = int(input())

"""
 Final Obstacle Map
"""
def obstacles(x, y):
    BlankImage = 255 * np.ones(shape=[200, 300, 3], dtype=np.uint8)
    # Window name in which image is displayed
    map = 'Final Map'

    # Draw a circular obstacle on the map
    r = 25  # Radius of circular obstacle
    BlackColor = (0, 0, 0)  # black color for the obstacle
    WhiteColor = (255,255,255)
    for a in range(200):
        for b in range(300):
            i = a - 50
            j = b - 225
            if ((i ** 2 + j ** 2) <= r ** 2):
                BlankImage[a,b] = BlackColor

    # Draw an ellipse shaped obstacle on the map
    ElCenter = (150, 100)  # Center coordinates of the ellipse shaped obstacle
    ElMajor = 40  # Major axis length of the ellipse
    ElMinor = 20  # Minor axis length of the ellipse
    for a in range(200):
        for b in range(300):
            j = a - 100
            i = b - 150
            if (((i ** 2 / ElMajor ** 2) + (j ** 2 / ElMinor ** 2)) <= 1):
                BlankImage[a,b] = BlackColor

    # Draw the polygon obstacle on the map
    # Vertices of the polygon
    # polygon = np.array([[20, 80], [25, 15], [75, 15], [100, 50], [75, 80], [50, 50]], np.int32)
    for i in range(200):
        for j in range(300):
            if(((i + (13)*j - 140 > 0) and (i - 15 > 0) and (i - (1.4)*j + 90 > 0) and (i + (1.2)*j - 170 <= 0))):
                BlankImage[i,j] = BlackColor
            if ((i - (1.2) * j + 10 > 0) and (i + j - 100 > 0)):
                BlankImage[i,j] = WhiteColor

    # Draw the diamond shaped obstacle on the map
    # Vertices of the diamond
    #Diamond = np.array([[225, 190], [250, 175], [225, 160], [200, 175], [225, 190]], np.int32)
    for a in range(200):
        for b in range(300):
            i = a
            j = 200 - b
            if((i - (0.6)*j - 145 > 0) and (i + (0.6) * j - 155 <= 0) and (i + (0.6) * j - 115 > 0) and
                     (i - (0.6) * j - 185 <= 0)):
                BlankImage[a,b] = BlackColor

    # The rectangular obstacle
    for a in range(200):
        for b in range(300):
            j = a
            i = 200 - b
            if ((i - (1.73) * j + 135 > 0) and (i + (0.58) * j - 96.35 <= 0) and (i - (1.73) * j - 15.54 <= 0) and
                    (i + (0.58) * j - 84.81 >= 0)):
                BlankImage[b, a] = BlackColor

    # Displaying the final map with obstacles
    cv2.imshow(map, BlankImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    return False

# Function call - (10,190) is not an obstacle and (10,10) is an obstacle
# test = obstacles(10, 10)
# print(test)