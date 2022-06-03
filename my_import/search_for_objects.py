import my_import.point_search as ps
import my_import.new_point 


def get_geometry_points(layer_name):
    #layer_name = "poligon"
    project = QgsProject.instance()
    list_layers = project.mapLayersByName(layer_name)
    my_layer = list_layers[0]
    features = my_layer.getFeatures()
    object_chec=0
    point_list=[]
    #for feature in features:
    # retrieve every feature with its geometry and attributes
    print("Feature ID: ", feature.id())
    line_list=[]#array storing points
    # fetch geometry
    # show some information about the feature geometry
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PointGeometry:
        # the geometry type can be of single or multi type
        if geomSingleType:
            x = geom.asPoint()
            print("Point: ", x)
        else:
            x = geom.asMultiPoint()
            print("MultiPoint: ", x)
    elif geom.type() == QgsWkbTypes.LineGeometry:
        if geomSingleType:
            x = geom.asPolyline()
            print("Line: ", x, "length: ", geom.length())
        else:
            x = geom.asMultiPolyline()
            print("MultiLine: ", x, "length: ", geom.length())
    elif geom.type() == QgsWkbTypes.PolygonGeometry:
        if geomSingleType:
            x = geom.asPolygon()
            print("Polygon: ", x, "Area: ", geom.area())
        else:
            x = geom.asMultiPolygon()
            print("MultiPolygon: ", x, "Area: ", geom.area())
    else:
        print("Unknown or invalid geometry")
    # fetch attributes
    attrs = feature.attributes()
    # attrs is a list. It contains all the attribute values of this feature
    print(attrs)




layer_name = "poligon"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
point_list=[]
for feature in features:
    geom = feature.geometry()
    #list_line = geom.asPolygon()
    list_line = geom.asMultiPolygon()
    print("new_object")
    old_x,old_y=None,None
    for line in list_line:
        point_of_line=0
        line_list=[]
        line=line[0]
        for point in line:         
            # print(point)
            # print("Point: x: ", point.x())
            # print("       y: ", point.y())
            # if old_x!=None:
            #     print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))            
            old_x,old_y=point.x(),point.y()
            line_list.append([point.x(),point.y(),"Plg-"+str(object_chec)])
            object_chec+=1
    point_list+=ps.new_poligon(line_list)
# for i in point_list:
#   i.print_connect()
 
#/////////////////////////////////////// 

project = QgsProject.instance()
layer_name = "points"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
points=[]
for feature in features:
    geom = feature.geometry()
    point = geom.asPoint()
    # print("Point: x: ", point.x())
    # print("       y: ", point.y())
    points.append([point.x(),point.y(),"P-"+str(object_chec)])
    object_chec+=1
point_list+=ps.new_points(points)
# for i in point_list:
#   i.print_connect()
  
  #////////////////////////////////////////////////////
  
project = QgsProject.instance()
layer_name = "wenera_3"
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
        # print("Point: x: ", point.x())
        # print("       y: ", point.y())
        # if old_x!=None:
        #     print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))
        old_x,old_y=point.x(),point.y()
        line_list.append([point.x(),point.y(),"L-"+str(object_chec)])
        object_chec+=1
        point_list+=ps.new_line(line_list)
print(point_list)
# for i in point_list:
#   i.print_connect()
#   new_point.draw_point(i.point.x,i.point.y)

# persistent homology



# import my_import.persistent_diagram as per_d
# import imp
# imp.reload(per_d)

# per_d.diagram(point_list)

#for i in point_list:
#  i.print_connect()