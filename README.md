# House Price Prediction Project
By Ben Belnap (003177064)

## Project Overview
This project implements a machine learning solution to predict house prices using the Ames Housing Dataset. The goal is to provide quick and accurate home value estimates for a mortgage company, making the appraisal process more efficient and consistent.

## Project Structure
```
House-Price-Prediction-Machine-Learning/
├── data/                   # Dataset storage
├── models/                 # Saved model files
├── notebooks/             # Jupyter notebooks
│   └── house_price_prediction.ipynb
└── src/                   # Source code
```

## Setup Instructions

1. Run the setup script:
```bash
python setup.py
```

2. Activate the virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

3. Download the Ames Housing Dataset from Kaggle and place it in the `data` directory:
[Ames Housing Dataset](https://www.kaggle.com/datasets/prevek18/ames-housing-dataset/data)

4. Launch Jupyter Notebook:
```bash
jupyter notebook
```

## Project Timeline
- Data exploration: August 1st to 3rd
- Data cleaning and preparation: August 4th to 8th
- Modeling: August 9th to 15th
- Evaluation: August 16th to 18th
- Final reporting and documentation: August 19th to 21st

## Success Criteria
The project will be considered successful if the mean absolute error is less than 10% on the test dataset.

## Technologies Used
- Python 3.x
- POLARS
- Pandas
- Scikit-learn
- XGBoost
- Jupyter Notebook
- Matplotlib/Seaborn
