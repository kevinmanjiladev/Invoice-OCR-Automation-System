import cv2
import os
from src.utils.file_ops import ensure_dir
from config.settings import CLEANED_DIR
from src.utils.logger import get_logger

logger=get_logger(__name__)

def preprocess(image_path):
    logger.info(f'Preprocessing: {image_path}')
    img=cv2.imread(image_path)
    if img is None:
        logger.error(f"Could not read image: {image_path}")
        return None
    # Convert to grayscale — removes color noise, makes text sharper
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Deskew or denoise
    denoised=cv2.fastNlMeansDenoising(gray,h=10)

    # Thresholding — makes text black, background white (better for OCR)
    _,thresh=cv2.threshold(denoised,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    ensure_dir(CLEANED_DIR)

    filename=os.path.basename(image_path)
    save_path=f"{CLEANED_DIR}/{filename}"
    cv2.imwrite(save_path,thresh)

    logger.info(f"Saved cleaned image:{save_path}")
    return thresh


