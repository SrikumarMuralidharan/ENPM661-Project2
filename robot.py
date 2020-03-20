import cv2
import numpy as np
import math
import time
from collections import deque

class Robot:
    def __init__(self,maze):
        self.maze = maze

    def move(self,point,direction,step_size,theta):
        self.threshold = 0.5
        self.Visited_node=np.zeros(shape=[int(self.maze.maze_w/self.threshold), int(self.maze.maze_h/self.threshold), 12], dtype=np.uint8)
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
        BlankImage = self.maze.BlankImage
        print('shape0')
        print(BlankImage.shape[0])
        print('shape1')
        print(BlankImage.shape[1])
        nodes = []

        # Checked points are additionally stored in a set which is much faster for 
        # checking if the node has already been visited
        costs = np.full((400,600),np.inf)
        parents = np.full((400,600),np.nan,dtype=np.int32)

         #set start node to have parent of -1 and cost of 0
        nodes.append(start_point) #add the start node to nodes
        costs[2*start_point[0][1],2*start_point[0][0]] = 0
        parents[2*start_point[0][1],2*start_point[0][0]] = -1

        # The queue is strucuted as a deque which allows for much faster operation
        # when accessing the first item in the list
        queue = deque()
        queue.append(0) #set the start_node as the first node in the queue

        isgoal = False
        cost2come = 0
        i=0

        while queue:
            i+=1
            break
            print('iteration:'+str(i))
            # Set the current node as the top of the queue and remove it
            parent = queue.popleft()
            cur_node = nodes[parent]
            print('cur_node')
            print(cur_node)
            cost2come = costs[int(2*cur_node[0][1]),int(2*cur_node[0][0])]
            neighbors = self.check_neighbors(cur_node)

            for n in neighbors:
                p = n[0]    #new_point
                c = n[1]    #cost
                if self.Visited_node[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]!=1:
                    print('neigbor')
                    print(p)
                    nodes.append(p)
                    self.Visited_node[int(2*(p[0][0]))][int(2*(p[0][1]))][int(p[1]/30)]=1
                    queue.append(len(nodes)-1)
                if cost2come + c + self.Cost2Go_calc(p[0],goal_point) < costs[int(2*p[0][1]),int(2*p[0][0])]:
                    costs[int(2*p[0][1]),int(2*p[0][0])] = cost2come + c + self.Cost2Go_calc(p[0],goal_point)
                    parents[int(2*p[0][1]),int(2*p[0][0])] = parent
                if self.Reached_Goal_Area(p[0], goal_point):
                    isgoal = True
                    queue.clear()
                    break

        self.nodes = nodes
        self.parents = parents
        self.costs = costs
        self.foundGoal = isgoal


    def generate_path(self):
        nodes = self.nodes
        parents = self.parents
        #Assume the last item in nodes is the goal node
        goal = nodes[-1]
        parent = parents[int(2*goal[0][1]),int(2*goal[0][0])]
        path_nodes = [parent]
        while parent != -1:
            parent_node = nodes[path_nodes[-1]]
            parent = parents[int(2*parent_node[0][1]),int(2*parent_node[0][0])]
            path_nodes.append(parent)
        self.path = [goal]
        for ind in path_nodes:
            if ind == -1:
                break
            else:
                self.path.insert(0,nodes[ind])


class RigidRobot(Robot):
    def __init__(self,maze):
        super().__init__(maze)
        self.get_params()

    def get_params(self):
        print('Please enter the size of your robot')
        size_str = input('radius: ')
        if size_str.isdigit():
            self.radius = int(size_str)
        else:
            print('Please enter a number')
            quit()
        
        print('Please enter the clearance for your robot')
        clear_str = input('clearance: ')
        if clear_str.isdigit():
            self.clearance = int(clear_str)
        else:
            print('Please enter a number')
            quit()


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
            cv2.circle(self.maze.BlankImage,(sx,sy),self.radius,(0,0,255),-1)
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