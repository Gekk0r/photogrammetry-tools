from scipy.spatial import ConvexHull
import numpy as np

def pnt_in_pointcloud(points, new_pt):
    hull = ConvexHull(points)
    new_pts = points + new_pt
    new_hull = ConvexHull(new_pts)
    if hull == new_hull:
        return True
    else:
        return False

poly = [[0,0,0],[0,0.1,0],[0.1,0.1,-0.03],[0.1,0,-0.03]]
point = [0,1,2]

print(pnt_in_pointcloud(poly, point))