import numpy as np


def quattomatrix(x, y, z, w):
    """
    Transformation from quaternion to Matrix 4x4

    Parameters:
    x, y, z, w (float): Quaternion

    Returns:
    numpy array: matrix 4x4

    """
    destination = np.zeros((4, 1, 4))

    destination[0][0] = 1.0 - 2.0 * y * y - 2.0 * z * z
    destination[0][1] = 2.0 * x * y + 2.0 * z * w
    destination[0][2] = 2.0 * x * z - 2.0 * y * w
    destination[0][3] = 0.0

    destination[1][0] = 2.0 * x * y - 2.0 * z * w
    destination[1][1] = 1.0 - 2.0 * x * x - 2.0 * z * z
    destination[1][2] = 2.0 * z * y + 2.0 * x * w
    destination[1][3] = 0.0

    destination[2][0] = 2.0 * x * z + 2.0 * y * w
    destination[2][1] = 2.0 * z * y - 2.0 * x * w
    destination[2][2] = 1.0 - 2.0 * x * x - 2.0 * y * y
    destination[2][3] = 0.0

    destination[3][0] = 0.0
    destination[3][1] = 0.0
    destination[3][2] = 0.0
    destination[3][3] = 1.0

    return destination


def worldtoimage(point, flenght, center, imgsize, rotmatrix, distortion=False):
    if distortion is True:
        width = imgsize[0]
        height = imgsize[1]
        matrix = rotmatrix

        tmp_0 = (matrix[0][0] * (point[0] - center[0]) + matrix[0][1] * (point[1] - center[1])
               + matrix[0][2] * (point[2] - center[2]))
        tmp_1 = (matrix[2][0] * (point[0] - center[0]) + matrix[2][1] * (point[1] - center[1])
               + matrix[2][2] * (point[2] - center[2]))
        sensorX = -flenght * tmp_0 / tmp_1

        tmp_0 = (matrix[1][0] * (point[0] - center[0]) + matrix[1][1] * (point[1] - center[1])
                 + matrix[1][2] * (point[2] - center[2]))
        tmp_1 = (matrix[2][0] * (point[0] - center[0]) + matrix[2][1] * (point[1] - center[1])
                 + matrix[2][2] * (point[2] - center[2]))

        sensorY = -flenght * tmp_0 / tmp_1

        return [sensorX, sensorY]


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

    def distance(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z

        return float(np.sqrt(dx * dx + dy * dy + dz * dz))

    def squaredDistance(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z

        return float(dx * dx + dy * dy + dz * dz)

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
