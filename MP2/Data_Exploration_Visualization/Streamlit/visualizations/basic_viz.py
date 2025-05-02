import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np

def plot_wine_distribution(df):
    """
    Plot distribution of wine types
    """
    wine_counts = df['wine_type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        wine_counts.index, 
        wine_counts.values,
        color=['darkred', 'gold']
    )
    
    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height + 5,
            f'{int(height)}',
            ha='center', 
            va='bottom'
        )
    
    ax.set_title('Distribution of Wine Types')
    ax.set_xlabel('Wine Type')
    ax.set_ylabel('Count')
    
    return fig

def plot_feature_histogram(df, feature, bins=20):
    """
    Plot histogram for a selected feature with wine type differentiation
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.histplot(
        data=df, 
        x=feature, 
        hue='wine_type', 
        bins=bins, 
        kde=True,
        palette=['darkred', 'gold'],
        ax=ax
    )
    
    ax.set_title(f'Distribution of {feature} by Wine Type')
    ax.set_xlabel(feature)
    ax.set_ylabel('Count')
    
    return fig

def plot_quality_distribution(df):
    """
    Plot distribution of wine quality scores
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    quality_counts = df['quality'].value_counts().sort_index()
    
    sns.countplot(
        data=df,
        x='quality',
        hue='wine_type',
        palette=['darkred', 'gold'],
        ax=ax
    )
    
    ax.set_title('Distribution of Wine Quality Scores')
    ax.set_xlabel('Quality Score')
    ax.set_ylabel('Count')
    
    return fig

def plot_correlation_matrix(df, size=(10, 8)):
    """
    Plot correlation matrix for all numeric features
    """
    # Calculate correlation matrix
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=size)
    
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f",
        linewidths=0.5,
        vmin=-1, 
        vmax=1,
        ax=ax
    )
    
    plt.title('Feature Correlation Matrix')
    
    return fig

def plot_boxplots(df, features, ncols=3):
    """
    Plot boxplots for selected features by wine type
    """
    nrows = (len(features) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 4))
    axes = axes.flatten()

    for i, feature in enumerate(features):
        if i < len(axes):
            sns.boxplot(
                data=df,
                x='wine_type',
                y=feature,
                hue='wine_type',
                palette=['darkred', 'gold'],
                ax=axes[i]
            )
            axes[i].set_title(f'{feature} by Wine Type')
            axes[i].set_xlabel('Wine Type')
            axes[i].set_ylabel(feature)

        
            legend = axes[i].get_legend()
            if legend is not None:
                legend.remove()

    for j in range(len(features), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    return fig



def plot_ph_bin_distribution(bin_counts):
    """
    Plot distribution of pH bins
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(
        bin_counts.index,
        bin_counts.values,
        color='skyblue'
    )
    
    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            height + 5,
            f'{int(height)}',
            ha='center', 
            va='bottom'
        )
    
    ax.set_title('Distribution of pH Bins')
    ax.set_xlabel('pH Range')
    ax.set_ylabel('Count')
    
    return fig