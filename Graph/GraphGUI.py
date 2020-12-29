import tkinter as tk
from tkinter import colorchooser
from Graph import Graph,GenerateGraph,Vertex
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
        self.create_menu.add_command(label='Adjacency list',command=self.create_input_window2)
        self.create_menu.add_command(label='Adjacency matrix')
        self.create_menu.add_command(label='List of edges and List of Vertexes')
        self.main_menu.add_cascade(label='Create Graph',menu=self.create_menu)


        # settings
        self.main_menu.add_command(label="Settings",command=self.create_settings_window)


        self.root.mainloop()

    def create_input_window1(self,type):
        """Create input window for Graphs: Kn,Cn,Pn,On"""
        input_window1=tk.Toplevel(bg='white',bd=4)
        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2
        input_window1.geometry('+{}+{}'.format(w,h))
        input_window1.title('')

        if type == 'Kp,q':
            p_lbl=tk.Label(input_window1,text='p',bg='white')
            p_lbl.grid(row=0,column=0,padx=3,pady=3,sticky='E') 

            var = tk.IntVar(value=2) #initial value
            p_val=tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=var)
            p_val.grid(row=0,column=1,padx=3,pady=3)

            q_lbl=tk.Label(input_window1,text='q',bg='white')
            q_lbl.grid(row=0,column=2,padx=3,pady=3)

            var = tk.IntVar(value=3) #initial value
            q_val=tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=var)
            q_val.grid(row=0,column=3,padx=3,pady=3)

            def btnDraw_event():
                p=int(p_val.get())
                q=int(q_val.get())
                input_window1.destroy()
                self.graph=self.graph_generator.Kpq(p,q)
                self.DrawGraph()

            btnDraw=tk.Button(input_window1,text='Draw '+type,width=8,height=1,command=btnDraw_event)
            btnDraw.grid(row=2,column=0,padx=3,pady=3)
        else:
            n_lbl=tk.Label(input_window1,text='n',bg='white')
            n_lbl.grid(row=0,column=0,padx=3,pady=3,sticky='E') 

            var = tk.IntVar(value=3) #initial value
            n_val=tk.Spinbox(input_window1,from_= 1, to = 50, width = 5,textvariable=var)
            n_val.grid(row=0,column=1,padx=3,pady=3)
        
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

            btnDraw=tk.Button(input_window1,text='Draw '+type,width=8,height=1,command=btnDraw_event)
            btnDraw.grid(row=2,column=0,padx=3,pady=3)


        def btnCanel_event():
            input_window1.destroy()

        btnCancel=tk.Button(input_window1,text='Cancel',width=8,height=1,command=btnCanel_event)
        btnCancel.grid(row=2,column=4,padx=3,pady=3)


    def create_input_window2(self):
        """Create input window for Defining a graph with adjacency lists"""
        input_window2=tk.Toplevel(bg='white',bd=4)
        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2
        input_window2.geometry('+{}+{}'.format(w,h))
        input_window2.title('')

        box = tk.Listbox(input_window2,selectmode='EXTENDED')
        box.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(input_window2,command=box.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        box.config(yscrollcommand=scroll.set)

        btns_frame=tk.Frame(input_window2,bg='white')
        btns_frame.pack(side=tk.LEFT,padx=10)

        input_lbl=tk.Label(btns_frame,text="Enter a vertex and adjacent vertices\n (example - '1:2,4,7')",bg='white')
        input_lbl.pack()

        input_entry=tk.Entry(btns_frame)
        input_entry.pack(anchor=tk.N)

        def addItem():
            box.insert(tk.END, input_entry.get())
            input_entry.delete(0, tk.END)

        btnAdd=tk.Button(btns_frame,text='Add',command=addItem)
        btnAdd.pack(fill=tk.X)

        def del_Items():
            select = list(box.curselection())
            select.reverse()
            for i in select:
                box.delete(i)

        btnDel=tk.Button(btns_frame,text='Delete',command=del_Items)
        btnDel.pack(fill=tk.X)

        def save_graph():  ### can make better
            g_str=box.get(0,tk.END)
            g={}
            for line in g_str:
                s=line.split(',')
                vertexes=s[0].split(':')+s[1:]
                g[Vertex(vertexes[0])]=list(Vertex(vertexes[i]) for i in range(1,len(vertexes)))
             
            V=list(g.keys())
            for v in V:
                v_list=[]
                for u in g[v]:
                    v_list.append(V[V.index(u)])
                g[v]=v_list

            self.graph=Graph(g)
            input_window2.destroy()
            self.DrawGraph()

           
        btnDraw=tk.Button(btns_frame,text='Draw',command=save_graph)
        btnDraw.pack(fill=tk.X)

    def create_settings_window(self):
        """Create a window for layout settings"""
        settings_window=tk.Toplevel(bg='white',bd=4)

        w,h=self.root.winfo_width()//2,self.root.winfo_height()//2

        settings_window.geometry('+{}+{}'.format(w,h))
        settings_window.title('settings')

        colors_vertex=['red','black','lavender','peach puff','deep sky blue','dark sea green','salmon','SkyBlue1']
        colors_edges=['black','gray63','thistle2','SlateGray4','azure','lavender','cornflower blue']

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
        
        
            


            
         

    def DrawGraph(self):
        self.canvas.delete('all')
        self.layout.Draw(self.graph)


   




Window=GraphGUI()

