import matplotlib
matplotlib.use("Agg")
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from keras.utils import plot_model
from sklearn.model_selection import train_test_split
from model.smilenet import SmileNet
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import cv2
import pandas as pd

# 解析输入的命令行
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", type=str, help="path of dataset", default=".\\ML\\dataset\\dataset\\celeba")
ap.add_argument("-m", "--model", type=str, default="x.model", help="path of output model")
ap.add_argument("-p", "--plot", type=str, default="plot.png", help="path of output accuracy/loss plot")
args = ap.parse_args()

# 初始化参数
epochs = 20
lr = 1e-3
batch_size = 64
img_dims = (96, 96, 3)

data = []
labels = []

# load image files from the dataset
dataset_path = args.dataset
random.seed(42)

df = pd.read_csv(dataset_path + "/labels.csv", sep='\t', usecols=[1, 2])
for row in df.itertuples():
    image_file_path = dataset_path + "/img/" + getattr(row, 'img_name')
    label = int(getattr(row, 'gender'))
    image = cv2.imread(image_file_path)
    # 调整图像大小为网络输入层的大小
    image = cv2.resize(image, (img_dims[0], img_dims[1]))
    image = img_to_array(image)
    data.append(image)
    labels.append([label])


# 预处理
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# 将数据集分割成测试集和验证集
(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=42)
trainY = to_categorical(trainY, num_classes=2)
testY = to_categorical(testY, num_classes=2)

print(trainY)
print(testY)
# augmenting datset 
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")

# build model
model = SmileNet.build(width=img_dims[0], height=img_dims[1], depth=img_dims[2],
                            classes=2)

# compile the model
opt = Adam(lr=lr, decay=lr / epochs)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

# train the model
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=batch_size),
                        validation_data=(testX, testY),
                        steps_per_epoch=len(trainX) // batch_size,
                        epochs=epochs, verbose=1)

# save the model to disk
model.save(args.model)

# plot training/validation loss/accuracy
plt.style.use("ggplot")
plt.figure()
N = epochs
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")

plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="upper right")

# save plot to disk
plt.savefig(args.plot)

