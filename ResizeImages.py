import os
from PIL import Image

final_dataset_dir = 'Dataset'
directory = final_dataset_dir + '/Testing'
# directory = final_dataset_dir + '/Training'

def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)


for image in os.listdir(directory):
    resizeImage(image)
