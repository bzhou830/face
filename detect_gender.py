from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras.utils import get_file
import numpy as np
import argparse
import cv2
import os

# handle command line arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to input image")
# args = ap.parse_args()

# download pre-trained model file (one-time download)
model_path = "gender_detection.model"

# read input image
image = cv2.imread("C:\\Users\\Bz\\Desktop\\ML\\dataset\\dataset\\celeba\\img\\1002.jpg")
if image is None:
    print("Could not read input image")
    exit()

# load pre-trained model
model = load_model(model_path)

faces_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faces_cascade.detectMultiScale(gray, 1.3, 5)
if len(faces) != 1:
    print(args.image, "could not fount face")
    exit()


classes = ['man', 'woman']
for face in faces:
    x, y, width, height = face
    face_region = image[y:y + height, x:x + width]
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    face_crop = np.copy(image[y:y + height, x:x + width])
    # preprocessing for gender detection model
    face_crop = cv2.resize(face_crop, (96, 96))
    face_crop = face_crop.astype("float") / 255.0
    face_crop = img_to_array(face_crop)
    face_crop = np.expand_dims(face_crop, axis=0)

    # apply gender detection on face
    conf = model.predict([face_crop])[0]
    print(conf)
    print(classes)
    # get label with max accuracy
    idx = np.argmax(conf)
    label = classes[idx]
    label = "{}: {:.2f}%".format(label, conf[idx] * 100)

    Y = y - 10 if y - 10 > 10 else y + 10
    # write label and confidence above face rectangle
    cv2.putText(image, label, (x, Y),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


# display output
cv2.imshow("gender detection", image)

# press any key to close window           
cv2.waitKey()

# save output
cv2.imwrite("gender_detection.jpg", image)

# release resources
cv2.destroyAllWindows()
