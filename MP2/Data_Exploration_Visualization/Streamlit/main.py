import streamlit as st
import pandas as pd
from utils.data_processing import load_data, get_wine_statistics
from visualizations.basic_viz import plot_wine_distribution, plot_quality_distribution

# Set page configuration
st.set_page_config(
    page_title="Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

# Application title
st.title("Wine Quality Analysis")
st.write("Explore factors affecting wine quality through data visualization and analysis.")

# Load data
try:
    df_combined = load_data("combined_wine_data_cleaned.csv")
    st.success("Dataset successfully loaded!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Get basic statistics
wine_stats = get_wine_statistics(df_combined)

# Show basic overview
st.header("Dataset Overview")
col1, col2 = st.columns(2)

with col1:
    st.write(f"**Total samples:** {wine_stats['total_samples']}")
    st.write(f"**Red wine samples:** {wine_stats['red_samples']}")
    st.write(f"**White wine samples:** {wine_stats['white_samples']}")
    st.write(f"**Quality range:** {wine_stats['quality_range'][0]} to {wine_stats['quality_range'][1]}")
    st.write(f"**Average quality score:** {wine_stats['avg_quality']:.2f}")

with col2:
    st.subheader("Wine Type Distribution")
    fig = plot_wine_distribution(df_combined)
    st.pyplot(fig)

# Show sample of the data
st.header("Sample Data")
st.dataframe(df_combined.head(10), use_container_width=True)

# Information about navigation
st.header("App Navigation")
st.markdown("""
Use the sidebar to navigate between different pages:

1. **Data Overview** - Explore the dataset structure and basic statistics
2. **Wine Comparison** - Compare properties between red and white wines
3. **Feature Analysis** - Analyze individual features and their distributions
4. **Feature Relationships** - Explore relationships between different features
5. **3D Visualization** - View complex relationships in 3D visualizations
""")

# Information about wine quality
st.header("Wine Quality Information")
st.write("""
The quality of wine is influenced by various chemical properties.
Key factors that tend to positively influence wine quality include:

- **Alcohol Content**: Higher alcohol content often correlates with better quality
- **Acidity Balance**: The right balance of fixed acidity, volatile acidity, and citric acid
- **Sulphates**: Moderate levels of sulphates tend to preserve wine better
- **pH**: The proper pH level helps with wine stability and taste

Red and white wines have different characteristics:
* White wines typically have higher residual sugar and sulfur dioxide levels
* Red wines typically have higher fixed acidity and sulphates
""")

# How to use the app
st.header("How to Use This App")
st.write("""
1. Navigate through the pages using the sidebar menu
2. Select different features and parameters to visualize
3. Compare properties of red and white wines
4. Explore what factors influence wine quality
5. Analyze feature relationships and distributions
""")