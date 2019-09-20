from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--input_nvm", dest="input_nvm",
                    help="input nvm file", metavar="")
parser.add_argument("-o", "--output_folder", dest="output_folder",
                    help="output folder", metavar="")

args = parser.parse_args()

class PointsNVM(object):

    def __init__(self, path, outpath):

        self.cameraName = dict()
        self.cameraList = dict()

        self.path = path
        self.outpath = outpath

        file = open(self.path, 'r')
        lines = file.readlines()

        self.num_img = int(lines[2])
        self.index_tie = int(self.num_img + 4)
        self.num_tie = int(lines[self.index_tie])

        self.extractName(lines)
        self.extract(lines)

    def extractName(self, lines):
        for index in range(3, self.index_tie - 1):
                cameraTMP = lines[index].strip().split(" ")
                self.cameraName[str(index - 3)] = cameraTMP[0]

    def extract(self, lines):
        for id_point in range(1, self.num_tie):
            line = lines[self.index_tie + id_point].strip().split(" ")
            num_img = int(line[6])
            for shift in range(0, num_img):
                index_camera = 7 + (shift * 4)
                camera = self.cameraName[line[index_camera]]
                position = line[index_camera + 2] + " " + line[index_camera + 3]

                if camera in self.cameraList.keys():
                    self.cameraList[camera].append((str(id_point), position))
                else:
                    self.cameraList[camera] = []
                    self.cameraList[camera].append((str(id_point), position))
        
        for camera in self.cameraList.keys():
            file_out = open(self.outpath + camera + ".txt", 'w')
            for element in self.cameraList[camera]:
                file_out.write(" ".join(element) + "\n")

if args.input_nvm is None or args.output_folder is None:
    print("check inputs!")
else:
    PointsNVM(args.input_nvm, args.output_folder)