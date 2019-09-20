from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-ig", "--input_gt", dest="input_gt",
                    help="ground truth point cloud", metavar="")
parser.add_argument("-is", "--input_sp", dest="input_sp",
                    help="supervised point cloud", metavar="")
parser.add_argument("-c", "--config_class", dest="config_class",
                    help="remapping classes fromy 0_POLES 1_CABLES 2_GROUND 3_VEGETATION 4_ROAD", metavar="")

args = parser.parse_args()


class evaluation:

    def overallAccuracy(self, eval_dict, pcl_len):
        tp = 0
        for key in eval_dict.keys():
            tp += eval_dict[key]["TP"]

        result = (tp / pcl_len) * 100

        return result

    def recall(self, eval_dict, segment):
        tp = eval_dict[segment]["TP"]
        fn = eval_dict[segment]["FN"]

        return tp / (tp + fn)

    def precision(self, eval_dict, segment):
        tp = eval_dict[segment]["TP"]
        fp = eval_dict[segment]["FP"]

        return tp / (tp + fp)

    def f1(self, recall, precision):
        return 2 * recall * precision / (precision + recall)

    def countPoints(self, pcl, value):
        counter = 0
        for key in pcl.keys():
            if value == int(pcl[key].split(".")[0]):
                counter += 1
        return counter

    def evalClassification(self, gt_path, super_path, config):
        # Ground truth file

        gt_file = open(gt_path, "r")
        gt_index = config
        gt_dict = dict()

        # Supervised truth file

        super_file = open(super_path, "r")
        super_dict = dict()

        for line in gt_file:
            if "//" in line:
                pass
            else:
                key = line.strip().split(" ")
                values = key[3]
                key = " ".join(key[0:3])
                gt_dict[key] = values

        for line in super_file:
            if "//" in line:
                pass
            else:
                key = line.strip().split(" ")
                values = key[3]
                key = " ".join(key[0:3])
                super_dict[key] = values

        conf_matr = {"FP": {}, "FN": {}}

        for elem in range(len(config)):
            for item in range(len(config)):
                conf_matr["FP"][str(elem)] = [0] * len(config)
                conf_matr["FN"][str(elem)] = [0] * len(config)

        eval_dict = {"0": {"TP": 0, "FP": 0, "FN": 0}, "1": {"TP": 0, "FP": 0, "FN": 0},
                     "2": {"TP": 0, "FP": 0, "FN": 0},
                     "3": {"TP": 0, "FP": 0, "FN": 0}, "4": {"TP": 0, "FP": 0, "FN": 0},
                     "5": {"TP": 0, "FP": 0, "FN": 0}, "6": {"TP": 0, "FP": 0, "FN": 0},
                     "7": {"TP": 0, "FP": 0, "FN": 0}, "8": {"TP": 0, "FP": 0, "FN": 0}}

        # Vegetation ground_truth == supervised -> TP(Vegetation)
        # Vegetation ground_truth != supervised (cable) -> FP(Vegetation) -> FN(cable)
        errors = 0
        errors_file = open("errors.txt", "w")
        for key in super_dict.keys():
            try:
                key_dict = super_dict[key].split(".")[0]
                if int(super_dict[key].split(".")[0]) == gt_index.index(gt_dict[key].split(".")[0]):
                    eval_dict[key_dict]["TP"] += 1
                else:
                    key_gt = str(gt_index.index(gt_dict[key].split(".")[0]))
                    eval_dict[key_dict]["FP"] += 1
                    eval_dict[key_gt]["FN"] += 1

                    conf_matr["FP"][key_dict][int(key_gt)] += 1
                    conf_matr["FN"][key_gt][int(key_dict)] += 1

            except:
                errors += 1
                errors_file.write(key + "\n")

        # print(countPoints(gt_dict, 4))
        log = open("log.txt", "w")

        print("Errors ", errors)
        print(eval_dict)

        log.write("Confusion Matrix  (row: ground truth; class order: 0,1,2,3,4)\n")
        for elem in range(len(config)):
            conf_matr["FN"][str(elem)][elem] = eval_dict[str(elem)]["TP"]
            tmp = [str(i) for i in conf_matr["FN"][str(elem)]]
            tmp = ','.join(tmp)
            log.write(tmp + "\n")

        log.write("\n")
        print(conf_matr)

        print("Ground truth file ", gt_path)
        print("Ground truth number", len(gt_dict.keys()))
        print("Supervised file ", super_path)
        print("Supervised number", len(super_dict.keys()))
        print("Overall Accuracy [%]:" + str(self.overallAccuracy(eval_dict, len(super_dict.keys()))))

        log.write("Errors: " + str(errors) + "\n")
        log.write("Ground truth file: " + gt_path.split("/")[-1] + "\n")
        log.write("Ground truth number: " + str(len(gt_dict.keys()) - errors) + "\n")
        log.write("Supervised file: " + super_path.split("/")[-1] + "\n")
        log.write("Supervised number: " + str(len(super_dict.keys()) - errors) + "\n")
        log.write("Overall Accuracy [%]: " + str(self.overallAccuracy(eval_dict, len(super_dict.keys()))) + "\n")

        for segment in eval_dict.keys():

            try:
                print("Class : ", segment)
                recall = self.recall(eval_dict, segment)
                precision = self.precision(eval_dict, segment)
                f_1 = self.f1(recall, precision)

                print("Recall [%]: ", recall * 100)
                print("Precision [%]: ", precision * 100)
                print("F1: ", f_1)

                log.write("Class : " + str(segment) + "\n")
                log.write("Recall [%]: " + str(recall * 100) + "\n")
                log.write("Precision [%]: " + str(precision * 100) + "\n")
                log.write("F1: " + str(f_1) + "\n")
            except:
                pass


if args.input_gt is None or args.input_sp is None:
    print("check inputs!")
else:
    if args.config_class is None:
        args.config_class = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    else:
        args.config_class = args.config_class.strip().split(",")
    eval = evaluation()
    eval.evalClassification(args.input_gt, args.input_sp, args.config_class)
