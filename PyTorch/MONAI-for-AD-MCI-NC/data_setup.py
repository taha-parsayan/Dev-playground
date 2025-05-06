"""
Contains functionality for creating PyTorch DataLoaders for 
image classification data with late fusion setup.
"""
import os
import nibabel as nib
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torchvision import transforms
from sklearn.model_selection import train_test_split
import numpy as np
import random

NUM_WORKERS = os.cpu_count()

# Custom dataset for separate PET and MRI processing (Late Fusion)
class MultiModalSeparateNiiDataset(Dataset):
    def __init__(self, data_dir, class_names, transform=None):
        self.data_dir = data_dir
        self.class_names = class_names
        self.transform = transform
        self.data = []

        for class_name in self.class_names:
            class_folder = os.path.join(data_dir, class_name)
            pet_files = [f for f in os.listdir(class_folder) if "SUV" in f]
            for pet_file in pet_files:
                subject_id = pet_file.replace("SUV.nii", "")
                pet_path = os.path.join(class_folder, f"{subject_id}SUV.nii")
                mri_path = os.path.join(class_folder, f"{subject_id}std_T1.nii")
                self.data.append((mri_path, pet_path, class_name))

        random.shuffle(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        pet_path, mri_path, label = self.data[idx]

        # Load images
        pet_img = nib.load(pet_path).get_fdata()
        mri_img = nib.load(mri_path).get_fdata()

        # Convert to tensors
        pet_tensor = torch.tensor(pet_img, dtype=torch.float32).unsqueeze(0)
        mri_tensor = torch.tensor(mri_img, dtype=torch.float32).unsqueeze(0)

        # Apply transform
        if self.transform:
            pet_tensor = self.transform(pet_tensor)
            mri_tensor = self.transform(mri_tensor)

        label_idx = torch.tensor(self.class_names.index(label), dtype=torch.long)

        combined = torch.cat([mri_tensor, pet_tensor], dim=0)  # Shape: [2, D, H, W]
        return combined, label_idx



# Modified function to create dataloaders for late fusion
def create_dataloaders(
    train_dir: str,
    test_dir: str,
    transform: transforms.Compose,
    batch_size: int,
    num_workers: int = 4,
    augmentation_transform: transforms.Compose = None
):
    class_names = os.listdir(train_dir)

    train_dataset = MultiModalSeparateNiiDataset(train_dir, class_names, transform)
    test_dataset = MultiModalSeparateNiiDataset(test_dir, class_names, transform)

    if augmentation_transform is not None:
        augmented_dataset = MultiModalSeparateNiiDataset(train_dir, class_names, augmentation_transform)
        train_dataset = ConcatDataset([train_dataset, augmented_dataset])

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    test_dataloader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return train_dataloader, test_dataloader, class_names
