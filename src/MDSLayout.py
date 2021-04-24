
from Point import Point
from Graph import Graph,Vertex,Edge
import tkinter as tk
import random
import math
import numpy as np


class Parametrs():
    """Parametrs for graph drawing"""
    def __init__(self):
        self.vertex_marking=tk.BooleanVar()   
        self.vertex_color=tk.StringVar(value="red")
        self.edge_color=tk.StringVar(value="black")
        self.vertex_rad=tk.IntVar(value=5)
        self.edges_length=tk.IntVar(value=100)
        self.edges_width=tk.IntVar(value=1)

    def get_vertex_marking(self):
        return self.vertex_marking.get()

    def get_vertex_color(self):
        return self.vertex_color.get()

    def get_edge_color(self):
        return self.edge_color.get()

    def get_vertex_rad(self):
        return int(self.vertex_rad.get())

    def get_edges_length(self):
        return int(self.edges_length.get())

    def get_edges_width(self):
        return int(self.edges_width.get())



class MDSLayout():
    """Graph layout by multidimensional scaling"""
    def __init__(self,root,canvas,parametrs):
        self.root=root
        self.canvas=canvas
        self.parametrs=parametrs

    def disp_text(self,name):
        p=name.find('\n')
        if p==-1:
            return len(name)*3
        else:
            return p*3

    def move_vertex(self,v):
            self.canvas.coords(v.id,v.pos.x-v.rad,v.pos.y-v.rad,v.pos.x+v.rad,v.pos.y+v.rad)
            self.canvas.tag_raise(v.id)
            if self.parametrs.get_vertex_marking():
                self.canvas.coords(v.name_id,v.pos.x-v.rad-self.disp_text(str(v.name)),v.pos.y)

    def move_edge(self,e):
            self.canvas.coords(e.id,e.v.pos.x,e.v.pos.y,e.u.pos.x,e.u.pos.y)

    def move_vertex_by_mouse(self,event,v,graph,edges):
        w=self.canvas.winfo_width()
        h=self.canvas.winfo_height()
        if event.x>0 and event.x<w and event.y>0 and event.y<h:
            self.canvas.coords(v.id,event.x-v.rad,event.y-v.rad,event.x+v.rad,event.y+v.rad)

            v.pos.x=event.x
            v.pos.y=event.y

            self.canvas.tag_raise(v.id)

            if self.parametrs.get_vertex_marking():
                #self.canvas.tag_raise(v.name_id)
                self.canvas.coords(v.name_id,event.x-v.rad-self.disp_text(str(v.name)),event.y)

            for e in edges:
                if e in graph.get_incident_edges(v):
                    self.move_edge(e)

    def place_vertexes_on_canvas(self,graph,edges):

        rad=self.parametrs.get_vertex_rad()
        w=self.canvas.winfo_width()
        h=self.canvas.winfo_height()

        for v in graph.vertexes:
            if v.root:
                v.rad=rad*2
            else:
                v.rad=rad
            v.pos=Point(random.randint(v.rad,w-v.rad),random.randint(v.rad,h-v.rad))
            v.id=self.canvas.create_oval(v.pos.x-v.rad,v.pos.y-v.rad,v.pos.x+v.rad,v.pos.y+v.rad,fill=self.parametrs.get_vertex_color())
            self.canvas.tag_bind(v.id, '<B1-Motion>',lambda event,vertex=v:self.move_vertex_by_mouse(event,vertex,graph,edges)) 
            if self.parametrs.get_vertex_marking():
                v.name_id=self.canvas.create_text(0,0,text=str(v.name),width=100,fill='black')

    def place_edges_on_canvas(self,graph,edges):
        for e in edges:
            e.id=self.canvas.create_line(e.v.pos.x,e.v.pos.y,e.u.pos.x,e.u.pos.y,
                 fill=self.parametrs.get_edge_color(),width=self.parametrs.get_edges_width())

    def GetWeightMatrix(self,D):
        """Weight matrix for each vertex in graph"""
        n=len(D)
        W=np.ones((n,n))
        for i in range(n):
            for j in range(i+1,n):
                W[i][j]=W[j][i]=D[i][j]**-2

        return W

    def stress(self,v,i,D,W,graph):
        dx,dy=0,0
        w_sum=0.0
        for j,u in enumerate(graph.vertexes):
            if u!=v:
                w_sum+=W[i][j]
                try:
                    dx+=W[i][j]*(u.pos.x+D[i][j]*(v.pos.x-u.pos.x)/abs(v.pos-u.pos))
                    dy+=W[i][j]*(u.pos.y+D[i][j]*(v.pos.y-u.pos.y)/abs(v.pos-u.pos))
                except ZeroDivisionError:
                    dx+=W[i][j]*(u.pos.x+D[i][j]*(v.pos.x-u.pos.x)/0.00001)
                    dy+=W[i][j]*(u.pos.y+D[i][j]*(v.pos.y-u.pos.y)/0.00001)

        return Point(dx/w_sum,dy/w_sum)

    def Draw(self,graph):

        D=graph.floyd(self.parametrs.get_edges_length())
        W=self.GetWeightMatrix(D)

        edges=graph.get_edges()

        self.place_vertexes_on_canvas(graph,edges)
        self.place_edges_on_canvas(graph,edges)

        def move():
            find_place=0
            for i,v in enumerate(graph.vertexes):
                new_place=self.stress(v,i,D,W,graph)
                 
                if abs(new_place-v.pos)<0.0001:
                    find_place+=1

                v.pos=new_place


            for v in graph.vertexes:
                self.move_vertex(v)

            for e in edges:
                self.move_edge(e)

            if find_place<len(graph.vertexes):
                self.root.after(1, move)
            else:
                print("stop drawing")


        self.root.after(1,move)

