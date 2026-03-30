import streamlit as st 
from PIL import Image 
from pipeline import process_image, model, mocr, lama, trans
import tempfile
import os
import io

st.title("MANGA")
 
uploaded = st.file_uploader("Загрузи страницу манги", type=["jpg", "png"])

if uploaded is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name
    image = Image.open(tmp_path)
    st.image(image)
    
    clicked = st.button("Перевести")
    if clicked:
        result = process_image(tmp_path, model, mocr, lama, trans)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Оригинал")
            st.image(image)
        with col2:
            st.header("Перевод")
            st.image(result)
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            buf.seek(0)
            st.download_button("Скачать", buf, "result.png", "image/png")