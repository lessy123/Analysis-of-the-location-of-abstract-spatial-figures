


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
delet_lines_and_points
if caps & QgsVectorDataProvider.DeleteFeatures:
    res = layer.dataProvider().deleteFeatures([5, 10])