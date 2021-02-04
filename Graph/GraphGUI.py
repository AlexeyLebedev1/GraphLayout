import tkinter as tk
import numpy as np
from Graph import Graph,GenerateGraph,Vertex,Edge
from MDSLayout import Parametrs,MDSLayout


class GraphGUI():
    def __init__(self):
        """Create main frame"""

        self.graph=Graph()
        self.graph_generator=GenerateGraph()


        self.root=tk.Tk()
        self.root.title('Graph Layout and Algorithms')
        self.root.geometry('1020x620+100+50') 

        #canvas for drawing graph
        self.canvas=tk.Canvas(self.root,width=1020,height=620,bg='white')   
        self.canvas.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        #parametrs for graph drawing
        self.parametrs=Parametrs()

        self.layout=MDSLayout(self.root,self.canvas,self.parametrs)        

        self.main_menu=tk.Menu(self.root,bg='white')                        
        self.root.config(menu=self.main_menu)

        # abstarct graphs classes
        self.classes_menu=tk.Menu(self.main_menu,tearoff=0)                
        self.classes_menu.add_command(label='Kn',command=lambda name='Kn':self.create_input_window1(name))
        self.classes_menu.add_command(label='Kp,q',command=lambda name='Kp,q':self.create_input_window1(name))
        self.classes_menu.add_command(label='Cn',command=lambda name='Cn':self.create_input_window1(name))
        self.classes_menu.add_command(label='Pn',command=lambda name='Pn':self.create_input_window1(name))
        self.classes_menu.add_command(label='On',command=lambda name='On':self.create_input_window1(name))
        self.classes_menu.add_command(label='Qn',command=lambda name='Qn':self.create_input_window1(name))
        self.main_menu.add_cascade(label='Special graphs',menu=self.classes_menu)


        # ways to init graph
        self.create_menu=tk.Menu(self.main_menu,tearoff=0)
        self.create_menu.add_command(label='Adjacency list',command=lambda init_way='adjacency list':self.create_input_window2(init_way))
        self.create_menu.add_command(label='Adjacency matrix',command=lambda init_way='adjacency matrix':self.create_input_window2(init_way))
        self.create_menu.add_command(label='List of edges and List of Vertexes',
                                     command=lambda init_way='list of vertexes and list of edges':self.create_input_window2(init_way))
        self.main_menu.add_cascade(label='Create Graph',menu=self.create_menu)

        # operations
        self.main_menu.add_command(label="Operations",command=self.create_operations_window)

        # algorithm
        self.algorithm_menu=tk.Menu(self.main_menu,tearoff=0)
        self.algorithm_menu.add_command(label='BFS tree',command=lambda procedure='BFS':self.set_start_vertex(procedure))
        self.algorithm_menu.add_command(label='DFS tree',command=lambda procedure='DFS':self.set_start_vertex(procedure))

        def f(name_algo):
            if name_algo=='Eulerian cycle':
                cycle=self.graph.find_Eulerian_cycle()
                if cycle:
                    print(name_algo+':')
                    print(cycle)
                else:
                    print('There are not '+name_algo)
            elif name_algo=='Hamiltonian cycle':
                cycle=self.graph.find_Hamiltonian_cycle()
                if cycle:
                    print(name_algo+':')
                    print(cycle)
                else:
                    print('There are not '+name_algo)

            elif name_algo=='Decision tree':
                self.graph=self.graph.get_decision_tree()
                self.DrawGraph()
            elif name_algo=='Max independent sets':
                S=self.graph.get_max_independent_sets()
                print(name_algo+':')
                print(S)
            elif name_algo=='Independent number':
                print(name_algo+'=',self.graph.get_independence_number())

            elif name_algo=='Vertex coverage number':
                print(name_algo+'=',self.graph.get_vertex_coverage_number())
            #elif name_algo=='Max clique':
                #S=self.graph.max_clique()
                #print(name_algo+':')
                #print(S)
            #elif name_algo=='Clique number':
                #print(name_algo+'=',self.graph.clique_number())

        self.algorithm_menu.add_command(label='Eulerian cycle',command=lambda name='Eulerian cycle':f(name))
        self.algorithm_menu.add_command(label='Hamiltonian cycle',command=lambda name='Hamiltonian cycle':f(name))
        #self.algorithm_menu.add_command(label='Hamiltonian path',command=lambda name='Hamiltonian path':f(name))
        self.algorithm_menu.add_command(label='Decision tree',command=lambda name='Decision tree':f(name))
        self.algorithm_menu.add_command(label='Max independent sets',command=lambda name='Max independent sets':f(name))
        self.algorithm_menu.add_command(label='Independent number',command=lambda name='Independent number':f(name))
        self.algorithm_menu.add_command(label='Vertex coverage number',command=lambda name='Vertex coverage number':f(name))
        #self.algorithm_menu.add_command(label='Max clique',command=lambda name='Max clique':f(name))
        #self.algorithm_menu.add_command(label='Clique number',command=lambda name='Clique number':f(name))


        self.main_menu.add_cascade(label='Algorithms',menu=self.algorithm_menu)


        # settings
        self.main_menu.add_command(label="Settings",command=self.create_settings_window)

        


        self.root.mainloop()

    def create_input_window1(self,type):
        """Create input window for Graphs: Kn,Kp,q,Cn,Pn,On,Qn"""
        input_window1=tk.Toplevel(bg='white',bd=4)
        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2
        input_window1.geometry('+{}+{}'.format(w,h))
        input_window1.title('Input graph')


        if type == 'Kp,q':
            tk.Label(input_window1,text='p',bg='white').grid(row=0,column=0,padx=3,pady=3,sticky='E')
            p_val = tk.IntVar(value=2) #initial value
            tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=p_val).grid(row=0,column=1,padx=3,pady=3)

            tk.Label(input_window1,text='q',bg='white').grid(row=0,column=2,padx=3,pady=3)
            q_val = tk.IntVar(value=3) #initial value
            tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=q_val).grid(row=0,column=3,padx=3,pady=3)

            def btnDraw_event():
                p=int(p_val.get())
                q=int(q_val.get())
                input_window1.destroy()
                self.graph=self.graph_generator.Kpq(p,q)
                self.DrawGraph()

            tk.Button(input_window1,text='Draw '+type,width=8,height=1,command=btnDraw_event).grid(row=3,column=0,padx=3,pady=3)

        else:
            tk.Label(input_window1,text='n',bg='white').grid(row=0,column=0,padx=3,pady=3,sticky='E')
            n_val = tk.IntVar(value=3) #initial value
            tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=n_val).grid(row=0,column=1,padx=3,pady=3)
        
            def btnDraw_event():
                n=int(n_val.get())
                input_window1.destroy()
                if type=='Kn':
                    self.graph=self.graph_generator.Kn(n)
                elif type=='Cn':
                    self.graph=self.graph_generator.Cn(n)
                elif type=='Pn':
                    self.graph=self.graph_generator.Pn(n)
                elif type=='On':
                    self.graph=self.graph_generator.On(n)
                elif type=='Qn':
                    self.graph=self.graph_generator.Qn(n,self.parametrs.get_vertex_marking())

                self.DrawGraph()


            tk.Button(input_window1,text='Draw '+type,width=8,height=1,command=btnDraw_event).grid(row=3,column=0,padx=3,pady=3)


        def btnCanel_event():
            input_window1.destroy()

        tk.Button(input_window1,text='Cancel',width=8,height=1,command=btnCanel_event).grid(row=3,column=4,padx=3,pady=3)


    def create_input_window2(self,init_way):
        """Create input window for Defining a graph with adjacency lists"""
        input_window2=tk.Toplevel(bg='white',bd=4)
        w,h=self.root.winfo_width()//3,self.root.winfo_height()//3
        input_window2.geometry('+{}+{}'.format(w,h))
        input_window2.title('Init graph')

        tk.Label(input_window2,text='Input '+init_way,bg='white').pack()
        graph_text=tk.Text(input_window2,bg='white')
        graph_text.pack(expand=True)
        
        if init_way=='list of vertexes and list of edges':
            graph_text.insert(1.0,'V:\n\n')
            graph_text.insert(3.0,'E:')

        def save_graph():
            if init_way=='adjacency list':
                text=graph_text.get(1.0,tk.END)
                g={}
                lines=text.split('\n')
                lines.pop(-1)
                for line in lines:
                    s=line.split(',')
                    vertexes=s[0].split(':')+s[1:]  
                    g[vertexes[0]]=vertexes[1:]           

                self.graph=self.graph_generator.adjacency_list(g)
                
            elif init_way=='adjacency matrix':
                text=graph_text.get(1.0,tk.END)
                lines=text.split('\n')
                lines.pop(-1)
                n=len(lines[0])
                matrix=np.zeros((n,n))
                for i,line in enumerate(lines):
                    for j,a in enumerate(line):
                        if a=='1':
                            matrix[i][j]=1

                self.graph=self.graph_generator.adjacency_matrix(matrix)

            elif init_way=='list of vertexes and list of edges':
                text=graph_text.get(1.0,tk.END)
                Vstr,Estr=text.split('\n\n')
                V=Vstr[2:].split(',')
                Estr=Estr[2:-1].split('),')
                E=[]
                for estr in Estr:
                    e=[]
                    for a in estr:
                        if a not in '(,)':
                            e.append(a)
                    E.append(e)

                self.graph=self.graph_generator.set_V_E(V,E)

            input_window2.destroy()
            self.DrawGraph()

           
        tk.Button(input_window2,text='Draw',command=save_graph).pack(side=tk.LEFT)


    def create_settings_window(self):
        """Create a window for layout settings"""
        settings_window=tk.Toplevel(bg='white',bd=4)

        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2

        settings_window.geometry('+{}+{}'.format(w,h))
        settings_window.title('settings')

        colors_vertex=['red','black','lavender','peach puff','deep sky blue','dark sea green','salmon','SkyBlue1','white']
        colors_edges=['red','black','lavender','peach puff','deep sky blue','dark sea green','salmon','SkyBlue1','white']

        colorVlbl=tk.Label(settings_window,text='Vertexes color: ',bg='white')
        colorVlbl.grid(row=0,column=0,padx=3,pady=3,sticky='W')
        for i,color in enumerate(colors_vertex):
            tk.Radiobutton(settings_window,text=color,variable=self.parametrs.vertex_color,value=color,bg='white',
                           selectcolor=color,justify=tk.LEFT).grid(row=i+1,column=0,sticky='W')

        colorElbl=tk.Label(settings_window,text='Edges color: ',bg='white')
        colorElbl.grid(row=0,column=1,padx=3,pady=3,sticky='W')
        for i,color in enumerate(colors_edges):
            tk.Radiobutton(settings_window,text=color,variable=self.parametrs.edge_color,value=color,bg='white',
                           selectcolor=color,justify=tk.LEFT).grid(row=i+1,column=1,sticky='W')


        tk.Checkbutton(settings_window,text='Vertex marking',variable=self.parametrs.vertex_marking,
                       bg='white').grid(row=0,column=2,padx=3,pady=3,sticky='W')


        tk.Label(settings_window,text='Vertex radius: ',bg='white').grid(row=1,column=2,padx=3,pady=3,sticky='W')
        tk.Spinbox(settings_window,from_=1,to=15,textvariable=self.parametrs.vertex_rad).grid(row=2,column=2,padx=3,pady=3,sticky='W')

        tk.Label(settings_window,text='Edges length: ',bg='white').grid(row=3,column=2,padx=3,pady=3,sticky='W')
        tk.Spinbox(settings_window,from_=10,increment=10,to=300,textvariable=self.parametrs.edges_length).grid(row=4,column=2,padx=3,pady=3,sticky='W')

        tk.Label(settings_window,text='Edges width: ',bg='white').grid(row=5,column=2,padx=3,pady=3,sticky='W')
        tk.Spinbox(settings_window,from_=1,to=10,textvariable=self.parametrs.edges_width).grid(row=6,column=2,padx=3,pady=3,sticky='W')


        last_c,last_r=settings_window.grid_size()
        tk.Button(settings_window,text='Save',command=settings_window.destroy,
                  relief=tk.RAISED,width=8).grid(column=last_c,row=last_r,padx=3,pady=3,sticky='W')



           
    def create_operations_window(self):         
        operations_window=tk.Toplevel(bg='white',bd=4)

        w,h=self.root.winfo_width()//3,self.root.winfo_height()//3

        operations_window.geometry('+{}+{}'.format(w,h))
        operations_window.title('Operations')

        graph=[Graph(),Graph()]

        def init_graph_panel(graph_frm,i):
            special_graphs_frm=tk.LabelFrame(graph_frm,text='Special graphs',bg='white')
            special_graphs_frm.pack()

            type_graph=tk.StringVar(value='Kn')

            n_count=tk.IntVar(value=3)
            n_box=tk.Spinbox(special_graphs_frm,from_ =1,to=50,textvariable=n_count,width = 5)
            n_lbl=tk.Label(special_graphs_frm,text='n:',bg='white')
            n_lbl.grid(column=0,row=6,padx=3,pady=3,sticky='W')
            n_box.grid(column=0,row=7,padx=3,pady=3,sticky='W')
        

            p_count,q_count=tk.IntVar(value=3),tk.IntVar(value=3)
            p_box=tk.Spinbox(special_graphs_frm,from_ =1,to=50,textvariable=p_count,width = 5)
            p_lbl=tk.Label(special_graphs_frm,text='p:',bg='white')
            q_box=tk.Spinbox(special_graphs_frm,from_ =1,to=50,textvariable=q_count,width = 5)
            q_lbl=tk.Label(special_graphs_frm,text='q:',bg='white')


            def input_n():
                n_lbl.grid(column=0,row=6,padx=3,pady=3,sticky='W')
                n_box.grid(column=0,row=7,padx=3,pady=3,sticky='W')

                p_box.grid_forget()
                q_box.grid_forget()
                p_lbl.grid_forget()
                q_lbl.grid_forget()

            def input_pq():
                p_lbl.grid(column=0,row=6,padx=3,pady=3,sticky='W')
                p_box.grid(column=0,row=7,padx=3,pady=3,sticky='W')

                q_lbl.grid(column=1,row=6,padx=3,pady=3,sticky='W')
                q_box.grid(column=1,row=7,padx=3,pady=3,sticky='W')

                n_lbl.grid_forget()
                n_box.grid_forget()

            tk.Radiobutton(special_graphs_frm,text='Kn',bg='white',variable=type_graph,value='Kn',command=input_n).grid(column=0,row=0,padx=3,pady=3,sticky='W')
            tk.Radiobutton(special_graphs_frm,text='Kp,q',bg='white',variable=type_graph,value='Kp,q',command=input_pq).grid(column=0,row=1,padx=3,pady=3,sticky='W')
            tk.Radiobutton(special_graphs_frm,text='Pn',bg='white',variable=type_graph,value='Pn',command=input_n).grid(column=0,row=2,padx=3,pady=3,sticky='W')
            tk.Radiobutton(special_graphs_frm,text='Cn',bg='white',variable=type_graph,value='Cn',command=input_n).grid(column=0,row=3,padx=3,pady=3,sticky='W')
            tk.Radiobutton(special_graphs_frm,text='Qn',bg='white',variable=type_graph,value='Qn',command=input_n).grid(column=0,row=4,padx=3,pady=3,sticky='W')
            tk.Radiobutton(special_graphs_frm,text='On',bg='white',variable=type_graph,value='On',command=input_n).grid(column=0,row=5,padx=3,pady=3,sticky='W')

            def save_graph():
                if type_graph.get()=='Kn':
                    graph[i]=self.graph_generator.Kn(int(n_count.get()))
                elif type_graph.get()=='Kp,q':
                    graph[i]=self.graph_generator.Kpq(int(p_count.get()),int(q_count.get()))
                elif type_graph.get()=='Pn':
                    graph[i]=self.graph_generator.Pn(int(n_count.get()))
                elif type_graph.get()=='Cn':
                    graph[i]=self.graph_generator.Cn(int(n_count.get()))
                elif type_graph.get()=='Qn':
                    graph[i]=self.graph_generator.Qn(int(n_count.get()))
                elif type_graph.get()=='On':
                    graph[i]=self.graph_generator.Pn(int(n_count.get()))

            tk.Button(special_graphs_frm,text='Save',bg='white',command=save_graph).grid(column=0,row=8,padx=3,pady=3,sticky='W')


        g1_frm=tk.LabelFrame(operations_window,text='Graph1',bg='white')
        g1_frm.grid(column=0,row=0,padx=3,pady=3,sticky='W')

        g2_frm=tk.LabelFrame(operations_window,text='Graph2',bg='white')
        g2_frm.grid(column=2,row=0,padx=3,pady=3,sticky='W')

        init_graph_panel(g1_frm,0)
        init_graph_panel(g2_frm,1)


        def composition():
            self.graph=graph[0]*graph[1]

        def draw():
            operations_window.destroy()
            self.DrawGraph()

        def inverse(i):
            graph[i]=~graph[i]
            self.graph=graph[i]

        tk.Button(operations_window,text='Composition',bg='white',command=composition).grid(column=1,row=0,padx=3,pady=3,sticky='W')
        tk.Button(operations_window,text='~Graph1',bg='white',command=lambda i=0:inverse(i)).grid(column=1,row=1,padx=3,pady=3,sticky='W')
        tk.Button(operations_window,text='~Graph2',bg='white',command=lambda i=1:inverse(i)).grid(column=1,row=2,padx=3,pady=3,sticky='W')
        tk.Button(operations_window,text='Draw',bg='white',command=draw).grid(column=1,row=9,padx=3,pady=3,sticky='W')


    def set_start_vertex(self,procedure):
        """Create a window for setting start vertex"""
        start_vertex_window=tk.Toplevel(bg='white',bd=4)
        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2
        start_vertex_window.geometry('+{}+{}'.format(w,h))
        start_vertex_window.title('Set start vertex')  

        scrollbar = tk.Scrollbar(start_vertex_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        vertex_list=self.graph.get_vertexes()
        start_vertex_box=tk.Listbox(start_vertex_window,yscrollcommand=scrollbar.set,width=10,selectmode=tk.SINGLE)
        for v in vertex_list:
            start_vertex_box.insert(tk.END,v.name)

        tk.Label(start_vertex_window,text='Set start vertex:',bg='white').pack()
        start_vertex_box.pack( fill=tk.BOTH)
        scrollbar.config(command=start_vertex_box.yview)

        #build_tree=tk.BooleanVar(value=True)

        def save_start_vertex():
            index=start_vertex_box.curselection()
            if len(index):
                if procedure=='BFS':
                    start_vertex_window.destroy()
                    self.graph=self.graph.get_bfs_tree(vertex_list[index[0]])
                    self.DrawGraph()
                    vertex_list[index[0]].root=False
                else:
                    start_vertex_window.destroy()
                    self.graph=self.graph.get_dfs_tree(vertex_list[index[0]])
                    self.DrawGraph()
                    vertex_list[index[0]].root=False

        tk.Button(start_vertex_window,text='Draw '+ procedure+' tree',bg='white',command=save_start_vertex).pack()


    def DrawGraph(self):
        self.canvas.delete('all')
        self.layout.Draw(self.graph)


   

Window=GraphGUI()

