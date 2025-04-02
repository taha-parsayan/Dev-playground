import os
import nibabel as nib
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torchvision import datasets, transforms
from sklearn.model_selection import train_test_split
from PIL import Image
import os

NUM_WORKERS = os.cpu_count()

# Function to load MRI slices
def load_mri_slices(nifti_path, axis):
    """
    Load a 3D MRI scan and extract 2D slices along the specified axis.
    Returns slices as torch tensors.
    """
    img = nib.load(nifti_path)
    data = img.get_fdata()
    
    # Extract slices from 3D images and keep them as numpy arrays (2D slices)
    slices = [data.take(i, axis=axis) for i in range(data.shape[axis])]
    
    # Replace NaNs with 0 and convert to tensor (without normalization here)
    slices = [
        torch.tensor(np.nan_to_num(s, nan=0.0), dtype=torch.float32)  # Replace NaNs with 0 and convert to tensor
        for s in slices
    ]
    
    return slices


# ---------------------------------------------------------------

# Custom dataset to load NIfTI files and extract slices
def load_nifti_data(data_dir, class_names, axis=0, transform=None):
    data = []
    
    for class_name in class_names:
        class_folder = os.path.join(data_dir, class_name)
        for filename in os.listdir(class_folder):
            if filename.endswith(".nii"):  # Ensure only .nii files are used
                file_path = os.path.join(class_folder, filename)
                slices = load_mri_slices(file_path, axis)
                
                # Apply transformations if provided
                
                if transform:
                        #slices = [transform(s.expand(3, -1, -1)) for s in slices]  # Convert [1, H, W] → [3, H, W]
                        slices = [transform(s.unsqueeze(0)) for s in slices]  # Keep grayscale with 1 channel
                
                # Stack slices into a tensor of shape (num_slices, C, H, W)
                img_tensor = torch.stack(slices)  # Shape: (num_slices, C, H, W)
                
                # Convert the label to an index (e.g., AD=0, MCI=1, NC=2)
                label_idx = class_names.index(class_name)
                
                data.append((img_tensor, label_idx))
    
    return data

# ---------------------------------------------------------------

# Function to create dataloaders
def create_dataloaders(
    train_dir: str, 
    test_dir: str,
    transform: transforms.Compose,
    batch_size: int, 
    num_workers: int=4,
    augmentation_transform: transforms.Compose = None,  # Default to None
    axis: int = 0  # Axis for slicing (0=axial, 1=sagittal, 2=coronal)
):
    """Creates training and testing DataLoaders for .nii files."""
    
    class_names = os.listdir(train_dir)  # AD, MCI, NC
    
    # Load training and test data using the new data loading function
    train_data = load_nifti_data(train_dir, class_names, axis=axis, transform=transform)
    test_data = load_nifti_data(test_dir, class_names, axis=axis, transform=transform)
    
    # If augmentation is provided, apply it to the training data
    if augmentation_transform is not None:
        augmented_train_data = load_nifti_data(train_dir, class_names, axis=axis, transform=augmentation_transform)
        train_data.extend(augmented_train_data)  # Append the augmented data to the original
    
    # Convert lists to DataLoader
    train_dataloader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    
    test_dataloader = DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return train_dataloader, test_dataloader, class_names

#path = '/work/TahaPourmaohammad#7093/Project/Taha_database/Codes/Data/train/NC/009_S_0751.nii'
#train_dir = '/work/TahaPourmaohammad#7093/Project/Taha_database/Codes/Data/train'
#slices = load_mri_slices(path, axis=0)
#print(slices[0].shape)
#print(len(slices))
#print(type(slices))
