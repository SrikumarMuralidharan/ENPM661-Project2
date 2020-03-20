from maze import Maze
from robot import RigidRobot

write_to_video = False
show_visualization = True
stepsize = 100 #controls the number of nodes shown in each frame of visualization

mymaze = Maze()

# Ask user for start point and goal point
mymaze.get_user_nodes()

# Construct the robot
robot = RigidRobot(mymaze)

robot.A_Star()

if robot.foundGoal:
    robot.generate_path()
else:
    print('The goal could not be found')
    exit()

# Visualize the path
robot.visualize(show_visualization,write_to_video,stepsize)
