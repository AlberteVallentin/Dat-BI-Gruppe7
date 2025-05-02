# BI Group 7 – Business Intelligence Mini Projects

**Course:** DAT 2025  
**Institution:** CPH Business Academy, Lyngby  
**Group Members:** Kamilla, Jeanette, Alberte, Juvena, Felicia

---

## Feedback for moderator 
By clicking this link you can view a google docs file where each group member has written their feedback for the Moderator. Just click on a group member's name in the menu to the left.

https://docs.google.com/document/d/1L6qfNpk3U535JQsXDJuy-SeXQDQ6648tX9VZY33LJOs/edit?usp=sharing

---

## Project Overview

This repository contains an overview of mini projects completed as part of the Business Intelligence course. All projects are developed using **Jupyter Notebooks** and focus on key data science skills including preprocessing, exploration, and visualisation.

### MP1 – Data Preprocessing

**Folder:** `MP1/DataPreProcessing`

Topics:
- Working with JSON and image data
- Parsing data from different formats
- Exploratory scripts on tariffs and images

**Key files:**
- `MP1_JSON.ipynb`
- `Trump_Images.ipynb`
- `Trump_Tariffs.ipynb`

### MP2 – Data Exploration and Visualisation

**Folder:** `MP2/Data_Exploration`

Focus:  
A mini project exploring **wine quality data**, using Python for data analysis and visualisation.

**Datasets Used:**
- `winequality-red.xlsx`
- `winequality-white.xlsx`
- `combined_wine_data.xlsx`

---

## Tools Used

- Jupyter Notebook  
- Python (pandas, matplotlib, seaborn, etc.)  
- Power BI (visual reporting)

---

## Running the Streamlit App

To run the Streamlit dashboard locally, follow these steps:

1. **Open Anaconda Navigator**  
   Launch Anaconda and open **VSCode** from within Anaconda.

2. **Navigate to the `Streamlit` Folder**  
   In VSCode, open a terminal and make sure you're in the `Streamlit` directory of the project.

3. **Install Required Packages**  
   In the terminal, run the following command to install all necessary packages:

   ```bash
   pip install streamlit pandas numpy matplotlib seaborn plotly scipy scikit-learn requests beautifulsoup4 transformers
   ```

4. **Run the App**  
   Once dependencies are installed, launch the app with:

   ```bash
   streamlit run main.py
   ```

   This will open a local Streamlit web app in your browser.  
   You can also run these commands in any other terminal (e.g. Windows Terminal, macOS Terminal) as long as your Python environment is activated.
