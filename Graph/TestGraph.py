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



if __name__ == '__main__':
    unittest.main()
