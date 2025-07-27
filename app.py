import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import os
import tempfile
from io import BytesIO
import zipfile

st.title("📄 PDF to Image Converter (ZIP Download)")
st.write("Upload a scanned PDF file. This app will convert each page into a JPEG image and bundle them in a downloadable ZIP.")

uploaded_file = st.file_uploader("Upload your scanned PDF", type=["pdf"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "input.pdf")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("🔄 Converting PDF pages to images...")
        images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir)
        st.success(f"✅ Converted {len(images)} pages.")

        # Convert to ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for i, img in enumerate(images):
                img_byte = BytesIO()
                img.save(img_byte, format="JPEG")
                zipf.writestr(f"page_{i+1}.jpg", img_byte.getvalue())
        zip_buffer.seek(0)

        st.download_button("📥 Download All Images as ZIP", data=zip_buffer, file_name="converted_images.zip", mime="application/zip")
