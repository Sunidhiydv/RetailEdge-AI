import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app_logic import load_data, predict_score

# 1. UI Styling: Wide mode config and Dark/Glassmorphism Theme
st.set_page_config(page_title="Olist Insights Hub", layout="wide", initial_sidebar_state="expanded")

st.markdown('''
<style>
    /* Dark Theme Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(25, 30, 45) 0%, rgb(10, 15, 25) 90%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Elegant Sidebar with Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 20, 30, 0.2) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    h1, h2, h3, p { color: #f1f5f9; }
    
    /* Metric styling for Electric Blue pop */
    [data-testid="stMetricValue"] {
        color: #00e5ff !important; 
        font-weight: 800;
        font-size: 2.2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 1.1rem;
        letter-spacing: 0.03em;
    }
    
    hr {
        border-color: rgba(255, 255, 255, 0.1);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
</style>
''', unsafe_allow_html=True)

# Data loader using Streamlit Cache
@st.cache_data
def get_data():
    return load_data('streamlit_data.csv')

df = get_data()

# 2. Sidebar configuration
with st.sidebar:
    # Logo Placeholder
    st.markdown("""
        <div style="text-align: center; padding-top: 1rem; padding-bottom: 2rem;">
            <div style="background: rgba(0, 229, 255, 0.05); border-radius: 50%; width: 110px; height: 110px; margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 2px solid #00e5ff; box-shadow: 0px 0px 15px rgba(0,229,255,0.2);">
                <span style="font-size: 3rem;">📊</span>
            </div>
            <h2 style="color: #00e5ff; margin-top: 1.2rem; font-weight: bold;">Olist Analyzer</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    nav_selection = st.radio("NAVIGATION", ["Executive Summary", "Category Analytics", "Strategy Simulator"])

# Page Routing
if nav_selection == "Executive Summary":
    st.title("Executive Summary")
    st.write("A high-level overview of our sample dataset and logistics performance.")
    
    # 3. Big Metric Cards
    col1, col2, col3 = st.columns(3)
    if not df.empty:
        total_sample = f"{len(df):,}"
        
        # Searching dynamically for what implies delivery duration
        if 'Delivery_Speed_Days' in df.columns:
            avg_days = round(df['Delivery_Speed_Days'].mean(), 1)
        elif 'Delivery_Delay_Days' in df.columns: # fallback if needed
            avg_days = round(df['Delivery_Delay_Days'].mean(), 1)
        else:
            avg_days = "N/A"
            
        avg_target = round(df['review_score'].mean(), 2) if 'review_score' in df.columns else "N/A"
    else:
        total_sample = "0"
        avg_days = "N/A"
        avg_target = "N/A"

    with col1:
        st.metric("Total Sample Orders", total_sample)
    with col2:
        st.metric("Avg. Delivery (Days)", avg_days)
    with col3:
        st.metric("Target Satisfaction", f"{avg_target} / 5.0")
        
    st.markdown("---")
    
    # Plotly Choropleth Map below
    st.subheader("Brazil Sales Hotspots")
    
    if not df.empty and 'customer_state' in df.columns:
        # Tallying up the orders
        geo_counts = df['customer_state'].value_counts().reset_index()
        geo_counts.columns = ['State', 'Total Orders']
        
        try:
            fig_map = px.choropleth(
                geo_counts,
                geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
                featureidkey="properties.sigla",
                locations="State",
                color="Total Orders",
                color_continuous_scale="Blues",
                title="Geographic Sales Analysis"
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': 'white'},
                margin={"r":0,"t":40,"l":0,"b":0}
            )
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.error("Map unable to load online GeoJSON.")
    else:
        st.info("State data not available for the Choropleth map.")

elif nav_selection == "Category Analytics":
    st.title("Category Analytics")
    if not df.empty and 'product_category_name_english' in df.columns:
        cat_counts = df['product_category_name_english'].value_counts().head(10).reset_index()
        cat_counts.columns = ['Category', 'Sales Volume']
        
        fig_bar = px.bar(cat_counts, x="Sales Volume", y="Category", orientation='h', 
                         color="Sales Volume", color_continuous_scale="Blues",
                         title="Top 10 Selling Product Categories")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': 'white'})
        fig_bar.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Category analytics are empty or missing 'product_category_name_english' data.")

elif nav_selection == "Strategy Simulator":
    # 4. Strategy Simulator Layout
    st.title("Strategy Simulator")
    st.markdown("Shift operational parameters below to dynamically predict their impact on satisfaction.")
    st.markdown("---")
    
    left_col, right_col = st.columns([1.2, 1])
    
    with left_col:
        st.markdown("<h3 style='color: #00e5ff;'>Operational Adjustments</h3>", unsafe_allow_html=True)
        # Interactive Sliders
        price_val = st.slider("💰 Price of Product (R$)", min_value=1.0, max_value=2000.0, value=150.0, step=10.0)
        freight_val = st.slider("🚚 Freight Value (R$)", min_value=0.0, max_value=250.0, value=25.0, step=1.0)
        delivery_days_val = st.slider("⏳ Delivery Speed (Days)", min_value=1.0, max_value=60.0, value=12.0, step=1.0)
    
    with right_col:
        st.markdown("<h3 style='color: #00e5ff;'>Predicted Satisfaction</h3>", unsafe_allow_html=True)
        score = predict_score(price_val, freight_val, delivery_days_val)
        
        if score is not None:
            # Plotly Indicator
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix': ' / 5.0', 'font': {'color': '#00e5ff', 'size': 50}},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [1, 5], 'tickwidth': 2, 'tickcolor': "white"},
                    'bar': {'color': "#00e5ff"},
                    'bgcolor': "rgba(255,255,255,0.05)",
                    'borderwidth': 1.5,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [1, 3], 'color': "rgba(255, 99, 71, 0.4)"},  # Red
                        {'range': [3, 4], 'color': "rgba(255, 215, 0, 0.4)"},  # Yellow/Gold
                        {'range': [4, 5], 'color': "rgba(50, 205, 50, 0.4)"}   # Green
                    ]
                }
            ))
            
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "white"},
                height=350,
                margin={"r":20,"t":20,"l":20,"b":20}
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.warning("Prediction unavailable. Ensure your model and feature pickle files act are present in the folder.")

# 5. Footer Project Methodology
st.markdown("<br><br><br>", unsafe_allow_html=True)  # Spacer
with st.expander("📚 Project Methodology"):
    st.write("""
    ### Random Forest Approach
    
    This simulator acts as an active deployment of a **Random Forest Regressor** pipeline predicting the customer review score.
    
    * **Ensemble Strategy:** Multiple randomized decision trees independently evaluate the customer parameters (Price, Freight, Delay) and converge to find a true average rating.
    * **Robust Predictions:** By aggregating predictions from hundreds of independent trees, our algorithm prevents edge-case overfitting from Olist's diverse e-commerce landscape.
    * **Usage Mechanics:** When sliders are shifted, an active dictionary array mapping matches the original training labels seamlessly to update the Plotly metric via Streamlit cache flows.
    """)
