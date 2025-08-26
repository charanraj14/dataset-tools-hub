import os
from PIL import Image
import streamlit as st

def delete_small_images(root_folder, min_width=None, min_height=None):
    deleted_count = 0
    kept_count = 0
    checked_count = 0
    logs = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                checked_count += 1

                # --- Check Conditions ---
                delete_flag = False
                if min_width and width < min_width:
                    delete_flag = True
                if min_height and height < min_height:
                    delete_flag = True

                if delete_flag:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        logs.append(f"🗑️ Deleted: {file_path} (W:{width}px, H:{height}px)")
                    except Exception as del_err:
                        logs.append(f"⚠️ Could not delete {file_path} - {del_err}")
                else:
                    kept_count += 1
                    logs.append(f"✅ Kept: {file_path} (W:{width}px, H:{height}px)")
            except Exception as e:
                logs.append(f"❌ Not an image or unreadable: {file_path} - {e}")

    return checked_count, deleted_count, kept_count, logs


# ================= STREAMLIT APP =================
st.header("🖼️ Dataset Sanitizer (Resolution-based)")

# st.write("""
# This tool checks all images in a folder (including subfolders) and deletes images
# whose **width and/or height are below thresholds**.  

# ### ✅ Use Cases:
# - Clean datasets by removing low-resolution images.  
# - Filter out tiny thumbnails before training a model.  
# - Ensure image quality standards.  
# """)

st.write("This helps you filter out low-resolution or unusable images before training a model.")

st.write("""
### 📝 How it Works:
- If you leave both fields **empty (0)** → nothing will be deleted.  
- If you enter only **Minimum Width** → images smaller than that width will be deleted.  
- If you enter only **Minimum Height** → images smaller than that height will be deleted.  
- If you enter **both Width & Height** → images smaller than either dimension will be deleted.  


""")


folder = st.text_input("Enter the root folder path:")
min_width = st.number_input("Minimum width (px)", min_value=0, value=0)
min_height = st.number_input("Minimum height (px)", min_value=0, value=0)

if st.button("Run Cleaner"):
    if folder.strip():
        checked, deleted, kept, logs = delete_small_images(
            folder, 
            min_width if min_width > 0 else None, 
            min_height if min_height > 0 else None
        )
        st.success(f"✔ Checked: {checked}, Deleted: {deleted}, Kept: {kept}")
        
        with st.expander("📜 Detailed Logs"):
            for log in logs:
                st.write(log)
    else:
        st.error("Please enter a valid folder path.")
