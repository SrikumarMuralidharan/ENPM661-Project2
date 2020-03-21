import cv2
import numpy as np
import math
import time
from sys import exit

class Robot:
    def __init__(self,maze):
        self.maze = maze
        self.threshold = 0.5
        self.Visited_node=np.zeros(shape=[int(self.maze.maze_w/self.threshold), int(self.maze.maze_h/self.threshold), 12], dtype=np.uint8)

    def move(self,point,direction,step_size,theta):
        ang = math.radians(theta)
        ang_p = math.radians(point[1])    
        x = point[0][0]
        y = point[0][1]
        
        if direction == 'Z':    
            x_1 = round(2*(x+(step_size*math.cos(ang_p))))/2
            y_1 = round(2*(y+(step_size*math.sin(ang_p))))/2
            new_point = [(x_1,y_1), point[1]]
            
        elif direction == 'T':
            x_1 = round(2*(x+(step_size*math.cos(ang+ang_p))))/2
            y_1 = round(2*(y+(step_size*math.sin(ang+ang_p))))/2
            if (point[1]+theta < 0):
                new_point = [(x_1,y_1), theta+point[1]+360]
            elif (point[1]+theta >= 360):
                new_point = [(x_1,y_1), theta+point[1]-360]
            else:
                new_point = [(x_1,y_1), theta+point[1]]
    
        elif direction == 'S':
            x_1 = round(2*(x+(step_size*math.cos((2*ang)+ang_p))))/2
            y_1 = round(2*(y+(step_size*math.sin((2*ang)+ang_p))))/2
            if (point[1]+(2*theta) < 0):
                new_point = [(x_1,y_1), (2*theta)+point[1]+360]
            elif (point[1]+(2*theta) >= 360):
                new_point = [(x_1,y_1), (2*theta)+point[1]-360]
            else:
                new_point = [(x_1,y_1), (2*theta)+point[1]]
    
        elif direction == 'MT':
            x_1 = round(2*(x+(step_size*math.cos(ang_p-ang))))/2
            y_1 = round(2*(y+(step_size*math.sin(ang_p-ang))))/2
            if (point[1] < theta):
                new_point = [(x_1,y_1), point[1]+360-theta]
            else:
                new_point = [(x_1,y_1), point[1]-theta]
            
        elif direction == 'MS':
            x_1 = round(2*(x+(step_size*math.cos(ang_p-(2*ang)))))/2
            y_1 = round(2*(y+(step_size*math.sin(ang_p-(2*ang)))))/2
            if (point[1] < (2*theta)):
                new_point = [(x_1,y_1), point[1]+360-(2*theta)]
            else:
                new_point = [(x_1,y_1), point[1]-(2*theta)]
            
        return new_point


    def check_neighbors(self,cur_node):
        directions = ['Z','T','S','MT','MS']
        neighbors = []
        for direction in directions:
            new_point = self.move(cur_node,direction,1,30)
            if self.maze.in_maze(new_point[0]):
                cost = abs(new_point[0][0]-cur_node[0][0]) + abs(new_point[0][1]-cur_node[0][1])              
                neighbors.append((new_point,cost))
                
        return neighbors
    
    def Cost2Go_calc(self, point, goal):
        dist = abs(point[0]-goal[0]) + abs(point[1]-goal[1])
        return dist
        
    def Reached_Goal_Area(self, point, goal):
        threshold_rad = 1.5
        if ((point[0]-goal[0]) ** 2 + (point[1]-goal[1])**2 <= threshold_rad**2):
            return True
        return False
        
    def A_Star(self):
              
        start_point = self.maze.start
        goal_point = self.maze.goal
        #BlankImage = self.maze.BlankImage
        
        self.nodes = []
        #Doubling threshold values in order to compensate for floating values and converting 
        #them to int by mult by 2. Clearly, float numbers are rounded to 0.5 types as that is the threshold
        self.cost2come = np.full((600,400,12),np.inf)
        self.cost2go = np.full((600,400,12),np.inf)
        self.parents = np.full((600,400,12),np.nan,dtype=np.int32)

        self.nodes.append(start_point) #add the start node to nodes
        
        #set start node to have parent of -1 and cost of 0, calculate cos2go for startnode
        self.cost2come[2*start_point[0][0]][2*start_point[0][0]][int(start_point[1]/30)] = 0
        self.cost2go[2*start_point[0][0]][2*start_point[0][0]][int(start_point[1]/30)] = self.Cost2Go_calc(start_point[0], goal_point)
        self.parents[2*start_point[0][1],2*start_point[0][0]] = -1
        
        #setting starting node to be a visited node
        self.Visited_node[2*start_point[0][0]][2*start_point[0][1]][int(start_point[1]/30)]=1
        
        #setting c2c and c2g values to be the same as start point values
        c2c = 0
        c2g = self.cost2go[2*start_point[0][0]][2*start_point[0][1]][int(start_point[1]/30)]

        queue = [(0, c2c+c2g)]        #queue designed as a list of tuples
        isgoal = False
        
        def queue_sec_element(a):
            return a[1]
        while queue:
            
            #sort queue according to c2c+c2g value
            queue.sort(key = queue_sec_element)
            
            # Set the current node as the top of the queue and remove it
            parent,cost  = queue.pop(0)
            
            # Setting current node to be the node at parent location
            cur_node = self.nodes[parent]
            
            #Updating c2c value at this location
            c2c = self.cost2come[int(2*cur_node[0][0])][int(2*cur_node[0][1])][int(cur_node[1]/30)]
            #formulating neighbours around this location
            neighbors = self.check_neighbors(cur_node)

            for n in neighbors:
                print('neighbor')
                print(n)
                p = n[0]    #new_point
                c = n[1]    #cost
                c2g=self.Cost2Go_calc(p[0],goal_point)
                
            
                #condition to check for unvisited node
                if self.Visited_node[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]==0:
                    self.nodes.append(p)
                    self.Visited_node[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]=1
                    self.cost2come[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]= c2c+c
                    self.parents[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]=parent
                    i=int(round(p[0][0]))
                    j=int(round(p[0][1]))
                    self.maze.Blankimage[i,j] = (0,255,255)
                    queue.append((len(self.nodes)-1, c2g))
                
                #condition to check for visited node and updating cost based on realtime values
                elif c2c + c < self.cost2come[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]:
                    self.cost2come[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]= c2c+c
                    self.parents[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]=parent
                   
                if self.Reached_Goal_Area(p[0], goal_point):
                    isgoal = True
                    queue.clear()
                    break

        self.foundGoal = isgoal
        

    def generate_path(self):
        #Assume the last item in nodes is the goal node
        goal = self.nodes[-1]
        parent = self.parents[int(2*goal[0][0])][int(2*goal[0][1])][int(goal[1]/30)]
        path_nodes = [parent]
        
        while parent>0:
            parent_node = self.nodes[path_nodes[-1]]
            parent = int(self.parents[int(2*parent_node[0][0])][int(2*parent_node[0][1])][int(parent_node[1]/30)])
            path_nodes.append(parent)
        self.path = [goal]
        for ind in path_nodes:
            if ind == -1:
                break
            else:
                self.path.insert(0,self.nodes[ind])


