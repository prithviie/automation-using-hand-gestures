# Automation using Hand Gestures

This project involves recognizing real time gestures and automating simple real life tasks such as turning on/off appliances, interacting with a television and other electronic items. This project implements **Home Automation using a Convolution Neural Network** based gesture classifier. These gestures are used as an actuation mechanism for actuating various household items. CLick [here](#output) to see the output.<br>

## About the Project

- The project involves recognizing real time gestures and automating simple real life tasks. There are **12** gestures that are recognized.
- The different gestures include - _Direction_left_, _Direction_right_, _Fist_, _Five-palm_, _OK_, _Stop_, _Thumbs_up_, _Thumbs_down_, _One_, _Two_ _Three_, _Four_ and _Five_, see [Dataset](Dataset).
- The dataset used is a custom dataset. It consists of 12,000 images for 12 of the gestures mentioned above. Each gesture has 1000 images corresponding to the right hand. Each image is resized to a dimension of 89x100.

## Requirements

- `Python 3`
- `tensorflow`
- `tflearn`
- `keras`
- `numpy`
- `sklearn`
- `cv2` (Camera/Video capture)
- `imutils` and `pillow` (image transforms)
- `pyfirmata` (interacting with the Arduino)
- `turtle` and `tkinter` (for simulation)
- `Pubnub` account with a publisher and subscriber key (to transmit messages over internet).

## File description

Directories:

- [`Dataset`](Dataset) custom dataset with 12,000 images.

- [`gifs`](gifs) gifs/images for simulation output.

- [`preprocessing`](preprocessing) (preprocessing files for dataset creation)

  - [`all_dataset_dirs.txt`](preprocessing/all_dataset_dirs.txt) keeps record of sub-directories created in Dataset.
  - [`create_final_dataset.py`](preprocessing/create_final_dataset.py) resizes all images from all gesture sub-directories to appropriate size.
  - [`gestures.txt`](preprocessing/gestures.txt) file containing list of gestures.
  - [`mk_dirs_for_dataset.py`](preprocessing/mk_dirs_for_dataset.py) creates a Dataset directory with sub-directories for various gestures.

- [`TrainedModel`](TrainedModel) contains the trained model.

Files:

- [`Actuator.py`](Actuator.py) to actuate devices/simulation (shows simulation as well as some hardware actuation on receiver side).

- [`ContinuousGesturePredictor.py`](ContinuousGesturePredictor.py) predict and transmit gesture over internet in real time.

- [`PalmTracker.py`](PalmTracker.py) for dataset creation.

- [`ModelTrainer.ipynb`](ModelTrainer.ipynb) to train the CNN.

Refer the [how to](#howto) section to get started.

## Some key insights

### Background Elimination Algorithm

The Background elimination algorithm uses the concept of **running average**. Here it is used to detect a hand and isolate it from the background. The algorithm analyses the first 30 frames of the video feed where it analyses the 'still' background. After the first 30 frames, if an object enters the region, that object is considered as _"not the background"_ and hence it is detected as the _object_ in the region. This way when a hand is brought in the region, it is properly detected.

### The Convolution Neural Network

The network contains of **7** hidden layers with **ReLU** as the activation function. Each of these layers is followed by a Max-Pool layer. The input shape to the network is (89x100x1).<br>
The network consists **1** fully-connected layer with **sigmoid** as the activation function.<br>
The network is trained over **10** epochs with a batch size of **50** and a learning rate of **0.001**. The optimizer used is **Adam**.<br>
The obtained accuracy for the validation set is **99.87%**.

### Real-Time Detection

The input image is fed into the network after thresholding and **background elimination**, background elimination is done using the concept of running average. The CNN model is **7** hidden layer architecture and it is trained on a custom dataset consisting of 12 gestures with a total of 1000 images for each gesture. The automation is **simulated using a GUI**. Some parts (lights in the house) of the actuation are also demonstrated using an **Arduino** (Hardware actuation). <br>

The recognized gesture is transmitted to another device and the corresponding actuation occurs on the receiver's side. The gesture classification is transmitted across devices via the internet using the [Pubnub](https://www.pubnub.com/) API. Refer [this](https://www.pubnub.com/blog/socket-programming-in-python-client-server-p2p/) article to get started with using the Pubnub API.

<h2 id="howto"> HOW TO </h2>

### Procedure for creating a custom dataset

_Note: All the files are to be executed from the root of the project directory only._

- fill in gesture names in [preprocessing/gestures.txt](preprocessing/gestures.txt).

- run [preprocessing/mk_dirs_for_dataset.py](preprocessing/mk_dirs_for_dataset.py): creates a _Dataset_ directory with sub-directories for various gestures, as shown below.

  - Dataset (Dataset directory created)
    - Gesture1 (directory 1)
    - Gesture2 (directory 2)
    - ..
    - .. (similarly for all gestures)

- run [PalmTracker.py](PalmTracker.py) for each of the gestures in _preprocessing/gestures.txt_.

  - input the gesture name (as per provided in _preprocessing/gestures.txt_ (case sensitive)).
  - input number of images to capture.
  - input from where to continue capturing (number) (images in the dataset are numbered). <br>
    (this opens up a window with the video feed. Wait for the background elimination algorithm to register the background before performing any gestures (you can see numbers 0 to 29 being printed over the console). Once that is done, you can start performing the gestures as required. Once you start performing the gestures, another window named _"Thresholded"_ opens up. To start recording/capturing the gestures, press '**s**' on your keyboard ('**q**' to quit)). <br>
    (generates images (with appropriate labels) in each of the sub-directories).

- run [preprocessing/create_final_dataset.py](preprocessing/create_final_dataset.py): run only after creating the entire dataset. Resizes all dataset images to appropriate size of 89x100.

### How to run the Real time prediction

Run [`ContinuousGesturePredictor.py`](ContinuousGesturePredictor.py) and wait for a window with the video feed to open up. Once the window opens, wait for the background elimination algorithm to register the background before performing any gestures (you can see numbers 0 to 29 being printed over the console). Once that is done, you can start performing the gestures as required. Once you start performing the gestures, another window named _"Thresholded"_ opens up. To start recognizing the gestures, press '**s**' on your keyboard ('**q**' to quit). Another window named _"Statistics"_ will open up and print the results. This same file will also transmit the recognised gesture over the internet using the Pubnub API. This file acts as the _publisher_ when transmitting the gesture.<br>

Run [`Actuator.py`](Actuator.py) on the same or another computer (connect the Arduino for hardware actuations if required), a window named _"Home"_ opens up with various appliances represented in a simple way. This file acts as the _subscriber_ and will receive any message transmitted by the _publisher_ (ContinuousGesturePredictor.py). As the messages (gestures) are received, the corresponding actuations occur in the simulation as well as the hardware. The actions corresponding to each gesture can be found in the table below.

## Various gestures mapped to their actuations

| Gesture         | Actuation          |
| --------------- | ------------------ |
| Thumbs up       | Red light ON       |
| Thumbs down     | Lighter Red ON     |
| Fist            | Red light OFF      |
| One             | Fan ON             |
| Two             | Green light ON     |
| Three           | Lighter Green ON   |
| Four            | Green OFF          |
| Palm-Five       | Floor clean        |
| Stop            | Fan OFF            |
| OK              | Predict rain       |
| Direction right | T.V channel change |

<h2 id="output"> Output </h2>

:octocat: Here is the final output:
![output](Result.gif)
