# Invoice OCR Automation System 🧾
> Automated Invoice Data Extraction using OCR + Local AI

InvoiceIQ is a local AI-powered invoice processing system. Upload any invoice image and it automatically extracts key fields — invoice number, date, vendor, total amount, GST, and line items — then saves the result as JSON and stores it in a MySQL database.

---

## Features

- 📷 Image preprocessing with OpenCV (grayscale, denoise, threshold)
- 🔍 OCR text extraction using PaddleOCR
- 🤖 AI-powered field extraction using Ollama (runs 100% locally, no API key needed)
- 💾 Saves structured output as JSON
- 🗄️ Stores extracted data into MySQL database
- 🌐 Clean web interface built with Streamlit

---

## Project Structure

```
INVOICE_OCR_AUTOMATION_SYSTEM/
│
├── app.py                        # CLI runner
├── requirements.txt
├── README.md
│
├── config/
│   ├── db_config.py              # MySQL connection helper
│   └── settings.py               # Global paths and feature flags
│
├── src/
│   ├── preprocessing/
│   │   └── preprocess.py         # OpenCV image cleaning
│   │
│   ├── ocr/
│   │   ├── ocr_engine.py         # PaddleOCR wrapper
│   │   └── text_utils.py         # Merge and clean OCR lines
│   │
│   ├── extraction/
│   │   ├── ollamatext_extractor.py  # Ollama LLM field extractor
│   │   └── schema.py             # Invoice field schema
│   │
│   ├── storage/
│   │   ├── save_json.py          # Save output as JSON
│   │   └── mysql_store.py        # Insert into MySQL
│   │
│   ├── utils/
│   │   ├── logger.py             # Logging setup
│   │   └── file_ops.py           # File helper functions
│   │
│   └── pipeline.py               # Connects all steps end-to-end
│
├── streamlit_app/
│   └── ui.py                     # Streamlit web interface
│
├── samples/
│   ├── raw/                      # Drop invoice images here
│   └── processed/                # OpenCV cleaned images
│
└── outputs/
    ├── extracted_json/           # Extracted invoice JSON files
    ├── cleaned_images/           # Saved preprocessed images
    └── logs/                     # Runtime logs (app.log)
```

---

## Requirements

- Python 3.9+
- MySQL server running locally
- [Ollama](https://ollama.com) installed and running

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourname/InvoiceIQ.git
cd InvoiceIQ
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Pull the Ollama model**
```bash
ollama pull llama3.2
```

**5. Set up MySQL**

Create the database and table:
```sql
CREATE DATABASE invoices;

USE invoices;

CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(100),
    date DATE,
    vendor VARCHAR(255),
    total_amount VARCHAR(50),
    gst VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**6. Update database credentials**

Edit `config/db_config.py` with your MySQL username and password.

---

## Usage

**Run the Streamlit web app**
```bash
streamlit run streamlit_app/ui.py
```
Then open http://localhost:8501 in your browser, upload an invoice image, and click **Extract Fields**.

**Run from the command line**
```bash
# Single invoice
python app.py samples/raw/invoice.jpg

# All invoices in the samples/raw folder
python app.py
```

---

## How It Works

```
Invoice Image
     ↓
OpenCV Preprocessing   →  grayscale, denoise, threshold
     ↓
PaddleOCR              →  extracts raw text lines
     ↓
Ollama (llama3.2)      →  understands text, returns structured JSON
     ↓
Save JSON              →  outputs/extracted_json/
     ↓
MySQL Insert           →  invoices table
```

---

## Configuration

All settings are in `config/settings.py`:

| Setting | Default | Description |
|---|---|---|
| `SAVE_JSON_OUTPUT` | `True` | Save extracted data as JSON |
| `SAVE_MYSQL` | `True` | Insert into MySQL |
| `IMAGE_DIR` | `samples/raw` | Input invoice folder |
| `OUTPUT_JSON_DIR` | `outputs/extracted_json` | JSON output folder |
| `LOG_DIR` | `outputs/logs` | Log file location |

To switch Ollama model, edit `src/extraction/ollamatext_extractor.py`:
```python
OLLAMA_MODEL = "llama3.2:latest"   # or gemma3:1b, mistral, etc.
```

---

## Dependencies

| Library | Purpose |
|---|---|
| `opencv-python` | Image preprocessing |
| `paddleocr` | OCR text extraction |
| `requests` | Communicate with Ollama API |
| `mysql-connector-python` | MySQL database connection |
| `streamlit` | Web interface |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'src'`**
Always run from the project root folder, not from inside a subfolder.

**`model not found` error**
Run `ollama list` to see available models, then update `OLLAMA_MODEL` in `ollamatext_extractor.py`.

**`Ollama is not running`**
Ollama starts automatically on boot. If it's not running: `ollama serve`

**All fields are NULL**
Check `outputs/logs/app.log` for the raw Ollama response to debug.

---

## Author

Kevin Manjila 
Built with PaddleOCR + Ollama + Streamlit