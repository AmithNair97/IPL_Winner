# 🏏 IPL Winner Predictor with AI-Powered Commentary

As a cricket fanatic since childhood, I've always been curious about predicting match outcomes using my game knowledge. That curiosity turned into a technical challenge — blending **machine learning**, **real-time AI**, and **data-driven storytelling**.

This project is a full-fledged **Streamlit app** that predicts the outcome of an IPL match and generates **live match commentary** using **LLaMA 8B via Groq API**.

---

## 🚀 Features

- ✅ Predict IPL match winners using team, venue, toss, and other inputs
- 🧠 AI-powered live commentary generated dynamically with match conditions
- 📊 Trained ML models (LogReg, XGBoost, Random Forest) with F1-score tuning
- 💬 Real-time commentary via **Groq API + LLaMA 8B**
- 🐳 Dockerized deployment support
- ⚙️ GitHub Actions for Continuous Integration

---

## 🧪 Dataset & Modeling

- **Dataset**: [Kaggle IPL Dataset](https://www.kaggle.com/datasets)
- **Initial model**: Logistic Regression — struggled with accuracy even after hyperparameter tuning.
- **Optimized models**:
  - **XGBoost** gave best results (based on F1-score — a balance between precision & recall)
  - **Random Forest** as fallback model
- **Preprocessing**:
  - Label Encoding of categorical features
  - Feature engineering for toss winner, venue, and playing teams

---

## 🗣️ AI Commentary Engine

Once the prediction is made, we generate a contextual commentary like:

> "CSK wins the toss and elects to bat first. With their strong record at Chepauk, they look confident. Our model predicts a CSK win!"

- **Model used**: `LLaMA 8B`
- **Platform**: [Groq API](https://console.groq.com/)
- **Inputs**: Teams, Toss, Venue, Predicted Winner

---

## 🧰 Tech Stack

| Component      | Technology                        |
|----------------|------------------------------------|
| ML Modeling    | Scikit-learn, RandomForest         |
| Frontend       | Streamlit                          |
| Commentary AI  | Groq API + LLaMA 8B                |
| Deployment     | Docker                             |
| CI/CD          | GitHub Actions                     |
| Data Handling  | Pandas, NumPy                      |

---



