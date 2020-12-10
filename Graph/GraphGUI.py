import tkinter as tk
from Graph import Graph,GenerateGraph,Vertex


class GraphGUI():
    def __init__(self):
        """Create main frame"""

        self.graph=Graph()
        self.graph_generator=GenerateGraph()


        self.root=root=tk.Tk()
        self.root.title('Graph Layout and algorithms')
        self.root.geometry('1020x620+100+50')       
        
        #canvas for drawing graph
        self.canvas=tk.Canvas(self.root,width=1020,height=620,bg='white')   
        self.canvas.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.main_menu=tk.Menu(self.root,bg='white')                        
        self.root.config(menu=self.main_menu)

        # abstarct graphs classes
        self.classes_menu=tk.Menu(self.main_menu,tearoff=0)                
        self.classes_menu.add_command(label='Kn',command=lambda name='Kn':self.create_input_window1(name))
        self.classes_menu.add_command(label='Kp,q',command=lambda name='Kp,q':self.create_input_window1(name))
        self.classes_menu.add_command(label='Cn',command=lambda name='Cn':self.create_input_window1(name))
        self.classes_menu.add_command(label='Pn',command=lambda name='Pn':self.create_input_window1(name))
        self.classes_menu.add_command(label='On',command=lambda name='On':self.create_input_window1(name))

        self.main_menu.add_cascade(label='Special graphs',menu=self.classes_menu)

        self.create_menu=tk.Menu(self.main_menu,tearoff=0)
        self.create_menu.add_command(label='Adjacency list',command=self.create_input_window2)
        self.create_menu.add_command(label='Adjacency matrix')
        self.create_menu.add_command(label='List of edges and List of Vertexes')

        self.main_menu.add_cascade(label='Create Graph',menu=self.create_menu)

        self.root.mainloop()

    def create_input_window1(self,type):
        """Create input window for Graphs: Kn,Cn,Pn,On"""
        input_window1=tk.Toplevel(bg='white',bd=4)
        input_window1.geometry('+200+200')
        input_window1.title('')

        if type == 'Kp,q':
            p_lbl=tk.Label(input_window1,text='p',bg='white')
            p_lbl.grid(row=0,column=0,padx=3,pady=3,sticky='E') 

            p_val=tk.Spinbox(input_window1,from_= 0, to = 50, width = 5)
            p_val.grid(row=0,column=1,padx=3,pady=3)

            q_lbl=tk.Label(input_window1,text='q',bg='white')
            q_lbl.grid(row=0,column=2,padx=3,pady=3)

            q_val=tk.Spinbox(input_window1,from_= 0, to = 50, width = 5)
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

            n_val=tk.Spinbox(input_window1,from_= 0, to = 50, width = 5)
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
        input_window2.geometry('+200+200')
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

        def save_graph():
            g_str=box.get(0,tk.END)
            g={}
            for line in g_str:
                s=line.split(',')
                vertexes=s[0].split(':')+s[1:]
                g[Vertex(vertexes[0])]=list(Vertex(vertexes[i]) for i in range(1,len(vertexes)))

            self.graph=Graph(g)
            input_window2.destroy()
            self.DrawGraph()

           
        btnDraw=tk.Button(btns_frame,text='Draw',command=save_graph)
        btnDraw.pack(fill=tk.X)
         

    def DrawGraph(self):
        self.canvas.delete('all')
        self.graph.Draw(self.root,self.canvas)


   




Window=GraphGUI()

