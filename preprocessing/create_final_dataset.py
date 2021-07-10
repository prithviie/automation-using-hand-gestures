import os
import shutil
from PIL import Image

# resizes all dataset images

dataset_dir = 'Dataset'


def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(imageName)


gestures_dirs = []
for dir in os.listdir(dataset_dir):
    gestures_dirs.append(f"{dataset_dir}/{dir.strip()}")


for loc in gestures_dirs:
    for image in os.listdir(loc):
        resizeImage(f"{loc}/{image}")
