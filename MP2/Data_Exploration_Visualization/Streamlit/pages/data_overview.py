import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processing import load_data, get_wine_statistics, get_feature_descriptions, filter_data
from visualizations.basic_viz import plot_correlation_matrix, plot_quality_distribution

# Set page configuration
st.set_page_config(
    page_title="Data Overview - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Data Overview")
st.write("Explore the wine quality dataset structure and statistics")

# Sidebar for filters
st.sidebar.header("Data Filters")

# Load data
try:
    df_combined = load_data("combined_wine_data_cleaned.csv")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Wine type filter
available_wine_types = df_combined['wine_type'].unique().tolist()
wine_type_filter = st.sidebar.multiselect(
    "Wine Type", 
    options=available_wine_types,
    default=available_wine_types
)

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
st.header("Dataset Sample")
st.dataframe(filtered_df.head(10), use_container_width=True)

# Dataset information
st.header("Dataset Information")
col1, col2 = st.columns(2)

with col1:
    # Basic stats
    st.subheader("Basic Statistics")
    wine_stats = get_wine_statistics(filtered_df)
    st.write(f"Total samples: {wine_stats['total_samples']}")
    for wine_type in filtered_df['wine_type'].unique():
        count = len(filtered_df[filtered_df['wine_type'] == wine_type])
        st.write(f"{wine_type.capitalize()} wine samples: {count}")
    st.write(f"Quality range: {wine_stats['quality_range'][0]} to {wine_stats['quality_range'][1]}")
    st.write(f"Average quality: {wine_stats['avg_quality']:.2f}")
    st.write(f"Average alcohol content: {wine_stats['avg_alcohol']:.2f}%")
    st.write(f"Average residual sugar: {wine_stats['avg_res_sugar']:.2f} g/dm³")

with col2:
    # Quality distribution
    st.subheader("Quality Distribution")
    fig = plot_quality_distribution(filtered_df)
    st.pyplot(fig)

# Column descriptions
st.header("Dataset Columns")
feature_descriptions = get_feature_descriptions()
col_info = pd.DataFrame({
    'Column': filtered_df.columns,
    'Data Type': filtered_df.dtypes.astype(str),
    'Description': [feature_descriptions.get(col, 'No description available') for col in filtered_df.columns]
})
st.table(col_info)

# Statistical summary
st.header("Statistical Summary")
st.dataframe(filtered_df.describe(), use_container_width=True)

# Correlation analysis
st.header("Correlation Analysis")
st.subheader("Correlation Matrix")
fig = plot_correlation_matrix(filtered_df)
st.pyplot(fig)

# Features most correlated with quality
st.subheader("Features Correlated with Quality")
corr_matrix = filtered_df.select_dtypes(include=[np.number]).corr()
quality_corr = corr_matrix['quality'].drop('quality').sort_values(ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.write("Most Positive Correlations:")
    st.dataframe(quality_corr.head(5), use_container_width=True)
    
with col2:
    st.write("Most Negative Correlations:")
    st.dataframe(quality_corr.sort_values().head(5), use_container_width=True)

# Data quality check
st.header("Data Quality Check")
missing_values = filtered_df.isnull().sum()
duplicates = filtered_df.duplicated().sum()

st.write(f"Missing values across all columns: {missing_values.sum()}")
st.write(f"Duplicate rows: {duplicates}")

if missing_values.sum() > 0:
    st.subheader("Missing Values by Column")
    missing_df = pd.DataFrame({
        'Column': missing_values.index,
        'Missing Values': missing_values.values
    })
    st.dataframe(missing_df[missing_df['Missing Values'] > 0], use_container_width=True)