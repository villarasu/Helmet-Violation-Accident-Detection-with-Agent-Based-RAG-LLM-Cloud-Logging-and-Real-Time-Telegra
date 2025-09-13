# Helmet Violation & Accident Detection — Problem Statement

## Problem Summary

Road safety teams struggle to monitor all cameras and quickly identify riders without helmets or detect accidents. Manual monitoring is slow, inconsistent, and often misses critical events.

We need an automated system that watches videos or uploaded images, detects two events **no-helmet**, and **accidents**—saves evidence, alerts the right people immediately, and makes review and reporting easy.

---

## Requirements

### Detection & Model

* Use a YOLO-based AI model to detect  no-helmet, and accident events in images and videos.

### Web App

* Simple **Streamlit** web app to upload files, run inference, view annotated results, and review incidents.

### Storage & Database

* Store original media and annotated outputs in **AWS S3**.
* Maintain clean, searchable incident records in **AWS RDS** (Postgres recommended).

### Alerts & Notifications

* Send real-time **Telegram** alerts for high-priority events including annotated images, timestamp, location (if available), and links to evidence in S3.
* Generate daily/weekly **email summaries** with counts, trends, and sample evidence.

### Chatbot & RAG

* Provide a chatbot interface that can answer queries against incident history (example: "Show today’s no-helmet cases near Gate 3"). Use a RAG approach with embeddings + retrieval.

### Operational Goals

* Alerts should arrive within seconds of detection.
* Incidents must be logged accurately and be easily searchable.
* System should be secure and cost-effective when deployed on AWS.

---

## Success Criteria

* Reliable detection of helmet/no-helmet/accident events with high precision and acceptable recall.
* Real-time alerts (<\~seconds) to Telegram for critical events.
* Accurate, queryable logs in RDS and accessible evidence in S3.
* Usable Streamlit UI for upload, review, and manual verification.
* Daily/weekly summary emails delivered to stakeholders.

---

### Submission Instructions

1. Save this file as `PROBLEM_STATEMENT.md` in your project repository or cloud storage.
2. Make the repository or file **public** or **shareable**.
3. Copy the shareable URL (e.g., GitHub: `https://github.com/yourusername/helmet-accident-project/blob/main/PROBLEM_STATEMENT.md`).
4. Paste the link in your LMS submission or email as your final project problem statement.
