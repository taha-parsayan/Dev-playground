"""
Contains functionality for creating PyTorch DataLoaders for 
image classification data.
"""
import os
import nibabel as nib
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, ConcatDataset
import os
import nibabel as nib
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torchvision import transforms
from sklearn.model_selection import train_test_split
import numpy as np

NUM_WORKERS = os.cpu_count()

# Custom dataset to load NIfTI files
class NiiDataset(Dataset):
    def __init__(self, data_dir, class_names, transform=None):
        self.data_dir = data_dir
        self.class_names = class_names
        self.transform = transform
        self.data = []
        
        # Load data
        for class_name in self.class_names:
            class_folder = os.path.join(data_dir, class_name)
            for filename in os.listdir(class_folder):
                if filename.endswith(".nii"):  # Ensure only .nii files are used
                    file_path = os.path.join(class_folder, filename)
                    self.data.append((file_path, class_name))
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        # Load the NIfTI file
        file_path, label = self.data[idx]
        img = nib.load(file_path).get_fdata()  # Read the NIfTI file
        
        # Convert the numpy array to a PyTorch tensor
        img_tensor = torch.tensor(img, dtype=torch.float32).unsqueeze(0)  # Add channel dim
        
        # Apply the transformations if any
        if self.transform:
            img_tensor = self.transform(img_tensor)
        
        # Convert the label to an index (e.g., AD=0, MCI=1, NC=2)
        label_idx = torch.tensor(self.class_names.index(label), dtype=torch.long)
        
        return img_tensor, label_idx


# Modified function to create dataloaders using NIfTI files
def create_dataloaders(
    train_dir: str, 
    test_dir: str,
    transform: transforms.Compose,
    batch_size: int, 
    num_workers: int=4,
    augmentation_transform: transforms.Compose = None  # Default to None
):
    """Creates training and testing DataLoaders for .nii files."""

    class_names = os.listdir(train_dir)  # AD, MCI, NC
    # Train and test datasets using NiiDataset
    train_dataset = NiiDataset(data_dir=train_dir, class_names=class_names, transform=transform)
    test_dataset = NiiDataset(data_dir=test_dir, class_names=class_names, transform=transform)

    # If there is augmentation
    if augmentation_transform is not None:
        augmentation_train_dataset = NiiDataset(data_dir=train_dir, class_names=class_names, transform=augmentation_transform)
        train_dataset = ConcatDataset([train_dataset, augmentation_train_dataset])
    
    # Turn datasets into data loaders
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
