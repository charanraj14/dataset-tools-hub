import streamlit as st

st.title("🧰 Dataset Tools Hub")

st.write("A collection of simple utilities to clean, organize, and balance datasets for ML projects.")

st.markdown("### 📂 1. Detection Dataset Splitter")
st.text("Split YOLO-format datasets into train/val/test with images & labels.")

st.markdown("### ⚖️ 2. Dataset Normalizer")
st.text("Balances dataset by limiting the maximum number of images per class.")

st.markdown("### 🖼️ 3. Dataset Sanitizer (Resolution-based)")
st.text("Removes low-resolution images below a chosen width/height threshold.")

st.markdown("### 📊 4. Dataset Class Counter")
st.text("Counts number of images per class in a dataset.")

st.markdown("### 🏷️ 5. Classification Dataset Splitter")
st.text("Splits classification datasets into train/val/test folders.")

st.write("---")
st.info("Select a tool from the sidebar to get started 🚀")
