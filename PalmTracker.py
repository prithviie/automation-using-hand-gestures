import os
import cv2
import imutils
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

bg = None
dataset_dir = 'Dataset'
gestures_file = 'preprocessing/gestures.txt'

gesture = input('Enter gesture name as per the name in preprocessing/gestures.txt (case sensitive): ')
mode = input('train or test? ').lower()
num_of_images = int(input('Number of images: '))

current_gesture_directory = f'{dataset_dir}/{gesture}_{mode}_images/{gesture.lower()}_{mode}_image_'
current_gesture = current_gesture_directory.index('/', 12)
current_gesture = current_gesture_directory[current_gesture+1:-1]

def get_labels():

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
        labels[gestures[i]] = integer_encoded[i]

    # print(labels)

    return labels


def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)


def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff,
                                threshold,
                                255,
                                cv2.THRESH_BINARY)[1]

    # get the contours in the thresholded image
    (cnts, _) = cv2.findContours(thresholded.copy(),
                                 cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


def main():
    # initialize labels dictionary
    try:
        labels = get_labels()
        label_id = labels[gesture]
    except Exception as e:
        print('Make sure you pass in the correct parameters.')
        quit()

    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0
    image_num = 0

    start_recording = False

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()
        if (grabbed == True):

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

                        # Mention the directory in which you wanna store the images followed by the image name
                        # cv2.imwrite(current_gesture_directory + str(image_num) + '.png', thresholded)
                        cv2.imwrite(f"{current_gesture_directory}{image_num}__l={label_id}.png", thresholded)
                        image_num += 1
                    cv2.imshow("Thresholded", thresholded)

            # draw the segmented hand
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

            # increment the number of frames
            num_frames += 1

            # showing number of images captured
            cv2.putText(clone, f"Captured {image_num} images", (15, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

            # display the frame with segmented hand
            cv2.imshow(f"Recording for {current_gesture}", clone)

            # observe the keypress by the user
            keypress = cv2.waitKey(1) & 0xFF

            # if the user pressed "q", then stop looping
            if keypress == ord("q") or image_num >= num_of_images:
                # free up memory
                camera.release()
                cv2.destroyAllWindows()
                break

            if keypress == ord("s"):
                start_recording = True

        else:
            print("[Warning!] Error input, Please check your camera or video")
            break


main()