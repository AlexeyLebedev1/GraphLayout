import unittest
from copy import copy
import numpy as np
import math
from Graph import Graph,GenerateGraph,Vertex,Edge
from Point import Point

class TestPoint(unittest.TestCase):
    def setUp(self):
        self.x1=5
        self.y1=6

        self.point1=Point(self.x1,self.y1)

        self.x2=-3
        self.y2=-4

        self.point2=Point(self.x2,self.y2)

    def test_init(self):
        self.assertEqual(self.x1,self.point1.x)
        self.assertEqual(self.y1,self.point1.y)

    def test_eq(self):
        tmp=Point(self.point1.x,self.point1.y)
        self.assertEqual(tmp,self.point1)

    def test_add(self):
        sum=self.point1+self.point2
        self.assertEqual(self.x1+self.x2,sum.x)
        self.assertEqual(self.y1+self.y2,sum.y)

    def test_sub(self):
        sum=self.point1-self.point2
        self.assertEqual(self.x1-self.x2,sum.x)
        self.assertEqual(self.y1-self.y2,sum.y)

    def test_mul(self):
        tmp=Point(self.point1.x*2,self.point1.y*2)
        self.assertEqual(tmp,self.point1*2)

    def test_truediv(self):
        tmp=Point(self.point1.x/2,self.point1.y/2)
        self.assertEqual(tmp,self.point1/2)

    def test_norm(self):
        self.assertEqual(5,self.point2.norm())

    def test_abs(self):
        self.assertEqual(5,abs(self.point2))



class TestVertex(unittest.TestCase):
    def setUp(self):
        self.name='x'
        self.vertex=Vertex(self.name)

    def test_init(self):
        self.assertEqual(self.name,self.vertex.name)
        self.assertEqual(Point(0,0),self.vertex.pos)
        self.assertEqual(None,self.vertex.id)
        self.assertEqual(None,self.vertex.name_id)
    
    def test_eq(self):
        tmp=Vertex(self.vertex.name)
        self.assertEqual(tmp,self.vertex)

    def test_ne(self):
        self.assertNotEqual(str(self.vertex.name),str(self.vertex.name)+str('v'))

    def test_hash(self):
        self.assertEqual(hash(self.name),hash(self.vertex))

    def test_str(self):
        self.assertEqual(str(self.name),str(self.vertex))

    def test_copy(self):
        self.assertEqual(Vertex(self.vertex.name),copy(self.vertex))


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.v=Vertex('a')
        self.u=Vertex('b')
        self.e1=Edge(self.v,self.u)
        self.e2=Edge(self.u,self.v)

    def test_eq(self):
        self.assertEqual(Edge(self.v,self.u),self.e1)
        self.assertEqual(self.e1,self.e2)

    def test_str(self):
        self.assertEqual('('+str(self.v)+','+str(self.u)+')',str(self.e1))

    def test_hash(self):
        self.assertEqual(hash(hash(self.v)+hash(self.u)),hash(self.e1))


