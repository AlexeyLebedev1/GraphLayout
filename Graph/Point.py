


class Point():
    """2d point"""
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __add__(self,other):
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        return Point(self.x-other.x,self.y-other.y)

    def __mul__(self,num):
        return Point(self.x*num,self.y*num)

    def __truediv__(self,num):
        return Point(self.x/num,self.y/num)

    def norm(self):
        return (self.x**2+self.y**2)**(1/2)
    
    def __abs__(self):
        return self.norm()
    



