# HR Analysis and Recruitment System

## 📌 Project Overview
The **HR Analysis and Recruitment System** is a machine learning-based application designed to analyze HR data, predict recruitment outcomes, and visualize key insights. The project integrates an ML model for HR analytics with a web-based front-end for easy interaction.

## 🔥 Features
- **HR Data Analysis:** Insights into employee satisfaction, job roles, and performance.
- **ML Predictions:** Predicts recruitment likelihood based on various parameters.
- **Visualization:** Generates interactive charts and graphs using Matplotlib and Seaborn.
- **Flask-based Web App:** User-friendly interface for HR managers.

## 🛠️ Technologies Used
- **Backend (ML Model & Processing):** Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
- **Web Framework:** Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Data Storage:** CSV-based HR datasets

## 📂 Project Structure
```
📁 HR-Analysis-Recruitment-System
│── 📂 static          # Stores generated images and CSS files
│── 📂 templates       # HTML templates (index.html, job.html, ana.html)
│── 📜 app.py         # Flask application
│── 📜 HR Analysis.ipynb  # Jupyter Notebook for data analysis
│── 📜 RECRUITMENT SYSTEM.ipynb  # ML model development
│── 📜 requirements.txt # Dependencies
│── 📜 README.md       # Project Documentation
```

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/HR-Analysis-Recruitment-System.git
cd HR-Analysis-Recruitment-System
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Flask App
```sh
python app.py
```

### 5️⃣ Open in Browser
Visit `http://127.0.0.1:5000/` to access the HR Analysis system.

## 📊 Visualizations & ML Model
The project generates multiple insights:
- **Employee satisfaction histogram**
- **Correlation between attributes**
- **Predictions on employee retention & hiring**

## 🤝 Contributing
Pull requests are welcome! If you have suggestions, feel free to fork the repository and submit a PR.

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

