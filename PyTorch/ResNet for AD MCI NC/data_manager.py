import os
import shutil
import pandas as pd

def copy_data(excel_file, source_root="ADNI", destination_root="Data", categories=["AD", "MCI", "NC"]):
    # Create Data/train/{category} and Data/test/{category} directories
    os.makedirs(os.path.join(destination_root, 'train'), exist_ok=True)
    os.makedirs(os.path.join(destination_root, 'test'), exist_ok=True)

    for category in categories:
        os.makedirs(os.path.join(destination_root, 'train', category), exist_ok=True)
        os.makedirs(os.path.join(destination_root, 'test', category), exist_ok=True)

    # Read Excel file and process each sheet
    xls = pd.ExcelFile(excel_file)

    for category in categories:
        if category in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=category, dtype=str)  # Read subject IDs as strings
            subject_ids = df.iloc[:, 0].tolist()  # Get the list of subject IDs

            # Sort subject_ids to ensure consistency
            subject_ids.sort()

            # Divide into 5 equal sections
            split_size = len(subject_ids) // 5
            sections = [subject_ids[i * split_size: (i + 1) * split_size] for i in range(5)]

            # The last section gets any remaining subjects (in case of uneven division)
            sections[-1].extend(subject_ids[5 * split_size:])

            # Use the first 2 sections for testing, the remaining 3 sections for training
            test_ids = [subject_id for section in sections[:1] for subject_id in section]  # First 1 sections for testing
            train_ids = [subject_id for section in sections[1:] for subject_id in section]  # Remaining 4 sections for training

            # Copy test set
            for subject_id in test_ids:
                src_file = os.path.join("../", category, source_root, subject_id, "GM.nii")
                dest_file = os.path.join(destination_root, 'test', category, f"{subject_id}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

            # Copy train set
            for subject_id in train_ids:
                src_file = os.path.join("../", category, source_root, subject_id, "GM.nii")
                dest_file = os.path.join(destination_root, 'train', category, f"{subject_id}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

    print("✅ Done! Train/Test split is balanced across all categories.")

'''
Usage Example:

excel_file = "../Subject list.xlsx"
source_root = "ADNI"
destination_root = "Data"
categories = ["AD", "MCI", "NC"]

copy_data(excel_file, source_root, destination_root, categories)
'''
