from sre_constants import FAILURE
from qgis import processing

import processing
# parameter_dictionary= 
# myresult=processing.run("native:dissolve", {'FIELD' : ['id'], 
#     'INPUT' : QgsProcessingFeatureSourceDefinition('C:/Users/Ne_ma/Documents/persistent_lines.shp', 
#         selectedFeaturesOnly=False, featureLimit=-1,
#         flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
#         geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 
#     'OUTPUT' : 'D:/Programm/Qgis/bin/my_import/experiments/group_lines.gpkg'})

#myresult=processing.run("native:dissolve", { 'FIELD' : ['id'], 'INPUT' : QgsProcessingFeatureSourceDefinition('C:/Users/Ne_ma/Documents/persistent_lines.shp', selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT' : 'ogr:dbname=\'D:/Programm/Qgis/bin/my_import/experiments/group_lines.gpkg\' table=\"dissolved\" (geom)' })
myresult=processing.run("native:dissolve", { 'FIELD' : ['id'], 'INPUT' : QgsProcessingFeatureSourceDefinition('C:/Users/Ne_ma/Documents/persistent_lines.shp', selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid), 'OUTPUT' : 'TEMPORARY_OUTPUT' })
layer = myresult['OUTPUT']
#print(myresult)
#print()
#print(layer.source())
QgsProject.instance().addMapLayer(myresult['OUTPUT'])
list_of_poligons=[]
delet=False
for i in range(1,layer.featureCount()+1):
        layer.selectByExpression(f"""ID='{i}'""")
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
        if delet: QgsProject.instance().removeMapLayer( poligon['OUTPUT'].id() )
# QgsProject.instance().removeMapLayer(myresult['OUTPUT'].id() )

#     list_of_poligons.append(processing.run("native:joinattributesbylocation", {'INPUT':poligon['OUTPUT'],'JOIN':layer.source(),'PREDICATE':[0],'JOIN_FIELDS':[],'METHOD':0,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT'}))
list_layers = []
re_list=[]
for i in list_of_poligons:
        for j in range(1,i['OUTPUT'].featureCount()+1):
                i['OUTPUT'].dataProvider().changeAttributeValues({ j :  { 0 : i } })
        QgsProject.instance().addMapLayer(i['OUTPUT'])
        list_layers.append(i['OUTPUT'].source())
        re_list.append(i['OUTPUT'].id())
# processing.run("qgis:exportaddgeometrycolumns", {'INPUT':'memory://MultiPolygon?crs=EPSG:4326&field=id:long(10,0)&field=layer:string(0,0)&field=path:string(0,0)&uid={0927923e-fa8d-4695-9986-343f00b7e703}','CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})        
        
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
                                print(f"""Объекты {i+1} входит в объект {j+1}""")
                                check+=1
                        elif area2==area0:
                                print(f"""Объекты {j+1} входит в объект {i+1}""")
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

# QgsProject.instance().addMapLayer(list_of_poligons['OUTPUT'])


if False:        
        #{ 'INPUT' : 'memory://MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={b1a4add2-88f7-4fb1-a80e-b548be94aad4}', 'KEEP_FIELDS' : False, 'OUTPUT' : 'TEMPORARY_OUTPUT' }
        print(list_of_poligons)
        QgsProject.instance().addMapLayer(list_of_poligons['OUTPUT'])
        new_poligons=processing.run("native:joinattributesbylocation", {'INPUT':list_of_poligons['OUTPUT'],'JOIN':layer.source(),'PREDICATE':[0],'JOIN_FIELDS':[],'METHOD':0,'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT'})
        print(new_poligons)
        QgsProject.instance().addMapLayer(new_poligons['OUTPUT'])
        myresult=processing.run("native:dissolve", { 'FIELD' : ['id_2'], 'INPUT' : new_poligons['OUTPUT'], 'OUTPUT' : 'TEMPORARY_OUTPUT' })
        QgsProject.instance().addMapLayer(myresult['OUTPUT'])

# print(list_of_poligons[0])
# QgsProject.instance().addMapLayer(list_of_poligons['OUTPUT'])
#processing.run("qgis:linestopolygons", {'INPUT':'memory://MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={9a78892f-95b0-48fd-8483-f54cfd564dfd}','OUTPUT':'TEMPORARY_OUTPUT'})
# myresult=processing.run("qgis:linestopolygons", {'INPUT':'memory://'+layer.source(),'OUTPUT':'TEMPORARY_OUTPUT'})
# print(myresult)
# print(myresult['OUTPUT'])
# QgsProject.instance().addMapLayer(myresult['OUTPUT'])

# myresult2=processing.run("native:dissolve", { 
#         'FIELD' : [], 
#         'INPUT' :  list_of_poligons['OUTPUT'].source(),
#         'OUTPUT' : 'TEMPORARY_OUTPUT' })
# QgsProject.instance().addMapLayer(myresult2['OUTPUT'])

"""  { 
        'INPUT' : QgsProcessingFeatureSourceDefinition(
                'MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={b1ba4e47-3b24-4baf-95d2-642f0345ad47}', 
                selectedFeaturesOnly=False, 
                featureLimit=-1, 
                flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature, 
                geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 
        'KEEP_FIELDS' : True, 
        'OUTPUT' : 'TEMPORARY_OUTPUT' }


{ 
        'INPUT' : QgsProcessingFeatureSourceDefinition(
                'MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={e85f74e7-3ecc-40b5-a600-1014409c60fb}', 
                selectedFeaturesOnly=True, 
                featureLimit=-1, 
                geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 
        'KEEP_FIELDS' : True, 
        'OUTPUT' : 'TEMPORARY_OUTPUT' }
"""

"""
{ 
'INPUT' : 
        'memory://MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={94729dd1-9287-4611-bb39-e5d261aad225}',
'KEEP_FIELDS' : True,
'OUTPUT' : 'TEMPORARY_OUTPUT' 
}


{ 'INPUT' : 
QgsProcessingFeatureSourceDefinition('MultiLineString?crs=EPSG:4326&field=id:long(10,0)&uid={94729dd1-9287-4611-bb39-e5d261aad225}', 
selectedFeaturesOnly=False, 
featureLimit=-1, 
flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature, 
geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid), 'KEEP_FIELDS' : True, 'OUTPUT' : 'TEMPORARY_OUTPUT' }




"""



# print(list_of_poligons)
# print(list_of_poligons['OUTPUT'])





"""
Запуск алгоритма 'Построить полигоны'…
Входные параметры:

"""
    

#data = iface.addVectorLayer(myresult['OUTPUT'],"layer name you like", "ogr")

#(res, outFeats) = layer.dataProvider()
if False:
    for alg in QgsApplication.processingRegistry().algorithms():
            print(alg.id(), "->", alg.displayName())

    QgsProcessingFeatureSourceDefinition(
        'C:/Users/Ne_ma/Documents/persistent_lines.shp', 
        selectedFeaturesOnly=False, featureLimit=-1, 
        flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, 
        geometryCheck=QgsFeatureRequest.GeometrySkipInvalid)