import cv2
import os
import zipfile
import time
import base64
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import torch
from torchvision import transforms
from PIL import Image

# Define paths
zip_file_path = r'C:\Users\Admin\Downloads\archive (9).zip'
extract_dir = r'C:\Users\Admin\Downloads\haarcascade'
csv_file_path = r'C:\Users\Admin\Downloads\alerts_log.csv'

# Extract Haar Cascade XML file
def unzip_cascade(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f'Haar Cascade XML extracted to {extract_to}')
    except Exception as e:
        print(f"Error extracting Haar Cascade XML: {e}")

unzip_cascade(zip_file_path, extract_dir)

def load_face_cascade(cascade_path):
    try:
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if face_cascade.empty():
            raise ValueError("Failed to load Haar Cascade.")
        print(f"Face cascade model loaded successfully from {cascade_path}")
        return face_cascade
    except Exception as e:
        print(f"Failed to load face cascade: {e}")
        return None

# Define the path to the Haar Cascade XML file
haar_cascade_file = os.path.join(extract_dir, 'haarcascade_frontalface_default.xml')
face_cascade = load_face_cascade(haar_cascade_file)

def authenticate_gmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    except Exception as e:
        print(f"Error during Gmail authentication: {e}")
        return None

def send_alert(subject, body, to_email):
    try:
        creds = authenticate_gmail()
        if creds is None:
            print("Failed to authenticate Gmail.")
            return
        
        service = build('gmail', 'v1', credentials=creds)
        
        message = MIMEMultipart()
        message['From'] = 'jessysteve251@gmail.com'
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Message sent successfully! Message ID: {send_message['id']}")
    except Exception as e:
        print(f"An error occurred while sending the alert: {e}")

def load_yolov5_model(model_path):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
        model.eval()
        print(f"YOLOv5 model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Failed to load YOLOv5 model: {e}")
        return None

# Define the path to the YOLOv5 model
yolov5_model_path = r'C:\Users\Admin\Downloads\yolov5\yolov5s.pt'
yolov5_model = load_yolov5_model(yolov5_model_path)

def log_alert_to_csv(subject, body, alert_type, location, timestamp):
    try:
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, alert_type, body, location])
        print(f"Alert logged to CSV file.")
    except Exception as e:
        print(f"Error logging alert to CSV: {e}")

def detect_objects_from_webcam(model, face_cascade, duration):
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam
    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    start_time = time.time()  # Record the start time
    alert_triggered_face = False
    alert_triggered_weapon = False
    location = "Static Location"  # Placeholder for actual location

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert frame to PIL image for YOLOv5
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = model(pil_img)

        # Draw rectangles around detected faces and weapons
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("Face detected!")  # Print statement for face detection

        # Process YOLOv5 results
        for detection in results.xyxy[0]:  # Iterate over detections
            x1, y1, x2, y2, conf, cls = detection
            label = model.names[int(cls)]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Detected: {label} with confidence {conf:.2f}")  # Print detected labels and confidences

            if label == 'weapon':
                if not alert_triggered_weapon:
                    print("Weapon detected!")
                    subject = "Alert: Weapon Detected"
                    body = "A weapon has been detected in the video stream."
                    to_email = 'jessysteve251@gmail.com'
                    send_alert(subject, body, to_email)
                    log_alert_to_csv(subject, body, 'Weapon', location, timestamp)
                    alert_triggered_weapon = True
            # Draw bounding boxes for detected objects
            if conf > 0.5:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the result
        cv2.imshow('Real-time Detection', frame)

        try:
            if len(faces) > 0 and not alert_triggered_face:
                print("Face detected!")
                subject = "Alert: Face Detected"
                body = "A face has been detected in the video stream."
                to_email = 'jessysteve251@gmail.com'
                send_alert(subject, body, to_email)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                log_alert_to_csv(subject, body, 'Face', location, timestamp)
                alert_triggered_face = True

            if len(faces) == 0:
                alert_triggered_face = False

            if len(results.xyxy[0]) == 0:  # Reset weapon alert if no weapon detected
                alert_triggered_weapon = False

        except Exception as e:
            print(f"Error during detection: {e}")

        # Check if the duration has passed
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            print("Duration elapsed. Exiting...")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()

# Run real-time detection for a specified duration (e.g., 60 seconds)
detect_objects_from_webcam(yolov5_model, face_cascade, duration=20)
