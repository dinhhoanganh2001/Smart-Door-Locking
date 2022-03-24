import sys
import numpy as np
from keras.models import load_model
from PIL import Image
from numpy import asarray
from numpy import expand_dims
from mtcnn.mtcnn import MTCNN
from os import listdir
from os.path import isdir
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from joblib import dump, load
from connect import *

# extract a single face from a given photograph
def extract_face(filename, required_size=(160, 160)):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    if len(results) == 0:
        print(filename)
        raise Exception("No face detected !")
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
    # enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        face = extract_face(path)
        # store
        faces.append(face)
    return faces


# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(directory):
    X, y = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        # load all faces in the subdirectory
        faces = load_faces(path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)


# get the face embedding for one face
def get_embedding(model, face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]


def predict(img_path, svm_model, facenet_model):
    face_pixels = extract_face(img_path)
    face_pixels = asarray(face_pixels)
    face_pixels_embedding = get_embedding(facenet_model, face_pixels)
    face_pixels_embedding = expand_dims(face_pixels_embedding, axis=0)
    in_encoder = Normalizer(norm='l2')
    face_pixels_embedding = in_encoder.transform(face_pixels_embedding)
    yhat_class = svm_model.predict(face_pixels_embedding)
    yhat_prob = svm_model.predict_proba(face_pixels_embedding)

    # get name
    class_index = yhat_class[0]
    class_probability = yhat_prob[0, class_index] * 100
    if class_probability < 85:
        screen = "Stranger detected, get out of this house !"
        print(screen)
        return screen,"Stranger",class_probability
    out_encoder = LabelEncoder()
    directory = 'image/train'
    y = list()
    for subdir in listdir(directory):
        y += [subdir]
    out_encoder.fit(asarray(y))
    predict_names = out_encoder.inverse_transform(yhat_class)
    screen = 'Hello '+ predict_names[0] + ', Welcome home :> '
    print(screen)
    return screen, predict_names[0], class_probability




# -----------------------------------------------------------
# In case new users or new images data added
# Run this to train the SVM model
# -----------------------------------------------------------
def train_svm_model(facenet_model):
    # load train dataset
    trainX, trainy = load_dataset('image/train/')
    # # load test dataset
    testX, testy = load_dataset('image/test/')
    # convert each face in the train set to an embedding
    newTrainX = list()
    for face_pixels in trainX:
        embedding = get_embedding(facenet_model, face_pixels)
        newTrainX.append(embedding)
    newTrainX = asarray(newTrainX)
    newTestX = list()
    for face_pixels in testX:
        embedding = get_embedding(facenet_model, face_pixels)
        newTestX.append(embedding)
    newTestX = asarray(newTestX)
    # normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(newTrainX)
    testX = in_encoder.transform(newTestX)
    # label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
    testy = out_encoder.transform(testy)
    # fit model
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(trainX, trainy)
    # predict
    yhat_train = svm_model.predict(trainX)
    yhat_test = svm_model.predict(testX)
    # score
    score_train = accuracy_score(trainy, yhat_train)
    score_test = accuracy_score(testy, yhat_test)
    # summarize
    print('Accuracy: train=%.3f, test=%.3f' % (score_train * 100, score_test * 100))
    dump(svm_model, 'svm_model.joblib')
    return svm_model