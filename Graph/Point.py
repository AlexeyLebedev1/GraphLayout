


class Point():
    """Точка на плоскости"""
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self,other):
        """Операция сложения"""
        return Point(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        """Операция вычитания"""
        return Point(self.x-other.x,self.y-other.y)
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y

    def length(self):
        """Длина радус вектора"""
        return (self.x**2+self.y**2)**(1/2)

    def __mul__(self,num):
        """Умножение на константу"""
        return Point(self.x*num,self.y*num)

    def __truediv__(self,num):
        """Деление на константу"""
        return Point(self.x/num,self.y/num)
    
    def __abs__(self):
        return self.length()
    



