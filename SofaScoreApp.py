import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. PAGE SETUP & AESTHETICS
# ==========================================
st.set_page_config(page_title="European Football Analytics", page_icon="⚽", layout="wide")

# Custom CSS for the "Dislocated" Sidebar and Dark Theme Aesthetics
st.markdown("""
    <style>
    /* Main Dark Theme Background */
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Dislocated floating sidebar effect */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
        border-radius: 15px;
        margin: 15px;
        padding: 10px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Custom Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #2b2b2b;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# League Color Dictionary mappings
LEAGUE_COLORS = {
    'England Premier League': '#3D195B',
    'Spain La Liga': '#EE8707',
    'Italy Serie A': '#008FD7',
    'Germany Bundesliga': '#D20515',
    'France Ligue 1': '#DAE025',
    'UEFA Champions League': '#0B0F19',
    'UEFA Europa League': '#F68E00',
    'UEFA Conference League': '#00B140'
}

# ==========================================
# 2. MOCK DATA LOADING (Replace with your Sofascore CSV)
# ==========================================
@st.cache_data
def load_data():
    # In production: return pd.read_csv("D:/Football Analytics/Custom_Football_Historical_Data.csv")
    
    # Mock data to demonstrate functionality
    np.random.seed(42)
    leagues = list(LEAGUE_COLORS.keys())
    data = pd.DataFrame({
        'Player': [f"Player {i}" for i in range(1, 101)],
        'League': np.random.choice(leagues, 100),
        'Position': np.random.choice(['FW', 'MF', 'DF', 'GK'], 100),
        'Country': np.random.choice(['Spain', 'France', 'Brazil', 'England', 'Germany'], 100),
        'Goals': np.random.randint(0, 30, 100),
        'xG': np.random.uniform(0, 25, 100),
        'Big_Chances_Created': np.random.randint(0, 20, 100),
        'Assists': np.random.randint(0, 15, 100),
        'Tackles': np.random.randint(10, 80, 100),
        'Saves': np.random.randint(0, 100, 100),
        # Assuming you have image URLs in your dataset:
        'Player_Image': "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", 
        'Club_Logo': "https://cdn-icons-png.flaticon.com/512/861/861512.png"
    })
    return data

df = load_data()

# ==========================================
# 3. DISLOCATED SIDEBAR FILTERS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1165/1165183.png", width=60)
    st.markdown("### 🎛️ Analytics Engine")
    
    selected_leagues = st.multiselect("🏆 League", df['League'].unique(), default=df['League'].unique()[:2])
    selected_positions = st.multiselect("📍 Position", df['Position'].unique(), default=df['Position'].unique())
    selected_countries = st.multiselect("🌍 Country", df['Country'].unique(), default=df['Country'].unique())
    
    # Filter dataset
    filtered_df = df[
        (df['League'].isin(selected_leagues)) & 
        (df['Position'].isin(selected_positions)) &
        (df['Country'].isin(selected_countries))
    ]

st.title("🇪🇺 European Football Performance Hub (2020-Present)")

# ==========================================
# 4. TABS SETUP
# ==========================================
tab_atk, tab_pass, tab_def, tab_gk, tab_comp = st.tabs([
    "⚔️ Attack", "🎯 Passing", "🛡️ Defence", "🧤 Goalkeeping", "⚖️ Player Comparison"
])

# ------------------------------------------
# TAB 1: ATTACK
# ------------------------------------------
with tab_atk:
    st.subheader("Offensive Output & Threat")
    col1, col2, col3, col4 = st.columns(4)
    # Example metrics
    col1.metric("Top Scorer Goals", int(filtered_df['Goals'].max()))
    col2.metric("Highest xG", round(filtered_df['xG'].max(), 2))
    col3.metric("Total Big Chances Missed", 145) # Replace with real sum
    col4.metric("Avg Shots per 90", 2.4) # Replace with real mean
    
    st.markdown("#### Goals vs xG Outperformance")
    fig = px.scatter(filtered_df, x='xG', y='Goals', hover_name='Player', color='League',
                     color_discrete_map=LEAGUE_COLORS, template='plotly_dark')
    fig.add_shape(type='line', x0=0, y0=0, x1=30, y1=30, line=dict(color='White', dash='dash'))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# TAB 2: PASSING
# ------------------------------------------
with tab_pass:
    st.subheader("Playmaking & Progression")
    st.markdown("#### Big Chances Created vs Assists (Club Level)")
    
    fig_pass = px.scatter(filtered_df, x='Big_Chances_Created', y='Assists', 
                          hover_name='Player', size='Assists', color='League',
                          color_discrete_map=LEAGUE_COLORS, template='plotly_dark')
    st.plotly_chart(fig_pass, use_container_width=True)

# ------------------------------------------
# TAB 3: DEFENCE
# ------------------------------------------
with tab_def:
    st.subheader("Defensive Solidity & Actions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Tackles vs Interceptions")
        # Add your scatter/bar here
    with col2:
        st.markdown("#### Aerial vs Ground Duels Won %")
        # Add your chart here

# ------------------------------------------
# TAB 4: GOALKEEPING
# ------------------------------------------
with tab_gk:
    st.subheader("Shot Stopping & Distribution")
    gk_df = filtered_df[filtered_df['Position'] == 'GK']
    if not gk_df.empty:
        st.dataframe(gk_df[['Player', 'League', 'Saves']], use_container_width=True)
    else:
        st.info("Select 'GK' in the Position filter to view Goalkeeping stats.")

# ------------------------------------------
# TAB 5: PLAYER COMPARISON (Radar & 1v1)
# ------------------------------------------
with tab_comp:
    st.subheader("⚖️ Head-to-Head & Profile Comparison")
    
    comp_type = st.radio("Comparison Mode", ["Player vs League Average", "1v1 Head-to-Head"], horizontal=True)
    
    if comp_type == "1v1 Head-to-Head":
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            p1 = st.selectbox("Select Player 1", df['Player'].unique(), index=0)
            p1_data = df[df['Player'] == p1].iloc[0]
            st.markdown(f"**{p1}** | {p1_data['League']}")
            st.image(p1_data['Player_Image'], width=100) # Player Image
            
        with col_p2:
            p2 = st.selectbox("Select Player 2", df['Player'].unique(), index=1)
            p2_data = df[df['Player'] == p2].iloc[0]
            st.markdown(f"**{p2}** | {p2_data['League']}")
            st.image(p2_data['Player_Image'], width=100) # Player Image
            
        # Radar Chart Generation
        st.markdown("#### Tactical Profile Comparison")
        categories = ['Goals', 'xG', 'Assists', 'Big_Chances_Created', 'Tackles']
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[p1_data[cat] for cat in categories],
            theta=categories,
            fill='toself',
            name=p1,
            line_color='#1f77b4'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[p2_data[cat] for cat in categories],
            theta=categories,
            fill='toself',
            name=p2,
            line_color='#ff7f0e'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(df[categories].max())])),
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.info("Select a player to compare their normalized stats against the positional average in their league.")
        # Implementation for Player vs Average goes here