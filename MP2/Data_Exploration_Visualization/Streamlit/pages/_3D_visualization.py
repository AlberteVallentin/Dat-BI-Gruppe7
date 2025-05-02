import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processing import load_data, filter_data
from visualizations.advanced_viz import create_3d_scatter, create_3d_surface, create_3d_surface_with_points, create_pca_visualization

# Set page configuration
st.set_page_config(
    page_title="3D Visualization - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("3D Visualization")
st.write("Explore complex relationships between three variables in 3D space")

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
# Select visualization type
viz_type = st.radio(
    "Choose visualization type:",
    ["3D Scatter Plot", "3D Surface Plot", "PCA Visualization"],
    horizontal=True
)

# Get numeric columns
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
if 'quality' in numeric_cols:
    numeric_cols.remove('quality')  # We'll include quality as an option separately

if viz_type == "3D Scatter Plot":
    st.header("3D Scatter Plot")
    
    st.write("""
    A 3D scatter plot allows you to visualize the relationship between three variables at once.
    Each point represents a wine sample, colored by wine type.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_feature_3d = st.selectbox(
            "Select X-axis feature:",
            options=numeric_cols,
            index=numeric_cols.index('alcohol') if 'alcohol' in numeric_cols else 0,
            key="x_feature_3d"
        )
    
    with col2:
        y_feature_3d = st.selectbox(
            "Select Y-axis feature:",
            options=numeric_cols,
            index=numeric_cols.index('residual sugar') if 'residual sugar' in numeric_cols else 0,
            key="y_feature_3d"
        )
    
    with col3:
        z_feature_3d = st.selectbox(
            "Select Z-axis feature:",
            options=numeric_cols + ['quality'],
            index=(numeric_cols + ['quality']).index('quality') if 'quality' in numeric_cols + ['quality'] else 0,
            key="z_feature_3d"
        )
    
    # Create 3D scatter plot
    fig = create_3d_scatter(filtered_df, x_feature_3d, y_feature_3d, z_feature_3d)
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature correlations
    st.subheader("Pairwise Correlations")
    
    # Calculate correlations
    cols = [x_feature_3d, y_feature_3d, z_feature_3d]
    corr_matrix = filtered_df[cols].corr()
    
    # Display correlation matrix
    st.write("Correlation matrix between selected features:")
    st.write(corr_matrix)

elif viz_type == "3D Surface Plot":
    st.header("3D Surface Plot")
    
    st.write("""
    A 3D surface plot shows how two variables interact to influence a third variable.
    The surface represents a smoothed estimate of the relationship.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        x_surf = st.selectbox(
            "Select X-axis feature:",
            options=numeric_cols,
            index=numeric_cols.index('alcohol') if 'alcohol' in numeric_cols else 0,
            key="x_surf"
        )
    
    with col2:
        y_surf = st.selectbox(
            "Select Y-axis feature:",
            options=numeric_cols,
            index=numeric_cols.index('residual sugar') if 'residual sugar' in numeric_cols else 0,
            key="y_surf"
        )
    
    with col3:
        z_surf = st.selectbox(
            "Select Z-axis feature (to predict):",
            options=numeric_cols + ['quality'],
            index=(numeric_cols + ['quality']).index('quality') if 'quality' in numeric_cols + ['quality'] else 0,
            key="z_surf"
        )
    
    # Select wine type for surface plot
    wine_type_surf = st.radio(
        "Select wine type for surface plot:",
        options=filtered_df['wine_type'].unique().tolist() + ["both"],
        horizontal=True
    )
    
    # Choose whether to show points
    show_points = st.checkbox("Show data points on surface", value=True)
    
    # Create 3D surface plot
    if show_points:
        fig = create_3d_surface_with_points(filtered_df, x_surf, y_surf, z_surf, wine_type_surf)
    else:
        fig = create_3d_surface(filtered_df, x_surf, y_surf, z_surf, wine_type_surf)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        st.subheader("Interpretation")
        st.write(f"""
        This 3D surface shows how {x_surf} and {y_surf} jointly influence {z_surf}.
        
        - Peaks in the surface represent combinations of {x_surf} and {y_surf} that lead to higher {z_surf} values.
        - Valleys represent combinations that lead to lower {z_surf} values.
        - The steepness of the surface indicates how quickly {z_surf} changes as {x_surf} and {y_surf} change.
        """)
    else:
        st.warning("Not enough data to create a meaningful surface plot with the selected parameters.")

else:  # PCA Visualization
    st.header("Principal Component Analysis (PCA)")
    
    st.write("""
    PCA reduces the dimensionality of the data while preserving as much variance as possible.
    This visualization shows the data projected onto the first three principal components.
    """)
    
    # Create PCA visualization
    fig, total_var, components, feature_names = create_pca_visualization(filtered_df)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        
        # Display explained variance
        st.subheader("Explained Variance")
        st.write(f"Total explained variance by the first 3 components: {total_var:.2%}")
        
        # Show PCA components
        st.subheader("Principal Components")
        st.write("The values show how much each original feature contributes to each principal component.")
        
        component_df = pd.DataFrame(
            components,
            columns=feature_names,
            index=[f'PC{i+1}' for i in range(len(components))]
        )
        
        st.dataframe(component_df, use_container_width=True)
        
        # Find top contributing features
        st.subheader("Top Contributing Features")
        
        for i, pc in enumerate(component_df.index):
            # Get absolute contributions and sort
            contributions = component_df.loc[pc].abs().sort_values(ascending=False)
            top_features = contributions.head(3).index.tolist()
            
            st.write(f"**{pc}:** {', '.join(top_features)}")
        
        # Interpretation
        st.subheader("Interpretation")
        st.write("""
        Points that are close to each other in this 3D space have similar characteristics.
        Clusters of points may represent wines with similar properties.
        The distance between points of different wine types shows how different they are.
        """)
    else:
        st.warning("Could not create PCA visualization. Make sure there are enough numeric features and samples.")

# Information about 3D visualizations
st.markdown("---")
st.header("Understanding 3D Visualizations")
st.write("""
3D visualizations are powerful tools for exploring complex relationships that might not be visible in 2D plots.
Here's how to get the most out of them:

1. **Interaction:** Click and drag to rotate the plot. Scroll to zoom in and out.

2. **Patterns to look for:**
   - Clusters of points that might indicate groups of similar wines
   - Trends or patterns that show how variables interact
   - Separations between wine types in the feature space

3. **Limitations:**
   - 3D visualizations can sometimes be hard to interpret from a fixed viewpoint
   - Surface plots use interpolation, which is an estimate of the relationship
   - PCA reduces dimensionality, which means some information is lost
""")