class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        if self.x >= 0:
            self.x = " "+str(self.x)
        if self.y >= 0:
            self.y = " "+str(self.y)
        return "("+str(self.x)+","+str(self.y)+")"
class OutputObject:
    def __init__(self):
        self.central = '!'
        self.y_pos = '!'
        self.x_pos = '!'
        self.y_leaning = '!'
        self.x_leaning = '!'
    def __repr__(self):
        return self.central + self.y_pos + self.x_pos + self.y_leaning + self.x_leaning

def get_area(house_position,resource_center, output):
    #if central
    if(resource_center.y == house_position.y or resource_center.y == house_position.y-1):
        if resource_center.x > house_position.x:
            output.central = 'C'
            return Point(+3,0)
            return Point(house_position.x+3,house_position.y)
        else:
            output.central = 'C'
            return Point(-3,0)
            return Point(house_position.x-3,house_position.y)
    if(resource_center.x == house_position.x or resource_center.x == house_position.x+1):
        if resource_center.y > house_position.y:
            output.central = 'C'
            return Point(0,+3)
            return Point(house_position.x,house_position.y+3)
        else:
            output.central = 'C'
            return Point(0,-3)
            return Point(house_position.x,house_position.y-3)
    point = Point(0,0)
    #if diagnal
    if(resource_center.y < house_position.y):
        if(resource_center.x < house_position.x):
            if(resource_center.x-house_position.x <= resource_center.y-house_position.y):
                return Point(-3,-1)
            else:
                return Point(-1,-3)
        else:
            if(house_position.x-resource_center.x <= resource_center.y-house_position.y):
                return Point(3,-1)
            else:
                return Point(-3,1)
    else:
        if(resource_center.x < house_position.x):
            if(house_position.x-resource_center.x <= resource_center.y-house_position.y):
                return Point(-1,3)
            else:
                return Point(-3,1)
        else:
            if(resource_center.x-house_position.x <= resource_center.y-house_position.y):
                return Point(1,3)
            else:
                return Point(3,1)
  

house_position = Point(4,4)

for x in range(10):
    p_string = ''
    for y in range(10):
        ouput = OutputObject()
        p_string += str(get_area(house_position,Point(y,x),ouput)) #x y backwards this once to simulat aoe2
        #p_string += str(ouput) + "  "
    print(p_string)

