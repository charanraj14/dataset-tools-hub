import streamlit as st
import os
import glob
import shutil
import random

st.title("📂 Image Normalizer per Class")
st.write("""
This tool helps you **balance your dataset** by limiting the number of images per class.  

### 📝 How it Works:
- Provide the **input dataset folder** (must contain subfolders for each class).  
- Provide an **output folder** (normalized dataset will be saved here).  
- Enter the **maximum number of images per class (THRESH)**.  
- The tool will randomly pick up to that many images from each class and copy them into the output folder.  
""")

# --- User Inputs ---
path_to_dir = st.text_input("Enter Input Dataset Directory:")
path_to_save = st.text_input("Enter Output Directory:")
THRESH = st.number_input("Max Images per Class (THRESH):", min_value=1, value=1000)

if st.button("🚀 Normalize Dataset"):
    if not path_to_dir or not path_to_save:
        st.error("⚠️ Please provide both input and output paths")
    else:
        class_names = os.listdir(path_to_dir)
        t_cls = len(class_names)
        c_cls = 0
        total_copied = 0

        progress = st.progress(0)
        status = st.empty()

        for class_name in class_names:
            c_cls += 1
            img_list = glob.glob(f"{path_to_dir}/{class_name}/*.jpg")
            random.shuffle(img_list)
            total_c = len(img_list)
            c = 0

            for img_path in img_list:
                os.makedirs(f"{path_to_save}/{class_name}", exist_ok=True)
                shutil.copy(img_path, f"{path_to_save}/{class_name}")
                c += 1
                total_copied += 1

                # Update progress
                progress.progress(min(int((c_cls/t_cls)*100), 100))
                status.text(f"📌 Processing class {c_cls}/{t_cls} → Copied {c}/{total_c} images")

                if c == THRESH:
                    break

        st.success(f"✅ Done! Copied {total_copied} images into {path_to_save}")
