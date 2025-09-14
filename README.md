# 🚦 Helmet Violation & Accident Detection  
### Agent-Based RAG LLM | Cloud Logging | Real-Time Telegram Alerts  

## 📖 Overview  
Road safety teams face challenges in monitoring multiple cameras, identifying riders without helmets, and detecting accidents quickly. Manual review is time-consuming and error-prone.  

This project automates **helmet violation** and **accident detection** using a **YOLO-based model** with:  
- ✅ **Agent-based RAG LLM** for natural language querying of detection data  
- ☁ **Cloud logging** with AWS S3 + PostgreSQL (pgvector) for evidence and metadata storage  
- 📢 **Real-time Telegram alerts** for critical events  
- 📊 **Interactive dashboards** and **PDF/email reports** for review and reporting  

---

## ✨ Features  
- 🧠 **YOLOv8 Detection**: Detects helmets, no-helmet violations, and accidents from images/videos.  
- 📡 **Real-Time Alerts**: Sends Telegram notifications for accidents with proof links.  
- 🔍 **RAG Chatbot**: Semantic search and question answering on stored detection data.  
- 📁 **Cloud Storage**: Uploads detection evidence to **AWS S3** with presigned access links.  
- 🗄 **Vector Database**: Stores embeddings in PostgreSQL using **pgvector** for semantic search.  
- 📄 **PDF Reports**: Generates downloadable reports with detection summaries and links.  
- ✉ **Email Integration**: Sends PDF reports via SMTP.  
- 📊 **Streamlit Dashboard**: User-friendly UI for detection, analytics, and report generation.  

---

## 🛠️ Tech Stack  
| Component          | Technology                          |  
|--------------------|------------------------------------|  
| **Detection Model**| YOLOv8 (Ultralytics)               |  
| **Backend**        | Streamlit (Python)                 |  
| **Vector Search**   | PostgreSQL + pgvector              |  
| **Embeddings**      | Hugging Face API / SentenceTransformer |  
| **Cloud Storage**   | AWS S3                             |  
| **Notifications**   | Telegram Bot API                   |  
| **Reporting**       | FPDF + SMTP Email                  |  

---

## 📂 Project Structure  
```
📁 helmet-violation-accident-detection
 ├── app.py                 # Main Streamlit app
 ├── best.pt                # YOLO trained weights
 ├── requirements.txt       # Dependencies
 ├── README.md              # Project documentation
 └── (other config files)
```

---

## ⚙️ Setup Instructions  

### 1️⃣ **Clone Repository**  
```bash
git clone https://github.com/your-username/helmet-violation-accident-detection.git
cd helmet-violation-accident-detection
```

### 2️⃣ **Create Virtual Environment & Install Dependencies**  
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```

### 3️⃣ **Configure Secrets in Streamlit**  
Create `.streamlit/secrets.toml`:  
```toml
HF_API_KEY = "your_huggingface_api_key"

AWS_REGION = "your-region"
S3_BUCKET = "your-bucket"
AWS_ACCESS_KEY = "your-aws-access-key"
AWS_SECRET_KEY = "your-aws-secret-key"

TELEGRAM_TOKEN = "your-telegram-bot-token"
TELEGRAM_CHAT_ID = "your-chat-id"

SMTP_EMAIL = "your-email@example.com"
SMTP_PASS = "your-app-password"

RDS_HOST = "your-db-host"
RDS_DB = "your-db-name"
RDS_USER = "your-db-user"
RDS_PASS = "your-db-password"
```

### 4️⃣ **Database Setup**  
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE detections (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP DEFAULT NOW(),
  camera_id TEXT,
  location TEXT,
  class_label TEXT,
  confidence FLOAT,
  bbox_coordinates JSONB,
  s3_image_url TEXT,
  embedding VECTOR(384)
);
```

### 5️⃣ **Run the App**  
```bash
streamlit run app.py
```

---

## 🚀 Usage  

### **🔍 Detection Mode**  
1. Go to **Detect** mode in the sidebar.  
2. Upload an image/video.  
3. View detections with bounding boxes.  
4. Results are uploaded to AWS S3, logged in PostgreSQL, and alerts sent to Telegram.  

### **🤖 RAG Chatbot Mode**  
1. Switch to **RAG Chatbot** in the sidebar.  
2. Ask natural language questions like:  
   - “Accidents from last week”  
   - “Most helmet violations by camera”  
3. View retrieved records, charts, and generate reports.  
4. Download or email PDF summaries.  

---

## 📧 Telegram Alerts Example  
```
🚨 Accident Detected!
Camera: cam_001
Location: Main Street
Timestamp: 2025-09-14T20:15:32
Confidence: 0.92
Proof: [Presigned S3 URL]
```

---

## 📊 Sample Questions for RAG  
- “Show helmet violations by location.”  
- “Top 5 cameras with the most detections.”  
- “Accidents by day for the last 2 weeks.”  

---

## 🧪 Testing  
- Upload test images/videos to verify detection.  
- Use a mock PostgreSQL instance and local storage for development.  
- Test Hugging Face API fallback to local embeddings.  
- Verify Telegram bot alerts using test chat IDs.  

---

## 🛡️ Best Practices & Notes  
- Use **App Passwords** for Gmail SMTP.  
- Protect `.streamlit/secrets.toml` — never commit to GitHub.  
- Rotate API keys and AWS credentials regularly.  
- Enable IAM policies for S3 security.  
- Train YOLO with diverse datasets for accuracy.  

---
 
