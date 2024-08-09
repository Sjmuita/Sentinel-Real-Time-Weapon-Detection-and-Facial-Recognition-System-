# Sentinel
This application uses YOLOv5 for weapon detection and Haar Cascade for facial recognition, capturing webcam feeds to detect threats. It sends real-time email alerts and logs events with timestamps and locations to enhance public safety.


# Real-Time Weapon Detection and Facial Recognition System

## Overview

This project aims to enhance public safety by developing a real-time weapon detection and facial recognition system. Utilizing YOLOv5 for weapon detection and a Haar Cascade model for facial recognition, this application is designed to monitor webcam feeds, detect weapons and faces, and send real-time alerts. Alerts are also logged with timestamps and locations in a CSV file.

## Features

- **Real-Time Weapon Detection:** Detects weapons in video feeds using YOLOv5.
- **Real-Time Facial Recognition:** Detects faces using the Haar Cascade model.
- **Alert System:** Sends email alerts via Gmail and logs alerts with timestamps and locations in a CSV file.
- **Webcam Integration:** Captures real-time video from the default webcam.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/weapon-detection-facial-recognition.git
    cd weapon-detection-facial-recognition
    ```

2. **Set Up Environment**

    Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download YOLOv5 and Haar Cascade Models**

    - YOLOv5: Clone the YOLOv5 repository into your project directory:
    
      ```bash
      git clone https://github.com/ultralytics/yolov5.git
      ```

    - Haar Cascade: Download the Haar Cascade XML file from the OpenCV repository or use the one provided in the `models` directory.

5. **Configure Email Alerts**

    Update the `config.py` file with your Gmail credentials and other configuration details:

    ```python
    EMAIL_ADDRESS = 'your-email@gmail.com'
    EMAIL_PASSWORD = 'your-password'
    ```

## Usage

1. **Run the Application**

    ```bash
    CSV FILE.py
    ```

2. **Stop the Application**

    The application can be terminated manually or based on elapsed time.

## Code Structure

- Exploratory Data Analysis
- Model Training
- Main script to start the real-time detection and alerting system.
- Contains functions for weapon detection and facial recognition.
- Manages the alert system and logging to CSV.
- Configuration file for email alerts and other settings.
- Directory containing the YOLOv5 and Haar Cascade model files.

## Challenges and Solutions

- **Training Time and Performance:** Addressed by fine-tuning with pre-trained weights and using hardware acceleration.
- **Alert Delivery:** Overcame Gmail authentication issues with proper authentication flows and token management.
- **Real-Time Processing:** Optimized model inference and video handling for improved performance.

## Future Work

- **Enhanced Accuracy:** Explore advanced models and techniques.
- **Location Tracking:** Integrate GPS or IP-based location services.
- **User Interface:** Develop a user interface for easier management and monitoring.
- **Social Media Analysis:** Implement natural language processing for predictive analysis of unrest.
- **Agitator Identification:** Integrate face recognition models for identifying known agitators.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.



---

**Disclaimer:** This project is for educational and research purposes only. Ensure to comply with all local laws and regulations related to surveillance and privacy.

