import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from utils.data_processing import load_data, filter_data
from visualizations.feature_viz import plot_feature_comparison, plot_feature_violin
from visualizations.basic_viz import plot_boxplots

# Set page configuration
st.set_page_config(
    page_title="Wine Comparison - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Wine Type Comparison")
st.write("Compare different chemical properties between red and white wines")

# Sidebar for filters
st.sidebar.header("Data Filters")

# Load data
try:
    df_combined = load_data("combined_wine_data_cleaned.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Wine type filter - force selection of both types for comparison
available_wine_types = df_combined['wine_type'].unique().tolist()
wine_type_filter = st.sidebar.multiselect(
    "Wine Type", 
    options=available_wine_types,
    default=available_wine_types
)

if len(wine_type_filter) < 2 and len(available_wine_types) > 1:
    st.warning("Please select at least two wine types for comparison")

# Quality filter
min_quality, max_quality = int(df_combined['quality'].min()), int(df_combined['quality'].max())
quality_range = st.sidebar.slider(
    "Quality Range", 
    min_value=min_quality, 
    max_value=max_quality,
    value=(min_quality, max_quality)
)

# Apply filters
filtered_df = filter_data(df_combined, wine_type_filter, quality_range)
st.sidebar.write(f"Filtered samples: {len(filtered_df)}")

# Main content
if len(filtered_df['wine_type'].unique()) < 2:
    st.warning("Please select at least two wine types to compare")
    st.stop()

# Feature selection for comparison
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
if 'quality' in numeric_cols:
    numeric_cols.remove('quality')  # Remove quality for separate analysis

comparison_feature = st.selectbox(
    "Select a feature to compare between wine types:",
    options=numeric_cols,
    index=numeric_cols.index('alcohol') if 'alcohol' in numeric_cols else 0
)

# Comparison visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Average {comparison_feature} by Wine Type")
    fig = plot_feature_comparison(filtered_df, comparison_feature)
    st.pyplot(fig)

with col2:
    st.subheader(f"Distribution of {comparison_feature}")
    fig = plot_feature_violin(filtered_df, comparison_feature)
    st.pyplot(fig)

# Statistical test for difference
st.header("Statistical Comparison")

# Compare wine types for the selected feature
wine_types = filtered_df['wine_type'].unique()
if len(wine_types) == 2:
    data1 = filtered_df[filtered_df['wine_type'] == wine_types[0]][comparison_feature].dropna()
    data2 = filtered_df[filtered_df['wine_type'] == wine_types[1]][comparison_feature].dropna()
    
    if len(data1) > 0 and len(data2) > 0:
        # Calculate statistics
        mean1 = data1.mean()
        mean2 = data2.mean()
        median1 = data1.median()
        median2 = data2.median()
        std1 = data1.std()
        std2 = data2.std()
        
        # Display statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{wine_types[0].capitalize()} Wine")
            st.write(f"Mean: {mean1:.4f}")
            st.write(f"Median: {median1:.4f}")
            st.write(f"Standard Deviation: {std1:.4f}")
            st.write(f"Sample Size: {len(data1)}")
        
        with col2:
            st.subheader(f"{wine_types[1].capitalize()} Wine")
            st.write(f"Mean: {mean2:.4f}")
            st.write(f"Median: {median2:.4f}")
            st.write(f"Standard Deviation: {std2:.4f}")
            st.write(f"Sample Size: {len(data2)}")
        
        # Calculate absolute and percentage difference
        abs_diff = abs(mean1 - mean2)
        if min(mean1, mean2) > 0:
            pct_diff = abs_diff / min(mean1, mean2) * 100
            st.write(f"Absolute difference: {abs_diff:.4f} ({pct_diff:.2f}%)")
        else:
            st.write(f"Absolute difference: {abs_diff:.4f}")
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=False)
        
        st.subheader("Independent t-test results")
        st.write(f"t-statistic: {t_stat:.4f}")
        st.write(f"p-value: {p_value:.4f}")
        
        if p_value < 0.05:
            st.write(f"**Interpretation:** There is a statistically significant difference in " +
                   f"{comparison_feature} between {wine_types[0]} and {wine_types[1]} wines (p < 0.05).")
        else:
            st.write(f"**Interpretation:** There is no statistically significant difference in " +
                   f"{comparison_feature} between {wine_types[0]} and {wine_types[1]} wines (p ≥ 0.05).")
    else:
        st.write("Not enough data for statistical testing")
else:
    st.write("Need exactly two wine types for statistical comparison")

# Comparison of multiple features at once
st.header("Comparison of Multiple Features")

# Default important features
default_features = ['alcohol', 'residual sugar', 'pH', 'volatile acidity', 'citric acid', 'sulphates']
# Filter to only include available features
important_features = [f for f in default_features if f in numeric_cols]

selected_features = st.multiselect(
    "Select features to compare:",
    options=numeric_cols,
    default=important_features[:min(6, len(important_features))]
)

if selected_features:
    fig = plot_boxplots(filtered_df, selected_features)
    st.pyplot(fig)
else:
    st.write("Please select at least one feature to compare")

# Summary of key differences
st.header("Summary of Key Differences")

# Calculate differences for key features
key_features = ['alcohol', 'residual sugar', 'fixed acidity', 'volatile acidity', 
               'citric acid', 'pH', 'sulphates', 'density']
key_features = [f for f in key_features if f in numeric_cols]

if len(wine_types) == 2:
    diff_data = []
    for feature in key_features:
        mean1 = filtered_df[filtered_df['wine_type'] == wine_types[0]][feature].mean()
        mean2 = filtered_df[filtered_df['wine_type'] == wine_types[1]][feature].mean()
        abs_diff = abs(mean1 - mean2)
        if min(mean1, mean2) > 0:
            pct_diff = abs_diff / min(mean1, mean2) * 100
        else:
            pct_diff = float('nan')
        
        higher = wine_types[0] if mean1 > mean2 else wine_types[1]
        
        diff_data.append({
            'Feature': feature,
            f'{wine_types[0]} Mean': mean1,
            f'{wine_types[1]} Mean': mean2,
            'Absolute Difference': abs_diff,
            'Percentage Difference': pct_diff,
            'Higher In': higher
        })
    
    # Create DataFrame and sort by percentage difference
    diff_df = pd.DataFrame(diff_data)
    diff_df = diff_df.sort_values('Percentage Difference', ascending=False)
    
    # Format the table
    display_df = diff_df.copy()
    for col in display_df.columns:
        if col not in ['Feature', 'Higher In']:
            if col == 'Percentage Difference':
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/A")
            else:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    st.dataframe(display_df, use_container_width=True)
    
    # Most and least different
    if len(diff_df) > 0:
        most_diff = diff_df.iloc[0]['Feature']
        st.write(f"**Most different feature:** {most_diff} - {wine_types[0].capitalize()} and {wine_types[1].capitalize()} wines differ by {diff_df.iloc[0]['Percentage Difference']:.2f}%")
        
        if len(diff_df) > 1:
            least_diff = diff_df.iloc[-1]['Feature']
            st.write(f"**Least different feature:** {least_diff} - {wine_types[0].capitalize()} and {wine_types[1].capitalize()} wines differ by {diff_df.iloc[-1]['Percentage Difference']:.2f}%")