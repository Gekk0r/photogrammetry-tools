import glob
import os

from liblas import file
from liblas import header
from liblas import point


def setClassification(f, path, class_id):
    file_a = open(path, "r")
    for line in file_a:
        tmp = line.split(" ")
        if "comment" in tmp:
            continue
        else:
            if len(tmp) > 5:
                pt = point.Point()
                c = pt.color
                pt.x, pt.y, pt.z = (float(tmp[0]) * 100000, float(tmp[1]) * 100000, float(tmp[2]) * 100000)
                c.red, c.green, c.blue = (int(tmp[3]), int(tmp[4]), int(tmp[5]))
                pt.color = c

                # if tmp[3:6] == ["204", "153", "0"]:
                #     pt.classification = 2
                pt.classification = class_id

                f.write(pt)


def read_header_from_las(path):
    f = file.File(path, mode='r')
    h = f.header
    print(h.major_version, h.minor_version, h.dataformat_id, h.point_records_count)


# Initialize las file and read all ply inside a path folder
def initialize_las(path):
    h = header.Header()
    h.dataformat_id = 3
    h.major_version = 1
    h.minor_version = 3
    h.scale = [0.00001, 0.00001, 0.00001]
    f = file.File('pointcloud_classified.las', mode="w", header=h)

    # Classification by name of pcl in input
    for filename in glob.glob(os.path.join(path, '*.ply')):
        print(filename)
        name = filename.split("/")[-1]
        name = name.split(".")[0]
        pathfile = filename

        if name == "rgb":
            setClassification(f, pathfile, 1)
        if name == "ground":
            setClassification(f, pathfile, 2)
        if name == "vegetation":
            setClassification(f, pathfile, 3)
        if name == "road":
            setClassification(f, pathfile, 4)
        if name == "cables":
            setClassification(f, pathfile, 5)
        if name == "building":
            setClassification(f, pathfile, 6)
        if name == "poles":
            setClassification(f, pathfile, 7)
        if name == "anomalies":
            setClassification(f, pathfile, 8)

# Example
# initialize_las("classi")
