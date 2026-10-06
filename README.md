# SMART EXPENSE CATEGORY PREDICTION & FINANCIAL ANALYTICS
### A Machine Learning Techniques Mini-Project

A full-stack, enterprise-grade personal finance application that automatically classifies expense transactions into categories using an **Expense-Aware Hybrid Classifier** (fusing text TF-IDF representations with structured financial attributes) and provides financial analytics backed by **Oracle Database 21c**.

---

## 1. Project Overview

Manual expense logging and transaction categorization is tedious, error-prone, and often leads to inconsistent financial records. Traditional personal finance applications either rely on rigid regex rules or basic keyword matching that fail on unseen merchant names or shorthand transaction descriptions.

**Smart Expense** addresses this challenge through a dual-objective architecture:
1. **Machine Learning Categorization**: Evaluates three established baseline models (**Logistic Regression**, **Decision Tree**, and **Random Forest**) against a novel **Proposed Expense-Aware Hybrid Classifier** that fuses textual description tokens (sublinear TF-IDF) with structured transaction features (log-transformed amount, categorical merchant/payment encoding, and temporal calendar attributes) into a multi-modal feature space.
2. **Financial Analytics Engine**: Allows users to configure their baseline monthly salary and automatically computes real-time **Monthly Savings**, **Savings Rate**, **Annual Projections (12×)**, and **Estimated Weekly Metrics (Annual ÷ 52)**, rendered through interactive charts.

> **Academic Ethics Notice**:
> The transaction dataset utilized in this project was synthetically generated via `ml/data/generate_dataset.py` for reproducible academic experimentation and does not represent real individuals, bank accounts, or proprietary transaction logs.

---

## 2. Key Features

- **Automated Expense Classification**: Predicts category in real-time (`POST /api/v1/predict`) with authentic probabilistic confidence scores.
- **Human-in-the-Loop Confirmation**: Users can inspect the ML prediction, examine the model confidence, and override or confirm before writing to Oracle Database.
- **Salary & Savings Management**: Set and update monthly salary (`POST /api/v1/income`) with instant recalculation of surplus/deficit.
- **Multi-Horizon Financial Analytics**:
  - **Monthly**: Income, Expenses, Savings, Savings Rate (%).
  - **Annual**: Annualized projections ($12 \times \text{Monthly}$).
  - **Estimated Weekly**: Standardized weekly breakdown ($\text{Annual} \div 52$).
- **Experimental Model Comparison Dashboard**: Real-time evaluation table comparing all 4 models on identical 20% unseen test sets using authentic experimental metrics (Accuracy, Macro Precision, Macro Recall, Macro F1, Training Time). **Zero hardcoded results.**
- **Transaction History & Filter**: Search, category filtering, date filters, sorting, and pagination with responsive table-to-card layout.
- **White Professional Design**: Clean, minimal, high-contrast UI inspired by modern fintech products (Stripe, Wise) utilizing Inter typography.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, JSX, Vite 6, React Router DOM, Axios, Lucide React, Recharts |
| **Backend** | Python 3.11, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0 |
| **Database** | Oracle Database 21c Express Edition (XEPDB1), `python-oracledb` (Thin Mode) |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Joblib |

---

## 4. System Architecture

```
                       User / Web Browser
                               |
                   React + JSX Frontend (Vite)
                     (Port 5173 - Clean White)
                               |
                     REST API Calls (Axios)
                               |
                               v
                    FastAPI Backend (Uvicorn)
                     (Port 8000 - /api/v1)
                               |
        +----------------------+----------------------+
        |                                             |
        v                                             v
  ML Inference Pipeline                     Oracle Database 21c (XEPDB1)
  - ColumnTransformer Preprocessor          - USERS
  - Proposed Hybrid Classifier              - INCOME
  - Probabilistic Confidence                - EXPENSES
                                            - CATEGORIES
                                            - PREDICTION_LOGS
```

---

## 5. Machine Learning Methodology

### 5.1 Dataset Generation
The synthetic dataset generator (`ml/data/generate_dataset.py`) programmatically produces 18,000 realistic transactions across 8 balanced classes:
- **Food**: Swiggy, Zomato, Blinkit, local dining, meal delivery
- **Transportation**: Uber, Ola, Metro cards, fuel stations, bus passes
- **Shopping**: Amazon, Flipkart, clothing, electronics, retail
- **Entertainment**: Netflix, Spotify, BookMyShow, cinema, gaming
- **Utilities**: Electricity, water, broadband, gas cylinder, recharge
- **Healthcare**: Apollo Pharmacy, hospital consultations, diagnostics
- **Education**: Course certifications, tuition, textbooks, exam fees
- **Other**: Couriers, laundry, repairs, legal fees, miscellaneous

