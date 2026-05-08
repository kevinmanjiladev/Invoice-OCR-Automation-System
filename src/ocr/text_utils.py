def merge_lines(lines):
    # Join all OCR lines into one big string for regex to search through
    return "\n".join(lines)

def clean_text(text):
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)