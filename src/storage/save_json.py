import os
import json
from src.utils.logger import get_logger
from config.settings import OUTPUT_JSON_DIR

logger=get_logger(__name__)
def save_to_json(data,filename):
    os.makedirs(OUTPUT_JSON_DIR,exist_ok=True)
    filepath=os.path.join(OUTPUT_JSON_DIR,filename)

    with open(filepath,"w") as f:
        json.dump(data,f,indent=4)

    logger.info(f"Saved JSON:{filepath}")
    return filepath
