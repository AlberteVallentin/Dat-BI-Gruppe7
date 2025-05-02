import streamlit as st
import pandas as pd
from utils.web_scraper import fetch_web_content, search_youtube_videos
from utils.text_processing import summarize_text
from utils.data_processing import load_data, filter_data

# Set page configuration
st.set_page_config(
    page_title="Wine Education - Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

st.title("Wine Education Resources")
st.write("Learn more about wine quality from experts and educational resources")

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

# Main content
st.header("Video Resources")

# Topics for YouTube videos
topics = [
    "Wine tasting techniques",
    "Understanding wine quality factors",
    "How wine aging affects quality",
    "Wine regions and terroir",
    "Wine fermentation process explained",
    "Red vs white wine production differences"
]

selected_topic = st.selectbox("Select a topic to explore:", topics)

st.subheader(f"Videos about: {selected_topic}")

# Search for videos on the selected topic
with st.spinner("Searching for educational videos..."):
    video_urls = search_youtube_videos(selected_topic + " wine", max_results=3)

if video_urls:
    for i, url in enumerate(video_urls):
        video_id = url.split("v=")[1]
        st.write(f"Video {i+1}:")
        st.video(url)
else:
    st.write("No videos found for this topic. Try another search term.")

# Expert insights section
st.header("Expert Insights")

expert_topics = {
    "Wine Critics": "https://en.wikipedia.org/wiki/Wine_critic",
    "Sommelier": "https://en.wikipedia.org/wiki/Sommelier",
    "Winemaking": "https://en.wikipedia.org/wiki/Winemaking",
    "Wine Faults": "https://en.wikipedia.org/wiki/Wine_fault"
}

selected_expert_topic = st.selectbox("Select a topic to learn about:", list(expert_topics.keys()))

# Fetch and display content for the selected topic
with st.spinner(f"Fetching information about {selected_expert_topic}..."):
    url = expert_topics[selected_expert_topic]
    content = fetch_web_content(url)
    
    if content:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the first few paragraphs
        paragraphs = soup.find_all('p')
        topic_text = ""
        for p in paragraphs[:5]:
            if p.text.strip():
                topic_text += p.text + " "
        
        # Summarize the content
        if topic_text:
            summary = summarize_text(topic_text, max_sentences=5)
            st.write(summary)
            st.write(f"Source: [Wikipedia - {selected_expert_topic}]({url})")
        else:
            st.write(f"Could not extract information about {selected_expert_topic}.")
    else:
        st.write(f"Could not fetch information about {selected_expert_topic}.")

# Interactive Q&A section
st.header("Wine Quality FAQ")

questions = [
    "What makes a wine 'good quality'?",
    "How does climate affect wine quality?",
    "What is the role of tannins in wine quality?",
    "How important is vintage in determining wine quality?",
    "What does 'balance' mean in wine tasting?",
    "How does oak aging affect wine quality?",
    "What's the relationship between price and quality in wine?"
]

selected_question = st.selectbox("Select a question:", questions)

# Predefined answers to common questions
answers = {
    "What makes a wine 'good quality'?": """
    Wine quality is subjective but generally assessed on several factors:
    
    - **Balance**: No single component (acidity, tannin, alcohol, sweetness) dominates
- **Complexity**: Multiple layers of flavors and aromas that develop over time
    - **Length**: How long the flavors persist after swallowing
    - **Typicity**: How well it represents its grape variety and region
    - **Structure**: The framework of acid, tannin, alcohol that supports the flavors
    - **Intensity**: Concentration and depth of flavor
    
    Professional wine critics often use standardized methods like blind tasting to evaluate quality objectively, though personal preference always plays a role in wine appreciation.
    """,
    
    "How does climate affect wine quality?": """
    Climate is one of the most significant factors affecting wine quality:
    
    - **Cool climate regions** (like Burgundy or Germany) tend to produce wines with higher acidity, lower alcohol, and more delicate flavors
    - **Warm climate regions** (like parts of California or Australia) often produce fuller-bodied wines with higher alcohol, riper fruit flavors, and lower acidity
    - **Diurnal temperature variation** (difference between day and night temperatures) helps develop complexity while preserving acidity
    - **Rainfall timing and amount** affects grape development and can influence harvest decisions
    - **Climate change** is significantly impacting wine regions globally, altering traditional growing patterns and quality parameters
    """,
    
    "What is the role of tannins in wine quality?": """
    Tannins are natural compounds found primarily in red wines that contribute significantly to quality:
    
    - They provide **structure and texture**, creating the drying, astringent sensation felt in the mouth
    - **High-quality tannins** feel smooth and integrated rather than harsh or bitter
    - They contribute to a wine's **aging potential** by acting as natural preservatives
    - They help create **balance** with other components like fruit, acid, and alcohol
    - The **source of tannins** matters: grape skin and seed tannins differ from oak barrel tannins
    - **Tannin management** during winemaking is a critical skill that impacts final wine quality
    """,
    
    "How important is vintage in determining wine quality?": """
    Vintage (the year grapes were harvested) can significantly impact wine quality:
    
    - **Weather conditions** during the growing season affect grape ripeness, flavor development, and overall quality
    - Regions with **variable climates** (like Bordeaux or Burgundy) show more vintage variation than consistent climate regions
    - **Great vintages** occur when weather conditions are optimal throughout the growing season
    - **Challenging vintages** may still produce excellent wines from skilled winemakers
    - Vintage importance varies by **wine style**: it's typically more crucial for age-worthy red wines than for wines meant to be consumed young
    - Understanding vintage conditions helps consumers **set expectations** about a wine's character and quality
    """,
    
    "What does 'balance' mean in wine tasting?": """
    Balance is perhaps the most important indicator of quality in wine:
    
    - It refers to the **harmonious integration** of all components: fruit, acid, tannin, alcohol, and oak
    - In a balanced wine, no single element **overwhelms** the others
    - Different wine styles have different **balance points**: a dessert wine has higher sweetness but is balanced by high acidity
    - **Unbalanced wines** might feel too acidic, too alcoholic, too tannic, or too sweet
    - Balance contributes to a wine's **drinkability** and often its **aging potential**
    - It's often described as a wine feeling "complete" or "harmonious" when tasted
    """,
    
    "How does oak aging affect wine quality?": """
    Oak aging is a traditional technique that can significantly influence wine quality:
    
    - It adds **complexity** through flavors like vanilla, spice, toast, coconut, or smoke
    - It allows **controlled oxidation**, softening the wine's structure over time
    - Oak contributes **tannins** that can enhance structure and aging potential
    - **New oak** imparts stronger flavors than older, previously used barrels
    - **Oak origin** (French, American, etc.) affects the flavor profile
    - **Over-oaking** can mask the wine's inherent character and is considered a quality flaw
    - High-quality wines show **integration** between oak and wine components
    """,
    
    "What's the relationship between price and quality in wine?": """
    The relationship between wine price and quality is complex:
    
    - There's **generally a correlation** between price and quality up to a certain point
    - **Diminishing returns** occur at higher price points, where small quality increases cost much more
    - **Production costs** (vineyard location, harvesting methods, aging requirements) influence price
    - **Scarcity and demand** often drive prices more than objective quality measures
    - **Brand prestige and reputation** can significantly affect price regardless of quality
    - **Value wines** can offer excellent quality-to-price ratios, especially from less famous regions
    - **Blind tasting studies** regularly show that price and perceived quality correlate less than expected
    """
}

# Display the answer to the selected question
if selected_question in answers:
    st.write(answers[selected_question])

# Wine vocabulary section
st.header("Wine Vocabulary")

# Create a dataframe with wine terms and definitions
wine_terms = {
    "Acidity": "The tart or sour taste in wine that gives it freshness and structure",
    "Body": "The perceived weight and fullness of wine in the mouth (light, medium, or full)",
    "Bouquet": "The complex aromas that develop in aged wines",
    "Finish": "The aftertaste or final impression of a wine after swallowing",
    "Legs": "The streams that form on the glass when swirling wine, indicating alcohol content",
    "Mouthfeel": "The texture and physical sensations of wine in the mouth",
    "Nose": "The aroma or smell of a wine",
    "Tannin": "Astringent compounds that create a drying sensation in the mouth",
    "Terroir": "The complete natural environment in which a wine is produced",
    "Vintage": "The year in which the grapes for a wine were harvested"
}

terms_df = pd.DataFrame({
    "Term": wine_terms.keys(),
    "Definition": wine_terms.values()
})

# Display the wine vocabulary table
st.dataframe(terms_df, use_container_width=True)

# Wine quality assessment guide
st.header("DIY Wine Quality Assessment")

st.write("""
### How to Evaluate Wine Quality Yourself

Follow these steps to assess wine quality like a professional:

1. **Look** at the wine:
   - Check clarity, color depth, and viscosity
   - Tilt the glass to observe color variation from rim to center

2. **Smell** the wine:
   - First impression: initial aromas immediately after pouring
   - Swirl and smell again: releases more complex aromas
   - Identify primary (grape), secondary (fermentation), and tertiary (aging) aromas

3. **Taste** the wine:
   - Take a small sip and "chew" it to spread across your palate
   - Assess sweetness, acidity, tannin, body, and alcohol
   - Note the progression of flavors from initial taste to finish
   - Evaluate balance, complexity, and length

4. **Consider** the context:
   - Is the wine typical of its variety and region?
   - Does it show appropriate development for its age?
   - How does it compare to other wines of similar type?

Remember that practice improves your tasting ability, and keeping notes helps track your observations and preferences.
""")

# Footer with additional resources
st.markdown("---")
st.subheader("Additional Resources")

st.write("""
- [Wine Spectator](https://www.winespectator.com/) - Wine ratings, reviews, and education
- [Wine Folly](https://winefolly.com/) - Wine education and visual guides
- [GuildSomm](https://www.guildsomm.com/) - Professional resource for wine knowledge
- [Court of Master Sommeliers](https://www.mastersommeliers.org/) - Professional wine education
""")