import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata

def create_3d_scatter(df, x_col, y_col, z_col):
    """
    Create an interactive 3D scatter plot using Plotly
    """
    fig = px.scatter_3d(
        df,
        x=x_col,
        y=y_col,
        z=z_col,
        color='wine_type',
        color_discrete_map={'red': 'darkred', 'white': 'gold'},
        opacity=0.7,
        title=f'3D Relationship: {x_col} vs {y_col} vs {z_col}'
    )
    
    # Update layout
    fig.update_layout(
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    
    return fig

def create_3d_surface(df, x_col, y_col, z_col, wine_type=None):
    """
    Create a 3D surface plot to visualize the interaction effect
    """
    # Filter data by wine type if specified
    if wine_type and wine_type != "both":
        plot_data = df[df['wine_type'] == wine_type]
    else:
        plot_data = df
    
    if len(plot_data) < 20:
        st.warning("Not enough data points to create a meaningful surface plot.")
        return None
    
    try:
        # Create a grid for the surface plot
        x_unique = np.linspace(plot_data[x_col].min(), plot_data[x_col].max(), 20)
        y_unique = np.linspace(plot_data[y_col].min(), plot_data[y_col].max(), 20)
        x_grid, y_grid = np.meshgrid(x_unique, y_unique)
        
        # Fit a simple interpolation
        z_grid = griddata(
            (plot_data[x_col], plot_data[y_col]),
            plot_data[z_col],
            (x_grid, y_grid),
            method='cubic'
        )
        
        # Create the 3D surface plot
        fig = go.Figure(data=[
            go.Surface(
                x=x_grid, 
                y=y_grid, 
                z=z_grid,
                colorscale='Viridis'
            )
        ])
        
        fig.update_layout(
            title=f'Surface Plot: Effect of {x_col} and {y_col} on {z_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            ),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating surface plot: {e}")
        return None

def create_3d_surface_with_points(df, x_col, y_col, z_col, wine_type=None):
    """
    Create a 3D surface plot with scatter points
    """
    # Filter data by wine type if specified
    if wine_type and wine_type != "both":
        plot_data = df[df['wine_type'] == wine_type]
    else:
        plot_data = df
    
    if len(plot_data) < 20:
        st.warning("Not enough data points to create a meaningful surface plot.")
        return None
    
    try:
        # Create a grid for the surface plot
        x_unique = np.linspace(plot_data[x_col].min(), plot_data[x_col].max(), 20)
        y_unique = np.linspace(plot_data[y_col].min(), plot_data[y_col].max(), 20)
        x_grid, y_grid = np.meshgrid(x_unique, y_unique)
        
        # Fit a simple interpolation
        z_grid = griddata(
            (plot_data[x_col], plot_data[y_col]),
            plot_data[z_col],
            (x_grid, y_grid),
            method='cubic'
        )
        
        # Create the 3D surface plot with points
        fig = go.Figure(data=[
            go.Surface(
                x=x_grid, 
                y=y_grid, 
                z=z_grid,
                colorscale='Viridis',
                opacity=0.8
            )
        ])
        
        # Add scatter points
        colors = plot_data['wine_type'].map({'red': 'darkred', 'white': 'gold'})
        if wine_type:
            color = 'darkred' if wine_type == 'red' else 'gold'
        else:
            color = colors
            
        fig.add_trace(
            go.Scatter3d(
                x=plot_data[x_col],
                y=plot_data[y_col],
                z=plot_data[z_col],
                mode='markers',
                marker=dict(
                    size=4,
                    color=color,
                    opacity=0.7
                ),
                name='Actual Data Points'
            )
        )
        
        fig.update_layout(
            title=f'Surface Plot with Data Points: {x_col} and {y_col} on {z_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            ),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating surface plot with points: {e}")
        return None

def create_pca_visualization(df, n_components=3):
    """
    Create a 3D visualization of PCA-transformed data
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != 'quality']  # Exclude quality
    
    if len(numeric_cols) < 3:
        st.warning("Not enough numeric features for PCA visualization.")
        return None
    
    try:
        # Standardize the data
        X = df[numeric_cols].values
        X_std = StandardScaler().fit_transform(X)
        
        # Apply PCA
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X_std)
        
        # Create a DataFrame with PCA results
        pca_df = pd.DataFrame(
            data=X_pca,
            columns=[f'PC{i+1}' for i in range(n_components)]
        )
        pca_df['wine_type'] = df['wine_type'].values
        pca_df['quality'] = df['quality'].values
        
        # Create 3D scatter plot
        fig = px.scatter_3d(
            pca_df,
            x='PC1',
            y='PC2',
            z='PC3',
            color='wine_type',
            symbol='quality',
            color_discrete_map={'red': 'darkred', 'white': 'gold'},
            opacity=0.7,
            title='PCA Visualization of Wine Data'
        )
        
        # Update layout
        fig.update_layout(
            scene=dict(
                xaxis_title=f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)',
                yaxis_title=f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)',
                zaxis_title=f'PC3 ({pca.explained_variance_ratio_[2]:.2%} variance)'
            ),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        # Calculate total explained variance
        total_var = sum(pca.explained_variance_ratio_)
        
        return fig, total_var, pca.components_, numeric_cols
    
    except Exception as e:
        st.error(f"Error creating PCA visualization: {e}")
        return None, None, None, None