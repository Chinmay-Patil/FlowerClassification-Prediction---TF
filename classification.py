# -*- coding: utf-8 -*-
"""Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NejN8BLbBcCrfiw0_ibbsGHX1QaGh6zE
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

from __future__ import  absolute_import,division,print_function,unicode_literals

import numpy as np  #Multidimensional Calculations
import pandas as pd #Data Analytics 
import tensorflow as tf

CSV_COLUMN_NAMES = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

train_path = tf.keras.utils.get_file(
    "iris_training.csv", "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv")
test_path = tf.keras.utils.get_file(
    "iris_test.csv", "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv")

train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)

train_y = train.pop("Species")
test_y = test.pop("Species")

def input_fn(features,label,training= True,batch_size = 256):

  dataset = tf.data.Dataset.from_tensor_slices((dict(features), label ))

  if training:
      dataset = dataset.shuffle(1000).repeat()
    
  return dataset.batch(batch_size)

feature_columns=[]

for key in train.keys():
  feature_columns.append(tf.feature_column.numeric_column(key=key))

classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,hidden_units=[30,10],n_classes= 3)

classifier.train(
    
    input_fn = lambda : input_fn(train,train_y,training = True),steps = 5000
)

eval_result = classifier.evaluate(input_fn = lambda : input_fn(test,test_y,training = True),steps = 5000)

print(f'Eval result is {eval_result}')

def input_fnn(features, batch_size = 256):

  return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

features = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
predict = {}


print("please print the values as prompted")

for feature in features:
   valid =True
   while valid:
     value = input(feature + ":")
     if not value.isdigit(): valid = False
   predict[feature] = [float(value)]

predictions = classifier.predict(input_fn=lambda: input_fnn(predict))
for pred_dict in predictions:
    class_id = pred_dict['class_ids'][0]
    probability = pred_dict['probabilities'][class_id]

    print('Prediction is "{}" ({:.1f}%)'.format(
        SPECIES[class_id], 100 * probability))