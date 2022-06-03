# "layer" is a QgsVectorLayer instance
import my_import.point_search as ps
#import my_import.new_point as new_point
import my_import.persistent_diagram as per_d
import imp
imp.reload(ps)
imp.reload(per_d)
import numpy as np
#imp.reload(new_point)
layer_names=["кладбище 1","кладбище 2","кладбище 3"]
#layer_names=["barrier_l_copy"]
count_object= int(1)

delet = False


if count_object!=1:
    count_object-=1

def delet_lines_and_points(text=["persistent_lines","persistent_points"]):
    """
    Удаляет все элементы слоя 
    text - список слоев, из которого удаляется элемент
    """
    
    for i in text:
        layer = project.mapLayersByName(i)[0]
        caps = layer.dataProvider().capabilities()
        features = layer.getFeatures()
        for feature in features:
                attrs = feature.attributes()
                for i in attrs:
                    if caps & QgsVectorDataProvider.DeleteFeatures:
                        res = layer.dataProvider().deleteFeatures([0])
                        
    # layer.selectAll()
def draw_points(point_list,name_point=False,layer_name="persistent_points"):
    """_summary_

    Args:
        point_list ([Note],...): Список точек
        name_point (bool, optional): Чек поинт, будет ли использоваться групповое имя
        или каждой точке дадут новое
    """
    if name_point:
        for i in point_list:
            if to_print:
                i.print_connect()
            draw_point(point_check,project,i.point.x,i.point.y,layer_name=layer_name)
    else:
        point_check=0
        for i in point_list:
            if to_print:
                i.print_connect()
            draw_point(point_check,project,i.point.x,i.point.y,layer_name=layer_name)
            point_check+=1
def draw_point(name,project,x=1723,y=-1456,layer_name="persistent_points"):
    """Рисует точки

    Args:
        name (_type_): первый атрибут - id объекта
        project (_type_): _description_
        x (int, optional): х-координата. Defaults to 1723.
        y (int, optional): y-координата. Defaults to -1456.
        layer_name (str, optional): Название поля, в которое вносится изменение. Defaults to "persistent_points".
    """
    layer = project.mapLayersByName(layer_name)[0]
    caps = layer.dataProvider().capabilities()

    if caps & QgsVectorDataProvider.AddFeatures:
        feat = QgsFeature(layer.fields())
        #feat.setAttributes([0, 'hello'])
        # Or set a single attribute by key or by index:
        #feat.setAttribute('name', 'hello')
        feat.setAttribute(0, name)
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x, y)))
        (res, outFeats) = layer.dataProvider().addFeatures([feat])    
def draw_line(name,project,x0=1723,y0=-1456,x1=1223,y1=-956,layer_name="persistent_lines"):
    """_summary_

    Args:
        name ("str"): id - объекта, является атрибутом
        project (_type_): _description_
        x0 (int, optional): x-координата первого объекта. Defaults to 1723.
        y0 (int, optional): у-координата первого объекта. Defaults to -1456.
        x1 (int, optional): x-координата второго объекта. Defaults to 1223.
        y1 (int, optional): у-координата второго объекта. Defaults to -956.
        layer_name (str, optional): поле, в которое заносятся данные. Defaults to "persistent_lines".
    """
    layer = project.mapLayersByName(layer_name)[0]
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.AddFeatures:
        #print(layer.fields())
        feat = QgsFeature(layer.fields())
        feat.setAttribute(0, name)
        feat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(x0, y0),
        QgsPointXY(x1, y1)]))
        (res, outFeats) = layer.dataProvider().addFeatures([feat])
def connect_by_treshold(point_list,treshold=0):
    """Связывание точек по трешхолду

    Args:
        point_list ([Note,...]): Список точек
        treshold (int, optional): трешхолд. Defaults to 0.
    """
    print("start draw_lines")
    new_points=np.copy(point_list)
    while len(new_points):
        point=new_points[0]
        new_points=new_points[1:]
        for i in range(len(new_points)):
            if point.whether_connected(new_points[i]):
                continue
            elif ((point.point.x - new_points[i].point.x)**2+
                  (point.point.y - new_points[i].point.y)**2)**0.5<=treshold: 
                point.new_connection(new_points[i])               
def rename_group_of_points_lines(points):
    """Переименование группы

    Args:
        points ([Note]): список точек
    """
    name=1
    for i in points:
        if i.rename(name):
            name+=1
