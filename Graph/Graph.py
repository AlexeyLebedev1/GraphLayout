from Point import Point
import random


class Vertex():
    """Вершина графа"""
    def __init__(self,name):
        self.name=name
        self.pos=Point(0,0)
        self.id=None              #идентификатор для отрисовки

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




    def Draw(self,root,canvas,vertex_marking=False):

        # mass
        alpha = 1.0
        beta = .0001
        k = 1.0
        #damping
        eta = .99
        delta_t = .01

        ids={}

        text_pos={}
        def move_vertex(v):
            new_pos=v.pos*500
            new_pos.x=abs(int(new_pos.x))
            new_pos.y=abs(int(new_pos.y))
            canvas.coords(v.id,new_pos.x-5,new_pos.y-5,new_pos.x+5,new_pos.y+5)
            if vertex_marking:
                canvas.coords(text_pos[v],new_pos.x-10,new_pos.y)
            
        dp={}

        def move_vertex_by_mouse(event,v):
            if event.x>0 and event.x<canvas.winfo_width() and event.y>0 and event.y<canvas.winfo_height():
                canvas.coords(v.id,event.x-5,event.y-5,event.x+5,event.y+5)

        for v in self.vertexes:
            v.pos=Point(random.random(),random.random())
            dp[v]=Point(0.0,0.0)
            v.id=canvas.create_oval(245, 245, 255, 255, fill="red")
            canvas.tag_bind(v.id, '<B1-Motion>',lambda event:move_vertex_by_mouse(event,v)) #!!!!
            if vertex_marking:
                text_pos[v]=canvas.create_text(0,0,text=str(v.name),width=100,fill='black')
            move_vertex(v)

        def move_line(id,p1,p2):
            new_pos1=p1*500
            new_pos1.x=abs(int(new_pos1.x))
            new_pos1.y=abs(int(new_pos1.y))

            new_pos2=p2*500
            new_pos2.x=abs(int(new_pos2.x))
            new_pos2.y=abs(int(new_pos2.y))

            canvas.coords(id,new_pos1.x,new_pos1.y,new_pos2.x,new_pos2.y)


        lids=[]
        for [v,u] in self.get_edges():
            id=canvas.create_line(0,0,0,0)
            lids.append(id)
            move_line(id,v.pos,u.pos)

        def Coulomb_force(p1,p2):    #repulsive force
            d=p2-p1
            if d.length()==0:
                const=0
            else:
                const=beta/(d.length()**3)

            return d*(-const)

        def Hooke_force(p1, p2, delta=0.1): #attractive force
            d=p2-p1
            dl=d.length()-delta
            const=k*dl/d.length()
            return d*const

        def move():
            Ek=Point(0.0,0.0)
            for v in self.vertexes:
                F=Point(0.0,0.0)
                for u in self.vertexes:
                    if u in self.vertexes[v]:
                        Fuv=Hooke_force(v.pos,u.pos)
                    else:
                        Fuv=Coulomb_force(v.pos,u.pos)
                    F+=Fuv
                dp[v].x=(dp[v].x+alpha*F.x*delta_t)*eta
                dp[v].y=(dp[v].y+alpha*F.y*delta_t)*eta
                Ek+=Point(dp[v].x**2,dp[v].y**2)*alpha

            energy=float(Ek.length())

            for v in self.vertexes:
                v.pos+=dp[v]*delta_t
                move_vertex(v)

            k=0
            V=self.get_vertexes()
            for i,v in enumerate(V[:-1]):
                for u in V[i+1:]:
                    if u in self.vertexes[v]:
                        id=lids[k]
                        k+=1
                        move_line(id,v.pos,u.pos)

            if energy>=0.000001:
                root.after(1, move)


        root.after(1,move)

        root.mainloop()


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
        for i in range(n):
            neighbors=[]
            for j in range(n):
                if i!=j:
                    neighbors.append(Vertex(j))
            g[Vertex(i)]=neighbors

        return Graph(g)

    def Kpq(self,p,q):
        g={}
        for i in range(p):
            neighbors=[]
            for j in range(p,p+q):
                neighbors.append(Vertex(j))
            g[Vertex(i)]=neighbors

        for i in range(p,p+q):
            neighbors=[]
            for j in range(p):
                neighbors.append(Vertex(j))
            g[Vertex(i)]=neighbors 
        return Graph(g)

    def Cn(self,n):
        if n<3:
            return Graph()
        g={}
        g[Vertex(0)]=[Vertex(1),Vertex(n-1)]
        for i in range(1,n-1):
            g[Vertex(i)]=[Vertex(i-1),Vertex(i+1)]

        g[Vertex(n-1)]=[Vertex(0),Vertex(n-2)]

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
        g[Vertex(0)]=[Vertex(1)]
        for i in range(1,n-1):
            g[Vertex(i)]=[Vertex(i-1),Vertex(i+1)]

        g[Vertex(n-1)]=[Vertex(n-2)]

        return Graph(g)

    def Qn(self,n):
        if n<1:
            return Graph()
        g=self.Pn(2)
        for i in range(n-1):
            g*=self.Pn(2)
        
        #изменяем имена вершин в бинарные числа 
        g_str=g.get_str()
        names=g_str.keys()
        new_names=[]
        for name in names:
            new_name=''
            for ch in name:
                if ch=='0'or ch=='1':
                    new_name+=ch

            new_names.append(new_name)

        binary_g={}
        old_names=g_str.keys()
        for name_new,name in zip(new_names,old_names):
            adjacent_names=[]
            for next_name,old_name in zip(new_names,old_names):
                if old_name in g_str[name]:
                    adjacent_names.append(Vertex(next_name))

            binary_g[Vertex(name_new)]=adjacent_names

        return Graph(binary_g)




