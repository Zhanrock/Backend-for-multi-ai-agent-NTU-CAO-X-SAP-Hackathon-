# app/utils/helpers.py
import json
import pandas as pd

def load_json(path):
    """Load JSON file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_csv(path):
    """Load CSV file"""
    return pd.read_csv(path, quotechar='"', skip_blank_lines=True)

def save_csv(df, path):
    """Save DataFrame to CSV"""
    df.to_csv(path, index=False)

def get_project_root():
    """Get the project root directory"""
    import os
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