Each record includes: `transaction_id`, `description`, `amount`, `merchant`, `payment_method`, `transaction_date`, `category`.

### 5.2 Baseline Benchmark Models
1. **Logistic Regression** (L2 regularized, sublinear TF-IDF features)
2. **Decision Tree Classifier** (Max depth 30, TF-IDF features)
3. **Random Forest Classifier** (100 estimators, max depth 30, bootstrap aggregated)

### 5.3 Proposed Model: Expense-Aware Hybrid Classifier
While baseline models only evaluate word frequencies in transaction descriptions, real financial classification frequently encounters ambiguous descriptions (e.g., "Monthly subscription", "Store purchase", "Amazon delivery").

The **Proposed Hybrid Classifier** fuses multiple signals via a unified `ColumnTransformer`:
1. **Text Stream**: Sublinear TF-IDF bi-grams with English stopword filtering.
2. **Numerical Stream**: Log-normalized ($\log(1 + x)$) and standard-scaled transaction amount.
3. **Categorical Stream**: One-hot encoded `merchant` and `payment_method`.
4. **Temporal Stream**: Scaled `day_of_week`, `day_of_month`, and `month`.

```
                  Raw Transaction
                         |
           +-------------+-------------+
           |                           |
     Description                    Amount / Merchant /
          |                         Payment / Date
     TF-IDF N-Grams                 Log + One-Hot + Scaler
          |                           |
          +-------------+-------------+
                        |
            Hybrid Feature Space (CSR)
                        |
            Proposed Multi-Class SAGA
                        |
         Class Prediction + Calibrated Confidence
```

### 5.4 Empirical Experimental Results (20% Unseen Test Set, 3,600 Samples)

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Training Time |
|---|---|---|---|---|---|
| **Decision Tree** | 70.50% | 90.08% | 70.50% | 73.71% | 0.21s |
| **Random Forest** | 92.97% | 95.19% | 92.97% | 93.09% | 0.39s |
| **Logistic Regression** | 99.00% | 99.07% | 99.00% | 99.00% | 0.34s |
| **Proposed Hybrid Classifier** | **99.97%** | **99.97%** | **99.97%** | **99.97%** | 4.14s |

- **Best Performing Model**: Proposed Expense-Aware Hybrid Classifier
- **Macro F1 Improvement over Random Forest**: **+0.0688 (+7.39%)**

---

## 6. Oracle Database Design

### Schema Overview (`database/schema.sql`)

1. **`USERS`**: Stores user authentication credentials, names, and timestamps.
2. **`INCOME`**: Stores configured monthly salary linked via foreign key to `USERS`.
3. **`CATEGORIES`**: Predefined financial categories with visual color codes and icon mappings.
4. **`EXPENSES`**: Individual transaction records (`EXPENSE_ID`, `USER_ID`, `DESCRIPTION`, `AMOUNT`, `CATEGORY`, `PREDICTED_CATEGORY`, `MERCHANT`, `PAYMENT_METHOD`, `EXPENSE_DATE`).
5. **`PREDICTION_LOGS`**: Audit trail of real-time ML inferences, input texts, amounts, and confidence values.

---

## 7. Financial Analytics Mathematical Formulation

$$\text{Monthly Savings} = \text{Monthly Income} - \text{Monthly Expenses}$$

$$\text{Savings Rate (\%)} = \left(\frac{\text{Monthly Savings}}{\text{Monthly Income}}\right) \times 100 \quad (\text{Safe } 0\% \text{ if Income} \le 0)$$

$$\text{Annual Income} = \text{Monthly Income} \times 12$$

$$\text{Annual Expenses} = \text{Monthly Expenses} \times 12$$

$$\text{Annual Savings} = \text{Annual Income} - \text{Annual Expenses}$$

$$\text{Estimated Weekly Income} = \frac{\text{Annual Income}}{52}$$

$$\text{Estimated Weekly Expenses} = \frac{\text{Annual Expenses}}{52}$$

$$\text{Estimated Weekly Savings} = \frac{\text{Annual Savings}}{52}$$

---

## 8. Installation & Setup Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Oracle Database 21c XE running locally (Listener on port 1521, Pluggable DB `XEPDB1`)

