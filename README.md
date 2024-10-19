# Smart Door Locking
Multi-disciplinary Project Specializing in AI - Sem212
## Summary
The project contains 3 major modules:
* **AI Module**: Face Recognition, using a pre-trained model (Facenet) to get the image embeddings, classify the face using the embedding input vector by train a SVM.
* **Software Module**: A **Kivy** mobile application which contains some features such as authentication (Login/SignUp), managing user profiles, uploading images from storage, checking record, modify member's list.
* **IoT Module**: A IoT gateway implementation which means a Microbit connected with some devices (sensors and camera) communicating with AI server and backend mobile application server.

My team has total 5 members, I'm responsible for AI and Software module
## Problem
The problem can be described as:
* Has a image database of K members(person lived in the house), can be stored on **Firebase Storage**.
* The camera in front of the door will capture the image and recognize the people in database or not, if familiar, unlock and open the door, otherwise, send warnning to the admin's mobile application.
* The application supports some features for both guests and members in the house, the admin(owner of the house) can modify the member list(add/delete) and check the recognize history anytime.

## Installation

### Environment
#### For AI module and gateway:
```bash
pip install -r requirements.txt
```


#### For Kotlin application:
* Android version >= 5.1 (API level 22).
* Highly recommend **PyCharm** IDE to run the code.
* The project folder is ```application```. So you just clone this, build and run in your IDE.
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
* **FrontEnd**: **Kivy** application contains some features communicate with **Firebase** such as: authentication, check recognize history, ...

## Performance
| SVM     | Training Accuracy | Validation Accuracy
|---------|-------------------| ------------------
| 3 users | 99%              | 99%
| 5 users |                   |


## Mock-up
<p style="text-align:center;"><img src="https://firebasestorage.googleapis.com/v0/b/pipai212.appspot.com/o/welcome.png?alt=media&token=9c8cd259-0833-4ff9-b7e8-0f4c7ec59881" width="500"></p>

<p style="text-align:center;"><img src="https://firebasestorage.googleapis.com/v0/b/pipai212.appspot.com/o/history.PNG?alt=media&token=437c8532-8a48-498d-8300-f888eff0c850" width="500"></p>

## Challenges
* Lacking of cloud server to maintain the python code, I have to run the Python script on local host.
* The Microbit don't have Wifi connected feature, so It had to connect serially through USB port.
* Mobile applicaton is not optimize

## What next?
* IoT: improve the connection (Wifi, eliminate serial port), maintain code on a Cloud server.
* AI: next time, I will use transfer learning and train the network based on VietNamese Faces data-set, implement the algorithm myself.
* Software: increase UI for easier look (change to use **Kotlin** for building mobile app).

## References
* [Adafruit-IO Python manual](https://adafruit-io-python-client.readthedocs.io/en/latest/)
* [FaceNet: A Unified Embedding for Face Recognition and Clustering](https://arxiv.org/pdf/1503.03832.pdf)
* [How to Develop a Face Recognition System Using FaceNet in Keras](https://machinelearningmastery.com/how-to-develop-a-face-recognition-system-using-facenet-in-keras-and-an-svm-classifier/)
* [Kotlin docs](https://kotlinlang.org/docs/home.html)
* [Build your own IoT gateway with python](https://www.studocu.com/vn/document/hcmc-university-of-technology/computer-architecture/build-your-own-io-t-gateway-with-python/23237989)
