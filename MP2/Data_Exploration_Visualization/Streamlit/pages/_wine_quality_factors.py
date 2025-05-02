# wine_quality_factors.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from utils.data_processing import load_data, filter_data

# Set page configuration
st.set_page_config(
    page_title="Wine Quality Factors - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Wine Quality Factors")
st.write("Learn about non-numeric factors that influence wine quality")

# Sidebar for filters (keeping consistent with other pages)
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

# Helper function to fetch and parse web content
def fetch_web_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Error fetching content: {e}")
        return None

# Simple text summarization function
def summarize_text(text, max_sentences=5):
    # Clean the text
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences - this is a simple approach and can be improved
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', clean_text)
    
    # Select first few sentences for summary (simple extractive summarization)
    summary_sentences = sentences[:max_sentences]
    summary = ' '.join(summary_sentences)
    
    return summary

# Main content
st.header("Non-Numeric Factors Affecting Wine Quality")

# Tabs for different categories of information
tabs = st.tabs(["Geographical Origin", "Production Technology", "Human Taste", "Wine Types"])

# Tab 1: Geographical Origin
with tabs[0]:
    st.subheader("How Geography Affects Wine Quality")
    
    # Fetch content about geographical origin
    geo_url = "https://en.wikipedia.org/wiki/Terroir"
    
    with st.expander("What is Terroir?", expanded=True):
        geo_content = fetch_web_content(geo_url)
        if geo_content:
            soup = BeautifulSoup(geo_content, 'html.parser')
            
            # Get the first paragraph about terroir
            terroir_info = ""
            p_tags = soup.find_all('p')
            for p in p_tags[:3]:  # First few paragraphs
                if p.text.strip():
                    terroir_info += p.text + " "
            
            # Summarize
            if terroir_info:
                summary = summarize_text(terroir_info)
                st.write(summary)
                st.write("Source: [Wikipedia - Terroir](https://en.wikipedia.org/wiki/Terroir)")
            else:
                st.write("Could not extract information about terroir.")
    
    # Wine regions
    with st.expander("Famous Wine Regions"):
        st.write("""
        Different regions are known for producing wines with specific characteristics:
        
        - **Bordeaux, France**: Known for full-bodied reds, primarily from Cabernet Sauvignon and Merlot
        - **Burgundy, France**: Renowned for Pinot Noir (red) and Chardonnay (white)
        - **Tuscany, Italy**: Famous for Chianti and other Sangiovese-based wines
        - **Rioja, Spain**: Known for high-quality Tempranillo wines
        - **Napa Valley, USA**: Celebrated for world-class Cabernet Sauvignon
        - **Marlborough, New Zealand**: Recognized for distinctive Sauvignon Blanc
        """)
        
        # Display a wine regions map or image
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Wine_regions.svg/1000px-Wine_regions.svg.png", 
                 caption="World's Major Wine Regions")

# Tab 2: Production Technology
with tabs[1]:
    st.subheader("Wine Production Technologies")
    
    # Fermentation
    with st.expander("Fermentation Process", expanded=True):
        fermentation_url = "https://en.wikipedia.org/wiki/Winemaking"
        ferment_content = fetch_web_content(fermentation_url)
        
        if ferment_content:
            soup = BeautifulSoup(ferment_content, 'html.parser')
            
            # Extract paragraph about fermentation
            fermentation_info = ""
            ferment_section = soup.find(id="Fermentation")
            if ferment_section:
                parent = ferment_section.parent
                next_tag = parent.find_next_sibling()
                
                while next_tag and next_tag.name == 'p':
                    fermentation_info += next_tag.text + " "
                    next_tag = next_tag.find_next_sibling()
            
            # If we couldn't find the fermentation section, get some general info
            if not fermentation_info:
                p_tags = soup.find_all('p')
                for p in p_tags[:5]:
                    if 'fermentation' in p.text.lower():
                        fermentation_info += p.text + " "
            
            # Summarize the information
            if fermentation_info:
                summary = summarize_text(fermentation_info)
                st.write(summary)
                st.write("Source: [Wikipedia - Winemaking](https://en.wikipedia.org/wiki/Winemaking)")
            else:
                st.write("""
                Fermentation is the process where yeast converts grape sugar into alcohol and carbon dioxide.
                The type of yeast, fermentation temperature, and duration all affect the final wine quality.
                """)
    
    # Aging
    with st.expander("Aging Techniques"):
        st.write("""
        Wine aging significantly impacts quality:
        
        - **Oak Barrel Aging**: Imparts vanilla, toast, and spice flavors
        - **Stainless Steel Aging**: Preserves fresh fruit flavors and acidity
        - **Bottle Aging**: Allows complex flavors to develop over time
        - **Sur Lie Aging**: Adds richness and complexity (common for Chardonnay)
        """)
        
        # Show image of oak barrels
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Oak_barrels_in_Napa_Valley.jpg/1280px-Oak_barrels_in_Napa_Valley.jpg", 
                 caption="Oak Barrel Aging")

