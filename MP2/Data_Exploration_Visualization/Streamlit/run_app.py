import os
import streamlit.web.cli as stcli
import sys

def run():
    sys.argv = ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    # Ensure the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Check if the data file exists, print message if not
    if not os.path.exists("combined_wine_data_cleaned.csv"):
        print("WARNING: Data file 'data/combined_wine_data_cleaned.csv' not found.")
        print("Please make sure to place the data file in the data directory before running the app.")
    
    # Run the Streamlit app
    run()