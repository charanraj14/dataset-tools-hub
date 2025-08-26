import streamlit as st
import os
import shutil
import random
from pathlib import Path

def split_dataset(dataset_dir, output_dir, split_ratio):
    image_extensions = ['.jpg', '.jpeg', '.png']
    total_train, total_val = 0, 0

    # Ensure output folders exist
    for split in split_ratio.keys():
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    # Case 1: flat folder with images
    images = [f for f in os.listdir(dataset_dir) if Path(f).suffix.lower() in image_extensions]

    if images:
        random.shuffle(images)
        n = len(images)
        n_train = int(split_ratio['train'] * n)
        n_val = n - n_train

        splits = {
            'train': images[:n_train],
            'val': images[n_train:n_train + n_val],
        }

        progress = st.progress(0)
        done = 0
        for split, split_images in splits.items():
            target_dir = os.path.join(output_dir, split)
            os.makedirs(target_dir, exist_ok=True)
            for img_name in split_images:
                shutil.copy2(os.path.join(dataset_dir, img_name),
                             os.path.join(target_dir, img_name))
                done += 1
                progress.progress(done / n)

        total_train, total_val = n_train, n_val

    else:  # Case 2: class subfolders
        for class_folder in os.listdir(dataset_dir):
            class_path = os.path.join(dataset_dir, class_folder)
            if not os.path.isdir(class_path):
                continue

            images = [f for f in os.listdir(class_path) if Path(f).suffix.lower() in image_extensions]
            random.shuffle(images)

            n = len(images)
            n_train = int(split_ratio['train'] * n)
            n_val = n - n_train

            splits = {
                'train': images[:n_train],
                'val': images[n_train:n_train + n_val],
            }

            progress = st.progress(0)
            done = 0
            for split, split_images in splits.items():
                target_dir = os.path.join(output_dir, split, class_folder)
                os.makedirs(target_dir, exist_ok=True)
                for img_name in split_images:
                    shutil.copy2(os.path.join(class_path, img_name),
                                 os.path.join(target_dir, img_name))
                    done += 1
                    progress.progress(done / n)

            total_train += n_train
            total_val += n_val

    return total_train, total_val


# ---- Streamlit UI ----
st.title("📂 Dataset Splitter")
st.write("""### 📂 5. Dataset Splitter (Classification)
Split classification datasets (folder per class) into **train/val/test** sets.  
Each split will keep the **class folder structure intact**.  

**📝 How it Works:**
- Provide dataset path (with class subfolders).  
- Choose **split ratios** (e.g., 70/30).  
- Data will be reorganized into `train/`, `val/`, and `test/` folders, each containing class subfolders.  

---""")
dataset_dir = st.text_input("Enter Dataset Directory Path:")
output_dir = st.text_input("Enter Output Directory Path:")

col1, col2 = st.columns(2)
with col1:
    train_ratio = st.number_input("Train Ratio", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
with col2:
    val_ratio = st.number_input("Validation Ratio", min_value=0.0, max_value=1.0, value=0.3, step=0.1)

if st.button("🚀 Split Dataset"):
    if not dataset_dir or not output_dir:
        st.error("⚠️ Please enter both dataset and output paths")
    elif round(train_ratio + val_ratio, 2) != 1.0:
        st.error("⚠️ Train + Validation ratios must sum to 1.0")
    else:
        with st.spinner("Splitting dataset..."):
            train_count, val_count = split_dataset(dataset_dir, output_dir, {"train": train_ratio, "val": val_ratio})
        st.success("✅ Dataset split complete!")
        st.info(f"📊 Final Count → Train: {train_count}, Validation: {val_count}")
