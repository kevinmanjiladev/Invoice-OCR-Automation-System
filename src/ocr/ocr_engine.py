from paddleocr import PaddleOCR
from src.utils.logger import get_logger

logger=get_logger(__name__)

ocr=PaddleOCR(use_angle_cls=True,lang="en",show_log=False)

def run_ocr(image):
    logger.info("Running OCR...✅")
    result=ocr.ocr(image,cls=True)

    lines=[]
    for block in result:
        for line in block:
            text=line[1][0]
            confidence=line[1][1]
            if confidence>0.5:
                lines.append(text)
    
    logger.info(f"OCR Extracted {len(lines)} lines")
    return lines