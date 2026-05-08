from config.db_config import get_connection
from src.utils.logger import get_logger
from datetime import datetime

logger=get_logger(__name__)

def parse_date(date_str):
    if not date_str:
        return None
    # Try common date formats Ollama might return
    formats=[
        "%d-%b-%Y",   # 12-May-2021
        "%d/%m/%Y",   # 12/05/2021
        "%Y-%m-%d",   # 2021-05-12 (already correct)
        "%d-%m-%Y",   # 12-05-2021
        "%B %d, %Y",  # May 12, 2021
        "%d %B %Y",   # 12 May 2021
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    logger.error(f"Could not parse date: {date_str}")
    return None

def store_invoice(data):
    conn=get_connection()
    if not conn:
        logger.error("Cannot store invoice — DB connection failed")
        return

    cursor=conn.cursor()
    query="""
        INSERT INTO invoices (invoice_number, date, vendor, total_amount, gst)
        VALUES (%s, %s, %s, %s, %s)
    """
    values=(
        data.get("invoice_number"),
        parse_date(data.get("date")),   # convert to YYYY-MM-DD before inserting
        data.get("vendor"),
        data.get("total_amount"),
        data.get("gst")
    )
    cursor.execute(query,values)
    conn.commit()
    logger.info(f"Stored invoice in DB: {data.get('invoice_number')}")
    cursor.close()
    conn.close()