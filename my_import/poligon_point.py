import my_import.point_search as ps
# print(123)
project = QgsProject.instance()
layer_name = "poligon"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
point_list=[]
for feature in features:
    geom = feature.geometry()
    #multi linestring
    list_line = geom.asPolygon()

    print("new_object")
    #line=list_line[1]
    old_x,old_y=None,None
    for line in list_line:
        point_of_line=0
        line_list=[]
        for point in line:         
#            ps.new_lines(point.x(),point.y())
            print("Point: x: ", point.x())
            print("       y: ", point.y())
            if old_x!=None:
                print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))
            
            old_x,old_y=point.x(),point.y()
            line_list.append([point.x(),point.y(),"Plg-"+str(object_chec)])
            object_chec+=1
    point_list+=ps.new_poligon(line_list)
for i in point_list:
  i.print_connect()
