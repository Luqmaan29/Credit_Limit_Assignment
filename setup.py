"""
Setup script for Credit Limit Assignment System
Run this to set up the complete environment
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'models']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}/")

def install_requirements():
    """Install required packages"""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Successfully installed all requirements")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True

def generate_data():
    """Generate synthetic credit data"""
    print("\nGenerating synthetic credit dataset...")
    try:
        from data_generator import save_dataset
        save_dataset()
        print("✓ Successfully generated credit data")
    except Exception as e:
        print(f"✗ Error generating data: {e}")
        return False
    return True

def train_models():
    """Train ML models"""
    print("\nTraining machine learning models...")
    try:
        subprocess.check_call([sys.executable, 'model_training.py'])
        print("✓ Successfully trained models")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error training models: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("Credit Limit Assignment System - Setup")
    print("=" * 60)
    
    # Create directories
    print("\n[1/4] Creating directories...")
    create_directories()
    
    # Install requirements
    print("\n[2/4] Installing requirements...")
    if not install_requirements():
        print("\n✗ Setup failed at requirements installation")
        return
    
    # Generate data
    print("\n[3/4] Generating dataset...")
    if not generate_data():
        print("\n✗ Setup failed at data generation")
        return
    
    # Train models
    print("\n[4/4] Training models...")
    if not train_models():
        print("\n✗ Setup failed at model training")
        return
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the Streamlit app, run:")
    print("  streamlit run app.py")
    print("\nOr on Windows:")
    print("  python -m streamlit run app.py")

if __name__ == '__main__':
    main()

