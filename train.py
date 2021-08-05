import os
import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from keras.utils import np_utils
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model, Sequential


# 設定picture size及data path
picture_size = 128
img_path = './dataset_2/training_data/'

# 印出dataset中各類有幾張image
for cnt in os.listdir(img_path):
    print(str(len(os.listdir(img_path + cnt))) + " " + cnt + " images")

# 記錄總共有幾張image
f_cnt = 0
for Floder_name in os.listdir(img_path):
    for filename in os.listdir(img_path + Floder_name):
        f_cnt +=1
print('all_image_file: ',f_cnt)

# 建立空的np_array (填label用)
label_default = np.zeros(shape=[f_cnt])
img_default = np.zeros(shape=[f_cnt,picture_size,picture_size])
f_cnt = 0

# 給各個floder中的image貼上label
for Floder_name in os.listdir(img_path):
    for filename in os.listdir(img_path + Floder_name):        
            
        temp = cv2.imread(img_path + Floder_name + "/" + filename,0)
        temp = cv2.resize(temp, (picture_size,picture_size))
        img_default[f_cnt] = temp
        
        if Floder_name == '1':
            label_default[f_cnt] = 0
        elif Floder_name == '2':
            label_default[f_cnt] = 1
        elif Floder_name == '3':
            label_default[f_cnt] = 2
        elif Floder_name == '4':
            label_default[f_cnt] = 3
        elif Floder_name == '5':
            label_default[f_cnt] = 4
            
        f_cnt +=1

# reshape成丟進model input的dimension
img_default = img_default.reshape(f_cnt,picture_size,picture_size,1)
img_default.shape

label_onehot=np_utils.to_categorical(label_default) # 做onehot encoding
print('label_onehot[0]:{},label_dim:{},shape:{}'.format(label_onehot[0],label_onehot.ndim,label_onehot.shape)) # Label(Encoding結果 , 維度, shape)
img_default = img_default / 255.0 # 做 normalization


random_seed  = 3 # 隨機分割
x_train, x_test, y_train, y_test = train_test_split(img_default, label_onehot, test_size = 0.2, random_state=random_seed) # 切分訓練及測試集
print('x_train.shape:{}\n,y_train.shape:{}\nx_test.shape:{}\ny_test.shape:{}'.format(x_train.shape, y_train.shape, x_test.shape, y_test.shape)) #(train_img, train_label, test_img, test_label)


casese = 5 # 有五種分類

model = Sequential([
    Conv2D(64, 3, activation='relu', input_shape=(picture_size,picture_size,1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(32, 3, activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(casese, activation='softmax')
])

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=20)

# 將訓練好的model儲存成json及h5檔
import json
model_json = model.to_json()
with open("model_trained.json", "w") as json_file:
    json.dump(model_json, json_file)
model.save("model_trained.h5")
