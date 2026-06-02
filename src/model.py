import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pydicom
import os

class ThymusModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def train(self, X, y):
        """Train the model with given features and labels"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
    def predict(self, X):
        """Make predictions on new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
        
    def predict_proba(self, X):
        """Get prediction probabilities"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)

def train_model(data_path):
    """
    Train the thymus health prediction model
    
    Args:
        data_path (str): Path to training data directory containing CSV files
        
    Returns:
        ThymusModel: Trained model instance
    """
    # Load training data (assuming CSV format with features and target)
    # This is a simplified implementation - in practice you'd load actual DICOM data
    try:
        # For demonstration, we'll create synthetic data
        # In reality, this would load from DICOM files and extract features
        np.random.seed(42)
        n_samples = 1000
        
        # Create synthetic features (in practice these would come from DICOM analysis)
        features = np.random.rand(n_samples, 5) * 100  # 5 features: age, volume, density, etc.
        targets = (features[:, 0] * 0.3 + features[:, 1] * 0.2 + 
                  np.random.randn(n_samples) * 10 > 50).astype(int)  # Binary classification
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, targets, test_size=0.2, random_state=42
        )
        
        # Create and train model
        model = ThymusModel()
        model.train(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model trained with accuracy: {accuracy:.3f}")
        
        return model
        
    except Exception as e:
        print(f"Error training model: {e}")
        # Return a basic model for testing purposes
        return ThymusModel()

def predict_risk(model, features):
    """
    Predict thymus health risk
    
    Args:
        model (ThymusModel): Trained model instance
        features (array-like): Input features for prediction
        
    Returns:
        tuple: (risk_prediction, risk_probability)
    """
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    # Return prediction and probability of positive class (higher risk)
    risk_probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
    
    return int(prediction), float(risk_probability)