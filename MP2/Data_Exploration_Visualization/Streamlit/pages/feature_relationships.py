import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processing import load_data, filter_data, get_correlation_stats
from visualizations.feature_viz import plot_feature_pair

# Set page configuration
st.set_page_config(
    page_title="Feature Relationships - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Feature Relationships")
st.write("Explore relationships between different wine characteristics")

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
st.header("Relationship Between Two Features")

# Feature selection
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
if 'quality' in numeric_cols:
    numeric_cols.remove('quality')  # We'll include quality as an option separately

col1, col2 = st.columns(2)

with col1:
    x_feature = st.selectbox(
        "Select X-axis feature:",
        options=numeric_cols,
        index=numeric_cols.index('alcohol') if 'alcohol' in numeric_cols else 0,
        key="scatter_x"
    )

with col2:
    y_feature = st.selectbox(
        "Select Y-axis feature:",
        options=numeric_cols + ['quality'],
        index=(numeric_cols + ['quality']).index('quality') if 'quality' in numeric_cols + ['quality'] else 0,
        key="scatter_y"
    )

# Plot scatter plot with regression lines
fig = plot_feature_pair(filtered_df, x_feature, y_feature)
st.pyplot(fig)

# Display correlation statistics
st.header("Correlation Statistics")

# Overall correlation
overall_corr, overall_interp = get_correlation_stats(filtered_df, x_feature, y_feature)
st.write(f"**Overall correlation:** {overall_corr:.4f} ({overall_interp})")

# Correlation by wine type
col1, col2 = st.columns(2)

for i, wine_type in enumerate(filtered_df['wine_type'].unique()):
    corr, interpretation = get_correlation_stats(filtered_df, x_feature, y_feature, wine_type)
    
    with col1 if i == 0 else col2:
        st.subheader(f"{wine_type.capitalize()} Wine")
        if corr is not None:
            st.write(f"Correlation: {corr:.4f}")
            st.write(f"Interpretation: {interpretation}")
        else:
            st.write("Not enough data for correlation analysis")

# Additional insights
st.header("Additional Insights")

# Calculate statistics for high vs low quality wines
high_quality_threshold = filtered_df['quality'].quantile(0.75)
high_quality = filtered_df[filtered_df['quality'] >= high_quality_threshold]
low_quality = filtered_df[filtered_df['quality'] < high_quality_threshold]

col1, col2 = st.columns(2)

with col1:
    st.subheader("High Quality Wines")
    st.write(f"Number of samples: {len(high_quality)}")
    st.write(f"Mean {x_feature}: {high_quality[x_feature].mean():.4f}")
    st.write(f"Mean {y_feature}: {high_quality[y_feature].mean():.4f}")

with col2:
    st.subheader("Low/Medium Quality Wines")
    st.write(f"Number of samples: {len(low_quality)}")
    st.write(f"Mean {x_feature}: {low_quality[x_feature].mean():.4f}")
    st.write(f"Mean {y_feature}: {low_quality[y_feature].mean():.4f}")

# Feature combinations with strongest correlations
st.header("Feature Combinations with Strongest Correlations")

# Calculate all pairwise correlations
corr_pairs = []

for i, feat1 in enumerate(numeric_cols):
    for feat2 in numeric_cols[i+1:]:  # Avoid duplicates and self-correlations
        corr = filtered_df[[feat1, feat2]].corr().iloc[0, 1]
        corr_pairs.append({
            'Feature 1': feat1,
            'Feature 2': feat2,
            'Correlation': corr,
            'Abs Correlation': abs(corr)
        })

# Create DataFrame and sort by absolute correlation
corr_df = pd.DataFrame(corr_pairs)
corr_df = corr_df.sort_values('Abs Correlation', ascending=False)

# Show top correlations
st.subheader("Top Positive Correlations")
positive_corr = corr_df[corr_df['Correlation'] > 0].head(5)
for _, row in positive_corr.iterrows():
    st.write(f"**{row['Feature 1']} and {row['Feature 2']}:** {row['Correlation']:.4f}")

st.subheader("Top Negative Correlations")
negative_corr = corr_df[corr_df['Correlation'] < 0].head(5)
for _, row in negative_corr.iterrows():
    st.write(f"**{row['Feature 1']} and {row['Feature 2']}:** {row['Correlation']:.4f}")

# Option to visualize a selected top correlation
if len(corr_df) > 0:
    st.subheader("Visualize Top Correlation")
    
    selected_correlation = st.selectbox(
        "Select a correlation to visualize:",
        options=[f"{row['Feature 1']} vs {row['Feature 2']} ({row['Correlation']:.4f})" 
                for _, row in corr_df.head(10).iterrows()]
    )
    
    if selected_correlation:
        # Extract feature names
        feat1, feat2 = selected_correlation.split(' vs ')[0], selected_correlation.split(' vs ')[1].split(' (')[0]
        
        # Plot the selected correlation
        fig = plot_feature_pair(filtered_df, feat1, feat2)
        st.pyplot(fig)