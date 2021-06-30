# Automation with Hand Gesture Recognition using Background elimination and CNN

## About the Project

- The project involves recognizing real time gestures and automating stuff around us. These are 12 gestures that are recognized.
- The different gestures include - Direction_left, Direction_right, Fist, Five-palm, OK, Stop, Thumbs_up, Thumbs_down, One - Five.
- Several actuations are mapped to these gestures.
- A custom dataset containing 12 gestures was created and the CNN model was trained on the same. Each gesture has 1000 images (right handed) of size 89x100. There are a total of 12,000 images in the dataset.

## Table of contents

- Directories

  - [Dataset](Dataset) => Custom dataset with 12,000 images.

  - [gifs](gifs) => Gifs/images for output.

  - [preprocessing](preprocessing) => Preprocessing files for dataset creation.

    - [all_dataset_dirs.txt](preprocessing/all_dataset_dirs.txt) => keeps record of sub-directories created in 'Dataset'.
    - [create_final_dataset.py](preprocessing/create_final_dataset.py) => resizes all images from all gesture sub-directories to appropriate size of 89x100.
    - [gestures.txt](preprocessing/gestures.txt) => file containing list of gestures.
    - [mk_dirs_for_dataset.py](preprocessing/mk_dirs_for_dataset.py) => creates a 'Dataset' directory with sub directories for various gestures.

  - [TrainedModel](TrainedModel) => Holds the trained model.

- Files

  - [PalmTracker.py](PalmTracker.py) => For dataset creation.

  - [ModelTrainerNew.py](ModelTrainerNew.py) => Train the CNN.

  - [ContinuousGesturePredcitor.py](ContinuousGesturePredcitor.py) => Predict and transmit gesture over internet in real time.

  - [actuator.py](actuator.py) => Run on other devices (shows simulation as well as some hardware actuation on reciever side).

## Procedure for creating custom dataset

- fill in gesture names in [preprocessing/gestures.txt](preprocessing/gestures.txt).

- run [preprocessing/mk_dirs_for_dataset.py](preprocessing/mk_dirs_for_dataset.py) (creates a 'Dataset' directory with sub directories for various gestures).

  - Dataset (Dataset directory created)
    - Gesture1
    - Gesture2
    - ..
    - .. (similarly for all gestures)

- run [PalmTracker.py](PalmTracker.py) => for each of the gestures in preprocessing/gestures.txt.

  - input the gesture name (as per provided in preprocessing/gestures.txt (case sensitive)).
  - input number of images to capture.
  - input from where to continue capturing (number)
    (generates images (with appropriate labels) in each of the sub directories).

- run [preprocessing/create_final_dataset.py](preprocessing/create_final_dataset.py) => run after creating the entire dataset.

  - resizes all images from all gesture sub-directories to appropriate size (89x100).
