import streamlit as st
import cv2
import os
from streamlit_image_zoom import image_zoom

st.title("🖼️ Image Resizer Tool with Zoom & Pan")

# === Inputs from user ===
image_path = st.text_input("📄 Enter Image Path:")
width = st.number_input("Desired Width", min_value=1, value=640)
height = st.number_input("Desired Height", min_value=1, value=640)

if st.button("🚀 Resize Image"):
    if not image_path:
        st.error("⚠️ Please provide a valid image path")
    else:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            st.error("❌ Error: Image not found at given path.")
        else:
            # Resize image
            resized_image = cv2.resize(image, (width, height))

            # Auto-generate output filename
            base, ext = os.path.splitext(image_path)
            output_path = base + f"_resized{ext}"

            # Save resized image
            cv2.imwrite(output_path, resized_image)
            st.success(f"✅ Resized image saved at: {output_path}")

            # Show image with zoom + pan enabled
            st.subheader("🔍 Interactive View (Zoom & Drag)")
            image_zoom(resized_image)  # scroll to zoom, drag to pan
