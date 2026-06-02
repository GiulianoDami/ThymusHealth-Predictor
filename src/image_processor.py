import pydicom
import numpy as np
from scipy import ndimage
from sklearn.preprocessing import StandardScaler

def load_dicom(file_path):
    """
    Load a DICOM file and return the image data and metadata.
    
    Args:
        file_path (str): Path to the DICOM file
        
    Returns:
        tuple: (image_data, metadata)
    """
    try:
        dicom = pydicom.dcmread(file_path)
        image_data = dicom.pixel_array
        metadata = {
            'patient_id': getattr(dicom, 'PatientID', None),
            'study_date': getattr(dicom, 'StudyDate', None),
            'slice_thickness': getattr(dicom, 'SliceThickness', None),
            'pixel_spacing': getattr(dicom, 'PixelSpacing', None)
        }
        return image_data, metadata
    except Exception as e:
        raise ValueError(f"Error loading DICOM file: {str(e)}")

def preprocess_image(dicom_data):
    """
    Preprocess the DICOM image data for further analysis.
    
    Args:
        dicom_data (numpy.ndarray): Raw DICOM image data
        
    Returns:
        numpy.ndarray: Preprocessed image data
    """
    # Convert to float32 and normalize to [0, 1]
    image = dicom_data.astype(np.float32)
    
    # Apply windowing to enhance visualization (standard lung window)
    # HU range for lung window: -1000 to 1000
    image = np.clip(image, -1000, 1000)
    image = (image + 1000) / 2000.0
    
    # Normalize using z-score
    scaler = StandardScaler()
    flat_image = image.flatten().reshape(-1, 1)
    normalized = scaler.fit_transform(flat_image)
    image = normalized.reshape(image.shape)
    
    return image

def extract_thymus_region(image_data):
    """
    Extract the thymus region from the image data using basic segmentation.
    
    Args:
        image_data (numpy.ndarray): Preprocessed image data
        
    Returns:
        numpy.ndarray: Binary mask of the thymus region
    """
    # Simple threshold-based segmentation
    # Thymus typically has HU values between 20-80
    threshold_low = 20
    threshold_high = 80
    
    # Create binary mask
    thymus_mask = np.zeros_like(image_data, dtype=np.uint8)
    thymus_mask[(image_data >= threshold_low) & (image_data <= threshold_high)] = 1
    
    # Apply morphological operations to clean up the mask
    structure = ndimage.generate_binary_structure(2, 2)
    thymus_mask = ndimage.binary_closing(thymus_mask, structure=structure)
    thymus_mask = ndimage.binary_opening(thymus_mask, structure=structure)
    
    # Remove small connected components
    labeled_array, num_features = ndimage.label(thymus_mask)
    if num_features > 0:
        sizes = ndimage.sum(thymus_mask, labeled_array, range(1, num_features + 1))
        mask_size = sizes < 50  # Remove components smaller than 50 pixels
        remove_pixel = mask_size[labeled_array - 1]
        thymus_mask[remove_pixel] = 0
    
    return thymus_mask