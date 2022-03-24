# Smart Door
Multi-disciplinary Project Specializing in AI - Sem212
## Summary
The project contains 3 major modules:
* **AI Module**: Face Recognition, using a pre-trained model (Facenet) to get the image embeddings, classify the face using the embedding input vector by train a SVM.
* **Software Module**: A **Kotlin** mobile application which contains some features such as authentication (Login/SignUp), managing user profiles, uploading images from storage, checking record, modify member's list.
* **IoT Module**: A IoT gateway implementation which means a Microbit connected with some devices (sensors and camera) communicating with AI server and backend mobile application server.

## Problem
The problem can be described as:
* Has a image database of K members(person lived in the house), can be stored on **Firebase Storage**.
* The camera in front of the door will capture the image and recognize the people in the house, if familiar, unlock and open the door, otherwise, send the message to the admin's mobile application.
* The application supports some features for both guests and members in the house, the admin(owner of the house) can modify the member list(add/delete) and check the recognize history anytime.

## Installation

### Environment
#### For AI module and gateway:
```bash
pip install requirements.txt
```
* The ```.json``` file contains my account and project key on **Firebase Server**, so you have to change it to yours (just simplify create account and project on Firebase then generate the file).
* The ```facenet_keras.h5``` contains facenet model and its weight that have been pre-trained. If you want to load it, your Python version should satisfy ```Python <= 3.7```.Therefore, you should downgrade your Python version to make the code run.
* The ```AIO_USERNAME``` and ```AIO_KEY``` contains my **Adafruit-IO** account key. You should change it in the code by creating your own account and feeds on the **Adafruit-IO** server.

#### For Kotlin application:
* Android version >= 5.1 (API level 22).
* Highly recommend **Android Studio** IDE to run the code.
* The project folder is ```application```. So you just clone this, build and run in your IDE.
* The ```.apk``` is build in ```application\app\build\intermediates\apk\debug\app-debug.apk```, you can download and install on your android device.
### Data-set
* Since I used pre-trained model to get embedding, so I didn't have to train a network to learn the similarity and difference between faces, that's mean I only need the image database of members in the house. 


## Overview

<p style="text-align:center;"><img src="https://firebasestorage.googleapis.com/v0/b/mp212-ai.appspot.com/o/camera_capture%2FScreenshot%202022-03-23%20233414.png?alt=media&token=f4af20b9-585f-4f2e-8124-ee4403cdcf1b" width="600" height="400"></p>


The figure above showed the work flow of the IoT+AI application:
* **Microbit system**: A Microbit connected with many sensor devices
  * Input:
    * [Touch button](https://wiki.chipfc.com/index.php?title=Chipi_-_Touch_Key): used to capture the image when user push on.
    * [DHT11](https://wiki.chipfc.com/index.php?title=Chipi_-_Humidity_%26_Temperature_Sensor): measure the room temperature, alert admin for occurrence of fire and open the door immediately.
    * [Magnetic switch](https://wiki.chipfc.com/index.php?title=C%E1%BA%A3m_bi%E1%BA%BFn_m%E1%BB%9F_c%E1%BB%ADa_c%C3%B4ng_t%E1%BA%AFc_t%E1%BB%AB): used to detect the door is opened or not.
  * Output:
    * [Buzzer](https://wiki.chipfc.com/index.php?title=Chipi_-_Buzzer): to announce stranger or familiar person when recognizes.
    * [LCD I2C](https://lastminuteengineers.com/i2c-lcd-arduino-tutorial/): to display the system status (Capturing, Welcome,...)
* **IoT gateway**: A laptop connected with a camera, this will communicate between the Microbit system with the cloud server via Python.
* **Cloud Server**: includes MQTT server (**Adafruit-IO**), Cloud Server(AI model) and Backend Server(**Firebase** database and Storage). In this project, I run the AI model on localhost(on my own laptop), hence the cloud server is actually localhost on my laptop.
* **FrontEnd**: **Kotlin** application contains some features communicate with **Firebase** such as: authentication, check recognize history, ...

## Performance
| SVM     | Training Accuracy | Validation Accuracy
|---------|-------------------| ------------------
| 3 users | 100%              | 100%
| 5 users |                   |

## How It's used?
* Connect Microbit with your laptop, specify your serial port name before running the code, for more instruction follow [here](https://firebasestorage.googleapis.com/v0/b/mp212-ai.appspot.com/o/camera_capture%2FSerial%20Simulation_en_v0.docx.pdf?alt=media&token=058d0480-42ef-49a1-b29c-cb26f804a784). Now, your laptop's currently a gateway to communicate between microbit and python code.
* Download the `JavaScript` program and put it into Microbit. To do that, you can simply go [here](https://makecode.microbit.org/_LTgHce4LpECk), connect and download the program to it.
* Now, setup's done, let's copy and put your image database into ```image\``` folder, remember to split the dataset to train and validation. Now look at ```main.py```:
```python
if __name__ == "__main__":
    # main()
    # In case you want to train the svm model again #
    facenet_model = load_model('model/facenet_keras.h5')
    svm_model = train_svm_model(facenet_model)
```
This is for building a SVM classifier based on your own dataset, then it will create model file```svm_model.joblib```. Next time we just need to run main() to load the model and predict.
```bash
python main.py
```

* When running, push on touch button for 1-2 seconds to capture your images, wait and see the result :).

## Mock-up
### Authentication
![Alt Text](https://firebasestorage.googleapis.com/v0/b/mp212-ai.appspot.com/o/camera_capture%2Fauthentication.gif?alt=media&token=8112af09-defe-42e6-aa74-20fb8ae78cbf)

### Profile management, check history, modify member
![Alt Text](https://firebasestorage.googleapis.com/v0/b/mp212-ai.appspot.com/o/camera_capture%2Fotherfeatures.gif?alt=media&token=3180b4c9-9c96-43bb-8a01-279c94b27bf1)

## Challenges
* Lacking of cloud server to maintain the python code, I have to run the Python script on local host.
* The Microbit don't have Wifi connected feature, so It had to connect serially through USB port.

## What next?
* IoT: improve the connection (Wifi, eliminate serial port), maintain code on a Cloud server.
* AI: next time, I will use transfer learning and train the network based on VietNamese Faces data-set, implement the algorithm myself.
* Software: increase UI for easier look.

## References
* [Adafruit-IO Python manual](https://adafruit-io-python-client.readthedocs.io/en/latest/)
* [FaceNet: A Unified Embedding for Face Recognition and Clustering](https://arxiv.org/pdf/1503.03832.pdf)
* [How to Develop a Face Recognition System Using FaceNet in Keras](https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/)
* [Kotlin docs](https://kotlinlang.org/docs/home.html)
* [Build your own IoT gateway with python](https://www.studocu.com/vn/document/hcmc-university-of-technology/computer-architecture/build-your-own-io-t-gateway-with-python/23237989)