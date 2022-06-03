import my_import.point_search as ps
# print(123)
project = QgsProject.instance()
layer_name = "points"
list_layers = project.mapLayersByName(layer_name)
my_layer = list_layers[0]
features = my_layer.getFeatures()
object_chec=0
point_list=[]
points=[]
for feature in features:
    geom = feature.geometry()
    #multi linestring
    point = geom.asPoint()
    print("Point: x: ", point.x())
    print("       y: ", point.y())
    points.append([point.x(),point.y(),"P-"+str(object_chec)])
    object_chec+=1
point_list+=ps.new_points(points)

for i in point_list:
  i.print_connect()





    