import my_import.point_search as ps
# project = QgsProject.instance()
# layer_name = "poligon_1"
# list_layers = project.mapLayersByName(layer_name)
# my_layer = list_layers[0]
# features = my_layer.getFeatures()
# object_chec=0
point_list=[]
# for feature in features:
#     geom = feature.geometry()
#     #list_line = geom.asPolygon()
#     list_line = geom.asMultiPolygon()
#     print("new_object")
#     old_x,old_y=None,None
#     for line in list_line:
#         point_of_line=0
#         line_list=[]
#         line=line[0]
#         for point in line:         
#             # print(point)
#             # print("Point: x: ", point.x())
#             # print("       y: ", point.y())
#             # if old_x!=None:
#             #     print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))            
#             old_x,old_y=point.x(),point.y()
#             line_list.append([point.x(),point.y(),"Plg-"+str(object_chec)])
#             object_chec+=1
#     point_list+=ps.new_poligon(line_list)
# # for i in point_list:
# #   i.print_connect()
 
#/////////////////////////////////////// 

project = QgsProject.instance()
layer_name = "points_1"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
points=[]
for feature in features:
    geom = feature.geometry()
    point = geom.asPoint()
    #print("Point: x: ", point.x())
    #print("       y: ", point.y())
    points.append([point.x(),point.y(),"P-"+str(object_chec)])
    object_chec+=1
point_list+=ps.new_points(points)
# for i in point_list:
#   i.print_connect()
  
  #////////////////////////////////////////////////////
  
project = QgsProject.instance()
layer_name = "lines_1"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
for feature in features:
    geom = feature.geometry()
    #list_line = geom.asPolyline()
    list_line = geom.asMultiPolyline()
    print("new_object")
    old_x,old_y=None,None
    list_line=list_line[0]
    for point in list_line:
        point_of_line=0
        line_list=[]
        #print("Point: x: ", point.x())
        #print("       y: ", point.y())
        # if old_x!=None:
        #     print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))
        old_x,old_y=point.x(),point.y()
        line_list.append([point.x(),point.y(),"L-"+str(object_chec)])
        object_chec+=1
        point_list+=ps.new_line(line_list)
print(point_list)
#for i in point_list:
#  i.print_connect()

# persistent homology

import my_import.persistent_diagram as per_d
print(len(point_list))
per_d.diagram(point_list)

#for i in point_list:
#  i.print_connect()