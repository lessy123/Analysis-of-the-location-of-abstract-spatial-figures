#layer = iface.activeLayer()

def draw_point(name,project,x=1723,y=-1456,layer_name="persistent_points"):
    layer = project.mapLayersByName(layer_name)[0]
    caps = layer.dataProvider().capabilities()

    if caps & QgsVectorDataProvider.AddFeatures:
        feat = QgsFeature(layer.fields())
        #feat.setAttributes([0, 'hello'])
        # Or set a single attribute by key or by index:
        #feat.setAttribute('name', 'hello')
        feat.setAttribute(0, '1')
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(1723, -1456)))
        (res, outFeats) = layer.dataProvider().addFeatures([feat])
        

if __name__=="__main__" or __name__=="__console__":
    project = QgsProject.instance()
    draw_point(0,project)