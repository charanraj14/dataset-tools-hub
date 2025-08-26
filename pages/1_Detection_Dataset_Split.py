import streamlit as st
import os
import random
import shutil

# ---------------- Dataset Split Function ----------------
def split_dataset(source_dir, dest_dir, train_ratio, val_ratio, test_ratio, class_names):
    image_dir = os.path.join(source_dir, "images")
    label_dir = os.path.join(source_dir, "labels")

    # Output folders
    train_images = os.path.join(dest_dir, "train", "images")
    train_labels = os.path.join(dest_dir, "train", "labels")
    val_images = os.path.join(dest_dir, "valid", "images")
    val_labels = os.path.join(dest_dir, "valid", "labels")
    test_images = os.path.join(dest_dir, "test", "images")
    test_labels = os.path.join(dest_dir, "test", "labels")

    # Create directories
    os.makedirs(train_images, exist_ok=True)
    os.makedirs(train_labels, exist_ok=True)
    os.makedirs(val_images, exist_ok=True)
    os.makedirs(val_labels, exist_ok=True)
    if test_ratio > 0:
        os.makedirs(test_images, exist_ok=True)
        os.makedirs(test_labels, exist_ok=True)

    # Get all image files
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.png','jpeg'))]
    random.shuffle(image_files)

    n_total = len(image_files)
    n_train = int(train_ratio * n_total)
    n_val = int(val_ratio * n_total)
    n_test = n_total - n_train - n_val

    train_files = image_files[:n_train]
    val_files = image_files[n_train:n_train + n_val]
    test_files = image_files[n_train + n_val:] if test_ratio > 0 else []

    def move_files(file_list, image_dst, label_dst):
        for img_file in file_list:
            label_file = os.path.splitext(img_file)[0] + ".txt"
            img_src_path = os.path.join(image_dir, img_file)
            label_src_path = os.path.join(label_dir, label_file)

            # Copy image
            if os.path.exists(img_src_path):
                shutil.copy(img_src_path, os.path.join(image_dst, img_file))

            # Copy label
            if os.path.exists(label_src_path):
                shutil.copy(label_src_path, os.path.join(label_dst, label_file))

    # Move files
    move_files(train_files, train_images, train_labels)
    move_files(val_files, val_images, val_labels)
    if test_ratio > 0:
        move_files(test_files, test_images, test_labels)

    # Create data.yaml
    yaml_path = os.path.join(dest_dir, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(f"train: {dest_dir}/train/images\n")
        f.write(f"val: {dest_dir}/valid/images\n")
        if test_ratio > 0:
            f.write(f"test: {dest_dir}/test/images\n")
        f.write("\n")
        f.write(f"nc: {len(class_names)}\n")
        f.write(f"names: {class_names}\n")

    return len(train_files), len(val_files), len(test_files)


# ---------------- Streamlit UI ----------------
st.title("📂 YOLO Dataset Splitter")

st.markdown("""
### 📖 How to Use
1. Prepare your dataset folder with **images/** and **labels/** subfolders.  
   Example:  

2. Enter the source dataset path and choose an output folder.  
3. Adjust train/val/test ratios (make sure they sum to 1.0 if test is used).  
4. Select your **classes.names** file (one class per line).  
5. Click **🚀 Split Dataset**.  
6. You'll get train/valid/test folders and a `data.yaml`.  
""")

# Inputs
source_dir = st.text_input("📁 Source Dataset Directory (must contain 'images' and 'labels'):")
dest_dir = st.text_input("📂 Destination Directory:")

col1, col2, col3 = st.columns(3)
with col1:
 train_ratio = st.number_input("Train Ratio", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
with col2:
 val_ratio = st.number_input("Validation Ratio", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
with col3:
 test_ratio = st.number_input("Test Ratio (optional)", min_value=0.0, max_value=1.0, value=0.1, step=0.1)

classes_file = st.text_input("📄 Path to classes.names file:")

if st.button("🚀 Split Dataset"):
 if not source_dir or not dest_dir:
     st.error("⚠️ Please enter both source and destination paths")
 elif round(train_ratio + val_ratio + test_ratio, 2) != 1.0:
     st.error("⚠️ Train + Validation + Test ratios must sum to 1.0")
 elif not classes_file or not os.path.exists(classes_file):
     st.error("⚠️ Please provide a valid classes.names file path")
 else:
     with open(classes_file, "r") as f:
         class_names = [line.strip() for line in f.readlines() if line.strip()]

     with st.spinner("Splitting dataset..."):
         train_count, val_count, test_count = split_dataset(
             source_dir, dest_dir, train_ratio, val_ratio, test_ratio, class_names
         )
     st.success("✅ Dataset split complete!")
     st.info(f"📊 Train: {train_count}, Validation: {val_count}, Test: {test_count}")
