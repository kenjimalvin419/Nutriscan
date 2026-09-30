import os
import numpy as np
import cv2
import tensorflow as tf

# 1. Path dasar (samakan dengan training)
# BASE_DIR selalu berdasarkan lokasi file ini (notebooks/inference.py)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))     
BASE_DIR = os.path.dirname(THIS_DIR)                      


DATASET_DIR = os.path.join(BASE_DIR, "dataset")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "muac_model_v1.keras")

print("BASE_DIR   :", BASE_DIR)
print("IMAGES_DIR :", IMAGES_DIR)
print("MODELS_DIR :", MODELS_DIR)
print("MODEL_PATH :", MODEL_PATH)

# 2. Load model
from tensorflow import keras
from keras.models import load_model
muac_model = load_model(MODEL_PATH)
print("Model loaded.")

# 3. Fungsi preprocessing (HARUS sama dengan yang dipakai saat training)
IMG_HEIGHT = 224
IMG_WIDTH = 224

def load_and_preprocess_image(img_path, img_height=IMG_HEIGHT, img_width=IMG_WIDTH):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found or unreadable: {img_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_width, img_height))
    img = img.astype("float32") / 255.0   # sama dengan training
    return img

def predict_muac_from_path(img_path: str) -> float:
    """
    Prediksi MUAC (cm) dari path gambar.
    """
    img = load_and_preprocess_image(img_path)
    inp = np.expand_dims(img, axis=0)  # shape jadi (1, 224, 224, 3)
    pred = muac_model.predict(inp, verbose=0)[0][0]
    return float(pred)
