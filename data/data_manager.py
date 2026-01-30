import pandas as pd
import os

DATA_FILE = "study_data.csv"

def load_data():
    """Load study data from CSV or create empty dataframe"""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Date", "Subject", "Hours"])
    return df

def save_data(df):
    """Save dataframe to CSV"""
    df.to_csv(DATA_FILE, index=False)

def add_record(date, subject, hours):
    """Add a new study record"""
    df = load_data()
    new_entry = pd.DataFrame([[date, subject, hours]], columns=["Date", "Subject", "Hours"])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    return df
