

point_of_line=0
point_start=0
end_poligon=False

def new_point(cor):
    return Node(cor[0],cor[1],cor[2])

def new_points(coordinats):
    nodes=[]
    for i in coordinats:
        nodes.append(Node(i[0],i[1],i[2]))
    return nodes

def new_line(coordinats):
    cor=coordinats.pop(0)
    nodes=[Node(cor[0],cor[1],cor[2])]
    for i in coordinats:
        nodes.append(Node(i[0],i[1],i[2]))
        nodes[len(nodes)-1].new_connection(nodes[len(nodes)-2])
    return nodes

def new_poligon(coordinats):
    cor=coordinats.pop(0)
    nodes=[Node(cor[0],cor[1],cor[2])]
    for i in coordinats:
        nodes.append(Node(i[0],i[1],i[2]))
        nodes[len(nodes)-1].new_connection(nodes[len(nodes)-2])
    nodes[0].new_connection(nodes[-1])    
    return nodes

def new_poligon_v2(coordinats):    
    cor=coordinats.pop(0)
    nodes=[Node(cor[0],cor[1],cor[2])]
    for i in coordinats:
        nodes.append(Node(i[0],i[1],i[2]))
        for j in range(len(nodes)-1):
            nodes[j].new_connection(nodes[len(nodes)-1])
    #nodes[0].new_connection(nodes[-1])    
    return nodes
    #return nodes
    #list_of_points.append(node)
    #if point_of_line!=0:
    #    node.connect(point_of_line)
    #if point_start==0:
    #    point_start=node
    #point_of_line=node
    #if end_poligon:
    #    node.connect(point_start)

class Point:
  def __init__(self, x,y):
    self.x=x
    self.y=y

class Node:
  def __init__(self, x,y,name=None):
    """_summary_

      Args:
          x (_type_): координаты
          y (_type_): координаты
          name (_type_, optional): имя переменной. Defaults to None.
    """
    self.point=Point(x,y)
    self.connect=[]
    self.name=name
    self.name_grup=0
  def new_connection(self,node):
    """_summary_

      Args:
          node (_type_): Модуль, с которым будет построено соединение
    """
    self.connect.append(node)
    node.connect.append(self)
  def whether_connected(self,node):
    """_summary_

      Args:
          node (Node): Узел, с которым идет проверка соединения

      Returns:
          Bool: Соединена ли точка
    """
    for i in self.connect:
        if node==i:
            return True
    return False
  def rename(self,name):
    """_summary_ Меняет название группы, при условии, что его не было, на name. 
      Args:
          name (str or int): Имя, на которое будут переименовываться все объекты
    """
    useful=False
    if self.name_grup==0:
        self.name_grup=name
        useful=True
        for i in self.connect:
            i.rename(name)
    return useful
      
  def print_connect(self):
      """
      Выводит информаию о точке и всех с ней соединенных объектов
      """
      print("Название точки: ",self.name)
      print("Координаты точки: ",self.point.x,":",self.point.y)
      if  len(self.connect)>0:
          print("Данная точка соединена с:")
      for i in self.connect:
        print("Название: ",i.name)
        print("Координаты: ",i.point.x,":",i.point.y)
      print("--------------")
      
  # def __repr__ (self):
  #   return f'Node ({self.point! r}, {self.connect! r},{self.name! r}, {self.name_grup! r}) '



# if __name__ == '__main__':
#     import persistent_diagram as pd
#     object_1=[[1,2,"p-1"],
#               [1,4,"p-2"],
#               [5,2,"p-3"],
#               [7,2,"p-4"],
#               [9,9,"p-5"]]
#     list_of_points=[]
#     list_of_points+=new_points(object_1)
#     for i in list_of_points:
#         i.print_connect()
#     pd.diagram(list_of_points)
    

if __name__ == '__main__':
    object_1=[[1,2,"p-1"],
              [1,4,"p-2"],
              [5,2,"p-3"],
              [7,2,"p-4"],
              [9,9,"p-5"]]
    list_of_points=[]
    list_of_points+=new_poligon_v2(object_1)
    for i in list_of_points:
        i.print_connect()


      

# if __name__ == '__main__':

#     point1=Node(1,1,"t-1")
#     point2=Node(1,3,"t-2")
#     point2.new_connection(point1)
#     #if point1.whether_connected(point2):
#     #    print("Точка соединена")
#     #else:
#     #    print("No")
#     point2.print_connect()
#     point2.new_connection(Node(1,10,"t-3"))
#     point2.print_connect()

#     # new_line(2,7,"l-1")
#     # new_line(3,8,"l-2")
#     # new_line(0,5,"l-3")
#     # list_of_points[0].print_connect()
