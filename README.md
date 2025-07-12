# 🏏 IPL Match Outcome Prediction 🎯

This project uses machine learning to predict the outcome of IPL cricket matches based on real-time match data such as team names, scores, overs, venue, and toss information. It provides a user-friendly Streamlit web app for input and displays instant predictions.

---

## 🚀 Features

- Real-time input via a clean Streamlit interface  
- Label encoding for categorical features  
- Automatically computes features like current and required run rates  
- Displays winner prediction instantly  
- Logistic Regression model used (can be extended to others)

---

## 🧠 Model

The model is a **Logistic Regression classifier** trained on historical IPL match data. The input features include encoded team names, venue, toss decision, and match stats like score, overs, and wickets left.

---


## 📦 Project Structure

```text
IPL Predictor/
├── data/                         # Contains input CSV files
│   ├── matches.csv
│   └── deliveries.csv
│
├── EDA/                          # Contains model and encoders
│   ├── eda.ipynb                 # Exploratory Data Analysis + Model Training
│   ├── ipl_logreg_best.pkl       # Trained logistic regression model
│   ├── label_encoder_*.pkl       # Encoders for categorical features
│
├── app.py                        # Streamlit app to predict match outcome
├── model_train.py (optional)     # Script to retrain the model (if needed)
├── requirements.txt              # List of dependencies
└── .env                          # (Optional) Environment file for secret keys



---

## 📊 Dataset Description

### 1. `matches.csv`
Contains match-level information like:
- Teams, venue, toss winner/decision
- Match result

### 2. `deliveries.csv`
Contains ball-by-ball data like:
- Runs per ball
- Wickets per delivery
- Player stats

---

## 🔧 Installation & Setup

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/IPL-Predictor.git
cd IPL-Predictor
Step 2: Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Step 3: Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Step 4: Run the Streamlit app
bash
Copy
Edit
streamlit run app.py
🔎 Features Considered for Prediction
Feature	Description
Batting Team	Categorical (label encoded)
Bowling Team	Categorical (label encoded)
Venue	Categorical (label encoded)
Toss Winner	Categorical (label encoded)
Toss Decision	Categorical (bat/field)
Current Score	Integer
Wickets Lost	Integer
Overs Completed	Float
Target Score	Integer
Current Run Rate	Auto-calculated
Required Run Rate	Auto-calculated

Note: Only 9 features are passed to the model after computation and encoding.

🧠 Machine Learning Model
Algorithm: Logistic Regression (Scikit-learn)

Target: 1 if batting team wins, 0 if bowling team wins

Encoding: LabelEncoder for categorical fields

Metrics: Accuracy, confusion matrix

🎮 How the App Works
User selects match details from dropdowns and sliders.

Streamlit computes required features like run rates.

Encoders transform categorical features into numeric values.

Model predicts the outcome based on the input.

The result (Batting Team Wins or Bowling Team Wins) is displayed instantly.

🧪 Sample Input (Behind-the-Scenes)
python
Copy
Edit
input_data = {
    'current_score': 150,
    'target_score': 160,
    'batting_team': 'Kolkata Knight Riders',
    'bowling_team': 'Delhi Capitals',
    'venue': 'Eden Gardens',
    'toss_winner': 'Delhi Capitals',
    'toss_decision': 'bat',
    'remaining_overs': 5.0,
    'wickets_left': 7,
    'run_rate': 10.0,
    'required_run_rate': 2.0
}
```
---
## 📸 App Interface

Here’s a glimpse of the Streamlit app predicting IPL match outcome:

![App Screenshot](Screenshot%202025-07-06%20at%2011.27.42.png)




