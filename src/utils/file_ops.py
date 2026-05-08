import os
import cv2
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
def save_temp_image(image,path="temp.jpg"):
    cv2.imwrite(path,image)
    return path