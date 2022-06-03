#layer = iface.activeLayer()
import my_import.point_search as ps


def draw_points(points):
    layer_name="persistent_points"
    layer = project.mapLayersByName(layer_name)[0]
    caps = layer.dataProvider().capabilities()

    if caps & QgsVectorDataProvider.AddFeatures:
        feat = QgsFeature(layer.fields())
        for i in range(len(points)):            
            feat.setAttribute(0, str(i))
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(points[i].point.x,points[i].point.y)))   
            (res, outFeats) = layer.dataProvider().addFeatures([feat])