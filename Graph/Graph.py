from Point import Point
import random
import math


class Vertex():
    """Вершина графа"""
    def __init__(self,name):
        self.name=name
        self.pos=Point(0,0)
        self.id=None              #идентификаторы для отрисовки
        self.name_id=None         

    def __eq__(self,other):
        return self.name==other.name

    def __ne__(self,other):
        return self.name!=other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class Edge():
    """Неориентированное ребро графа"""
    def __init__(self,v,u):
        self.v=v
        self.u=u
        self.id=None

    def __eq__(self,other):
        return [self.v,self.u]==[other.v,other.u] or [self.v,self.u]==[other.u,other.v] 
    

class Graph():
    """Неориентированный граф без кратных рёбер и петель"""

    def __init__(self,vertexes=None):
        """vertexes - словарь, ключи-вершины, значения - списки смежных вершин"""
        if(vertexes==None):
            vertexes={}
        self.vertexes=vertexes

    def __eq__(self,other):
        return self.vertexes==other.vertexes

    def get_vertexes(self):
        """Список вершин"""
        return list(self.vertexes.keys())

    def get_edges(self):
        """Список рёбер"""
        edges=[]
        for vertex in self.vertexes:
            for neighbour in self.vertexes[vertex]:
                if Edge(neighbour,vertex) not in edges:
                    edges.append(Edge(vertex,neighbour))

        return edges

    def get_incident_edges(self,v):
        """Возвращает список рёбер,инцедентных вершине v"""
        edges=[]
        pos=list(self.vertexes.keys()).index(v)
        for i,u in enumerate(self.vertexes[v]):
            if i<pos:
                edges.append(Edge(u,v))
            else:
                edges.append(Edge(v,u))

        return edges
        
            
    def add_vertex(self,v):
        """Добавление вершины"""
        if v not in self.vertexes.keys():
            self.vertexes[v]=[]

    def add_edge(self,edge):
        """Добавление ребра.В случае если какая либо из вершин не входит в граф, она будет добавлена в граф"""
        if len(edge)==2 and edge[0]!=edge[1]:
            self.add_vertex(edge[0])
            self.add_vertex(edge[1])
            if edge[1] not in self.vertexes[edge[0]]:
                self.vertexes[edge[0]].append(edge[1])
            if edge[0] not in self.vertexes[edge[1]]:
                self.vertexes[edge[1]].append(edge[0])



 
    def floyd(self,length=100):                                             #length - длинна рёбер 
        """Нахождение матрицы расстояний с помощью алгоритма флойда"""

        D=[]
        for i,v in enumerate(self.vertexes):
            row=[]
            for j,u in enumerate(self.vertexes):
                if i==j:
                    row.append(0)
                elif u in self.vertexes[v]:
                    row.append(length)
                else:
                    row.append(math.inf)

            D.append(row)

        n=len(self.vertexes.keys())
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if D[i][k]<math.inf and D[k][j]<math.inf:
                        D[i][j]=min(D[i][j],D[i][k]+D[k][j])

        return D


    def get_str(self):
        """Возвращает граф как словарь со строковыми ключами и строковыми списками значений"""
        g={}
        for v in self.vertexes:
            adjacent=[]
            for u in self.vertexes[v]:
                adjacent.append(str(u.name))
            g[str(v.name)]=adjacent

        return g
            

    def __mul__(self,other):
        """Прямое произведение двух графов"""
        self_str=self.get_str()
        other_str=other.get_str()

        g={}

        for v in self.vertexes:
            for u in other.vertexes:
                vertex_name='('+str(v.name)+','+str(u.name)+')'
                g[Vertex(vertex_name)]=[]



        def vertex_patrition(two_vertex_str):
            """Разбиение веришины графа состоящего из произведение двух графов на две вершины из соответствующих графов"""
            stack=[]
            v1,v2='',''
            for i,s in enumerate(two_vertex_str):
                if s=='(':
                    stack.append(s)

                if s==')':
                    stack.pop()

                if s==',' and len(stack)==0:
                    v2=two_vertex_str[i+1:]
                    break

                v1+=s
          
            return v1,v2

        for v in g:
            for u in g:
                if v!=u:
                    x1,y1=vertex_patrition(v.name[1:-1])        
                    x2,y2=vertex_patrition(u.name[1:-1])

                    if x1==x2 and y1 in other_str[y2] or y1==y2 and x1 in self_str[x2]:
                        g[v].append(u)

        return Graph(g)




class GenerateGraph():
    """Генерация некоторых специальных графов соответсвующей размерности"""

    def Kn(self,n):
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        for i in range(n):
            neighbors=[]
            for j in range(n):
                if i!=j:
                    neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors

        return Graph(g)

    def Kpq(self,p,q):
        g={}
        vertexes=[Vertex(i) for i in range(p+q)]
        for i in range(p):
            neighbors=[]
            for j in range(p,p+q):
                neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors

        for i in range(p,p+q):
            neighbors=[]
            for j in range(p):
                neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors 

        return Graph(g)

    def Cn(self,n):
        if n<3:
            return Graph()
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        g[vertexes[0]]=[vertexes[1],vertexes[n-1]]
        for i in range(1,n-1):
            g[vertexes[i]]=[vertexes[i-1],vertexes[i+1]]

        g[vertexes[n-1]]=[vertexes[0],vertexes[n-2]]

        return Graph(g)

    def On(self,n):
        g={}
        for i in range(n):
            g[Vertex(i)]=[]

        return Graph(g)

    def Pn(self,n):
        if n==0:
            return Graph()
        if n==1:
            return self.On(1)
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        g[vertexes[0]]=[vertexes[1]]
        for i in range(1,n-1):
            g[vertexes[i]]=[vertexes[i-1],vertexes[i+1]]
        g[vertexes[n-1]]=[vertexes[n-2]]
        return Graph(g)

    def Qn(self,n,vertex_marking=False):
        if n<1:
            return Graph()
        g=self.Pn(2)
        for i in range(n-1):
            g*=self.Pn(2)
        
        if vertex_marking:
        #изменяем имена вершин в бинарные числа 
            g_str=g.get_str()
            old_names=g_str.keys()
            new_names=[]
            for name in old_names:
                new_name=''
                for ch in name:
                    if ch=='0'or ch=='1':
                        new_name+=ch

                new_names.append(new_name)

            binary_g={}
            vertexes=[Vertex(new_name) for new_name in new_names]
            for v in vertexes:
                binary_g[v]=[]
            for v,old_name in zip(vertexes,old_names):
                for u,name in zip(vertexes,old_names):
                    if name in g_str[old_name]:
                        binary_g[v].append(u)

            return Graph(binary_g)

        return g





