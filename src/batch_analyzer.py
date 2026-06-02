import os
import pydicom
import numpy as np
from scipy import ndimage
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchAnalyzer:
    """Class for batch processing of multiple CT scans"""
    
    def __init__(self):
        self.results = []
        
    def analyze_scan(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single CT scan file
        
        Args:
            file_path: Path to the DICOM file
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Read DICOM file
            ds = pydicom.dcmread(file_path)
            
            # Extract pixel data
            if hasattr(ds, 'pixel_array'):
                image_data = ds.pixel_array.astype(np.float32)
            else:
                logger.warning(f"No pixel array found in {file_path}")
                return None
                
            # Simple thresholding to segment thymus (this would be more sophisticated in practice)
            threshold = np.percentile(image_data, 75)
            binary_mask = image_data > threshold
            
            # Remove small noise
            cleaned_mask = ndimage.binary_opening(binary_mask)
            
            # Calculate volume (simplified - assumes uniform voxel spacing)
            voxel_volume = 1.0  # This should be calculated from DICOM metadata
            thymus_volume = np.sum(cleaned_mask) * voxel_volume
            
            # Calculate additional metrics
            mean_intensity = np.mean(image_data[binary_mask])
            max_intensity = np.max(image_data[binary_mask])
            
            return {
                'file_path': file_path,
                'thymus_volume': float(thymus_volume),
                'mean_intensity': float(mean_intensity),
                'max_intensity': float(max_intensity),
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {str(e)}")
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e)
            }
    
    def process_directory(self, folder_path: str) -> List[Dict[str, Any]]:
        """
        Process all CT scan files in a directory
        
        Args:
            folder_path: Path to directory containing CT scan files
            
        Returns:
            List of analysis results
        """
        results = []
        
        # Get all DICOM files in directory
        dicom_files = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.dcm', '.dicom')):
                dicom_files.append(os.path.join(folder_path, filename))
        
        logger.info(f"Found {len(dicom_files)} DICOM files to process")
        
        # Process each file
        for file_path in dicom_files:
            result = self.analyze_scan(file_path)
            if result:
                results.append(result)
        
        self.results = results
        return results

def process_directory(folder_path: str) -> List[Dict[str, Any]]:
    """
    Process all CT scan files in a directory
    
    Args:
        folder_path: Path to directory containing CT scan files
        
    Returns:
        List of analysis results
    """
    analyzer = BatchAnalyzer()
    return analyzer.process_directory(folder_path)

def generate_report(results: List[Dict[str, Any]]) -> str:
    """
    Generate a summary report from analysis results
    
    Args:
        results: List of analysis results
        
    Returns:
        Formatted report string
    """
    successful_results = [r for r in results if r['status'] == 'success']
    
    if not successful_results:
        return "No successful analyses performed."
    
    total_scans = len(successful_results)
    volumes = [r['thymus_volume'] for r in successful_results]
    mean_volume = np.mean(volumes)
    std_volume = np.std(volumes)
    
    report = f"""
Thymus Health Analysis Report
============================

Total Scans Processed: {total_scans}
Average Thymus Volume: {mean_volume:.2f} mm³
Volume Standard Deviation: {std_volume:.2f} mm³

Volume Range: {min(volumes):.2f} - {max(volumes):.2f} mm³

Analysis Summary:
- Successful analyses: {total_scans}
- Failed analyses: {len(results) - total_scans}

"""
    
    return report