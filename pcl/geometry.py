import numpy as np


class Vector3D:
    """Common base class for all Vector3"""
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    """Len is the length of the vector"""

    def length(self):
        return float(np.sqrt(self.x * self.x + self.y * self.y + self.z * self.z))

    def squaredLength(self):
        return float(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.length()
        return Vector3D(self.x / length, self.y / length, self.z / length)

    def invert(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def add(self, b):
        return Vector3D(self.x + b.x, self.y + b.y, self.z + b.z)

    def sub(self, b):
        return Vector3D(self.x - b.x, self.y - b.y, self.z - b.z)

    def mul(self, b):
        return Vector3D(self.x * b, self.y * b, self.z * b)


class BoundingBox:
    """Common base class for all Vector3"""
    Max = Vector3D(0, 0, 0)
    Min = Vector3D(0, 0, 0)

    def __init__(self):
        self.Max = Vector3D(np.float128(3.402823466e+38), np.float128(3.402823466e+38), np.float128(3.402823466e+38))
        self.Min = Vector3D(np.float128(-3.402823466e+38), np.float128(-3.402823466e+38), np.float128(-3.402823466e+38))

    def reset(self):
        self.Max = Vector3D(np.float128(3.402823466e+38), np.float128(3.402823466e+38), np.float128(3.402823466e+38))
        self.Min = Vector3D(np.float128(-3.402823466e+38), np.float128(-3.402823466e+38), np.float128(-3.402823466e+38))

    def setFromCoord(self, minvector, maxvector):
        self.Max = maxvector
        self.Min = minvector

    """ Center of the Box """

    def center(self):
        return self.Max.add(self.Min).mul(0.5)

    """ Gives the bbox dimensions """

    def size(self):
        return self.Max.sub(self.Min)

    """ Returns the halfed max size component """

    def extent(self):
        return np.max(self.size().x, np.max(self.size().y, self.size().z))

    def extendTo(self, pos):
        self.Min.x = np.min([self.Min.x, pos.x])
        self.Min.y = np.min([self.Min.y, pos.y])
        self.Min.z = np.min([self.Min.z, pos.z])
        self.Max.x = np.min([self.Max.x, pos.x])
        self.Max.y = np.min([self.Max.y, pos.y])
        self.Max.z = np.min([self.Max.z, pos.z])

    def contains(self, point):
        if self.Min.x <= point.x <= self.Max.x and point.y >= self.Min.y and point.y <= self.Max.y and self.Min.z <= point.z <= self.Max.z:
            return True
        else:
            return False


class Ray:
    """Common base class for all Vector3"""
    Origin = Vector3D(0, 0, 0)
    Direction = Vector3D(0, 0, 0)

    def __init__(self):
        self.Origin = Vector3D(0, 0, 0)
        self.Direction = Vector3D(0, 0, 0)

    def fromPoints(self, origin, direction):
        self.Origin = origin
        self.Direction = direction.sub(origin)
        self.Direction = self.Direction.normalize()

    """ Intersection """

    def intersects(self, bbox):
        epsilon = 0.000000001
        if self.Direction.x == 0:
            self.Direction.x = epsilon
        if self.Direction.y == 0:
            self.Direction.y = epsilon
        if self.Direction.z == 0:
            self.Direction.z = epsilon

        t1 = (bbox.Min.x - self.Origin.x) / self.Direction.x
        t2 = (bbox.Max.x - self.Origin.x) / self.Direction.x
        t3 = (bbox.Min.y - self.Origin.y) / self.Direction.y
        t4 = (bbox.Max.y - self.Origin.y) / self.Direction.y
        t5 = (bbox.Min.z - self.Origin.z) / self.Direction.z
        t6 = (bbox.Max.z - self.Origin.z) / self.Direction.z

        ## Magically compute something
        tmin = np.max([np.max([np.min([t1, t2]), np.min([t3, t4])]), np.min([t5, t6])])
        tmax = np.min([np.min([np.max([t1, t2]), np.max([t3, t4])]), np.max([t5, t6])])

        if tmax < 0 or tmax < tmin:
            return False

        return True


# ori = Vector3D(589827.799, 231380.010, 743.905)
# cen = Vector3D(589661.930, 231374.010, 749.620)
# size = Vector3D(178.040, 159.140, 70.000)
# bbox = BoundingBox()
#
# a_top_left = Vector3D(cen.x - (size.x / 2), cen.y + (size.y / 2), cen.z + (size.z / 2))
# a_bottom_left = Vector3D(cen.x - (size.x / 2), cen.y + (size.y / 2), cen.z - (size.z / 2))
#
# b_top_right = Vector3D(cen.x + (size.x / 2), cen.y + (size.y / 2), cen.z + (size.z / 2))
# b_bottom_right = Vector3D(cen.x + (size.x / 2), cen.y + (size.y / 2), cen.z - (size.z / 2))
#
# c_top_left = Vector3D(cen.x - (size.x / 2), cen.y - (size.y / 2), cen.z + (size.z / 2))
# c_bottom_left = Vector3D(cen.x - (size.x / 2), cen.y - (size.y / 2), cen.z - (size.z / 2))
#
# d_top_right = Vector3D(cen.x + (size.x / 2), cen.y - (size.y / 2), cen.z + (size.z / 2))
# d_bottom_right = Vector3D(cen.x + (size.x / 2), cen.y - (size.y / 2), cen.z - (size.z / 2))
#
# bbox.extendTo(a_top_left)
# bbox.extendTo(a_bottom_left)
# bbox.extendTo(b_top_right)
# bbox.extendTo(b_bottom_right)
# bbox.extendTo(c_top_left)
# bbox.extendTo(c_bottom_left)
# bbox.extendTo(d_top_right)
# bbox.extendTo(d_bottom_right)
#
# # test_a = Vector3D(589788.350, 231300.030, 710.365)
# # test_b = Vector3D(589965.959, 231453.290, 760.795)
#
# test_a = Vector3D(-1.247, -1.520, -1.656)
# test_b = Vector3D(-0.102, 1.394, -.0423)
#
#
# # cen = Vector3D(1, 2, 1.5)
# ori = Vector3D(1.874, 1.181, -9.677)
# bbox.setFromCoord(test_a, test_b)
# centerbbox = bbox.center()
# # bbox.setFromCoord(d_top_right, a_bottom_left)
# # b_bottom_right, c_top_left
# print(c_top_left.x, c_top_left.y, c_top_left.z)
#
# a = Ray()
# a.fromPoints(ori, bbox.center())
# print(a.intersects(bbox), bbox.contains(ori), bbox.center().z, a.Direction.x)
