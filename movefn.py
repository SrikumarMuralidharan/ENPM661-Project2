import math

def move(point,direction,step_size,theta):
    
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

print(move([(0,0),0],'Z',1,30))
print(move([(0,0),0],'T',1,30))
print(move([(0,0),0],'S',1,30))
print(move([(0,0),0],'MT',1,30))
print(move([(0,0),0],'MS',1,30))