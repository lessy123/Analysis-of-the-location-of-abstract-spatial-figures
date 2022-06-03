# "layer" is a QgsVectorLayer instance
import my_import.point_search as ps
#import my_import.new_point as new_point
import my_import.persistent_diagram as per_d
import imp
imp.reload(ps)
imp.reload(per_d)
import numpy as np


layer_names=["layer1","layer2"]


project = QgsProject.instance()
point_list=[]
to_print = False



for layer_name in layer_names:
    """
    находит все точки полей на карте в соответствии с полем ввода layer_names
    """
    layer = project.mapLayersByName(layer_name)
    my_layer = layer[0]   
    features = my_layer.getFeatures()

    for feature in features:
        # retrieve every feature with its geometry and attributes
        if to_print:
            print("Feature ID: ", feature.id())
        # fetch geometry
        # show some information about the feature geometry
        geom = feature.geometry()
        object_chec=0
        geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
        if geom.type() == QgsWkbTypes.PointGeometry:
            # the geometry type can be of single or multi type
            if geomSingleType:
                x = geom.asPoint()
                points=[]
                points.append([x.x(),x.y(),"P-"+str(feature.id())+"_"+str(object_chec)])
                object_chec+=1
                point_list+=ps.new_points(points)
                if to_print:
                    print("Point: ", x)
            else:       #доработать
                x = geom.asMultiPoint()
                for point in x:
                    points=[]
                    points.append([point.x(),point.y(),"P-"+str(feature.id())+"_"+str(object_chec)])
                    object_chec+=1
                    point_list+=ps.new_points(points)
                if to_print:
                    print("MultiPoint: ", x)
        elif geom.type() == QgsWkbTypes.LineGeometry:
            if geomSingleType:  
                x = geom.asPolyline()   
                line_list=[]
                for point in x:
                    point_of_line=0
                    line_list.append([point.x(),point.y(),"MPL-"+str(feature.id())+"_"+str(object_chec)])
                    object_chec+=1
                point_list+=ps.new_poligon(line_list)
                if to_print:
                    print("Line: ", x, "length: ", geom.length())
            else:
                x = geom.asMultiPolyline()
                old_x,old_y=None,None
                for line in x:
                    point_of_line=0
                    line_list=[]
                    for point in line:                  
                        old_x,old_y=point.x(),point.y()
                        line_list.append([point.x(),point.y(),"MPL-"+str(feature.id())+"_"+str(object_chec)])
                        object_chec+=1
                point_list+=ps.new_poligon(line_list)
                if to_print:
                    print("MultiLine: ", x, "length: ", geom.length())
        elif geom.type() == QgsWkbTypes.PolygonGeometry:
            if geomSingleType:  #доработать
                x = geom.asPolygon()                
                if to_print:
                    print("new_object")
                for line in x:                           
                    old_x,old_y=None,None
                    point_of_line=0
                    line_list=[]
                    for point in line:    
                            old_x,old_y=point.x(),point.y()
                            line_list.append([point.x(),point.y(),"MPlg-"+str(feature.id())+"_"+str(object_chec)])
                            object_chec+=1
                            if to_print:
                                print(point)
                                print("Point: x: ", point.x())
                                print("       y: ", point.y())
                    point_list+=ps.new_poligon(line_list)
                if to_print:
                    print("Polygon: ", x, "Area: ", geom.area())
            else:
                x = geom.asMultiPolygon()
                if to_print:
                    print("new_object")
                old_x,old_y=None,None
                for line in x:
                    point_of_line=0
                    line_list=[]
                    line=line[0]
                    for point in line:         
                        if to_print:
                            print(point)
                            print("Point: x: ", point.x())
                            print("       y: ", point.y())
                        # if old_x!=None:
                        #     print("line length:",((point.x()-old_x)**2+(point.y()-old_y)**2)**(0.5))            
                        old_x,old_y=point.x(),point.y()
                        line_list.append([point.x(),point.y(),"MPlg-"+str(feature.id())+"_"+str(object_chec)])
                        object_chec+=1
                point_list+=ps.new_poligon(line_list)
                if to_print:
                    print("MultiPolygon: ", x, "Area: ", geom.area())
        else:
            if to_print:
                print("Unknown or invalid geometry")
        # fetch attributes
        attrs = feature.attributes()
        # attrs is a list. It contains all the attribute values of this feature
        if to_print:
            print(attrs)
        # for this test only print the first feature
        #break
        # need to update!!!1]



