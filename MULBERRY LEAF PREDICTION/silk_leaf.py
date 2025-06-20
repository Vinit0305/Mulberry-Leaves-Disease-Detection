import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

filepath = 'model2.h5'
model = load_model(filepath)
print("Model Loaded Successfully")

def pred_leaf_diseases(tomato_plant):
  test_image = load_img(tomato_plant, target_size=(128, 128))
  print("Got Image for prediction")
  test_image = img_to_array(test_image)/255
  test_image = np.expand_dims(test_image, axis=0)
  result = model.predict(test_image)
  print('Raw result = ', result)
  pred = np.argmax(result, axis=1)[0]
  print("Prediction:", pred)
  for i in result:
     if 'e' in str(i):
         return "leaf is healthy", 'error.html'
     else:
        if pred==0:
            return "Leaf rust disease", 'index_leaf.html'
        elif pred==1:
            return "Leaf Spot Disease", 'index_leaf.html'
        elif pred==2:
            return "Mulberry Stem Canker", 'index_leaf.html'
        elif pred==3:
            return "Powdery Mildew", 'index_leaf.html'
        elif pred==4:
            return "Root Knot Disease", 'index_leaf.html'
