
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