import unittest
from Graph import Graph,GenerateGraph,Vertex
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
        """Проверка инициализации точки"""
        self.assertEqual(self.x1,self.point1.x)
        self.assertEqual(self.y1,self.point1.y)

    def test_add(self):
        """Проверка операции сложения"""
        sum=self.point1+self.point2
        self.assertEqual(self.x1+self.x2,sum.x)
        self.assertEqual(self.y1+self.y2,sum.y)

    def test_sub(self):
        """Проверка операции вычитания"""
        sum=self.point1-self.point2
        self.assertEqual(self.x1-self.x2,sum.x)
        self.assertEqual(self.y1-self.y2,sum.y)

    def test_eq(self):
        """Проверка операции сравнения (==)"""
        tmp=Point(self.point1.x,self.point1.y)
        self.assertEqual(tmp,self.point1)

    def test_length(self):
        self.assertEqual(5,self.point2.length())

    def test_mul(self):
        tmp=Point(self.point1.x*2,self.point1.y*2)
        self.assertEqual(tmp,self.point1*2)

    def test_truediv(self):
        tmp=Point(self.point1.x/2,self.point1.y/2)
        self.assertEqual(tmp,self.point1/2)

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


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.vertex_list={
               Vertex(1):[Vertex(2),Vertex(4),Vertex(6)],
               Vertex(2):[Vertex(1)],
               Vertex(3):[ Vertex(5), Vertex(9)],
               Vertex(4):[Vertex(1)],
               Vertex(5):[Vertex(3),Vertex(9)],
               Vertex(6):[Vertex(1)],
               Vertex(7):[Vertex(8),Vertex(10)],
               Vertex(8):[Vertex(7), Vertex(10), Vertex(11)],
               Vertex(9):[Vertex(3), Vertex(5)],
               Vertex(10):[Vertex(7), Vertex(8), Vertex(12)],
               Vertex(11):[Vertex(8),Vertex(12)],
               Vertex(12):[Vertex(10), Vertex(11)]
               }
        self.graph=Graph(self.vertex_list)
        self.edges_list=[[Vertex(1),Vertex(2)],[Vertex(1),Vertex(4)],[Vertex(1),Vertex(6)],
                         [Vertex(3),Vertex(5)],[Vertex(3),Vertex(9)],[Vertex(5),Vertex(9)],
                         [Vertex(7),Vertex(8)],[Vertex(7),Vertex(10)],[Vertex(8),Vertex(10)],
                         [Vertex(8),Vertex(11)],[Vertex(10),Vertex(12)],[Vertex(11),Vertex(12)]]

    def test_init(self):
        """Проверка инициализации графа"""
        self.assertEqual(self.vertex_list,self.graph.vertexes)

    def test_get_vertexes(self):
        """Проверка метода get_vertexes"""
        self.assertEqual(list(self.vertex_list.keys()),self.graph.get_vertexes())

    def test_get_edges(self):
        """Проверка метода get_edges"""
        self.assertEqual(self.edges_list,self.graph.get_edges())

    def test_add_vertex(self):
        """Проверка метода add_vertex. Добавляем новую вершину и уже существующую"""
        self.graph.add_vertex(Vertex(13))
        self.assertIn(Vertex(13),self.graph.vertexes.keys())

        self.graph.add_vertex(Vertex(5))
        self.assertIn(Vertex(5),self.graph.vertexes.keys())

    def test_add_edge(self):
        """Проверка метода add_edge. Добавляем новое ребро из новых вершин, новое ребро из старых вершин и уже существующее ребро """
        self.graph.add_edge([Vertex(14),Vertex(15)])
        self.assertIn(Vertex(15),self.graph.vertexes[Vertex(14)])
        self.assertIn(Vertex(14),self.graph.vertexes[Vertex(15)])

        self.graph.add_edge([Vertex(5),Vertex(10)])
        self.assertIn(Vertex(5),self.graph.vertexes[Vertex(10)])
        self.assertIn(Vertex(10),self.graph.vertexes[Vertex(5)])

        self.graph.add_edge([Vertex(1),Vertex(4)])
        self.assertIn(Vertex(1),self.graph.vertexes[Vertex(4)])
        self.assertIn(Vertex(4),self.graph.vertexes[Vertex(1)])

    def test_get_str(self):
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
        self.assertEqual(g_str,self.graph.get_str())

    def test_get_incident_edges(self):
        self.assertEqual(self.edges_list[:3],self.graph.get_incident_edges(Vertex(1)))



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
        self.assertEqual(self.Q3,self.generator.Qn(3))


if __name__ == '__main__':
    unittest.main()
