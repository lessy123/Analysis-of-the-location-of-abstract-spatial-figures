#layer = iface.activeLayer()
#text="persistent_points"
text=["persistent_lines","persistent_points"]

for i in text:
    layer = project.mapLayersByName(i)[0]

    caps = layer.dataProvider().capabilities()
    #features = layer.getFeatures()
    features = layer.getFeatures()
        #if True==False:
    for feature in features:
            attrs = feature.attributes()
            # attrs is a list. It contains all the attribute values of this feature
            #print(attrs)
            for i in attrs:
                if caps & QgsVectorDataProvider.DeleteFeatures:
                    #res = layer.dataProvider().deleteFeatures([5, 10])
                    res = layer.dataProvider().deleteFeatures([0])
    