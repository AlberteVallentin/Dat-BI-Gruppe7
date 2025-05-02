import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np

def plot_feature_comparison(df, feature):
    """
    Create bar chart to compare a feature across wine types
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    wine_means = df.groupby('wine_type')[feature].mean()
    
    wine_types = wine_means.index
    means = wine_means.values
    colors = ['darkred' if wt == 'red' else 'gold' for wt in wine_types]
    
    bars = ax.bar(wine_types, means, color=colors)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2., 
            height + 0.01 * max(means), 
            f'{height:.2f}', 
            ha='center', 
            va='bottom'
        )
    
    ax.set_title(f'Average {feature} by Wine Type')
    ax.set_xlabel('Wine Type')
    ax.set_ylabel(feature)
    
    return fig

def plot_feature_violin(df, feature):
    """
    Create violin plot to compare feature distribution across wine types
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.violinplot(
    data=df, 
    x='wine_type', 
    y=feature,
    hue='wine_type',
    palette=['darkred', 'gold'],
    legend=False,
    ax=ax
)
    
    ax.set_title(f'Distribution of {feature} by Wine Type')
    ax.set_xlabel('Wine Type')
    ax.set_ylabel(feature)
    
    return fig

def plot_feature_vs_quality(df, feature):
    """
    Create scatter plot to show relationship between a feature and quality
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.scatterplot(
        data=df,
        x=feature,
        y='quality',
        hue='wine_type',
        palette=['darkred', 'gold'],
        alpha=0.7,
        ax=ax
    )
    
    # Add regression lines for each wine type
    for wine_type in df['wine_type'].unique():
        wine_data = df[df['wine_type'] == wine_type]
        
        if len(wine_data) > 1:  # Need at least 2 points for regression
            color = 'darkred' if wine_type == 'red' else 'gold'
            
            sns.regplot(
                data=wine_data,
                x=feature,
                y='quality',
                scatter=False,
                color=color,
                line_kws={'linestyle': '--'},
                ax=ax
            )
    
    ax.set_title(f'Relationship between {feature} and Wine Quality')
    ax.set_xlabel(feature)
    ax.set_ylabel('Quality')
    
    return fig

def plot_scatter_matrix(df, features, size=(12, 10)):
    """
    Create scatter matrix for selected features
    """
    # Select only the specified features plus wine_type
    plot_df = df[features + ['wine_type']].copy()
    
    # Create scatter matrix
    fig = plt.figure(figsize=size)
    scatter_matrix = pd.plotting.scatter_matrix(
        plot_df,
        alpha=0.8,
        figsize=size,
        diagonal='kde',
        c=df['wine_type'].map({'red': 'darkred', 'white': 'gold'})
    )
    
    # Set title for each subplot
    for ax in scatter_matrix.flatten():
        ax.xaxis.label.set_rotation(45)
        ax.yaxis.label.set_rotation(0)
        ax.yaxis.label.set_ha('right')
    
    plt.tight_layout()
    plt.suptitle('Scatter Matrix of Selected Features', y=1.02, size=16)
    
    return fig

def plot_feature_pair(df, feature1, feature2):
    """
    Create detailed scatter plot between two features
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.scatterplot(
        data=df,
        x=feature1,
        y=feature2,
        hue='wine_type',
        palette=['darkred', 'gold'],
        alpha=0.7,
        ax=ax
    )
    
    # Add regression lines for each wine type
    for wine_type in df['wine_type'].unique():
        wine_data = df[df['wine_type'] == wine_type]
        
        if len(wine_data) > 1:  # Need at least 2 points for regression
            color = 'darkred' if wine_type == 'red' else 'gold'
            
            sns.regplot(
                data=wine_data,
                x=feature1,
                y=feature2,
                scatter=False,
                color=color,
                line_kws={'linestyle': '--'},
                ax=ax
            )
    
    ax.set_title(f'Relationship between {feature1} and {feature2}')
    ax.set_xlabel(feature1)
    ax.set_ylabel(feature2)
    
    return fig