# Tab 3: Human Taste
with tabs[2]:
    st.subheader("The Role of Human Taste and Perception")
    
    with st.expander("Wine Tasting Factors", expanded=True):
        st.write("""
        Human perception of wine quality involves multiple sensory aspects:
        
        - **Visual Assessment**: Color and clarity
        - **Aroma/Bouquet**: Detection of primary (grape variety), secondary (fermentation), and tertiary (aging) aromas
        - **Taste**: Balance of sweetness, acidity, tannin, and alcohol
        - **Mouthfeel**: Texture and body of the wine
        - **Finish**: Length and quality of aftertaste
        """)
    
    with st.expander("Professional Wine Evaluation"):
        # Fetch content about wine scoring systems
        scoring_url = "https://en.wikipedia.org/wiki/Wine_rating"
        score_content = fetch_web_content(scoring_url)
        
        if score_content:
            soup = BeautifulSoup(score_content, 'html.parser')
            
            # Extract info about wine scoring
            scoring_info = ""
            p_tags = soup.find_all('p')
            for p in p_tags[:3]:
                if p.text.strip():
                    scoring_info += p.text + " "
            
            if scoring_info:
                summary = summarize_text(scoring_info)
                st.write(summary)
                st.write("Source: [Wikipedia - Wine Rating](https://en.wikipedia.org/wiki/Wine_rating)")
            else:
                st.write("Could not extract information about wine rating systems.")
        
        # Add info about major rating systems
        st.write("""
        Major wine rating systems include:
        
        - **Robert Parker's 100-point scale**: Widely influential in wine pricing
        - **Wine Spectator's 100-point scale**: Used by the major wine publication
        - **Wine Enthusiast's 100-point scale**: Another major publication rating
        - **Decanter's 5-star system**: Popular in the UK and Europe
        """)

# Tab 4: Wine Types
with tabs[3]:
    st.subheader("Different Types of Wine")
    
    # Create columns for red and white wine
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Red Wine Varieties")
        
        red_varieties = {
            "Cabernet Sauvignon": "Full-bodied with high tannins and notes of black currant and cedar",
            "Merlot": "Medium-bodied with soft tannins and plum flavors",
            "Pinot Noir": "Light to medium-bodied with red fruit flavors and earthy notes",
            "Syrah/Shiraz": "Bold with pepper, blackberry, and sometimes smoky flavors",
            "Malbec": "Medium to full-bodied with dark fruit flavors and soft tannins"
        }
        
        for variety, description in red_varieties.items():
            st.markdown(f"**{variety}**: {description}")
    
    with col2:
        st.write("#### White Wine Varieties")
        
        white_varieties = {
            "Chardonnay": "Full-bodied with apple, pear, and often vanilla notes when oaked",
            "Sauvignon Blanc": "Crisp and aromatic with citrus, grass, and tropical fruit notes",
            "Riesling": "Ranges from dry to sweet with high acidity and floral aromas",
            "Pinot Grigio/Gris": "Light-bodied with apple, pear, and mineral notes",
            "Gewürztraminer": "Aromatic with lychee, rose, and spice notes"
        }
        
        for variety, description in white_varieties.items():
            st.markdown(f"**{variety}**: {description}")

