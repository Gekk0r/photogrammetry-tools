import json
import math
import numpy as np
from scipy.spatial.distance import pdist


class DataNVM(object):

    def __init__(self, name, path):

        self.cameraList = []
        self.data = dict()
        self.points = dict()
        self.pointsAllData = dict()
        self.dataAll = dict()
        self.points_img = dict()
        self.pointAngle = dict()

        self.name = name
        self.path = path

        file = open(self.path, 'r')
        lines = file.readlines()

        self.num_img = int(lines[2])
        self.index_tie = int(self.num_img + 4)
        self.num_tie = int(lines[self.index_tie])
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
        out = open("../exampleData/chart_points_aggregation_tsv.tsv", "w")
        out.write("point_number" + "\t" + "number_images" + "\n")

        for index in range(3, self.index_tie-1):
            cameraTMP = lines[index].strip().split(" ")
            camera = {"name": cameraTMP[0].split("/")[-1], "focal_lenght": cameraTMP[1], "quaternion": [cameraTMP[2], cameraTMP[3], cameraTMP[4], cameraTMP[5]],
                      "cameraCenter": [cameraTMP[6], cameraTMP[7], cameraTMP[8]], "radial": [cameraTMP[9], cameraTMP[10], cameraTMP[11]]}
            self.cameraList.append(camera)

        for index in range(self.index_tie + 1, len(lines) - 1):
            line = lines[index].strip().split(" ")
            self.pointsAllData[str(index - self.index_tie)] = {"id": str(index - self.index_tie),
                                                               "point3D": (line[0], line[1], line[2]),
                                                               "rgb": (line[3], line[4], line[5]), "num_imgs": line[6],
                                                               "list_images": []}

            self.interAngle(self.pointsAllData[str(index - self.index_tie)]["id"], self.pointsAllData[str(index - self.index_tie)]["point3D"], self.cameraList)

            self.points[str(index - self.index_tie)] = [int(line[6])]
            out.write(str(index - self.index_tie) + "\t" + line[6] + "\n")
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

        data = json.dumps(self.points)
        out = open("../exampleData/chart_points_aggregation.json", "w")
        out.write(data)
        data = json.dumps(self.data)
        out = open("../exampleData/chart_img_aggregation.json", "w")
        out.write(data)
        data = json.dumps(self.dataAll)
        out = open("../exampleData/chart_img.json", "w")
        out.write(data)
        data = json.dumps(self.pointsAllData)
        out = open("../exampleData/chart_points.json", "w")
        out.write(data)
        data = json.dumps(self.points_img)
        out = open("../exampleData/points_img.json", "w")
        out.write(data)
        data = json.dumps(self.pointAngle)
        out = open("../exampleData/chart_points_angle.json", "w")
        out.write(data)

    def extractName(self, id, lines):
        name = lines[3 + id].strip().split(" ")[0]
        name = name.split("/")[-1]
        return name

    def interAngle(self, name, pt, camList):
        vectors = []

        angle = []
        for cam in camList:
            vx = float(pt[0]) - float(cam['cameraCenter'][0])
            vy = float(pt[1]) - float(cam['cameraCenter'][1])
            vz = float(pt[2]) - float(cam['cameraCenter'][2])

            v = [vx, vy, vz]
            v = np.asarray([float(i) / sum(v) for i in v])
            vectors.append(v)
        for indexA in range(len(vectors)):
            for indexB in range(indexA, len(vectors)):
                angle.append(pdist(np.asarray([vectors[indexA], vectors[indexB]]), self.angle)[0])

        if "%.2f" % max(angle) in self.pointAngle.keys():
            self.pointAngle["%.2f" % max(angle)][0] += 1
        else:
            self.pointAngle["%.2f" % max(angle)] = [1]

pippo = DataNVM("pippo", "../exampleData/file_nvm.nvm")
