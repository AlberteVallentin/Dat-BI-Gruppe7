import pandas as pd
import numpy as np
from scipy import stats

def load_data(file_path):
    """
    Load wine quality data from CSV file
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def get_wine_statistics(df):
    """
    Get basic statistics for wine data
    """
    wine_counts = df['wine_type'].value_counts()
    
    wine_stats = {
        'total_samples': len(df),
        'red_samples': wine_counts.get('red', 0),
        'white_samples': wine_counts.get('white', 0),
        'quality_range': (df['quality'].min(), df['quality'].max()),
        'avg_quality': df['quality'].mean(),
        'avg_alcohol': df['alcohol'].mean(),
        'avg_res_sugar': df['residual sugar'].mean()
    }
    
    return wine_stats

def get_feature_descriptions():
    """
    Return descriptions for wine features
    """
    return {
        'fixed acidity': 'Most acids involved with wine or fixed or nonvolatile (do not evaporate readily)',
        'volatile acidity': 'The amount of acetic acid in wine, which at too high levels can lead to an unpleasant, vinegar taste',
        'citric acid': 'Found in small quantities, citric acid can add freshness and flavor to wines',
        'residual sugar': 'The amount of sugar remaining after fermentation stops',
        'chlorides': 'The amount of salt in the wine',
        'free sulfur dioxide': 'The free form of SO2 exists in equilibrium between molecular SO2 and bisulfite ion',
        'total sulfur dioxide': 'Amount of free and bound forms of S02',
        'density': 'The density of water is close to that of water depending on the percent alcohol and sugar content',
        'pH': 'Describes how acidic or basic a wine is on a scale from 0 (very acidic) to 14 (very basic)',
        'sulphates': 'A wine additive which can contribute to sulfur dioxide gas (S02) levels',
        'alcohol': 'The percent alcohol content of the wine',
        'quality': 'Output variable (based on sensory data, score between 0 and 10)',
        'wine_type': 'Type of wine (red or white)'
    }

def filter_data(df, wine_types=None, quality_range=None):
    """
    Filter data based on wine type and quality range
    """
    filtered_df = df.copy()
    
    if wine_types:
        filtered_df = filtered_df[filtered_df['wine_type'].isin(wine_types)]
    
    if quality_range:
        min_quality, max_quality = quality_range
        filtered_df = filtered_df[
            (filtered_df['quality'] >= min_quality) & 
            (filtered_df['quality'] <= max_quality)
        ]
    
    return filtered_df

def check_normality(df, column, wine_type=None):
    """
    Check if a column follows normal distribution
    """
    if wine_type:
        data = df[df['wine_type'] == wine_type][column].dropna()
    else:
        data = df[column].dropna()
    
    if len(data) < 3:
        return None, None, "Not enough data"
    
    # For large datasets, Shapiro-Wilk may not work, so we'll use D'Agostino's K^2 test instead
    if len(data) > 5000:
        stat, p_value = stats.normaltest(data)
        test_name = "D'Agostino's K^2"
    else:
        stat, p_value = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    
    is_normal = p_value > 0.05
    return stat, p_value, test_name

def get_correlation_stats(df, feature1, feature2, wine_type=None):
    """
    Get correlation statistics between two features
    """
    if wine_type:
        data = df[df['wine_type'] == wine_type][[feature1, feature2]].dropna()
    else:
        data = df[[feature1, feature2]].dropna()
    
    if len(data) < 2:
        return None, "Not enough data"
    
    corr = data.corr().iloc[0, 1]
    
    if abs(corr) < 0.3:
        strength = "weak"
    elif abs(corr) < 0.7:
        strength = "moderate"
    else:
        strength = "strong"
        
    direction = "positive" if corr > 0 else "negative"
    interpretation = f"{strength} {direction} correlation"
    
    return corr, interpretation

def bin_data_by_ph(df, n_bins=5):
    """
    Split the data into subsets by binning the pH attribute
    """
    # Calculate bin edges
    min_ph = df['pH'].min()
    max_ph = df['pH'].max()
    bin_edges = np.linspace(min_ph, max_ph, n_bins + 1)
    
    # Create labels for the bins
    if n_bins == 5:
        labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    else:
        labels = [f'Bin {i+1}' for i in range(n_bins)]
    
    # Apply binning
    df['pH_bin'] = pd.cut(
        df['pH'],
        bins=bin_edges,
        labels=labels,
        include_lowest=True
    )
    
    # Group by bin and get counts
    bin_counts = df['pH_bin'].value_counts().sort_index()
    
    # Create dictionary with subsets
    subsets = {}
    for bin_label in labels:
        subsets[bin_label] = df[df['pH_bin'] == bin_label]
    
    return subsets, bin_counts, bin_edges