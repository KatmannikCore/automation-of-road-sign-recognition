#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import csv
import cv2 as cv
import numpy as np
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from imgaug import augmenters as iaa

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from progress.bar import Bar
from alive_progress import alive_bar
import glob
import os
from PIL import Image
images = [] # images
labels = [] # corresponding labels

MIN_IMGS_IN_CLASS = 500
# Learning parameters
EPOCHS = 30
VALIDATION_SPLIT = 0.3
INIT_LR = 0.001
BATCH_SIZE = 256
SET_DECAY = True
path_txt = r'D:\Urban\yolov4\yolov4-opencv-python\train\treugolnik\a9'
path_test = r'D:\Urban\yolov4\yolov4-opencv-python\train\treugolnik\a9'
path_dir_arr = os.listdir(path_txt)
<<<<<<< HEAD
name = './models_200_10/treugolnik/suzenie.h5'
=======
name = './models_200_10/treugolnik/danger.h5'
>>>>>>> 998a996f7b9ff34b8162bd56787139ef7b4beec8

with alive_bar(len(os.listdir(path_txt) *10), force_tty=True) as bar_dir:
    for i in range(0, 10):
        for filename in os.listdir(path_txt):
            bar_dir()
            path = os.path.join(path_txt,filename)
            imagePaths = os.listdir(path)
            #bar2 = Bar('img', max=200)

            for img in imagePaths:
                try:
                    path_img = path + '\\'+ img
                    img = cv.imread(rf"{path_img}")
                    images.append(cv.resize(img, (28, 28)))
                    index = path_dir_arr.index(filename)
                    labels.append(index)
                except Exception as e:
                    print("error", e)



print('Number of loaded images: ' + str(len(images)))
print('Number of loaded labels: ' + str(len(labels)))


train_X = np.asarray(images)
train_X = train_X / 255
train_X = np.asarray(train_X, dtype = "float32")
train_Y = np.asarray(labels, dtype= "float32")

print('Shape of training array: ' + str(train_X.shape))

def count_images_in_classes(lbls):
    dct = {}
    for i in lbls:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    return dct
samples_distribution = count_images_in_classes(train_Y)
print(1,samples_distribution)

def distribution_diagram(dct):
    plt.bar(range(len(dct)), list(dct.values()), align='center')
    plt.xticks(range(len(dct)), list(dct.keys()), rotation=90, fontsize=7)
    plt.show()
distribution_diagram(samples_distribution)

def preview(images, labels):
    plt.figure(figsize=(16, 16))
    for c in range(len(np.unique(labels))):
        i = random.choice(np.where(labels == c)[0])
        plt.subplot(10, 10, c+1)
        plt.axis('off')
        plt.title('class: {}'.format(c))
        plt.imshow(images[i])

#preview(train_X, train_Y)


def augment_imgs(imgs, p):
    """
    Performs a set of augmentations with with a probability p
    """
    from imgaug import augmenters as iaa
    augs = iaa.SomeOf((2, 4),
                      [
                          iaa.Crop(px=(0, 4)),  # crop images from each side by 0 to 4px (randomly chosen)
                          iaa.Affine(scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}),
                          iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}),
                          iaa.Affine(rotate=(-45, 45)),  # rotate by -45 to +45 degrees)
                          iaa.Affine(shear=(-10, 10))  # shear by -10 to +10 degrees
                      ])

    seq = iaa.Sequential([iaa.Sometimes(p, augs)])
    res = seq.augment_images(imgs)
    return res


def augmentation(imgs, lbls):
    classes = count_images_in_classes(lbls)
    for i in range(len(classes)):
        if (classes[i] < MIN_IMGS_IN_CLASS):
            # Number of samples to be added
            add_num = MIN_IMGS_IN_CLASS - classes[i]
            imgs_for_augm = []
            lbls_for_augm = []
            for j in range(add_num):
                im_index = random.choice(np.where(lbls == i)[0])
                imgs_for_augm.append(imgs[im_index])
                lbls_for_augm.append(lbls[im_index])
            augmented_class = augment_imgs(imgs_for_augm, 1)
            augmented_class_np = np.array(augmented_class)
            augmented_lbls_np = np.array(lbls_for_augm)
            imgs = np.concatenate((imgs, augmented_class_np), axis=0)
            lbls = np.concatenate((lbls, augmented_lbls_np), axis=0)
    return (imgs, lbls)



