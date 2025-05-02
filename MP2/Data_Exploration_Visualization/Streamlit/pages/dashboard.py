import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_processing import load_data, filter_data
from visualizations.basic_viz import plot_wine_distribution, plot_quality_distribution, plot_correlation_matrix
from visualizations.feature_viz import plot_feature_comparison, plot_feature_vs_quality
from visualizations.advanced_viz import create_3d_scatter

# Set page configuration
st.set_page_config(
    page_title="Dashboard - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Wine Quality Dashboard")
st.write("Key visualizations and insights at a glance")

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

# Quick statistics at the top
st.header("Quick Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Samples", len(filtered_df))

with col2:
    red_samples = len(filtered_df[filtered_df['wine_type'] == 'red']) if 'red' in wine_type_filter else 0
    white_samples = len(filtered_df[filtered_df['wine_type'] == 'white']) if 'white' in wine_type_filter else 0
    
    if 'red' in wine_type_filter and 'white' in wine_type_filter:
        st.metric("Red/White Ratio", f"{red_samples}:{white_samples}")
    elif 'red' in wine_type_filter:
        st.metric("Red Wine Samples", red_samples)
    elif 'white' in wine_type_filter:
        st.metric("White Wine Samples", white_samples)

with col3:
    avg_quality = filtered_df['quality'].mean()
    st.metric("Average Quality", f"{avg_quality:.2f}")

with col4:
    avg_alcohol = filtered_df['alcohol'].mean()
    st.metric("Average Alcohol", f"{avg_alcohol:.2f}%")

# Row 1: Wine Distribution and Quality Distribution
st.header("Wine Types and Quality")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Wine Type Distribution")
    fig1 = plot_wine_distribution(filtered_df)
    st.pyplot(fig1)

with col2:
    st.subheader("Quality Distribution")
    fig2 = plot_quality_distribution(filtered_df)
    st.pyplot(fig2)

# Row 2: Key Feature Comparisons
st.header("Key Feature Comparisons")

# Choose 2 important features to compare
important_features = ['alcohol', 'residual sugar'] 

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Average {important_features[0]} by Wine Type")
    fig3 = plot_feature_comparison(filtered_df, important_features[0])
    st.pyplot(fig3)

with col2:
    st.subheader(f"Average {important_features[1]} by Wine Type")
    fig4 = plot_feature_comparison(filtered_df, important_features[1])
    st.pyplot(fig4)

# Row 3: Feature vs Quality
st.header("Quality Drivers")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Effect of {important_features[0]} on Wine Quality")
    fig5 = plot_feature_vs_quality(filtered_df, important_features[0])
    st.pyplot(fig5)

with col2:
    st.subheader(f"Effect of {important_features[1]} on Wine Quality")
    fig6 = plot_feature_vs_quality(filtered_df, important_features[1])
    st.pyplot(fig6)

# Row 4: Correlation Heatmap
st.header("Feature Correlations")
st.subheader("Correlation Matrix")
# Get only numeric columns for the correlation matrix, and limit to most important features
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
selected_cols = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 
                'chlorides', 'alcohol', 'pH', 'sulphates', 'quality']
# Ensure all selected columns exist in the dataset
selected_cols = [col for col in selected_cols if col in numeric_cols]

# Calculate correlation matrix for selected columns
corr_df = filtered_df[selected_cols]
fig7 = plot_correlation_matrix(corr_df, size=(10, 8))
st.pyplot(fig7)

# Row 5: 3D Visualization
st.header("3D Visualization")
st.subheader("Relationship between Key Features")

# This will show a 3D scatter plot of alcohol, residual sugar, and quality
fig8 = create_3d_scatter(filtered_df, 'alcohol', 'residual sugar', 'quality')
st.plotly_chart(fig8, use_container_width=True)

# Add insights section at the bottom
st.header("Key Insights")

# Calculate correlations with quality
quality_corr = filtered_df.corr()['quality'].drop('quality').sort_values(ascending=False)

# Find the top positive and negative correlations
top_pos = quality_corr.head(3)
top_neg = quality_corr.tail(3)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Positive Quality Factors")
    for feature, corr in top_pos.items():
        st.write(f"**{feature}**: {corr:.4f} correlation with quality")

with col2:
    st.subheader("Negative Quality Factors")
    for feature, corr in top_neg.items():
        st.write(f"**{feature}**: {corr:.4f} correlation with quality")

# Summarize differences between red and white wine
if 'red' in wine_type_filter and 'white' in wine_type_filter:
    st.subheader("Red vs White Wine Differences")
    
    # Key differences
    key_features = ['alcohol', 'residual sugar', 'fixed acidity', 'volatile acidity', 
                   'citric acid', 'pH', 'sulphates', 'density']
    key_features = [f for f in key_features if f in numeric_cols]
    
    differences = []
    for feature in key_features:
        red_mean = filtered_df[filtered_df['wine_type'] == 'red'][feature].mean()
        white_mean = filtered_df[filtered_df['wine_type'] == 'white'][feature].mean()
        abs_diff = abs(red_mean - white_mean)
        if min(red_mean, white_mean) > 0:
            pct_diff = abs_diff / min(red_mean, white_mean) * 100
        else:
            pct_diff = float('nan')
        
        higher = 'red' if red_mean > white_mean else 'white'
        
        differences.append({
            'Feature': feature,
            'Red Mean': red_mean,
            'White Mean': white_mean,
            'Absolute Difference': abs_diff,
            'Percentage Difference': pct_diff,
            'Higher In': higher
        })
    
    # Create DataFrame and sort by percentage difference
    diff_df = pd.DataFrame(differences)
    diff_df = diff_df.sort_values('Percentage Difference', ascending=False)
    
    # Show top 3 differences
    for i, row in diff_df.head(3).iterrows():
        feature = row['Feature']
        pct = row['Percentage Difference']
        higher = row['Higher In']
        red_val = row['Red Mean']
        white_val = row['White Mean']
        
        st.write(f"**{feature}**: {higher.capitalize()} wine has {pct:.1f}% higher {feature} " +
                f"(Red: {red_val:.2f}, White: {white_val:.2f})")
    
    # Quality difference
    red_quality = filtered_df[filtered_df['wine_type'] == 'red']['quality'].mean()
    white_quality = filtered_df[filtered_df['wine_type'] == 'white']['quality'].mean()
    quality_diff = abs(red_quality - white_quality)
    higher_quality = 'red' if red_quality > white_quality else 'white'
    
    st.write(f"**Quality**: {higher_quality.capitalize()} wine has higher average quality " +
            f"(Red: {red_quality:.2f}, White: {white_quality:.2f}, Difference: {quality_diff:.2f})")