def draw_lines_by_treshold(points,threshold=500,layer_name="persistent_lines"):
    """Рисует все линии, которые соответствуют трешхолду

    Args:
        points ([Note],...): список точек
        threshold (int, optional): ограничение связи. Defaults to 500.
        layer_name (str, optional): имя записывающего слоя. Defaults to "persistent_lines".
    """
    print("start draw_lines")
    new_points=np.copy(points)
    check=0
    while len(new_points):
        point=new_points[0]
        new_points=new_points[1:]
        for i in range(len(new_points)):          
            if point.whether_connected(new_points[i]):
                draw_line(name=check,project=project,x0=point.point.x,                
                          y0=point.point.y,x1=new_points[i].point.x,y1=new_points[i].point.y,layer_name=layer_name)
            elif ((point.point.x - new_points[i].point.x)**2+
                    (point.point.y - new_points[i].point.y)**2)**0.5<=threshold: 
                # def draw_line(name,project,x0=1723,y0=-1456,x1=1223,y1=-956,layer_name="persistent_lines"):

                draw_line(name=check,project=project,x0=point.point.x,                
                          y0=point.point.y,x1=new_points[i].point.x,y1=new_points[i].point.y,layer_name=layer_name)
            check+=1
def draw_lines(points,layer_name="persistent_lines"):
    """Рисует все линии

    Args:
        points ([Note],...): список точек
        threshold (int, optional): ограничение связи. Defaults to 500.
        layer_name (str, optional): имя записывающего слоя. Defaults to "persistent_lines".
    """
    print("start draw_lines")
    new_points=np.copy(points)
    x=-1
    while len(new_points):
        x+=1
        point=new_points[0]
        new_points=new_points[1:]
        y=x        
        for i in range(len(new_points)):
            y+=1         
            if point.whether_connected(new_points[i]):
                draw_line(name=point.name_grup,project=project,x0=point.point.x,                
                          y0=point.point.y,x1=new_points[i].point.x,y1=new_points[i].point.y,layer_name=layer_name)

#layer_names=["poligon_1",
#            "points_1",
#            "lines_1"]
            



project = QgsProject.instance()
point_list=[]
to_print=False

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
                point_list+=ps.new_line(line_list)
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
                point_list+=ps.new_line(line_list)
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
        # need to update!!!
        
print("Удаляются результаты прошлого опыта")
delet_lines_and_points()
#draw_points(point_list,layer_name="points")

print("Расчет персистентной диаграммы")
diagram = per_d.diagram(point_list)[0]
diagram_per=diagram[diagram[:,2]==0]
"""
print(diagram_per)
print(diagram_per[count_object])
print(diagram_per[len(diagram_per)-count_object])
print(diagram_per[len(diagram_per)-count_object][1])
print()
"""
porog=0


if len(diagram_per)<count_object:
    print("Ошибка, количество объектов ")
    count_object= len(diagram_per)+1
print(len(diagram_per),count_object)
if count_object==len(diagram_per)+1:
    porog=diagram_per[0][1] - 0.00001 * diagram_per[0][1]
elif count_object!=1:
    porog=diagram_per[len(diagram_per)-count_object][1] - 0.00000001 * diagram_per[len(diagram_per)-count_object][1]
else: porog=diagram_per[len(diagram_per)-count_object][1] + 0.1 * diagram_per[len(diagram_per)-count_object][1]
print("porog",porog)
connect_by_treshold(point_list,porog)
rename_group_of_points_lines(point_list)
draw_points(point_list)
draw_lines(point_list)


