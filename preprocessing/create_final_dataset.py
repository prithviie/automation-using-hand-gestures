import os
import shutil
from PIL import Image

# RESIZES ALL IMAGES FROM SUB-DIRECTORIES AND MOVES THEM INTO A SINGLE DIRECTORY - 'all_data_dir'

dataset_dir = 'Dataset'
all_data_dir = "All_data"


def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)


gestures_dirs = []
for dir in os.listdir(dataset_dir):
    gestures_dirs.append(f"{dataset_dir}/{dir.strip()}")


if not os.path.isdir(f"{dataset_dir}/{all_data_dir}"):
    os.mkdir(f"{dataset_dir}/{all_data_dir}")


for loc in gestures_dirs:
    for image in os.listdir(loc):
        resizeImage(f"{loc}/{image}")
        shutil.move(f"{loc}/{image}", f"{dataset_dir}/{all_data_dir}/")
