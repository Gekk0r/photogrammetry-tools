import numpy as np
import scipy.spatial as sp
from PIL import Image, ImageDraw
from scipy.spatial import Delaunay, ConvexHull
import glob, os
import skimage.draw as drw

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

        # Creation of a new image (mask)
        newImg1 = Image.new('RGB', (width, height))
        # width -= 1
        # height -= 1
        pixels1 = newImg1.load()

        # Reading points to create mask
        config = open(infile + ".txt", "r")
        lines = config.readlines()
        points = []
        for line in lines:
            if len(line) > 0:
                line = line.strip().split(" ")
                points.append((float(line[1]), float(line[2])))

        draw = True
        if len(points) > 3:
            hull = sp.ConvexHull(np.array(points))
        else:
            draw = False

        print(file, width, height)

        # pixels_image = im.load()
        # for i in range(0, width):
        #     if i == round(width / 4):
        #         print("25%")
        #     if i == round(width / 2):
        #         print("50%")
        #     if i == round(width / 2 + height / 4):
        #         print("75%")
        #     for j in range(0, height):
        #         if in_hull((i, j), hull):
        #             pixels1[i, j] = pixels_image[i, j]
        #         else:
        #             pixels1[i, j] = (0, 0, 0)
        # img_ = np.zeros((height, width), dtype=np.uint8)
        # points = np.array(points)
        # rr, cc = drw.polygon(points[0 : 4352 , :], points[:, 0: 3264])
        # img_[rr, cc] = 1
        #
        # mask = drw.polygon2mask((height, width), points)

        img = Image.new("RGB", (width, height), "#000000")
        img1 = ImageDraw.Draw(img)

        if(draw):
            arr_lst = (hull.points[hull.vertices])
            tup_lst = tuple(map(tuple, arr_lst))
            img1.polygon(tup_lst, fill="#eeeeff", outline="blue")

        # img.show()
        print("saving.....", infile + ".png")

        img.save(infile + ".png")


#
#
create("../exampleData/chigi/1/")
