import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tensorflow.python.framework import ops
import numpy as np
from PIL import Image
import cv2
import imutils
import os
from sklearn.preprocessing import LabelEncoder
from PalmTracker import *


# PUBNUB
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

ENTRY = "GestureControl"
CHANNEL = "Detect"
KILL_CONNECTION = "exit"
the_update = None

pnconfig = PNConfiguration()
pnconfig.publish_key = 'your publisher key'
pnconfig.subscribe_key = 'your subscriber key'
pnconfig.uuid = "serverUUID-PUB"

pubnub = PubNub(pnconfig)
# PUBNUB


checkpoint_path = 'TrainedModel/checkpoints/' + \
    'Gesture12RecognitionModel.tflearn'
best_checkpoint_path = 'TrainedModel/checkpoints/' + \
    'Gesture12RecognitionModelBest.tflearn'
saved_model_path = 'TrainedModel/' + 'Gesture12RecognitionModel.tflearn'

n_classes = len(os.listdir(dataset_dir))


def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(imageName)


def getPredictedClass():
    # Predict
    image = cv2.imread('Temp.png')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    prediction = model.predict([gray_image.reshape(89, 100, 1)])

    sum = 0
    for i in range(n_classes):
        sum += prediction[0][i]

    return np.argmax(prediction), (np.amax(prediction)/sum)


def get_labels_rev():

    gestures = []
    with open(gestures_file, 'r') as f:
        for line in f:
            line = line.strip()
            gestures.append(line)

    gestures.sort()
    gestures = np.array([gestures[i] for i in range(len(gestures))])
    integer_encoded = LabelEncoder().fit_transform(gestures)

    labels = {}
    for i in range(len(gestures)):
        labels[integer_encoded[i]] = gestures[i]

    # print(labels)

    return labels


labels = get_labels_rev()
func_map = {
    '11': 'Red ON',            # thumbs up
    '10': 'Red half ON',       # thumbs down
    '3': 'Red OFF',            # fist

    '12': 'Green ON',          # two
    '9': 'Green half ON',      # three
    '5': 'Green OFF',          # four

    '6': 'Get rain-value',        # ok

    '7': 'Fan ON',             # one
    '8': 'Fan OFF',            # stop

    '2': 'TV channel change',     # right

    '4': 'Clean floor'         # palm-five
}


def showStatistics(predictedClass, confidence):

    textImage = np.zeros((250, 512, 3), np.uint8)
    className = labels[predictedClass]

    cv2.putText(textImage, "Predicted class: " + className,
                (5, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1)

    cv2.putText(textImage, "Confidence: " + str(confidence * 100) + '%',
                (5, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                1)

    cv2.putText(textImage, "Actuate: " + func_map[str(predictedClass+1)],
                (5, 170),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1)

    cv2.imshow("Statistics", textImage)


def main():
    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0
    start_recording = False

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
            print(num_frames)

        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented) = hand

                # draw the segmented region and display the frame
                cv2.drawContours(
                    clone, [segmented + (right, top)], -1, (0, 0, 255))
                if start_recording:
                    cv2.imwrite('Temp.png', thresholded)
                    resizeImage('Temp.png')
                    predictedClass, confidence = getPredictedClass()
                    showStatistics(predictedClass, confidence)

                    # PUBNUB integration

                    the_update = str(int(predictedClass)+1)
                    the_message = {"entry": ENTRY, "update": the_update}
                    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

                    if envelope.status.is_error():
                        print("[PUBLISH: fail]")
                        print("error: {}".format(status.error))
                    else:
                        print("[PUBLISH: sent]")
                        print(f"Sent: {the_update}")

                    # PUBNUB integration

                cv2.imshow("Thresholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            the_update = KILL_CONNECTION
            break

        if keypress == ord("s"):
            start_recording = True


# Model defined
ops.reset_default_graph()
#                           [batch, height, width, in_channels]
convnet = input_data(shape=[None, 89, 100, 1], name='input')

convnet = conv_2d(convnet, nb_filter=32, filter_size=2, activation='relu')
convnet = max_pool_2d(convnet,  kernel_size=2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, n_units=1000, activation='relu')
convnet = dropout(convnet, keep_prob=0.75)

convnet = fully_connected(convnet, n_units=n_classes, activation='softmax')

convnet = regression(convnet,
                     optimizer='adam',
                     learning_rate=0.001,
                     loss='categorical_crossentropy',
                     name='regression')

model = tflearn.DNN(convnet,
                    checkpoint_path=checkpoint_path,
                    best_checkpoint_path=best_checkpoint_path)

# Load Saved Model
model.load(saved_model_path)

main()
