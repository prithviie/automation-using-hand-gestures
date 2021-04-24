from PIL import Image

current_gesture_directory = './TestDataset/Fist_images/fist_image_'
num_of_images = 1000

def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(imageName)

for i in range(0, num_of_images):
    # Mention the directory in which you wanna resize the images followed by the image name
    resizeImage(current_gesture_directory + str(i) + '.png')