train_X, train_Y = augmentation(train_X, train_Y)

print(train_X.shape)
print(train_Y.shape)

augmented_samples_distribution = count_images_in_classes(train_Y)
print(augmented_samples_distribution)

distribution_diagram(augmented_samples_distribution)

#preview(train_X, train_Y)

train_X = rgb2gray(train_X)
#preview(train_X, train_Y)

def build(width, height, depth, classes):
    # initialize the model along with the input shape to be
    # "channels last" and the channels dimension itself
    model = keras.Sequential()
    inputShape = (height, width, depth)
    chanDim = -1

    # CONV => RELU => BN => POOL
    model.add(Conv2D(8, (5, 5), padding="same", input_shape=inputShape))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # first set of (CONV => RELU => CONV => RELU) * 2 => POOL
    model.add(Conv2D(16, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(16, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # second set of (CONV => RELU => CONV => RELU) * 2 => POOL
    model.add(Conv2D(32, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(32, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # first set of FC => RELU layers
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # second set of FC => RELU layers
    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # softmax classifier
    model.add(Dense(classes))
    model.add(Activation("softmax"))

    # return the constructed network architecture
    return model

model = build(28, 28, 1, len(os.listdir(path_txt)))

if SET_DECAY == True:
    opt = Adam(learning_rate=INIT_LR, weight_decay=INIT_LR / (EPOCHS * 0.5))
else:
    opt = Adam(learning_rate=INIT_LR)
model.compile(loss="sparse_categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

test_images = [] # images
test_labels = [] # corresponding labels


with alive_bar(len(imagePaths), force_tty=True) as bar_img:
    try:
        for filename in os.listdir(path_test):
            bar_img()
            path = os.path.join(path_test, filename)
            imagePaths = os.listdir(path)
            for img in imagePaths:
                img = cv.imread(path + '/'+ img)
                test_images.append(cv.resize(img, (28, 28)))
                index = path_dir_arr.index(filename)
                test_labels.append(index)
    except Exception as e:
        print("error", e)
test_X = np.asarray(test_images)
test_X = test_X / 255
test_X = np.asarray(test_X, dtype = "float32")


test_X = rgb2gray(test_X)
print("test_X" ,test_X.shape)

test_Y = np.asarray(test_labels, dtype = "float32")

print("train_X",train_X.shape)
train_X_ext = np.expand_dims(train_X, axis=3)
print("train_X_ext",train_X_ext.shape)



print("test_X",test_X.shape)
test_X_ext = np.expand_dims(test_X, axis=1)
#test_X_ext = test_X_ext.reshape(63310, 28, 28, 1)
print("test_X_ext",test_X_ext.shape)
print("test_Y",test_Y.shape)
test_Y_ext = np.expand_dims(test_Y, axis=1)
#test_Y_ext = test_X_ext.reshape(63310, 28, 28, 1)
print("test_Y_ext",test_Y_ext.shape)
test_loss, test_acc = model.evaluate(test_X,  test_Y, verbose=1)

x_val = train_X_ext[:1000]
partial_x_train = train_X_ext[1000:]
y_val = train_Y[:1000]
partial_y_train = train_Y[1000:]

history = model.fit(partial_x_train,
                    partial_y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=VALIDATION_SPLIT, validation_data=(x_val, y_val))
model.save(name)


import matplotlib.pyplot as plt

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'bo', label='Потери при обучении')
plt.plot(epochs, val_loss, 'b', label='Потери при проверке')
plt.title('Потери при обучении и проверке',  fontsize=18)
plt.xlabel('Итерации',  fontsize=16)
plt.ylabel('Потери',  fontsize=16)
plt.legend()
plt.show()



#plt.plot(history.history['accuracy'])
##plt.plot(H.history['val_accuracy'])
#plt.title('Model accuracy')
#plt.ylabel('accuracy')
#plt.xlabel('epoch')
##plt.legend(['train', 'test'], loc='upper left')
#plt.show()
## summarize history for loss
#plt.plot(history.history['loss'])
##plt.plot(H.history['val_loss'])
#plt.title('Model loss')
#plt.ylabel('loss')
#plt.xlabel('epoch')
##plt.legend(['train', 'test'], loc='upper left')
#plt.show()


print(test_loss)
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/