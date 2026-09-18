import numpy as np
import tensorflow as tf
from PIL import Image


MODEL_PATH = "models/AgriSmart_Plant_Disease_Model.keras"

cnn_model = tf.keras.models.load_model(MODEL_PATH)


class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]


def predict_plant_image(image):
    img = image.resize((224, 224))

    img_array = np.asarray(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    predictions = cnn_model.predict(img_array, verbose=0)

    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]
    confidence = float(predictions[0][predicted_index])

    top_3_indices = np.argsort(predictions[0])[-3:][::-1]

    top_3 = []

    for index in top_3_indices:
        top_3.append({
            "class": class_names[index],
            "probability": float(predictions[0][index])
        })

    return {
        "plant_disease": predicted_class,
        "disease_confidence": confidence,
        "top_3_predictions": top_3
    }