# Interactive section
st.header("Interactive Learning")

learning_option = st.selectbox(
    "What would you like to learn more about?",
    ["Wine and Food Pairing", "Understanding Wine Labels", "Wine Storage Tips"]
)

if learning_option == "Wine and Food Pairing":
    st.subheader("Wine and Food Pairing Principles")
    
    pairing_url = "https://en.wikipedia.org/wiki/Wine_and_food_pairing"
    pairing_content = fetch_web_content(pairing_url)
    
    if pairing_content:
        soup = BeautifulSoup(pairing_content, 'html.parser')
        
        # Extract basic principles
        principles_info = ""
        p_tags = soup.find_all('p')
        for p in p_tags[:5]:
            if p.text.strip():
                principles_info += p.text + " "
        
        if principles_info:
            summary = summarize_text(principles_info, max_sentences=3)
            st.write(summary)
            st.write("Source: [Wikipedia - Wine and Food Pairing](https://en.wikipedia.org/wiki/Wine_and_food_pairing)")
    
    # Create a simple pairing table
    st.write("### Quick Pairing Guide")
    
    pairings = {
        "Light white wines (Pinot Grigio)": "Seafood, light salads, light pasta dishes",
        "Full-bodied white wines (Chardonnay)": "Creamy pasta, rich fish dishes, white meat",
        "Light red wines (Pinot Noir)": "Salmon, tuna, mushroom dishes, mild cheeses",
        "Medium red wines (Merlot)": "Chicken, pork, vegetable-based dishes",
        "Full-bodied red wines (Cabernet)": "Red meat, game, aged cheeses"
    }
    
    pairing_df = pd.DataFrame({
        "Wine Type": pairings.keys(),
        "Recommended Food Pairings": pairings.values()
    })
    
    st.table(pairing_df)

elif learning_option == "Understanding Wine Labels":
    st.subheader("How to Read Wine Labels")
    
    # Explain different label components
    st.write("""
    Wine labels contain important information about the wine:
    
    1. **Producer/Winery**: The company that made the wine
    2. **Region**: Where the grapes were grown (e.g., Napa Valley, Bordeaux)
    3. **Varietal/Grape**: The type of grape used (e.g., Cabernet Sauvignon)
    4. **Vintage**: The year the grapes were harvested
    5. **Appellation**: Legal designation of where grapes were grown
    6. **Alcohol Content**: Percentage of alcohol by volume
    """)
    
    # Example images of wine labels
    st.write("#### Example Wine Labels:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Australian_wine_label.jpg/800px-Australian_wine_label.jpg",
                 caption="Example of an Australian Wine Label")
        
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Etiquette_vin_AOC_Bordeaux.jpg/800px-Etiquette_vin_AOC_Bordeaux.jpg",
                 caption="Example of a French Wine Label")

else:  # Wine Storage Tips
    st.subheader("Proper Wine Storage")
    
    st.write("""
    Proper storage significantly impacts wine quality over time:
    
    - **Temperature**: Ideal range is 45-65°F (7-18°C), with 55°F (13°C) being optimal
    - **Humidity**: 60-70% humidity prevents corks from drying out
    - **Light**: Keep wine away from direct sunlight and fluorescent lights
    - **Position**: Store bottles horizontally to keep cork moist
    - **Vibration**: Minimize vibration which can disturb sediment and aging process
    - **Consistency**: Avoid temperature fluctuations which can damage wine
    """)
    
    st.write("#### Wine Storage Duration Guidelines:")
    
    storage_data = {
        "Wine Type": ["Light white wines", "Full-bodied white wines", "Light red wines", "Medium red wines", "Full-bodied red wines"],
        "Optimal Storage Time": ["1-2 years", "2-5 years", "2-5 years", "5-10 years", "10+ years"],
        "Examples": ["Pinot Grigio, Sauvignon Blanc", "Chardonnay, Viognier", "Pinot Noir, Gamay", "Merlot, Zinfandel", "Cabernet Sauvignon, Syrah"]
    }
    
    storage_df = pd.DataFrame(storage_data)
    st.table(storage_df)