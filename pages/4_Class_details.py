import streamlit as st
import os
from collections import defaultdict
from ultralytics import YOLO

st.title("📊 Dataset Class Counter")
st.write("""
Quickly count **number of images per class** in your dataset (classification or YOLO).  

**📝 How it Works:**
- Provide the **YOLO model path (.pt)** and the **dataset folder path**.  
- The tool will analyze and show the **distribution of images per class**.  
- Helps check if your dataset is **imbalanced** before training.  

---
""")
# --- User Inputs ---
model_path = st.text_input("Enter YOLO Model Path (.pt):")
dataset_dir = st.text_input("Enter Dataset Directory Path:")

if st.button("🔍 Count Images"):
    if not model_path or not dataset_dir:
        st.error("⚠️ Please provide both model path and dataset directory")
    else:
        # Load your trained model
        model = YOLO(model_path)

        # Get class names
        class_names = model.names
        st.write(f"### Number of Classes: {len(class_names)}")
        st.write(f"### Class Names: {class_names}")

        # Dictionary for counting
        class_counts = defaultdict(int)

        # Walk through dataset and count images per class
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                    class_label = os.path.basename(root)
                    class_counts[class_label] += 1

        # Print results
        st.subheader("Image Counts per Class")
        for cls in class_names.values():
            st.write(f"**{cls}** : {class_counts.get(cls, 0)} images")
