# 🏥 Chronic Kidney Disease (CKD) Prediction System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.12-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

A machine learning system that predicts CKD risk from clinical parameters with **92% accuracy**, featuring a Streamlit web interface for medical professionals.

## 📌 Key Features
- **Random Forest Classifier** trained on 400+ patient records
- **Web-based interface** built with Streamlit
- **Comprehensive input** (27 clinical parameters)
- **Risk probability** output with medical recommendations
- **Feature importance** visualization

## 🛠️ Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/ckd-prediction-project.git
cd ckd-prediction-project
Install dependencies:

bash
pip install -r requirements.txt
🚀 Usage
Run the Streamlit app:

bash
streamlit run app/app.py
Input patient data through the web form.

View prediction results:

🟢 Low Risk (<20% probability)

🔴 High Risk (>80% probability)

📊 Detailed risk breakdown

📂 Project Structure
text
ckd-prediction-project/
├── app/                  # Streamlit application
│   ├── app.py            # Main application code
│   └── assets/           # Images/static files
├── data/                 
│   └── ckd-dataset-v2.csv  # Original dataset
├── model/                
│   ├── ckd_model_v3.pkl    # Trained model
│   └── label_encoders.pkl  # Categorical encoders
├── notebooks/            
│   └── model_training.ipynb # Jupyter notebook
├── requirements.txt      # Python dependencies
└── README.md            # This file
📊 Model Performance
Metric	Score
Accuracy	0.92
Precision	0.91
Recall	0.93
AUC-ROC	0.96
Confusion Matrix:

text
              Predicted 0  Predicted 1
Actual 0         85          5
Actual 1          7         83
🧠 Key Parameters
The model prioritizes these clinical markers:

Serum Creatinine (SC)

Glomerular Filtration Rate (GFR)

Hemoglobin (Hemo)

Albumin (AL)

Blood Urea (BU)

🤝 How to Contribute
Fork the repository

Create a new branch (git checkout -b feature/your-feature)

Commit changes (git commit -m 'Add new feature')

Push to branch (git push origin feature/your-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see LICENSE for details.

📧 Contact
For questions or collaborations:
[Tejas-I-M] - rex91320@gmail.com
Project Link: https://github.com/Tejas-I-M/ckd-prediction-project
