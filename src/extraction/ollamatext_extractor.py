import json
import copy
import re
import requests
from src.utils.logger import get_logger
from src.extraction.schema import invoice_schema

logger=get_logger(__name__)

OLLAMA_URL="http://localhost:11434/api/generate"
OLLAMA_MODEL="llama3.2:latest"

def clean_numeric_commas(raw):
    # Removes commas inside numbers: 32,250.4 → 32250.4
    # Matches pattern: digit,digit inside a JSON value
    return re.sub(r'(\d),(\d)', r'\1\2', raw)

def extract_fields(text):
    data=copy.deepcopy(invoice_schema)

    prompt=f"""You are an invoice data extractor. Return ONLY a JSON object, nothing else.
Do not write any explanation, intro, or markdown. Do not use ```json blocks.
Just output the raw JSON and nothing else.

Extract these fields from the invoice text:
- invoice_number
- date
- vendor
- total_amount
- gst
- items (list of objects with: description, quantity, unit_price, amount)

If a field is not found, use null.

Invoice text:
{text}

Output only this JSON:
{{"invoice_number": null, "date": null, "vendor": null, "total_amount": null, "gst": null, "items": []}}"""

    try:
        response=requests.post(
            OLLAMA_URL,
            json={
                "model":OLLAMA_MODEL,
                "prompt":prompt,
                "stream":False
            },
            timeout=60
        )
        response.raise_for_status()

        raw=response.json().get("response","")
        logger.info(f"Ollama raw response: {raw}")

        # Strip markdown code blocks if model wraps in ```json ... ```
        raw=raw.strip()
        if raw.startswith("```"):
            raw=raw.split("```")[1]
            if raw.startswith("json"):
                raw=raw[4:]

        start=raw.find('{')
        end=raw.rfind('}')+1
        if start==-1 or end==0:
            logger.error("No JSON found in Ollama response")
            return data

        raw=clean_numeric_commas(raw[start:end])

        extracted=json.loads(raw)
        for key in data:
            if key in extracted:
                data[key]=extracted[key]

        logger.info(f"Ollama extracted: {data}")

    except requests.exceptions.ConnectionError:
        logger.error("Ollama is not running. Start it with: ollama serve")
    except json.JSONDecodeError as e:
        logger.error(f"Ollama returned invalid JSON: {e} | raw: {raw}")
    except Exception as e:
        logger.error(f"Ollama extraction failed: {e}")

    return data