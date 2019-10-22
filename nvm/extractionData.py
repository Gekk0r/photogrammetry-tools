import json
import math
import numpy as np
from scipy.spatial.distance import pdist

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--input_nvm", dest="input_nvm",
                    help="input nvm file", metavar="")
parser.add_argument("-o", "--output_folder", dest="output_folder",
                    help="output folder", metavar="")

args = parser.parse_args()

class DataNVM(object):

    def __init__(self, name, path, outpath=None, calculateInterAngle=True):

        self.cameraList = []
        self.data = dict()
        self.points = dict()
        self.pointsAllData = dict()
        self.dataAll = dict()
        self.points_img = dict() #TODO check
        self.pointAngle = dict()
        self.calculateInterAngle = calculateInterAngle

        self.name = name
        self.path = path
        self.outpath = outpath

        file = open(self.path, 'r')
        lines = file.readlines()

        self.num_img = int(lines[2])
        self.index_tie = int(self.num_img + 4)
        self.num_tie = int(lines[self.index_tie])

        if self.outpath is not None:
            out = open(self.outpath + "tiepoints.json", "w")
            json_data = {"num_tie": [self.num_tie]}
            data = json.dumps(json_data)
            out.write(data)

        self.extract(lines)

    def dotproduct(self, v1, v2):
        return sum((a * b) for a, b in zip(v1, v2))

    def length(self, v):
        return math.sqrt(self.dotproduct(v, v))

    def angle(self, v1, v2):
        elem = self.dotproduct(v1, v2) / (self.length(v1) * self.length(v2))
        if elem > 1.0:
            return math.acos(1)
        else:
            return math.acos(elem)

    def extract(self, lines):
        if self.outpath is not None:
            out = open(self.outpath + "chart_points_aggregation_tsv.tsv", "w")
            out.write("point_number" + "\t" + "number_images" + "\n")
            out_2 = open(self.outpath + "pcl_redundancy.txt", "w")

        for index in range(3, self.index_tie - 1):
            cameraTMP = lines[index].strip().split(" ")
            camera = {"name": cameraTMP[0].split("/")[-1], "focal_lenght": cameraTMP[1],
                      "quaternion": [float(cameraTMP[2]), float(cameraTMP[3]), float(cameraTMP[4]),
                                     float(cameraTMP[5])],
                      "cameraCenter": [float(cameraTMP[6]), float(cameraTMP[7]), float(cameraTMP[8])],
                      "radial": cameraTMP[9]}
            self.cameraList.append(camera)

        for index in range(self.index_tie + 1, len(lines) - 1):
            line = lines[index].strip().split(" ")
            self.pointsAllData[str(index - self.index_tie)] = {"id": str(index - self.index_tie),
                                                               "point3D": (line[0], line[1], line[2]),
                                                               "rgb": (line[3], line[4], line[5]), "num_imgs": line[6],
                                                               "list_images": [], "id_features":[]}
            if self.outpath is not None:
                out_2.write(line[0] + " " + line[1] + " " + line[2] + " " + line[6] + "\n")
                out.write(str(index - self.index_tie) + "\t" + line[6] + "\n")

            self.points[str(index - self.index_tie)] = [int(line[6])]

            if line[6] in self.points_img:
                self.points_img[line[6]][0] += 1
            else:
                self.points_img[line[6]] = [1]

            for tie in range(7, len(line), 4):
                self.pointsAllData[str(index - self.index_tie)]["list_images"].append(line[tie])
                name = self.extractName(int(line[tie]), lines)
                if name in self.data:
                    self.data[name][0] += 1
                else:
                    self.data[name] = [1]
                if line[tie] in self.dataAll:
                    self.dataAll[line[tie]]["id"].append(line[tie + 1])
                    self.dataAll[line[tie]]["point2D"].append((line[tie + 2], line[tie + 3]))
                else:
                    name = self.extractName(int(line[tie]), lines)
                    self.dataAll[line[tie]] = {"name": name, "id": [line[tie + 1]],
                                               "point2D": [(line[tie + 2], line[tie + 3])]}
                self.pointsAllData[str(index - self.index_tie)]["id_features"].append(line[tie + 1])

                if self.calculateInterAngle:
                    self.interAngle(self.pointsAllData[str(index - self.index_tie)]["id"],
                                    self.pointsAllData[str(index - self.index_tie)]["point3D"],
                                    self.pointsAllData[str(index - self.index_tie)]["list_images"])

        if self.outpath is not None:
            data = json.dumps(self.points)
            out = open(self.outpath + "chart_points_aggregation.json", "w")
            out.write(data)
            data = json.dumps(self.data)
            out = open(self.outpath + "chart_img_aggregation.json", "w")
            out.write(data)
            data = json.dumps(self.dataAll)
            out = open(self.outpath + "chart_img.json", "w")
            out.write(data)
            data = json.dumps(self.pointsAllData)
            out = open(self.outpath + "chart_points.json", "w")
            out.write(data)
            data = json.dumps(self.points_img)
            out = open(self.outpath + "points_img.json", "w")
            out.write(data)
            data = json.dumps(self.pointAngle)
            out = open(self.outpath + "chart_points_angle.json", "w")
            out.write(data)

        tmpCamList = dict()
        for camera in self.cameraList:
            tmpCamList[camera["name"]] = [camera["quaternion"], camera["cameraCenter"]];

        if self.outpath is not None:
            data = json.dumps(tmpCamList)
            out = open(self.outpath + "camere.json", "w")
            out.write(data)

    def extractName(self, id, lines):
        name = lines[3 + id].strip().split(" ")[0]
        name = name.split("/")[-1]
        return name

    def interAngle(self, name, pt, camList):
        vectors = []

        angle = []
        for cam in camList:
            vx = float(pt[0]) - float(self.cameraList[int(cam)]['cameraCenter'][0])
            vy = float(pt[1]) - float(self.cameraList[int(cam)]['cameraCenter'][1])
            vz = float(pt[2]) - float(self.cameraList[int(cam)]['cameraCenter'][2])

            v = [vx, vy, vz]

            try:
                v = np.asarray([float(i) / sum(v) for i in v])
                vectors.append(v)
            except:
                pass

        for indexA in range(len(vectors)):
            for indexB in range(indexA, len(vectors)):
                if indexA is not indexB:
                    angle.append(pdist(np.asarray([vectors[indexA], vectors[indexB]]), self.angle)[0])

        if len(angle) > 0:
            if "%.2f" % max(angle) in self.pointAngle.keys():
                self.pointAngle["%.2f" % max(angle)][0] += 1
            else:
                self.pointAngle["%.2f" % max(angle)] = [1]

# DataNVM("pippo", "/media/daniele/Data/TERNA/sparse/0/file_nvm.nvm",
#         "/media/daniele/Data/TERNA/sparse/0/")
# DataNVM("pippo", "../../static/users/daniele/geocart_fronte/nvm/sparse.nvm", "../../static/users/daniele/geocart_fronte/statistics/")


# pippo = DataNVM("pippo", "../exampleData/file_nvm.nvm")

if args.input_nvm is None or args.output_folder is None:
    print("check inputs!")
else:
    DataNVM("id", args.input_nvm, args.output_folder)
