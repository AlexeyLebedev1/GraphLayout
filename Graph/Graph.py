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
                if [neighbour,vertex] not in edges:
                    edges.append([vertex,neighbour])

        return edges

    def get_incident_edges(self,v):
        """Возвращает список рёбер,инцедентных вершине v"""
        edges=[]
        pos=list(self.vertexes.keys()).index(v)
        for i,u in enumerate(self.vertexes[v]):
            if i<pos:
                edges.append([u,v])
            else:
                edges.append([v,u])

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


    def floyd(self,length=200):
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


    def Draw(self,root,canvas,vertex_marking=False,rad=5):

        w=canvas.winfo_width()
        h=canvas.winfo_height()

        edges=[]

        def move_vertex(v):
            canvas.coords(v.id,v.pos.x-rad,v.pos.y-rad,v.pos.x+rad,v.pos.y+rad)
            canvas.tag_raise(v.id)
            if vertex_marking:
                canvas.coords(v.name_id,v.pos.x-2*rad,v.pos.y)

        def move_edge(id,v,u):
            canvas.coords(id,v.pos.x,v.pos.y,u.pos.x,u.pos.y)

        def move_vertex_by_mouse(event,v):
            if event.x>0 and event.x<w and event.y>0 and event.y<h:
                canvas.coords(v.id,event.x-rad,event.y-rad,event.x+rad,event.y+rad)

                v.pos.x=event.x
                v.pos.y=event.y

                canvas.tag_raise(v.id)

                if vertex_marking:
                    canvas.coords(v.name_id,event.x-2*rad,event.y)

                for i,[x,y] in enumerate(self.get_edges()):
                    if[x,y] in self.get_incident_edges(v):
                        move_edge(edges[i],x,y)


        for v in self.vertexes:
            v.pos=Point(random.randint(rad,w-rad),random.randint(rad,h-rad))
            v.id=canvas.create_oval(v.pos.x-rad,v.pos.y-rad,v.pos.x+rad,v.pos.y+rad,fill="red")
            canvas.tag_bind(v.id, '<B1-Motion>',lambda event,vertex=v:move_vertex_by_mouse(event,vertex)) 
            if vertex_marking:
                v.name_id=canvas.create_text(0,0,text=str(v.name),width=100,fill='black')
            move_vertex(v)

        
        for [v,u] in self.get_edges():
            id=canvas.create_line(0,0,0,0)
            edges.append(id)
            move_edge(id,v,u)

        D=self.floyd()
        

        def move():
            find_place=0
            for i,v in enumerate(self.vertexes):
                dx,dy=0,0
                for j,u in enumerate(self.vertexes):
                    if u!=v:
                        dx+=u.pos.x+D[i][j]*(v.pos.x-u.pos.x)/abs(v.pos-u.pos)
                        dy+=u.pos.y+D[i][j]*(v.pos.y-u.pos.y)/abs(v.pos-u.pos)
                
                new_place=Point(dx/(len(D)-1),dy/(len(D)-1))
                if abs(new_place-v.pos)<0.0001:
                    find_place+=1
                v.pos=new_place


            for v in self.vertexes:
                move_vertex(v)

            for [v,u],id in zip(self.get_edges(),edges):
                move_edge(id,v,u)

            if find_place<len(self.vertexes):
                root.after(1, move)
            else:
                print("it's over")


        root.after(1,move)

        






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





