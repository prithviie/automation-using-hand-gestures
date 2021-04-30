import os
import shutil
from PIL import Image

# RESIZES ALL IMAGES FROM SUB-DIRECTORIES AND MOVES THEM INTO A SINGLE DIRECTORY - 'all_data_dir'

all_dataset_dirs_file = 'all_dataset_dirs.txt'

dataset_dir = 'Dataset'
all_data_dir = "All_data"


def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)


if not os.path.isdir(f"{dataset_dir}/{all_data_dir}"):
    os.mkdir(f"{dataset_dir}/{all_data_dir}")


folders_to_copy_from = []

with open(f'{os.path.dirname(__file__)}/{all_dataset_dirs_file}', 'r') as f:
    for line in f:
        line = line.strip()
        if len(line) > 10:
            idx = line.index('/', 14)
            line = line[1:idx]
            folders_to_copy_from.append(line)


for loc in folders_to_copy_from:
    for image in os.listdir(loc):
        resizeImage(f"{loc}/{image}")


for loc in folders_to_copy_from:
    for f in os.listdir(loc):
        shutil.move(f"{loc}/{f}", f"{dataset_dir}/{all_data_dir}/")
