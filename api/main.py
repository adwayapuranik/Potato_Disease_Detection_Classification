# from fastapi import FastAPI, File, UploadFile
# import uvicorn
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# app = FastAPI()


# #MODEL = tf.keras.models.load_model("../models/1")
# MODEL = tf.keras.layers.TFSMLayer("../saved_models/1", call_endpoint="serving_default")
# CLASS_NAMES = ["Potato__Early_blight", "Potato__Late_blight", "Potato__healthy"]

# @app.get("/ping")
# async def ping():
#     return "hello I am alive"

# def read_file_as_image(data) -> np.ndarray:
#     image = np.array(Image.open(BytesIO(data)))
#     return image

# @app.post("/predict")
# async def predict(
#         file: UploadFile = File(...)
# ):
#     image = read_file_as_image(await file.read())
#     img_batch = np.expand_dims(image, 0)

#     predictions = MODEL(img_batch)

#     prediction_tensor = predictions['output_0']
#     prediction_array = prediction_tensor.numpy()

#     # Find the predicted class and confidence
#     predicted_class = CLASS_NAMES[np.argmax(prediction_array[0])]
#     confidence = np.max(prediction_array[0])

#     return {
#         'class': predicted_class,
#         'confidence': float(confidence),
#     }

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8001)

from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = FastAPI()

# Assuming your TensorFlow Serving endpoint is running and serving the model
MODEL = tf.keras.layers.TFSMLayer("../saved_models/1", call_endpoint="serving_default")

CLASS_NAMES = ["Potato__Early_blight", "Potato__Late_blight", "Potato__healthy"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive!"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    # Ensure that MODEL returns predictions in the expected format
    predictions = MODEL(img_batch)

    # Assuming the model returns a dictionary with keys like 'output_0'
    prediction_tensor = predictions['output_0']
    prediction_array = prediction_tensor.numpy()

    # Find the predicted class and confidence
    predicted_class = CLASS_NAMES[np.argmax(prediction_array[0])]
    confidence = float(np.max(prediction_array[0]))

    return {
        'class': predicted_class,
        'confidence': confidence,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
