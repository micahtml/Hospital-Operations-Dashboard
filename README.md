# 🏥 Hospital Operations Dashboard

An interactive, full-stack data analytics dashboard designed to simulate real-world hospital performance monitoring. Built with **Streamlit**, **SQLite**, and **Plotly**, this project showcases ETL, SQL, and data visualization skills applied to healthcare operations.

---

## 📊 Features

- **Interactive Filters:** by department and month
- **Key Performance Indicators (KPIs):**
  - Average Length of Stay
  - Readmission Rate
  - Infection Rate
  - Staff-to-Patient Ratio
  - Average Wait Time
  - Average Billing
- **Visualizations:**
  - Monthly Readmission Trend (Line Chart)
  - Length of Stay by Department (Bar Chart)
  - Infection Rate and Wait Time by Department (Bar Charts)
- **Data Tables:** Patient admissions and KPI breakdowns

---

## 🧱 Tech Stack

- Python
- Pandas & SQLite (ETL + Data Storage)
- Streamlit (Interactive Frontend)
- Plotly Express (Visualizations)

---

## 🗂️ Data Architecture

The project simulates and stores the following tables:

- `patients`
- `admissions`
- `staffing`
- `costs`
- `kpis`

---

## 🚀 How to Run Locally

1. Clone the repo or download the files
2. Ensure the following are in the same folder:
   - `hospital_dashboard_app.py`
   - `hospital_operations.db`
3. Install required packages:
```bash
pip install streamlit pandas plotly
```
4. Run the app:
```bash
streamlit run hospital_dashboard_app.py
```

---

## 🌐 Optional: Deploy to Streamlit Cloud

1. Push the project to GitHub
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Link your GitHub repo and set `hospital_dashboard_app.py` as the entry point
4. Deploy your dashboard and share the link!

---

## 💼 Use Case

This project is ideal for showcasing:
- Data modeling and SQL capabilities
- Healthcare analytics insight
- Dashboard development and KPI storytelling
- Readiness for **Data Analyst** or **Healthcare Business Intelligence** roles

---

## 📬 Author

Built by [Your Name] | [Your LinkedIn or Portfolio URL]