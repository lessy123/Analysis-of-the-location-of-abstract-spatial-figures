import numpy as np
from scipy.sparse import coo_matrix
from gtda.homology import VietorisRipsPersistence
import my_import.point_search as ps
#import point_search as ps

to_print=False


def diagram(points):   
    print("start persistent diagram")
    new_points=np.copy(points)
    row  = []
    col  = []
    data = []
    x=-1
    while len(new_points):
        x+=1
        point=new_points[0]
        new_points=new_points[1:]
        y=x        
        for i in range(len(new_points)):
            y+=1
            row.append(x)
            col.append(y)            
            if point.whether_connected(new_points[i]):
                data.append(0)
            else: 
                data.append(
                    ((point.point.x - new_points[i].point.x)**2+
                    (point.point.y - new_points[i].point.y)**2)**0.5)
    coo = coo_matrix((data, (row, col)), shape=(len(points), len(points)))
    persistent_diogram=VietorisRipsPersistence(metric="precomputed").fit_transform_plot([coo])
    print(persistent_diogram)
    print("The end of creat persistent diagram")
    return persistent_diogram
    
def diagram_v2(points):   
    print("start persistent diagram v2")
    new_points=np.copy(points)
    row  = []
    col  = []
    data = []
    x=-1
    while len(new_points)-1>x:
        x+=1
        point=new_points[x]
        print(x,len(new_points))        
        for i in range(len(new_points)):
            if new_points[i]==point:
                continue
            row.append(x)
            col.append(i)
            if point.whether_connected(new_points[i]):
                data.append(0)
            else: 
                data.append(
                    ((point.point.x - new_points[i].point.x)**2+
                    (point.point.y - new_points[i].point.y)**2)**0.5)
                    #new_points[i,0]-point[0])**2+(new_points[i,1]-point[1])**2)**0.5)
    print(len(data),len(row),len(col),len(points),len(points)*len(points))
    coo = coo_matrix((data, (row, col)), shape=(len(points), len(points)))
    print(coo)

    persistent_diogram=VietorisRipsPersistence(metric="precomputed").fit_transform_plot([coo])
    print(persistent_diogram)
    print("The end of creat persistent diagram")
# object_1=[[1,2,"p-1"],
#               [1,4,"p-2"],
#               [5,2,"p-3"],
#               [7,2,"p-4"],
#               [9,9,"p-5"]]
# list_of_points=[]
# list_of_points+=new_points(object_1)
# row = [ps.new_point([1,2,"p-1"])]
# col = [ps.new_point([1,4,"p-2"])]
# data = [0]
# coo = coo_matrix((data, (row, col)), shape=(2, 2))