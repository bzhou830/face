import matplotlib
matplotlib.use("Agg")
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from keras.utils import plot_model
from sklearn.model_selection import train_test_split
from model.smallervggnet import SmallerVGGNet
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import os
import glob
import pandas as pd

# handle command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", type=str,
	help="path to input dataset (i.e., directory of images)", default="D:/123456/A1")
ap.add_argument("-m", "--model", type=str, default="gender_detection.model",
	help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png",
	help="path to output accuracy/loss plot")
args = ap.parse_args()

# initial parameters
epochs = 100
lr = 1e-3
batch_size = 64
img_dims = (96,96,3)

data = []
labels = []

# load image files from the dataset
# image_files = [f for f in glob.glob(args.dataset + "/**/*", recursive=True) if not os.path.isdir(f)]
dataset_path = args.dataset
random.seed(42)
# random.shuffle(image_files)


# create groud-truth label from the image path
df = pd.read_csv(dataset_path + "/labels.csv", sep='\t', usecols=[1, 2])
for row in df.itertuples():
    # print(getattr(row, 'img_name'), getattr(row, 'gender'))  # 输出每一行
    image_file_path = dataset_path + "/img/" + getattr(row, 'img_name')
    label = int(getattr(row, 'gender'))

    image = cv2.imread(image_file_path)
    # 使用opencv识别出人脸区域，然后进行裁剪
    faces_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faces_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) != 1:
        print(image_file_path, "could not fount face")
        continue
    x, y, width, height = faces[0]
    face_region = image[y:y + height, x:x + width]
    # 调整图像大小为网络输入层的大小
    image = cv2.resize(image, (img_dims[0], img_dims[1]))
    image = img_to_array(image)
    data.append(image)
    labels.append([label])

cv2.waitKey(-1)
# pre-processing
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# split dataset for training and validation
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2,
                                                  random_state=42)
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

# augmenting datset 
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")

# build model
model = SmallerVGGNet.build(width=img_dims[0], height=img_dims[1], depth=img_dims[2],
                            classes=2)

# compile the model
opt = Adam(lr=lr, decay=lr/epochs)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

# train the model
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=batch_size),
                        validation_data=(testX,testY),
                        steps_per_epoch=len(trainX) // batch_size,
                        epochs=epochs, verbose=1)

# save the model to disk
model.save(args.model)

# plot training/validation loss/accuracy


# plt.style.use("ggplot")
# plt.figure()
# N = epochs
# plt.plot(np.arange(0,N), H.history["loss"], label="train_loss")
# plt.plot(np.arange(0,N), H.history["val_loss"], label="val_loss")
# plt.plot(np.arange(0,N), H.history["acc"], label="train_acc")
# plt.plot(np.arange(0,N), H.history["val_acc"], label="val_acc")
#
# plt.title("Training Loss and Accuracy")
# plt.xlabel("Epoch #")
# plt.ylabel("Loss/Accuracy")
# plt.legend(loc="upper right")
#
# # save plot to disk
# plt.savefig(args.plot)
