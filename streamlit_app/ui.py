import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import tempfile
from src.pipeline import run_pipeline

st.set_page_config(page_title="Invoice OCR", page_icon="🧾")
st.title("🧾 Invoice OCR System")
st.write("Upload an invoice image to extract its fields automatically.")

uploaded = st.file_uploader("Upload Invoice", type=["jpg", "jpeg", "png"])

if uploaded:
    # Save upload to a temp file so pipeline can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    st.image(tmp_path, caption="Uploaded Invoice", use_column_width=True)

    if st.button("Extract Fields"):
        with st.spinner("Processing..."):
            result = run_pipeline(tmp_path)

        if result:
            st.success("Extraction complete!")
            st.json(result)
        else:
            st.error("Could not process this image. Check the logs.")

        os.unlink(tmp_path)  # Clean up temp file