class TestGraph(unittest.TestCase):
    def setUp(self):
        V=list(Vertex(i) for i in range(1,13))
        self.adjacency_list = {
               V[0]:[ V[1],V[3],V[5] ],
               V[1]:[ V[0] ],
               V[2]:[ V[4],V[8] ],
               V[3]:[ V[0] ],
               V[4]:[ V[2],V[8] ],
               V[5]:[ V[0] ],
               V[6]:[ V[7],V[9] ],
               V[7]:[ V[6],V[9], V[10] ],
               V[8]:[ V[2],V[4] ],
               V[9]:[ V[6],V[7], V[11] ],
               V[10]:[ V[7],V[11] ],
               V[11]:[ V[9],V[10] ]
               }
        self.graph=Graph(self.adjacency_list)
        self.edges_list=[Edge(V[0],V[1]),Edge(V[0],V[3]),Edge(V[0],V[5]),
                         Edge(V[2],V[4]),Edge(V[2],V[8]),Edge(V[4],V[8]),
                         Edge(V[6],V[7]),Edge(V[6],V[9]),Edge(V[7],V[9]),
                         Edge(V[7],V[10]),Edge(V[9],V[11]),Edge(V[10],V[11])]

    def test_init(self):
        self.assertEqual(self.adjacency_list,self.graph.vertexes)

    def test_invert(self):
        V=copy(self.graph.get_vertexes())
        invert_list = {
            V[0]:[ V[2],V[4],V[6],V[7],V[8],V[9],V[10],V[11] ],
            V[1]:[ V[2],V[3],V[4],V[5],V[6],V[7],V[8],V[9],V[10],V[11] ],
            V[2]:[ V[0],V[1],V[3],V[5],V[6],V[7],V[9],V[10],V[11] ],
            V[3]:[ V[1],V[2],V[4],V[5],V[6],V[7],V[8],V[9],V[10],V[11] ],
            V[4]:[ V[0],V[1],V[3],V[5],V[6],V[7],V[9],V[10],V[11] ],
            V[5]:[ V[1],V[2],V[3],V[4],V[6],V[7],V[8],V[9],V[10],V[11] ],
            V[6]:[ V[0],V[1],V[2],V[3],V[4],V[5],V[8],V[10],V[11] ],
            V[7]:[ V[0],V[1],V[2],V[3],V[4],V[5],V[8],V[11] ],
            V[8]:[ V[0],V[1],V[3],V[5],V[6],V[7],V[9],V[10],V[11] ],
            V[9]:[ V[0],V[1],V[2],V[3],V[4],V[5],V[8],V[10] ],
            V[10]:[ V[0],V[1],V[2],V[3],V[4],V[5],V[6],V[8],V[9] ],
            V[11]:[ V[0],V[1],V[2],V[3],V[4],V[5],V[6],V[7],V[8] ]
            }
        self.assertEqual(Graph(invert_list),~(self.graph))


    def test_get_vertexes(self):
        self.assertEqual(list(self.adjacency_list.keys()),self.graph.get_vertexes())

    def test_get_edges(self):
        self.assertEqual(self.edges_list,self.graph.get_edges())

    def test_add_vertex(self):
        self.graph.add_vertex(Vertex(13))
        self.assertIn(Vertex(13),self.graph.vertexes.keys())

        self.graph.add_vertex(Vertex(5))
        self.assertIn(Vertex(5),self.graph.vertexes.keys())

    def test_add_edge(self):
        self.graph.add_edge(Edge(Vertex(14),Vertex(15)))
        self.assertIn(Vertex(15),self.graph.vertexes[Vertex(14)])
        self.assertIn(Vertex(14),self.graph.vertexes[Vertex(15)])

        self.graph.add_edge(Edge(Vertex(5),Vertex(10)))
        self.assertIn(Vertex(5),self.graph.vertexes[Vertex(10)])
        self.assertIn(Vertex(10),self.graph.vertexes[Vertex(5)])

        self.graph.add_edge(Edge(Vertex(1),Vertex(4)))
        self.assertIn(Vertex(1),self.graph.vertexes[Vertex(4)])
        self.assertIn(Vertex(4),self.graph.vertexes[Vertex(1)])

    def test_get_str_dict(self):
        g_str={'1':['2','4','6'],
               '2':['1'],
               '3':['5','9'],
               '4':['1'],
               '5':['3','9'],
               '6':['1'],
               '7':['8','10'],
               '8':['7','10','11'],
               '9':['3','5'],
               '10':['7','8','12'],
               '11':['8','12'],
               '12':['10','11']}
        self.assertEqual(g_str,self.graph.get_str_dict())

    def test_get_incident_edges(self):
        self.assertEqual(self.edges_list[:3],self.graph.get_incident_edges(Vertex(1)))

    def test_floyd(self):
        D=np.array([[0,1,math.inf,1,math.inf,1,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
                   [1,0,math.inf,2,math.inf,2,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
                   [math.inf,math.inf,0,math.inf,1,math.inf,math.inf,math.inf,1,math.inf,math.inf,math.inf],
                   [1,2,math.inf,0,math.inf,2,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
                   [math.inf,math.inf,1,math.inf,0,math.inf,math.inf,math.inf,1,math.inf,math.inf,math.inf],
                   [1,2,math.inf,2,math.inf,0,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
                   [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,0,1,math.inf,1,2,2],
                   [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,1,0,math.inf,1,1,2],
                   [math.inf,math.inf,1,math.inf,1,math.inf,math.inf,math.inf,0,math.inf,math.inf,math.inf],
                   [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,1,1,math.inf,0,2,1],
                   [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,2,1,math.inf,2,0,1],
                   [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,2,2,math.inf,1,1,0]])

        A=self.graph.floyd(length=1)
        self.assertEqual(True,np.array_equal(D,A))

    def test_mul(self):
        Q2=GenerateGraph().Pn(2)*GenerateGraph().Pn(2)
        V=[Vertex('(0,0)'),Vertex('(0,1)'),Vertex('(1,0)'),Vertex('(1,1)')]
        adjacency_list={V[0]:[V[1],V[2]],
                        V[1]:[V[0],V[3]],
                        V[2]:[V[0],V[3]],
                        V[3]:[V[1],V[2]]}
        self.assertEqual(Q2,Graph(adjacency_list))





class TestGenerateGraph(unittest.TestCase):
    def setUp(self):
        self.generator=GenerateGraph()

        self.K3=Graph({Vertex(0):[Vertex(1),Vertex(2)],
                       Vertex(1):[Vertex(0),Vertex(2)],
                       Vertex(2):[Vertex(0),Vertex(1)]})
        
        self.K23=Graph({Vertex(0):[Vertex(2),Vertex(3),Vertex(4)],
                        Vertex(1):[Vertex(2),Vertex(3),Vertex(4)],
                        Vertex(2):[Vertex(0),Vertex(1)],
                        Vertex(3):[Vertex(0),Vertex(1)],
                        Vertex(4):[Vertex(0),Vertex(1)]})

        self.C4=Graph({Vertex(0):[Vertex(1),Vertex(3)],
                       Vertex(1):[Vertex(0),Vertex(2)],
                       Vertex(2):[Vertex(1),Vertex(3)],
                       Vertex(3):[Vertex(0),Vertex(2)]})

        self.P4=Graph({Vertex(0):[Vertex(1)],
                       Vertex(1):[Vertex(0),Vertex(2)],
                       Vertex(2):[Vertex(1),Vertex(3)],
                       Vertex(3):[Vertex(2)]})

        self.O4=Graph({Vertex(0):[],
                       Vertex(1):[],
                       Vertex(2):[],
                       Vertex(3):[]})
        
        self.Q3=Graph({Vertex('000'):[Vertex('001'),Vertex('010'),Vertex('100')],
                       Vertex('001'):[Vertex('000'),Vertex('011'),Vertex('101')],
                       Vertex('010'):[Vertex('000'),Vertex('011'),Vertex('110')],
                       Vertex('011'):[Vertex('001'),Vertex('010'),Vertex('111')],
                       Vertex('100'):[Vertex('000'),Vertex('101'),Vertex('110')],
                       Vertex('101'):[Vertex('001'),Vertex('100'),Vertex('111')],
                       Vertex('110'):[Vertex('010'),Vertex('100'),Vertex('111')],
                       Vertex('111'):[Vertex('011'),Vertex('101'),Vertex('110')],
            })

    def testKn(self):
        self.assertEqual(self.K3,self.generator.Kn(3))

    def testKpq(self):
        self.assertEqual(self.K23,self.generator.Kpq(2,3))

    def testCn(self):
        self.assertEqual(self.C4,self.generator.Cn(4))

    def testPn(self):
        self.assertEqual(self.P4,self.generator.Pn(4))

    def testOn(self):
        self.assertEqual(self.O4,self.generator.On(4))

    def testQn(self):
        self.assertEqual(self.Q3,self.generator.Qn(3,True))

    def test_adjacency_list(self):
        K23={0:[2,3,4],
             1:[2,3,4],
             2:[0,1],
             3:[0,1],
             4:[0,1]}
        g=self.generator.adjacency_list(K23)
        self.assertEqual(self.K23,g)
        V=list(g.vertexes.keys())
        for v in g.vertexes:
            for u in g.vertexes[v]:
                self.assertEqual(id(u),id(V[V.index(u)]))

    def test_adjacency_matrix(self):
        K23matrix=np.array([[0,0,1,1,1],[0,0,1,1,1],[1,1,0,0,0],[1,1,0,0,0],[1,1,0,0,0]])
        g=self.generator.adjacency_matrix(K23matrix)
        self.assertEqual(self.K23,g)
        V=list(g.vertexes.keys())
        for v in g.vertexes:
            for u in g.vertexes[v]:
                self.assertEqual(id(u),id(V[V.index(u)]))

    def test_set_V_E(self):
        V=['000','001','010','011','100','101','110','111']
        E=[['000','001'],['000','010'],['000','100'],['001','011'],['001','101'],['010','011'],
           ['010','110'],['011','111'],['100','101'],['100','110'],['101','111'],['110','111']]

        g=self.generator.set_V_E(V,E)
        self.assertEqual(self.Q3,g)
        V=list(g.vertexes.keys())
        for v in g.vertexes:
            for u in g.vertexes[v]:
                self.assertEqual(id(u),id(V[V.index(u)]))


if __name__ == '__main__':
    unittest.main()
