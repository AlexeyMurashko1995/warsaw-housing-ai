# Warsaw Real Estate Price Predictor 🏠🤖

A production-ready data science project designed to scrape, clean, analyze, and predict apartment prices in Warsaw, Poland.

## 🎯 Goal
This project demonstrates the full end-to-end data engineering and machine learning lifecycle: from scraping raw web listings to preprocessing, feature engineering, and deploying a predictive AI model.

## 📊 Project Performance
- **Model Accuracy (R² Score):** **0.787** (Significant improvement from baseline 0.56).
- **Dataset Size:** 1,350+ unique verified listings from Otodom.
- **Key Features:** Area (m²), Number of Rooms, and District (One-Hot Encoded).

## 🛠 Tech Stack
- **Language:** Python 3.x
- **Scraping:** `BeautifulSoup4`, `Requests`
- **Data Engineering:** `Pandas`, `NumPy`
- **Machine Learning:** `Scikit-learn` (Linear Regression)
- **Visualization:** `Matplotlib`

## 📁 Project Structure
- `data_fetcher.py`: Robust scraper with error handling and multi-page support.
- `analytics_pro.py`: Data cleaning, median imputation, outlier removal, and model training.
- `warsaw_apartments.csv`: Raw collected data.
- `apartments_clean.csv`: Preprocessed dataset used for training.

## 🚀 Key Features
- **Data Imputation:** Missing values in the 'rooms' column are handled using median values to ensure outlier robustness.
- **Outlier Filtering:** Automated removal of listings with unrealistic prices per square meter.
- **Price Prediction:** Custom function to estimate the price of any apartment in Warsaw based on user input.

## 📈 Roadmap
- [x] Initial Scraper Setup
- [x] Room Count Extraction & Integration
- [x] Data Cleaning & Imputation (Median-based)
- [x] Model Training & R² Optimization
- [x] Code Refactoring for Clean Code Standards
- [ ] Web Interface Deployment (Streamlit)