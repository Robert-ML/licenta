from importlib.metadata import files
import os
import shutil

path = "./evaluation/"

# filter only for the folders
folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def get_selected(folders):
    detected_no = 0
    true_positives = 0
    false_positives = 0

    for folder in folders:
        detected_no += len(os.listdir(path + folder + "/detected/"))

        file = "selected.txt"
        file_path = path + folder + "/" + file
        # open file and read string separated by space
        selected = []
        with open(file_path, "r") as f:
            selected = f.read().split()

        true_positives += len(selected)

        detected_folder = path + folder + "/detected/"
        for name in selected:
            file_path = detected_folder + name + ".png"
            shutil.copyfile(file_path, path + folder + "/selected/" + name + ".png")
            try:
                os.symlink(os.path.abspath(path + folder + "/selected/" + name + ".png"), "/mnt/HD/School/A4/licenta/notebook/code/playground/detect_text/true_positives/" + folder + "-" + name + ".png")
                break
            except:
                pass

    false_positives = detected_no - true_positives
    print("Detected: " + str(detected_no))
    print("True positives: " + str(true_positives))
    print("False positives: " + str(false_positives))

def do_CER():
    path = "/mnt/HD/School/A4/licenta/notebook/code/playground/recognize_text/evaluate/"
    files = [x for x in os.listdir(path) if x.endswith(".txt")]

    CERs = []

    for file in files:
        CER = do_CER_file(file, path)
        print("CER: ", CER)
        CERs.append(CER)

    print("Mean CER: ", sum(CERs) / len(CERs))
    print(CERs)

def do_CER_file(file, path):
    f = open(path + file, "r")
    proc = [s for s in f.readline().split('\n')[0][1:-1].replace("\' \'", '').replace('\'', '').split(',') if s]
    gtru = f.readline().split('\n')[0][1:-1].replace("\' \'", '').replace('\'', '').split(',')
    f.close()

    l = min(len(proc), len(gtru))

    if (l == 0):
        return 1.0

    cer = 0.0
    tokens_length = 0
    for i in range(l):
        tokens_length += len(proc[i])
        for j in range(len(proc[i])):
            if (proc[i][j] != gtru[i][j]):
                cer += 1.0

    return cer / tokens_length

    for i in range(l, len(gtru)):
        tokens_length += len(gtru[i])
        cer += len(gtru[i])

    return cer / tokens_length

# get_selected(folders)
do_CER()