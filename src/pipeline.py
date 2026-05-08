from src.preprocessing.preprocess import preprocess
from src.ocr.ocr_engine import run_ocr
from src.ocr.text_utils import merge_lines,clean_text
from src.extraction.ollamatext_extractor import extract_fields
from src.storage.mysql_store import store_invoice
from src.storage.save_json import save_to_json
from config.settings import SAVE_JSON_OUTPUT,SAVE_MYSQL
from src.utils.logger import get_logger

logger=get_logger(__name__)

def run_pipeline(image_path):
    logger.info(f"Starting pipeline for: {image_path}")

    # 1.clean image
    cleaned=preprocess(image_path)
    if cleaned is None:
        return None
    
    # 2.Run ocr
    lines=run_ocr(cleaned)

    # 3.Merge and clean the text
    raw_text=merge_lines(lines)
    text=clean_text(raw_text)

    # 4.Extract fields using ollama
    data=extract_fields(text)

    # 5.Save outputs
    filename=image_path.split("/")[-1].replace(".jpg",".json").replace(".png",".json")

    if SAVE_JSON_OUTPUT:
        save_to_json(data,filename)
    if SAVE_MYSQL:
        store_invoice(data)

    logger.info("Pipeline Complete")
    return data