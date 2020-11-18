from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

model_path = "smile.model"
data = []
# read input image
image = cv2.imread("D:\\123456\\ML\\dataset\\dataset\\celeba\\img\\1.jpg")
src_image = np.copy(image)
if image is None:
    print("Could not read input image")
    exit()
# load model
model = load_model(model_path)
classes = ['not smile', 'smile']
image = cv2.resize(image, (64, 64))
image = img_to_array(image)
data.append(image)
data = np.array(data, dtype="float") / 255.0
res = model.predict(data)
print(res)
print(classes)
# get label with max accuracy
idx = np.argmax(res[0])
label = classes[idx]
print(label)
label = "{}: {:.2f}%".format(label, res[0][idx] * 100)

# write label and confidence
cv2.putText(src_image, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# display output
cv2.imshow("gender detection", src_image)

# press any key to close window
cv2.waitKey()
# save output
cv2.imwrite("gender_detection.jpg", src_image)
# release resources
cv2.destroyAllWindows()
