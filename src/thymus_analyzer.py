import pydicom
import numpy as np
from scipy import ndimage
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class ThymusAnalyzer:
    """Core analyzer for thymus health assessment from medical images."""
    
    def __init__(self):
        self.thymus_volume = None
        self.health_metrics = {}
        
    def load_image(self, file_path):
        """Load DICOM image from file path."""
        try:
            ds = pydicom.dcmread(file_path)
            return ds.pixel_array.astype(np.float32)
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
            
    def segment_thymus(self, image_data):
        """Segment thymus gland from CT scan data."""
        # Simple threshold-based segmentation
        threshold = np.percentile(image_data, 75)
        binary_mask = image_data > threshold
        
        # Remove small artifacts
        cleaned_mask = ndimage.binary_opening(binary_mask)
        cleaned_mask = ndimage.binary_closing(cleaned_mask)
        
        # Label connected components and select largest
        labeled_array, num_features = ndimage.label(cleaned_mask)
        if num_features == 0:
            return None
            
        # Find component with largest area
        component_sizes = ndimage.sum(cleaned_mask, labeled_array, range(num_features + 1))
        largest_component = np.argmax(component_sizes[1:]) + 1
        thymus_mask = labeled_array == largest_component
        
        return thymus_mask
        
    def calculate_volume(self, thymus_mask, spacing=None):
        """Calculate thymus volume from segmented mask."""
        if spacing is None:
            # Default voxel spacing (adjust based on actual data)
            spacing = [1.0, 1.0, 1.0]
            
        voxel_volume = np.prod(spacing)
        voxel_count = np.sum(thymus_mask)
        volume = voxel_count * voxel_volume
        
        return volume
        
    def predict_health_risk(self, volume):
        """Predict health risk based on thymus volume."""
        # Simplified model - in practice this would be more complex
        if volume < 100:
            risk_level = "High"
            risk_score = 0.8
        elif volume < 200:
            risk_level = "Moderate"
            risk_score = 0.5
        else:
            risk_level = "Low"
            risk_score = 0.2
            
        return risk_level, risk_score


def analyze_scan(file_path):
    """Analyze a medical scan and return health assessment."""
    analyzer = ThymusAnalyzer()
    
    # Load image data
    image_data = analyzer.load_image(file_path)
    
    # Segment thymus
    thymus_mask = analyzer.segment_thymus(image_data)
    
    if thymus_mask is None:
        raise ValueError("Could not segment thymus gland from image")
        
    # Calculate volume
    volume = analyzer.calculate_volume(thymus_mask)
    
    # Predict health risk
    risk_level, risk_score = analyzer.predict_health_risk(volume)
    
    # Compile results
    health_metrics = {
        'volume': volume,
        'risk_level': risk_level,
        'risk_score': risk_score,
        'segmentation_mask': thymus_mask
    }
    
    return health_metrics


def get_health_metrics(image_data):
    """Extract health metrics directly from image data."""
    analyzer = ThymusAnalyzer()
    
    # Segment thymus
    thymus_mask = analyzer.segment_thymus(image_data)
    
    if thymus_mask is None:
        return {'error': 'Thymus segmentation failed'}
        
    # Calculate volume
    volume = analyzer.calculate_volume(thymus_mask)
    
    # Additional metrics
    thymus_pixels = np.sum(thymus_mask)
    total_pixels = image_data.size
    thymus_ratio = thymus_pixels / total_pixels
    
    # Predict health risk
    risk_level, risk_score = analyzer.predict_health_risk(volume)
    
    return {
        'thymus_volume': volume,
        'thymus_pixel_ratio': thymus_ratio,
        'health_risk_level': risk_level,
        'health_risk_score': risk_score
    }