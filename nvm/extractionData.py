import json
import csv

class DataNVM(object):

    def __init__(self, name, path):

        self.data = dict()
        self.points = dict()
        self.pointsAllData = dict()
        self.dataAll = dict()
        self.points_img = dict()

        self.name = name
        self.path = path

        file = open(self.path, 'r')
        lines = file.readlines()

        self.num_img = int(lines[2])
        self.index_tie = int(self.num_img + 4)
        self.num_tie = int(lines[self.index_tie])
        self.extract(lines)

    def extract(self, lines):
        out = open("../exampleData/chart_points_aggregation_tsv.tsv", "w")
        out.write("point_number" + "\t" + "number_images" + "\n")
        for index in range(self.index_tie + 1, len(lines) - 1):
            line = lines[index].strip().split(" ")
            self.pointsAllData[str(index - self.index_tie)] = {"id": str(index - self.index_tie),
                                                        "point3D": (line[0], line[1], line[2]),
                                                        "rgb": (line[3], line[4], line[5]), "num_imgs": line[6],
                                                        "list_images": []}
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


    def extractName(self, id, lines):
        name = lines[3 + id].strip().split(" ")[0]
        name = name.split("/")[-1]
        return name


pippo = DataNVM("pippo", "../exampleData/file_nvm.nvm")