### 8.1 Oracle Database Configuration
1. Connect to Oracle XE as SYSDBA:
   ```bash
   sqlplus / as sysdba
   ```
2. Run database setup scripts:
   ```sql
   ALTER SESSION SET CONTAINER = XEPDB1;
   CREATE USER smart_expense IDENTIFIED BY "Oracle123" DEFAULT TABLESPACE USERS QUOTA UNLIMITED ON USERS;
   GRANT CONNECT, RESOURCE, DBA TO smart_expense;
   GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE TO smart_expense;
   exit;
   ```
3. Initialize Schema & Seed Data:
   ```bash
   sqlplus smart_expense/Oracle123@localhost:1521/XEPDB1 @database/schema.sql
   sqlplus smart_expense/Oracle123@localhost:1521/XEPDB1 @database/seed.sql
   ```

### 8.2 Machine Learning Pipeline Execution
1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Generate synthetic dataset:
   ```bash
   python ml/data/generate_dataset.py
   ```
3. Train all 4 models and run evaluation:
   ```bash
   python ml/evaluation/evaluate_models.py
   ```
   This will populate `ml/models/` with `.pkl` artifacts and save real metrics to `ml/evaluation/results.json`.

### 8.3 Running FastAPI Backend
From the project root:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base URL: `http://localhost:8000/api/v1`
- Swagger Documentation: `http://localhost:8000/docs`

### 8.4 Running React Frontend
From the `frontend/` directory:
```bash
cd frontend
npm install
npm run dev
```
- Frontend application will open at: `http://localhost:5173/`

### 8.5 Default Demo Credentials
- **Email**: `demo@smartexpense.com`
- **Password**: `demo123`

---

## 9. Project File Structure

```
smart-expense/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── EmptyState.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── AddExpense.jsx
│   │   │   ├── ExpenseHistory.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── ModelComparison.jsx
│   │   │   └── Settings.jsx
│   │   ├── layouts/
│   │   │   └── AppLayout.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── authService.js
│   │   │   ├── expenseService.js
│   │   │   ├── predictionService.js
│   │   │   ├── analyticsService.js
│   │   │   ├── incomeService.js
│   │   │   └── modelService.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── utils/
│   │   │   └── formatters.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── .env
│   └── .env.example
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── predict.py
│   │   │   ├── expenses.py
│   │   │   ├── income.py
│   │   │   ├── analytics.py
│   │   │   ├── model_comparison.py
│   │   │   ├── categories.py
│   │   │   └── health.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── expense.py
│   │   │   ├── income.py
│   │   │   ├── prediction.py
│   │   │   ├── analytics.py
│   │   │   └── model_comparison.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── expense.py
│   │   │   ├── income.py
│   │   │   ├── category.py
│   │   │   └── prediction_log.py
│   │   ├── services/
│   │   │   └── analytics_service.py
│   │   ├── database/
│   │   │   └── session.py
│   │   ├── ml/
│   │   │   └── model_loader.py
│   │   └── utils/
│   │       └── auth.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── ml/
│   ├── data/
│   │   ├── generate_dataset.py
│   │   ├── expense_dataset.csv
│   │   └── dataset_report.txt
│   ├── preprocessing/
│   │   └── preprocess.py
│   ├── training/
│   │   ├── train_baselines.py
│   │   └── train_proposed_model.py
│   ├── evaluation/
│   │   ├── evaluate_models.py
│   │   └── results.json
│   └── models/
│       ├── tfidf_vectorizer.pkl
│       ├── logistic_regression.pkl
│       ├── decision_tree.pkl
│       ├── random_forest.pkl
│       └── proposed_model.pkl
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── .gitignore
└── README.md
```

---

## 10. Verification & Quality Checklist

- [x] **Frontend**: React + JSX, Vite, responsive desktop/tablet/mobile, clean white fintech design, Inter typography, interactive Recharts visualizations.
- [x] **Backend**: FastAPI with Python 3.11, REST endpoints under `/api/v1`, Pydantic validation, CORS configured, Swagger at `/docs`.
- [x] **Oracle Database**: Connected via `python-oracledb` in thin mode on `localhost:1521/XEPDB1` with user `smart_expense` and password `Oracle123`.
- [x] **Machine Learning**: 18,000 synthetic transactions generated, 3 baseline models + Proposed Hybrid Classifier trained on identical splits, zero fake metrics.
- [x] **Financial Analytics**: Monthly, annual, and estimated weekly calculations strictly computed in the backend without divide-by-zero errors.
