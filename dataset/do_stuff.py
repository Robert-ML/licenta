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
            os.symlink(os.path.abspath(path + folder + "/selected/" + name + ".png"),
            "/mnt/HD/School/A4/licenta/notebook/code/playground/detect_text/true_positives/" + folder + "-" + name + ".png")

    false_positives = detected_no - true_positives
    print("Detected: " + str(detected_no))
    print("True positives: " + str(true_positives))
    print("False positives: " + str(false_positives))

get_selected(folders)
