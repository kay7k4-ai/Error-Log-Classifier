# 🧠 Error Log Classifier  
A Machine Learning-based system that automatically classifies log messages into categories like **ERROR**, **WARNING**, **INFO**, and **CRITICAL**. This project includes a fully working backend, frontend, and ML model integration designed for academic OJT requirements.

---

## 🚀 Project Overview
Applications generate thousands of logs every day. Manually inspecting them is slow and error-prone.  
This project automatically cleans, processes, and classifies logs using Machine Learning while providing a clean and modern web interface.

Key Features:
- Automated log classification  
- Drag & drop file upload + paste-log support  
- Modern UI with light/dark mode  
- Clean preprocessing pipeline  
- Trained ML model for fast inference  
---

## 🌐 Live Demo  

https://error-log-classifier-oee9.onrender.com/
  

## 🛠 Tech Stack

### **Frontend**
- HTML5  
- CSS3 (responsive + themed + glowing hover cards)  
- JavaScript  

### **Backend**
- Python  
- Flask  
- Gunicorn (for deployment)  

### **Machine Learning**
- scikit-learn  
- TF-IDF Vectorizer  
- Logistic Regression  
- Custom preprocessing scripts  

---

## 📁 Project Structure

Error-Log-Classifier/
│
├── web/
│ ├── app.py
│ ├── static/
│ │ ├── style.css
│ │ └── script.js
│ └── templates/
│ └── index.html
│
├── src/
│ ├── preprocessing/
│ │ ├── cleaner.py
│ │ └── preprocessor.py
│ ├── model/
│ │ └── vectorizer.py
│ └── classifier.py
│
├── model.pkl
├── vectorizer.pkl
├── train.py
├── requirements.txt
└── README.md

yaml

## 🧹 Log Preprocessing
The cleaning pipeline removes noise and prepares logs for ML classification. It includes:

- Lowercasing  
- Removing numbers  
- Removing URLs  
- Removing punctuation  
- Removing extra whitespace  
- Stopword removal  

---

## 🧠 ML Model
The pipeline uses:

- **TF-IDF vectorization** to convert log text into numerical form  
- **Logistic Regression** for classification  

Training saves two files:

- `model.pkl`  
- `vectorizer.pkl`

These are used by the Flask backend to classify logs instantly.

---

## ▶️ Running The Project Locally

### **1️⃣ Clone the repository**
git clone https://github.com/kay7k4-ai/Error-Log-Classifier
cd Error-Log-Classifier

### **2️⃣ Create a virtual environment**
python3 -m venv venv
source venv/bin/activate

markdown
Copy code

### **3️⃣ Install dependencies**
pip install -r requirements.txt

### **4️⃣ Run the web app**
python web/app.py

Open in browser:
http://127.0.0.1:5000

---

## 🎨 Frontend Features
- Clean and modern UI  
- Drag & Drop file upload  
- Paste-log textbox  
- Light/Dark theme toggle  
- Animated glowing hover effect  
- Instantly visible file name when selected  
- Responsive design  

---

## 🧪 How To Use

### Upload a log file:
1. Click **Choose File** or drag a `.txt` file  
2. Click **Classify Logs**  
3. See category results in the results table  

### Paste log text:
1. Paste logs into the text area  
2. Click **Classify Logs**  
3. View categorized output  

---

## 🧩 Training the Model

To retrain using your own data:

python train.py

This will:
- Clean logs  
- Vectorize text  
- Train logistic regression  
- Save `model.pkl` and `vectorizer.pkl`  

---

## 🚀 Deployment (Render / Railway / PythonAnywhere)

### Render (with `gunicorn`)
Build:
pip install -r requirements.txt

Start:
gunicorn web.app:app

### Railway (ZIP Upload)
- Upload project ZIP  
- Build command: `pip install -r requirements.txt`  
- Start command: `python web/app.py`  

---

## 🔮 Future Enhancements
- Downloadable classification report  
- Charts (error distribution)  
- API endpoint for other apps  
- Batch processing for large datasets  
- Confidence scores for predictions  

---

## 👩‍💻 Contributors
- **Karima** — Machine Learning, Backend. 
- **P Sirisha** — Frontend, Styling, UI  

---

## 📄 License
This project is for academic OJT and learning purposes.

---

# ⭐ Thank you for exploring the Error Log Classifier!