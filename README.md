# 📊 Financial Mathematics & Analysis Toolkit

## 📌 Overview
This repository contains two Python-based financial tools designed to automate complex calculations in **Corporate Finance** and **Market Risk Analysis**. 

1.  **NPV & IRR Calculator:** A capital budgeting tool built from scratch using numerical analysis.
2.  **CAPM Analysis:** A regression model that fetches real-time stock data to calculate risk metrics (Alpha & Beta).

---

## 🛠️ Technologies Used
* **Language:** Python 3.x
* **Data Science:** `pandas`, `numpy`
* **Statistics:** `statsmodels` (OLS Regression)
* **Data Fetching:** `yfinance` (Yahoo Finance API)
* **Visualization:** `matplotlib`, `seaborn`

---

## 📂 Project 1: NPV & IRR Calculator
### Description
A custom-built calculator for evaluating investment projects. Unlike standard libraries that use pre-built black-box functions, this tool implements the **Bisection Method** to solve for the Internal Rate of Return (IRR) numerically.

### Key Features
* **Numerical Analysis:** Solves for IRR using iterative root-finding (Sign-Change Logic) rather than built-in functions.
* **Visualizations:** Generates a dual-plot dashboard:
    * *Cash Flow Diagram:* Visualizes inflows (Green) vs. outflows (Red).
    * *NPV Profile:* Plots NPV against discount rates to visually identify the IRR.
* **Sensitivity Analysis:** Automatically calculates project value at 5%, 10%, and 15% discount rates.

### How it works
It utilizes the discrete discounting formula:
$$NPV = \sum_{t=0}^{n} \frac{C_t}{(1+r)^t}$$

---

## 📂 Project 2: CAPM Stock Analysis
### Description
An automated risk analysis tool that evaluates Indian equities using the **Capital Asset Pricing Model (CAPM)**. It downloads historical data for a target stock (e.g., Reliance) and compares it against a benchmark (Nifty 50) and key peers.

### Key Features
* **Real-Time Data:** Fetches 2 years of OHLC data using `yfinance`.
* **Defensive Coding:** Robust handling of data inconsistencies (e.g., missing 'Adj Close' columns).
* **Regression Engine:** Uses Ordinary Least Squares (OLS) to calculate:
    * **Beta ($\beta$):** Systematic Risk / Volatility.
    * **Alpha ($\alpha$):** Excess Return / Manager Skill.
* **Peer Correlation:** Generates a heatmap to analyze correlations with major peers (e.g., HDFC Bank, Infosys).

### Key Insight Example
* *Reliance Industries Analysis:* Found a Beta of **1.23** (High Risk) and a negative Alpha, indicating underperformance relative to the volatility taken.

---

## 🚀 How to Run

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install pandas numpy matplotlib seaborn statsmodels yfinance
