# Vendor Invoice Intelligence System

**Freight Cost Prediction & Invoice Risk Flagging**

## 📌 Table of Contents
* [Project Overview](#project-overview)
* [Business Objectives](#business-objectives)
* [Data Sources](#data-sources)
* [Exploratory Data Analysis](#exploratory-data-analysis)
* [Models Used](#models-used)
* [Evaluation Metrics](#evaluation-metrics)
* [Application](#application)
* [Project Structure](#project-structure)
* [How to Run This Project](#how-to-run-this-project)
* [Author & Contact](#author--contact)

---

## 📌 Project Overview
This project implements an **end-to-end machine learning system** designed to support finance teams by:
1. **Predicting expected freight cost** for vendor invoices.
2. **Flagging high-risk invoices** that require manual review due to abnormal cost, freight, or operational patterns.

---

## 🎯 Business Objectives

### 1. Freight Cost Prediction (Regression)
**Objective:**
Predict the expected freight cost for a vendor invoice using quantity, invoice value, and historical behavior.

**Why it matters:**
* Freight is a non-trivial component of landed cost.
* Poor freight estimation impacts margin analysis and budgeting.
* Early prediction improves procurement planning and vendor negotiation.

### 2. Invoice Risk Flagging (Classification)
**Objective:**
Predict whether a vendor invoice should be flagged for manual approval due to abnormal cost, freight, or delivery patterns.

**Why it matters:**
* Manual invoice review does not scale.
* Financial leakage often occurs in large or complex invoices.
* Early risk detection improves audit efficiency and operational control.

---

## 📂 Data Sources
Data is stored in a relational SQLite database (`inventory.db`) with the following tables:
* `vendor_invoice` – Invoice-level financial and timing data
* `purchases` – Item-level purchase details
* `purchase_prices` – Reference purchase prices
* `begin_inventory`, `end_inventory` – Inventory snapshots

SQL aggregation is used to generate **invoice-level features**.

---

## 📊 Exploratory Data Analysis (EDA)
EDA focuses on **business-driven questions**, such as:
* Do flagged invoices have higher financial exposure?
* Does freight scale linearly with quantity?
* Does freight cost depend on quantity?

Statistical tests (t-tests) are used to confirm that flagged invoices differ meaningfully from normal invoices.

---

## 🤖 Models Used

### Regression (Freight Prediction)
* Linear Regression (baseline)
* Decision Tree Regressor
* Random Forest Regressor (final model)

### Classification (Invoice Flagging)
* Logistic Regression (baseline)
* Decision Tree Classifier
* Random Forest Classifier (final model with GridSearchCV)

Hyperparameter tuning is performed using **GridSearchCV with F1-score** to handle class imbalance.

---

## 📈 Evaluation Metrics

### Freight Prediction
* MAE
* RMSE
* $R^2$ Score

### Invoice Flagging
* Accuracy
* Precision, Recall, F1-score
* Classification report
* Feature importance analysis

---

## 🖥️ End-to-End Application
A **Streamlit application** demonstrates the complete pipeline:
* Input invoice details
* Predict expected freight
* Flag invoices in real time
* Provide human-readable explanations

---

## 📂 Project Structure
```text
inventory-invoice-analytics/
├── data/
│   └── inventory.db
├── freight_cost_prediction/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
├── invoice_flagging/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
├── inference/
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
├── models/
│   ├── predict_freight_model.pkl
│   ├── scaler.pkl
│   └── Invoice Flagging.pkl
├── notebooks/
│   └── Predict Freight Cost.ipynb
├── app.py
├── README.md
└── .gitignore
---

## 👤 Author

**Rahidur Rahman**  
Bachelor of Science in Computer Science & Engineering  
*East Delta University (2025)*  

🔗 [LinkedIn](https://www.linkedin.com/in/rahidur-rahman/)  
📧 rahidurrahman12@gmail.com  
💻 [GitHub](https://github.com/rahidur12)

---

⭐ *If you find this project useful, feel free to star the repository!*
