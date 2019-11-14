import numpy as np
import scipy.spatial as sp
from PIL import Image
from scipy.spatial import Delaunay, ConvexHull
import glob, os


def in_hull(p, hull):
    """
    Test if points in `p` are in `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimensions
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the
    coordinates of `M` points in `K`dimensions for which Delaunay triangulation
    will be computed
    """

    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p) >= 0

def create(input_imgs_dir):
    for infile in glob.glob(input_imgs_dir + "*.JPG"):
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        width, height = im.size
        pixels_image = im.load()

        # Creation of a new image (mask)
        newImg1 = Image.new('RGB', (width, height))
        width -= 1
        height -= 1
        pixels1 = newImg1.load()

        # Reading points to create mask
        config = open(infile + ".txt", "r")
        lines = config.readlines()
        points = []
        for line in lines:
            if len(line) > 0:
                line = line.strip().split(" ")
                points.append((float(line[1]), float(line[2])))

        hull = sp.Delaunay(np.array(points))
        print(file, width, height)
        for i in range(0, width):
            if i == round(width / 4):
                print("25%")
            if i == round(width / 2):
                print("50%")
            if i == round(width / 2 + height / 4):
                print("75%")
            for j in range(0, height):
                if in_hull((i, j), hull):
                    pixels1[i, j] = pixels_image[i, j]
                else:
                    pixels1[i, j] = (0, 0, 0)

        print("saving.....")
        newImg1.save(infile + ".png")
#
#
create("../exampleData/venere/images/1/")
#
# im = Image.open("../exampleData/venere/images/1/IMG_0254.JPG")
# width, height = im.size
#
# pixels_image = im.load()
#
# newImg1 = Image.new('RGB', (width, height))
# width -= 1
# height -= 1
# pixels1 = newImg1.load()
#
# config = open("../exampleData/experiment/1IMG_0254.JPG.txt", "r")
# lines = config.readlines()
# points = []
# for line in lines:
#     if len(line) > 0:
#         line = line.strip().split(" ")
#         points.append((float(line[1]), float(line[2])))
#
# hull = sp.Delaunay(np.array(points))
# # hull = sp.ConvexHull(np.array(points))
# print(width, height)
# for i in range(0, width):
#     if i == round(width/4):
#         print("25%")
#     if i == round(width/2):
#         print("50%")
#     if i == round(width/2 + height/4):
#         print("75%")
#     for j in range(0, height):
#         if in_hull((i, j), hull):
#         # if magia(hull, float(i), float(j)):
#             pixels1[i, j] = pixels_image[i, j]
#         else:
#             pixels1[i, j] = (0, 0, 0)
#
# print("saving.....")
# newImg1.save("./img1.png")
#
# rgb_im = im.convert('RGB')
# r, g, b = rgb_im.getpixel((1, 1))
#
# print(r, g, b)
#
# print(hull.points)