class RigidRobot(Robot):
    def __init__(self,maze):
        super().__init__(maze)


    def visualize(self,show,output,stepsize):
        node_color = (102, 255, 255)
        if output:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            frame_size = (self.maze.BlankImage.shape[1], self.maze.BlankImage.shape[0])
            today = time.strftime("%m-%d__%H.%M.%S")
            videoname=str(today)
            fps_out = 60
            out = cv2.VideoWriter(str(videoname)+".mp4", fourcc, fps_out, frame_size)
            print("Writing to Video, Please Wait")

        cur_frame = 1
        tot_frames = (len(self.nodes)//stepsize)+1
  
        for i,point in enumerate(self.nodes):
            self.maze.BlankImage[int(round(point[0][1])),int(round(point[0][0]))] = node_color
            
            if i%stepsize == 0:
                if output:
                    print('Frame number:' + str(cur_frame) + ' of ' + str(tot_frames))
                    out.write(self.maze.BlankImage)
                    time.sleep(0.005)
                    cur_frame += 1
                if show:
                    cv2.imshow('Maze Visualization',self.maze.BlankImage)
                    
                if cv2.waitKey(1) == ord('q'):
                    exit()

        for point in self.path:
            sx = int(round(point[0][0]))
            #sy = self.maze.height-point[1]
            sy = int(round(point[0][1]))
            cv2.circle(self.maze.BlankImage,(sx,sy),self.maze.rob_rad,(0,0,255),-1)
            if output:
                out.write(self.maze.BlankImage)
                time.sleep(0.005)
            if show:
                cv2.imshow('Maze Visualization',self.maze.BlankImage)
            if cv2.waitKey(1) == ord('q'):
                exit()
            #if point == self.maze.goal:
            if self.Reached_Goal_Area(point[0], self.maze.goal):
                #cv2.imwrite('searched_nodes.png',self.maze.image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        if output:
            out.release()