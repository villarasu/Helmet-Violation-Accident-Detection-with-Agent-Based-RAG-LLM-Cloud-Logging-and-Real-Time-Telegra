import streamlit as st
from ultralytics import YOLO
import tempfile
import os
from PIL import Image
import pandas as pd
import requests
import io
from datetime import datetime

# ------------------------------
# Load YOLOv8 model
# ------------------------------
model = YOLO("best.pt")  # update path if needed
model.to("cpu")

# ------------------------------
# Telegram Alert Setup
# ------------------------------
TELEGRAM_BOT_TOKEN = "8246902414:AAGyJZHFAK0Sf6vn4XD6Ii2q9tTUYaJb4Bk"
TELEGRAM_CHAT_ID = "5931871418"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            st.info("Telegram alert message sent successfully!")
        else:
            st.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        st.error(f"Error sending Telegram message: {e}")

def send_telegram_photo(image, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    files = {"photo": ("detected.png", buffered, "image/png")}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            st.info("Telegram alert photo sent successfully!")
        else:
            st.error(f"Failed to send Telegram photo: {response.text}")
    except Exception as e:
        st.error(f"Error sending Telegram photo: {e}")

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Helmet & Accident Detection 🚦", page_icon="🪖", layout="wide")

# Sidebar - Detection Settings
st.sidebar.header("⚙️ Detection Settings")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.25, 0.05)
theme_choice = st.sidebar.radio("🎨 Choose Theme", ["Dark", "Light"])
st.sidebar.info("Adjust confidence & theme for better detection")

# Add optional location input from user
camera_location = st.sidebar.text_input("Camera/Location", "Main Street Camera #1")

# Main Title
st.markdown("<h1 style='text-align:center'>🪖 Helmet & Accident Detection System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Upload an image or video for detection</p>", unsafe_allow_html=True)

# File Upload
uploaded_file = st.file_uploader("📂 Upload Image/Video", type=["jpg", "jpeg", "png", "mp4"])

if uploaded_file:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original Image", width=500)
    elif uploaded_file.type == "video/mp4":
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        st.video(video_path)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Run Detection"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        violation_classes = ['without helmet', 'accident']  # Classes to alert on
        violation_classes_lower = [cls.lower() for cls in violation_classes]

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
            with st.spinner("🔍 Running detection..."):
                results = model.predict(img, conf=conf_threshold)
            res_img_array = results[0].plot()
            res_img = Image.fromarray(res_img_array)

            st.image(res_img, caption="Processed Image", width=500)

            boxes = results[0].boxes
            if boxes:
                class_ids = boxes.cls.cpu().numpy()
                confidences = boxes.conf.cpu().numpy()
                class_names = [results[0].names[int(i)] for i in class_ids]
            else:
                class_ids, confidences, class_names = [], [], []

            df = pd.Series(class_names).value_counts()

            st.subheader("📊 Detection Summary")
            for cls, count in df.items():
                st.markdown(f"<span class='badge'>{cls}: {count}</span>", unsafe_allow_html=True)

            labels_lower = [label.lower() for label in class_names]
            st.write("Detected labels (original):", class_names)
            st.write("Detected labels (lowercase):", labels_lower)
            st.write("Violation classes (lowercase):", violation_classes_lower)

            detected_violations = []
            for cls, conf in zip(labels_lower, confidences):
                if cls in violation_classes_lower:
                    detected_violations.append((cls, conf))

            st.write("Detected violations with confidence:", detected_violations)

            if detected_violations:
                # Compose detailed violation string with confidence scores
                violation_str = ', '.join([f"{cls} ({conf:.2f})" for cls, conf in detected_violations])

                msg = (
                    f"🚨 Helmet Violation Alert!\n"
                    f"Location: {camera_location}\n"
                    f"Time: {current_time}\n"
                    f"Violations: {violation_str}"
                )
                st.write("Sending Telegram alert with message and photo...")
                send_telegram_message(msg)
                send_telegram_photo(res_img, caption=msg)
            else:
                st.write("No violations detected, no Telegram alert sent.")

        elif uploaded_file.type == "video/mp4":
            with st.spinner("🔍 Processing video..."):
                output_dir = tempfile.mkdtemp()
                results = model.predict(
                    source=video_path,
                    save=True,
                    conf=conf_threshold,
                    project=output_dir,
                    name="result_video"
                )
                processed_video_path = os.path.join(output_dir, "result_video.mp4")

            st.success("✅ Video processed successfully!")
            st.subheader("🎥 Processed Video Preview")
            st.video(processed_video_path)

            st.subheader("📥 Download Processed Video")
            with open(processed_video_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download",
                    data=f,
                    file_name="processed_video.mp4",
                    mime="video/mp4"
                )

            if results and results[0].boxes:
                class_ids = results[0].boxes.cls.cpu().numpy()
                confidences = results[0].boxes.conf.cpu().numpy()
                class_names = [results[0].names[int(i)] for i in class_ids]

                df = pd.Series(class_names).value_counts()

                st.subheader("📊 Video Detection Summary")
                for cls, count in df.items():
                    st.markdown(f"<span class='badge'>{cls}: {count}</span>", unsafe_allow_html=True)

                labels_lower = [label.lower() for label in class_names]
                st.write("Detected labels in video (first frame):", class_names)
                st.write("Detected labels in video (lowercase):", labels_lower)

                detected_violations = []
                for cls, conf in zip(labels_lower, confidences):
                    if cls in violation_classes_lower:
                        detected_violations.append((cls, conf))

                st.write("Detected violations with confidence in video:", detected_violations)

                if detected_violations:
                    violation_str = ', '.join([f"{cls} ({conf:.2f})" for cls, conf in detected_violations])
                    msg = (
                        f"🚨 Helmet Violation Alert in video!\n"
                        f"Location: {camera_location}\n"
                        f"Time: {current_time}\n"
                        f"Violations: {violation_str}"
                    )
                    st.write("Sending Telegram alert message...")
                    send_telegram_message(msg)
                else:
                    st.write("No violations detected in video, no Telegram alert sent.")

        st.markdown("</div>", unsafe_allow_html=True)
