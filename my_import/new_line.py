def draw_line(name,project,x0=1723,y0=-1456,x1=1223,y1=-956,layer_name="persistent_lines"):
    layer = project.mapLayersByName(layer_name)[0]
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.AddFeatures:
        print(layer.fields())
        feat = QgsFeature(layer.fields())
        feat.setAttribute(0, name)
        feat.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(x0, y0),
        QgsPointXY(x1, y1)]))
        (res, outFeats) = layer.dataProvider().addFeatures([feat])
if __name__=="__main__" or __name__=="__console__":
    project = QgsProject.instance()
    draw_line(0,project)