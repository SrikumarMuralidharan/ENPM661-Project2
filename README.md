# ENPM661-Project2
Repository for Project-2 A* algorithm implementation

We have 3 .py files - maze.py, robot.py and A_star_rigid.py

maze.py - This file contains the code for the finalmap with all the obstacles and constraints that the robot has to follow along its path.
robot.py - This file contains the code for the rigid robot parameters, the action set that the algorithm follows and also the visualization details.
A_star_rigid.py - This file contains the code to finally generate the simulation and shows the reult. It calls the other two functions as well.

User inputs: 

Clearance: 1
Robot Radius: 1
Please enter a start point (x,y,theta)
start x: 50
start y: 30
start theta: 60
Please enter a goal point (x,y)
start x: 150
start y: 150

Our code starts to explore the various paths and finally shows the final path from the start node to the end node as a single red line.
We also print the nodes explored