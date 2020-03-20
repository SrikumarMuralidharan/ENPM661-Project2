import cv2
import numpy as np

class Maze:
    def __init__(self):
        
        self.maze_h = 200 
        self.maze_w = 300
        self.BlankImage = 255 * np.ones(shape=[self.maze_h, self.maze_w, 3], dtype=np.uint8)
        self.BlackColor = (0, 0, 0)
        
        self.draw_circle()
        self.draw_diamond()
        self.draw_polygon()
        self.draw_ellipse()
        self.draw_rotated_rect()
        cv2.imshow('map', self.BlankImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def in_maze(self,point):
        # Checks whether a point is in bounds and not an obstacle
        x = point[0]
        y = point[1]
        if 0<=x<self.maze_w and 0<=y<self.maze_h:
            return True
        return False

    def draw_circle(self):
        r = 25  # Radius of circular obstacle
        center = (225,150)
        for a in range(self.maze_h-center[1]-r,self.maze_h-center[1]+r+1):
            for b in range(center[0]-r,center[0]+r+1):
                i = a - 50
                j = b - 225
                if ((i ** 2 + j ** 2) <= r ** 2):
                    self.BlankImage[a,b] = self.BlackColor


    def draw_polygon(self):
        # Draws a polygon on the maze image
        for i in range(15, 81):
            for j in range(20, 101):
                if((i + (13)*j - 340 >= 0) and (i - (1.4)*j +20 >= 0) and (i + j - 100 <= 0)):
                    self.BlankImage[i,j] = self.BlackColor
                if((i - (1.4)*j +20 <= 0) and (i - 15 >= 0) and (i - (1.4)*j + 90 >= 0) and (i + (1.2)*j - 170<=0) and (i - (1.2)*j +10 <= 0)):
                    self.BlankImage[i,j] = self.BlackColor
    
    def draw_diamond(self):
        for i in range(160,191):
            for j in range(200,251):
                if((i - (0.6)*j - 25 >= 0) and (i + (0.6) * j - 325 <= 0) and (i - (0.6) * j - 55 <= 0) and (i + (0.6) * j - 295 >= 0)):
                    self.BlankImage[i,j] = self.BlackColor
        
    def draw_ellipse(self):
        # Draws an ellipse on the maze image
        ElCenter = (150, 100)  # Center coordinates of the ellipse shaped obstacle
        ElMajor = 40  # Major axis length of the ellipse
        ElMinor = 20  # Minor axis length of the ellipse
        for a in range(ElCenter[1]-ElMinor,ElCenter[1]+ElMinor+1):
            for b in range(ElCenter[0]-ElMajor,ElCenter[0]+ElMajor+1):
                j = a - 100
                i = b - 150
                if (((i ** 2 / ElMajor ** 2) + (j ** 2 / ElMinor ** 2)) <= 1):
                    self.BlankImage[a,b] = self.BlackColor


    def draw_rotated_rect(self):
        for i in range(123,171):
            for j in range(30, 101):
                if ((i - (0.577)*j - 115.15 <= 0) and (i + (1.73) * j - 184.55 >= 0) and (i - (0.577)*j - 103.60 >= 0) and (i + (1.73) * j - 334.35 <= 0)):
                    self.BlankImage[i,j] = self.BlackColor
                
                
    def get_user_nodes(self):
        print('Please enter a start point (x,y,theta)')
        start_str_x = input('start x: ')
        start_str_y = input('start y: ')
        start_str_theta = input('start theta:')
        start_point = [(int(start_str_x),200-int(start_str_y)), int(start_str_theta)]

        # Check if start point is valid in maze 
        if self.in_maze(start_point[0]):
            pass
        else:
            print("The start point is not valid")
            quit()
            
        print('Please enter a goal point (x,y)')
        goal_str_x = input('start x: ')
        goal_str_y = input('start y: ')
        goal_point = (int(goal_str_x),200-int(goal_str_y))

        # Check if goal point is valid in maze 
        if self.in_maze(goal_point):
            pass
        else:
            print("The goal point is not valid")
            quit()
            
        self.start = start_point
        self.goal = goal_point
        #print(self.start)
        #print(self.goal)

if __name__ == '__main__':
    mymaze = Maze()
    #mymaze.get_user_nodes()
    