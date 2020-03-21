import cv2
import numpy as np
from sys import exit

class Maze:
    def __init__(self):

        self.maze_h = 200
        self.maze_w = 300
        self.BlankImage = 255 * np.ones(shape=[self.maze_h, self.maze_w, 3], dtype=np.uint8)
        self.BlackColor = (0, 0, 0)
        self.RedColor = (255,0,0)
       

    def in_maze(self, point):
        
        # Checks whether a point is in bounds and not an obstacle
        # Return False => obstacle and True => if in the map and not an obstacle
        x = point[0]
        y = point[1]
        if 0 <= x < self.maze_w and 0 <= y < self.maze_h:
            if ((x >= self.center[0] - self.rc) and (x <= self.center[0] + self.rc) and
                    (y >= self.maze_h - self.center[1] - self.rc) and (y <= self.maze_h - self.center[1] + self.rc)):
                if ((x - 225) ** 2 + (y - 50) ** 2) <= self.rc ** 2:
                    print("Circular obstacle")
                    return False
            elif (x >= 108) and (x <= 192) and (y >= 78) and (y <= 122):
                if (((y - 100) ** 2 / self.ElMinorC ** 2) + ((x - 150) ** 2 / self.ElMajorC ** 2)) <= 1:
                    print("Elliptical obstacle")
                    return False
            elif ((x >= (200 - self.rob_clr)) and (x <= (250 + self.rob_clr)) and
                  (y >= (160 - self.rob_clr)) and (y <= (190 + self.rob_clr))):
                if ((y - 0.6 * x - (25 - self.rob_clr) >= 0) and (y + 0.6 * x - (325 + self.rob_clr) <= 0) and
                        (y - 0.6 * x - (55 + self.rob_clr) <= 0) and (y + 0.6 * x - (295 - self.rob_clr) >= 0)):
                    print("Diamond shaped obstacle")
                    return False
            elif ((x >= (30 - self.rob_clr)) and (x <= (100 + self.rob_clr)) and
                  (y >= (123 - self.rob_clr)) and (y <= (170 + self.rob_clr))):
                if ((y - 0.577 * x - (115.15 + self.rob_clr) <= 0) and (y + 1.73 * x - (184.55 - self.rob_clr) >= 0) and
                        (y - 0.577 * x - (103.60 - self.rob_clr) >= 0) and (y + 1.73 * x - (334.35 + self.rob_clr) <= 0)):
                    print("Rectangular obstacle")
                    return False
            elif (x >= (20 - self.rob_clr)) and (x <= (100 + self.rob_clr)) and (y >= (15 - self.rob_clr)) and (y <= (80 + self.rob_clr)):
                if (((y + (13) * x - (340 - self.rob_clr) >= 0) and (y - (1.4) * x + (20 + self.rob_clr) >= 0) and
                     (y + x - (100 + self.rob_clr) <= 0)) or ((y - (1.4) * x + (20 - self.rob_clr) <= 0) and
                    (y - (15 - self.rob_clr) >= 0) and (y - (1.4) * x + (90 + self.rob_clr) >= 0) and
                    (y + (1.2) * x - (170 + self.rob_clr) <= 0) and (y - (1.2) * x + (10 - self.rob_clr) <= 0))):
                    print("Polygonal obstacle")
                    return False
        return True

    def draw_circle(self,clr):
        self.r = 25  # Radius of circular obstacle
        self.rc = self.r + clr
        self.center = (225, 150)
        for a in range(self.maze_h - self.center[1] - self.rc, self.maze_h - self.center[1] + self.rc + 1):
            for b in range(self.center[0] - self.rc, self.center[0] + self.rc + 1):
                i = (a - 50)
                j = (b - 225)
                if (i ** 2 + j ** 2) <= self.rc ** 2:
                    self.BlankImage[a,b] = self.RedColor
                if (i ** 2 + j ** 2) <= self.r ** 2:
                    self.BlankImage[a, b] = self.BlackColor

    def draw_polygon(self,clr):
        # Draws a polygon on the maze image
        for i in range(15 - clr, 81 + clr):
            for j in range(20 - clr, 101 + clr):
                if ((i + (13) * j - (340 - 10*clr) >= 0)  and (i - (1.4) * j + (20 - clr) >= 0)  and (i + j - (100 + clr) <= 0)):
                    self.BlankImage[i, j] = self.RedColor
                if ((i - (1.4) * j + (20 - clr) <= 0) and (i - (15 - clr) >= 0) and (i - (1.4) * j + (90 + clr) >= 0) and
                        (i + (1.2) * j - (170 + clr) <= 0) and (i - (1.2) * j + (10 - clr) <= 0)):
                    self.BlankImage[i,j] = self.RedColor
                if (i + (13) * j - 340 >= 0) and (i - (1.4) * j + 20 >= 0) and (i + j - 100 <= 0):
                    self.BlankImage[i, j] = self.BlackColor
                if ((i - (1.4) * j + 20 <= 0) and (i - 15 >= 0) and (i - (1.4) * j + 90 >= 0) and
                        (i + (1.2) * j - 170 <= 0) and (i - (1.2) * j + 10 <= 0)):
                    self.BlankImage[i, j] = self.BlackColor

    def draw_diamond(self,clr):
        for i in range(160 - clr, 191 + clr):
            for j in range(200 - clr, 251 + clr):
                if ((i - (0.6) * j - (25 - clr) >= 0) and (i + (0.6) * j - (325 + clr) <= 0) and
                        (i - (0.6) * j - (55 + clr) <= 0) and (i + (0.6) * j - (295 - clr) >= 0)):
                    self.BlankImage[i, j] = self.RedColor
                if ((i - (0.6) * j - 25 >= 0) and (i + (0.6) * j - 325 <= 0) and (i - (0.6) * j - 55 <= 0) and
                        (i + (0.6) * j - 295 >= 0)):
                    self.BlankImage[i, j] = self.BlackColor

    def draw_ellipse(self,clr):
        # Draws an ellipse on the maze image
        ElCenter = (150, 100)  # Center coordinates of the ellipse shaped obstacle
        ElMajor = 40  # Major axis length of the ellipse
        self.ElMajorC = ElMajor + clr
        ElMinor = 20  # Minor axis length of the ellipse
        self.ElMinorC = ElMinor + clr
        for a in range(ElCenter[1] - self.ElMinorC, ElCenter[1] + self.ElMinorC + 1):
            for b in range(ElCenter[0] - self.ElMajorC, ElCenter[0] + self.ElMajorC + 1):
                j = a - 100
                i = b - 150
                if ((i ** 2 / self.ElMajorC ** 2) + (j ** 2 / self.ElMinorC ** 2)) <= 1:
                    self.BlankImage[a, b] = self.RedColor
                if ((i ** 2 / ElMajor ** 2) + (j ** 2 / ElMinor ** 2)) <= 1:
                    self.BlankImage[a, b] = self.BlackColor

    def draw_rotated_rect(self,clr):
        for i in range(123 - clr, 171 + clr):
            for j in range(30 - clr, 101 + clr):
                if ((i - (0.577) * j - (115.15 + clr) <= 0) and (i + (1.73) * j - (184.55 - clr) >= 0) and
                        (i - (0.577) * j - (103.60 - clr) >= 0) and (i + (1.73) * j - (334.35 + clr) <= 0)):
                    self.BlankImage[i, j] = self.RedColor
                if ((i - (0.577) * j - 115.15 <= 0) and (i + (1.73) * j - 184.55 >= 0) and
                        (i - (0.577) * j - 103.60 >= 0) and (i + (1.73) * j - 334.35 <= 0)):
                    self.BlankImage[i, j] = self.BlackColor

    def get_user_nodes(self):
        # Enter the robot radius and clearance
        print("Please enter the clearance you want between the robot and the obstacles and the robot radius")
        self.rob_clr = int(input('Clearance: '))
        self.rob_rad = int(input('Robot Radius: '))
        self.rob_clr = self.rob_clr+self.rob_rad

        self.draw_circle(self.rob_clr)
        self.draw_ellipse(self.rob_clr)
        self.draw_diamond(self.rob_clr)
        self.draw_polygon(self.rob_clr)
        self.draw_rotated_rect(self.rob_clr)
        cv2.imshow('map', self.BlankImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print('Please enter a start point (x,y,theta)')
        start_str_x = input('start x: ')
        start_str_y = input('start y: ')
        start_str_theta = input('start theta:')
        start_point = [(int(start_str_x), 200 - int(start_str_y)), int(start_str_theta)]

        # Check if start point is valid in maze
        if self.in_maze(start_point[0]):
            pass
        else:
            print("The start point is not valid")
            self.get_user_nodes()
            exit()

        print('Please enter a goal point (x,y)')
        goal_str_x = input('start x: ')
        goal_str_y = input('start y: ')
        goal_point = (int(goal_str_x), 200 - int(goal_str_y))

        # Check if goal point is valid in maze
        if self.in_maze(goal_point):
            pass
        else:
            print("The goal point is not valid")
            self.get_user_nodes()
            exit()

        self.start = start_point
        self.goal = goal_point
        

if __name__ == '__main__':
    mymaze = Maze()
    mymaze.get_user_nodes()