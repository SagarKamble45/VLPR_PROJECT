# 🚗 VLPR — Web-Based Vehicle License Plate Recognition System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?logo=flask)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green?logo=mongodb)
![EasyOCR](https://img.shields.io/badge/EasyOCR-Text%20Recognition-red)

A web-based Vehicle License Plate Recognition (VLPR) system that uses **YOLOv8** for real-time license plate detection and **EasyOCR** for character recognition. The system processes both uploaded videos and live webcam feeds, storing recognized plate data to a **MongoDB** database and delivering insights through a clean Flask web interface.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Setting Up the Output Folder](#setting-up-the-output-folder)
  - [Running the App](#running-the-app)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Known Issues & Notes](#known-issues--notes)
- [Contributing](#contributing)

---

## Overview

Unlike traditional VLPR systems that are confined to local hardware, this web-based solution operates over the internet, enabling remote access and real-time monitoring from any browser. It is designed for applications including:

- 🅿️ **Parking management** — automate entry/exit logging
- 🔒 **Security & surveillance** — track vehicle access
- 🚦 **Traffic monitoring** — analyze vehicle flow
- 📊 **Data analytics** — export and review plate data as CSV

---

## ✨ Features

- **Video Upload Detection** — Upload a video file and run VLPR processing frame-by-frame
- **Live Webcam Detection** — Real-time license plate recognition via browser webcam
- **YOLOv8-Powered Detection** — Custom-trained model (`Trained_Model.pt`) for accurate plate localization
- **EasyOCR Text Extraction** — GPU-accelerated character recognition with confidence scoring
- **Smart Plate Validation** — Character correction mapping (e.g., `O↔0`, `I↔1`) and format compliance checks
- **MongoDB Integration** — Separate collections for video and live-cam detections with timestamps
- **CSV Export** — Download collected plate data for offline analysis
- **Confidence Filtering** — Only stores plates with OCR confidence > 0.3 and length > 9 characters

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask + Flask-WTF |
| Object Detection | YOLOv8 (Ultralytics) |
| OCR Engine | EasyOCR |
| Computer Vision | OpenCV |
| Database | MongoDB (PyMongo) |
| Deep Learning | PyTorch + TorchVision |
| Frontend | HTML/CSS (Jinja2 Templates) |
| Data Processing | Pandas, NumPy |

---

## 📁 Project Structure

```
VLPR_PROJECT/
│
├── flaskapp.py               # Main Flask application & routes
├── YOLO_Video.py             # YOLOv8 video & webcam detection logic
├── add_data_to_db.py         # MongoDB connection, OCR, plate formatting
├── util.py                   # Utility functions (CSV export, image cleanup)
├── Trained_Model.pt          # Custom-trained YOLOv8 weights
├── requirements.txt          # Python dependencies
│
├── templates/                # HTML templates
│   ├── indexproject.html     # Home page
│   ├── ui.html               # Webcam interface
│   ├── video_output.html     # Video detection results
│   └── videoprojectnew.html  # Video upload page
│
├── static/
│   ├── images/               # Static assets (logo, header, sample images)
│   └── files/                # Uploaded video files (runtime)
│
├── output/                   # ⚠️ Must be created manually (see setup)
│   ├── IMAGES/
│   │   └── VIDEO_IMG/        # Cropped plate images from video
│   └── ...
│
└── SampleVideos/             # Sample test inputs
    ├── 1sample video.mp4
    └── sample_img.jpg
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- MongoDB running locally or a MongoDB Atlas connection string
- *(Recommended)* NVIDIA GPU with **CUDA** installed for faster inference
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/VLPR_PROJECT.git
   cd VLPR_PROJECT
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > 💡 **Tip:** For GPU acceleration, install the CUDA-compatible version of PyTorch from [pytorch.org](https://pytorch.org/get-started/locally/) before running the above command.

### Setting Up the Output Folder

> ⚠️ This step is **required** before running the app for the first time.

The application needs a specific output directory structure to save cropped plate images. You have two options:

**Option A — Download the pre-structured zip** (link in `imp.txt`) and extract it in your project root.

**Option B — Create it manually:**
```bash
mkdir -p output/IMAGES/VIDEO_IMG
```

### Update Hardcoded Paths

Before running, update the hardcoded local paths in the source files to match your environment:

- In `YOLO_Video.py` — update the model path:
  ```python
  model = YOLO("Trained_Model.pt")  # Use relative path
  ```
- In `util.py` — update the output folder path:
  ```python
  folder = 'output/IMAGES/VIDEO_IMG'
  ```

### Running the App

```bash
python flaskapp.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

---

## 🖥 Usage

1. **Home Page (`/`)** — Landing page with navigation options.
2. **Video Upload (`/FrontPage`)** — Upload an `.mp4` or similar video. The system processes it frame-by-frame and streams annotated output to the browser.
3. **Webcam Detection (`/webcam`)** — Grants access to your webcam for live license plate detection.
4. **Results & Export** — Detected plates (with timestamps and confidence scores) are stored in MongoDB and can be exported as CSV.

---

## ⚙️ How It Works

```
Input (Video / Webcam)
        │
        ▼
 YOLOv8 Detection
 (Trained_Model.pt)
        │
        ▼
 Bounding Box Extraction
 (confidence > 0.8)
        │
        ▼
 EasyOCR Character Recognition
        │
        ▼
 Plate Format Validation
 (length check + char mapping)
        │
        ▼
 Store to MongoDB
 (with timestamp)
        │
        ▼
 Stream Annotated Frames → Browser
```

**Character Correction Map**

To handle common OCR misreads, the system applies a correction mapping before validation:

| OCR Output | Corrected To |
|---|---|
| `O`, `o` | `0` |
| `T`, `I` | `1` |
| `J` | `3` |
| `A` | `4` |
| `G` | `6` |
| `S` | `5` |

---

## 🔧 Configuration

| Parameter | Location | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | `flaskapp.py` | `'VLPR_PROJECT'` | Flask session secret |
| `UPLOAD_FOLDER` | `flaskapp.py` | `'static/files'` | Video upload directory |
| OCR Confidence Threshold | `YOLO_Video.py` | `0.3` | Minimum OCR confidence to store |
| Plate Length Threshold | `YOLO_Video.py` | `9` | Minimum characters for valid plate |
| YOLO Confidence | `YOLO_Video.py` | `0.8` | Minimum detection confidence |

---

## 📸 Screenshots

> Sample output and detected plate images are available in `static/images/` and `output_folder.png`.

---

## ⚠️ Known Issues & Notes

- **Hardcoded paths**: Several files (`YOLO_Video.py`, `util.py`) contain absolute Windows-style paths. These must be updated to relative paths or environment variables before deployment.
- **GPU Recommended**: EasyOCR and YOLOv8 run significantly faster with a CUDA-enabled GPU. CPU-only inference may be slow on long videos.
- **MongoDB must be running**: The app will fail to store results if MongoDB is not accessible. Ensure your connection string in `add_data_to_db.py` is correct.
- **Plate format**: The validator currently checks for a specific 10-character format. Adjust `license_complies_format()` in `add_data_to_db.py` for different regional plate formats.

---

## 📄 License

This project is for educational and research purposes. Please ensure compliance with local laws when deploying license plate recognition systems.

---

## 👨‍💻 Creator - <strong>Sagar Kamble</strong> <a href="https://github.com/sagarkamble45">GitHub: @sagarkamble45</a>


