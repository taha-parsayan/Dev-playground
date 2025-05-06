import os
import shutil
import pandas as pd

def copy_data(image_type, excel_file, source_root="ADNI", source_dir="../", destination_root="Data", categories=["AD", "MCI", "NC"]):
    # Create Data/train/{category}, Data/test/{category}, and Data/valid/{category} directories
    os.makedirs(os.path.join(destination_root, 'train'), exist_ok=True)
    os.makedirs(os.path.join(destination_root, 'test'), exist_ok=True)
    os.makedirs(os.path.join(destination_root, 'valid'), exist_ok=True)

    for category in categories:
        os.makedirs(os.path.join(destination_root, 'train', category), exist_ok=True)
        os.makedirs(os.path.join(destination_root, 'test', category), exist_ok=True)
        os.makedirs(os.path.join(destination_root, 'valid', category), exist_ok=True)

    # Read Excel file and process each sheet
    xls = pd.ExcelFile(excel_file)

    for category in categories:
        if category in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=category, dtype=str)  # Read subject IDs as strings
            subject_ids = df.iloc[:, 0].tolist()  # Get the list of subject IDs

            # Sort subject_ids to ensure consistency
            subject_ids.sort()

            # Calculate split sizes
            total_subjects = len(subject_ids)
            train_size = int(0.75 * total_subjects)
            test_size = int(0.15 * total_subjects)

            # Split the data into train, test, and valid sets (75% for train, 15% for test, 15% for valid)
            train_ids = subject_ids[:train_size]
            test_ids = subject_ids[train_size:train_size + test_size]
            valid_ids = subject_ids[train_size + test_size:]

            # Copy train set
            for subject_id in train_ids:
                src_file = os.path.join(source_dir, category, source_root, subject_id, image_type + '.nii')
                dest_file = os.path.join(destination_root, 'train', category, f"{subject_id}{image_type}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

            # Copy test set
            for subject_id in test_ids:
                src_file = os.path.join(source_dir, category, source_root, subject_id, image_type + '.nii')
                dest_file = os.path.join(destination_root, 'test', category, f"{subject_id}{image_type}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

            # Copy valid set
            for subject_id in valid_ids:
                src_file = os.path.join(source_dir, category, source_root, subject_id, image_type + '.nii')
                dest_file = os.path.join(destination_root, 'valid', category, f"{subject_id}{image_type}.nii")

                if os.path.exists(src_file):
                    shutil.copy(src_file, dest_file)
                    print(f"Copied: {src_file} → {dest_file}")
                else:
                    print(f"Missing: {src_file}")

    print("✅ Done! Train/Test/Validation split is complete for all categories.")
