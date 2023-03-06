import os
import cv2
import numpy as np
import tensorflow as tf

from matplotlib import pyplot as plt
import matplotlib.cm as cm

import pickle
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

# model import 
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet import ResNet101, ResNet152
from tensorflow.keras.applications import EfficientNetB0, efficientnet_v2

from tensorflow.keras import datasets, layers, models
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Input, Dropout, BatchNormalization, Activation, Conv2D, GlobalAveragePooling2D, Average
import matplotlib.pyplot as plt
import tensorflow.keras.backend as K
from tensorflow.keras.models import Model
from tensorflow.keras.utils import get_custom_objects

from sklearn.model_selection import train_test_split
from PIL import Image
from skimage import color
from skimage import io
import time

'''!pip install split-folders
!pip install -U keras-efficientnet-v2
!pip install -U git+https://github.com/leondgarse/keras_efficientnet_v2'''

# Google TPU Install
resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])

tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.TPUStrategy(resolver)

# Data mount from google drive
from google.colab import drive
drive.mount('/content/drive')

folder_path = '/content/drive/MyDrive/imageRec_data/Training'
label_names = os.listdir(folder_path)
label_names

# Load train data
path = '/content/drive/MyDrive/imageRec_data'

# 서브 디렉토리 목록 출력
for root, subdirs, files in os.walk(path):
    for d in subdirs:
        fullpath = root + '/' + d
        print(fullpath)

# 서브 디렉토리별 파일 개수 출력
for root, subdirs, files in os.walk(path):
    if len(files) > 0:
        print(root, len(files))
        
folder_path = '/content/drive/MyDrive/imageRec_data/Training'
dataset = {}

# 이미지와 라벨 리스트에 담기
for label in os.listdir(folder_path):
    sub_path = folder_path+'/'+label+'/'
    dataset[label] = []
    for filename in os.listdir(sub_path):
        dataset[label].append(sub_path+filename)

dataset


# Image Preprocessing
label2index = {'seg0' : 0, 'seg1' : 1 , 'seg2' : 2}
labels = list(label2index.keys())
labels


## Resize with padding
'''
!mkdir resized
!mkdir resized/seg0
!mkdir resized/seg1
!mkdir resized/seg2'''

dataset.items() # dataset 확인

for label, filenames in dataset.items():
    for filename in filenames:
        img = cv2.imread(filename)

        percent = 1
        if(img.shape[1] > img.shape[0]):
            percent = 128/img.shape[1]
        else:
            percent = 128/img.shape[0]

        img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)

        y,x,h,w = (0,0,img.shape[0], img.shape[1])

        w_x = (128-(w-x))/2
        h_y = (128-(h-y))/2

        if(w_x < 0):
            w_x = 0
        elif(h_y < 0):
            h_y = 0

        M = np.float32([[1,0,w_x], [0,1,h_y]])
        img_re = cv2.warpAffine(img, M, (128, 128)) 
       
        cv2.imwrite('/content/resized/{0}/{1}'.format(label, filename.split("/")[-1]) , img_re)
        
path = '/content/resized'

# 서브 디렉토리 목록 출력
for root, subdirs, files in os.walk(path):
    for d in subdirs:
        fullpath = root + '/' + d
        print(fullpath)

# 서브 디렉토리별 파일 개수 출력
for root, subdirs, files in os.walk(path):
    if len(files) > 0:
        print(root, len(files))

        
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
)


folder_path

for label in  os.listdir(folder_path):
    label_path = folder_path + '/' + label + '/'
    for filename in os.listdir(label_path): 
        filepath = label_path + filename

        img = load_img(filepath)
        x = img_to_array(img)

        x = x.reshape((1,) + x.shape)
        
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=label_path, save_prefix=label, save_format='jpg'):
            i += 1
            if i > 2:
                break  
                
