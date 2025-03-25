import os
import shutil
import pandas as pd
import random

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

            # Get the list of subject IDs in the category
            subject_ids = df.iloc[:, 0].tolist()

            # Shuffle subject_ids randomly
            random.shuffle(subject_ids)

            # Calculate the number of images for the test set (1/5 of the total images)
            num_test = len(subject_ids) // 5

            # Split into train and test sets
            test_ids = subject_ids[:num_test]
            train_ids = subject_ids[num_test:]

            # Process test set
            for subject_id in test_ids:
                src_file = os.path.join("../", category, source_root, subject_id, "std_T1.nii")
                dest_file = os.path.join(destination_root, 'test', category, f"{subject_id}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

            # Process train set
            for subject_id in train_ids:
                src_file = os.path.join("../", category, source_root, subject_id, "std_T1.nii")
                dest_file = os.path.join(destination_root, 'train', category, f"{subject_id}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

    print("✅ Done! All files copied successfully.")


    '''
    How to usage:
    
    excel_file = "../Subject list.xlsx"
    source_root = "ADNI"
    destination_root = "Data"
    categories = ["AD", "MCI", "NC"]

    DM.copy_data(excel_file,source_root,destination_root,categories)
    '''