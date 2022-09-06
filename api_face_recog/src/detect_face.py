import cv2
import numpy as np
from .utils import *


def get_face_detect_data(data):
    nparr = np.fromstring(base64_decode(data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # image_data = detectImage(img)
    image_data = img
    return base64_encode(image_data)