delet = True
myresult=processing.run("native:dissolve", { 'FIELD' : ['id'], 'INPUT' : QgsProcessingFeatureSourceDefinition('C:/Users/Ne_ma/Documents/persistent_lines.shp', selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT' : 'TEMPORARY_OUTPUT' })

QgsProject.instance().addMapLayer(myresult['OUTPUT'])
layer = myresult['OUTPUT']
# QgsProject.instance().addMapLayer(myresult['OUTPUT'])
list_of_poligons=[]

for i in range(0,layer.featureCount()+1):
        # layer.selectByExpression(f"""ID='{i}'""")
        # layer.selectByExpression([i])
        layer.select(i)

        poligon=processing.run("native:polygonize", {
                'INPUT' : QgsProcessingFeatureSourceDefinition(
                        layer.source(), 
                        selectedFeaturesOnly=True, 
                        featureLimit=-1, 
                        #flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature, 
                        geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 
                'KEEP_FIELDS' : True, 'OUTPUT' : 'TEMPORARY_OUTPUT' }) 
        QgsProject.instance().addMapLayer(poligon['OUTPUT'])

        for j in range(1,poligon['OUTPUT'].featureCount()+1):
                poligon['OUTPUT'].dataProvider().changeAttributeValues({ j :  { 0 : i } })
                # poligon['OUTPUT'].attributeValueChanged(j,0,i)
        list_of_poligons.append(processing.run("native:dissolve", {'INPUT':poligon['OUTPUT'].source(),
                                        'FIELD':[],
                                        'OUTPUT':'TEMPORARY_OUTPUT'}))
        if delet:
            QgsProject.instance().removeMapLayer( poligon['OUTPUT'].id() )
            
        layer.removeSelection()

# QgsProject.instance().removeMapLayer(myresult['OUTPUT'].id() )

list_layers = []
re_list=[]
for i in list_of_poligons:
        for j in range(1,i['OUTPUT'].featureCount()+1):
                i['OUTPUT'].dataProvider().changeAttributeValues({ j :  { 0 : i } })
        QgsProject.instance().addMapLayer(i['OUTPUT'])
        list_layers.append(i['OUTPUT'].source())
        re_list.append(i['OUTPUT'].id())
        
basket=[]
check = 0
for i in range(len(list_of_poligons)):    
        for j in range(i+1,len(list_of_poligons)):
                intersection = processing.run("native:intersection", {
                        'INPUT':list_of_poligons[i]['OUTPUT'].source(),
                        'OVERLAY':list_of_poligons[j]['OUTPUT'].source(),
                        'INPUT_FIELDS':[],
                        'OVERLAY_FIELDS':[],
                        'OVERLAY_FIELDS_PREFIX':'',
                        'OUTPUT':'TEMPORARY_OUTPUT'})
                if intersection['OUTPUT'].featureCount():
                        QgsProject.instance().addMapLayer(intersection['OUTPUT'])
                        basket.append(intersection['OUTPUT'].id())
                        mat_intersection = processing.run("qgis:exportaddgeometrycolumns", {
                                'INPUT':intersection['OUTPUT'].source(),
                                'CALC_METHOD':0,
                                'OUTPUT':'TEMPORARY_OUTPUT'})
                        mat_layer1 = processing.run("qgis:exportaddgeometrycolumns", {
                                'INPUT':list_of_poligons[i]['OUTPUT'].source(),
                                'CALC_METHOD':0,
                                'OUTPUT':'TEMPORARY_OUTPUT'})
                        mat_layer2 = processing.run("qgis:exportaddgeometrycolumns", {
                                'INPUT':list_of_poligons[j]['OUTPUT'].source(),
                                'CALC_METHOD':0,
                                'OUTPUT':'TEMPORARY_OUTPUT'})
                        area1,area2,area0 = 0,0,0
                        iter = mat_intersection['OUTPUT'].getFeatures()                                
                        for feature in iter: area0=feature['area']
                        iter = mat_layer1['OUTPUT'].getFeatures()                                
                        for feature in iter: area1=feature['area']
                        iter = mat_layer2['OUTPUT'].getFeatures()                                
                        for feature in iter: area2=feature['area']
                        if area0<area1 and area0<area2:
                                check+=1
                                print(f"""Объекты {i+1} и {j+1} пересекаются""")
                        elif area1==area0:
                                print(f"""Объект {i+1} входит в объект {j+1}""")
                                check+=1
                        elif area2==area0:
                                print(f"""Объект {j+1} входит в объект {i+1}""")
                                check+=1
                       

if check==0:
    print(f"""Объекты не зависят друг от друга""")            
        
        
        
itog_layer=processing.run("native:mergevectorlayers", {'LAYERS':list_layers,
                                            'CRS':None,
                                            'OUTPUT':'TEMPORARY_OUTPUT'})

if delet:
    for i in re_list:
            QgsProject.instance().removeMapLayer(i)
    for i in basket:
            QgsProject.instance().removeMapLayer(i)

QgsProject.instance().addMapLayer(itog_layer['OUTPUT'])