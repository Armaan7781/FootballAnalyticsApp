import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚽ Football Analytics - European Leagues",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# DARK THEME CSS - FULL PAGE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #0f1528;
            --bg-tertiary: #1a1f3a;
            --accent: #00d9ff;
            --accent-secondary: #ff0080;
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
            --text-muted: rgba(255, 255, 255, 0.5);
        }
        
        * {
            margin: 0;
            padding: 0;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background-color: #0a0e27 !important;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #0f1528 !important;
        }
        
        [data-testid="stSidebarContent"] {
            background-color: #0f1528 !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background-color: #0f1528 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1a1f3a;
            border-bottom: 2px solid rgba(0, 217, 255, 0.2);
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #1a1f3a;
            color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            padding: 10px 20px;
            margin: 5px;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #00d9ff;
            color: #0a0e27;
            font-weight: 700;
        }
        
        .stTabs [data-baseweb="tab-list"] button:hover {
            background-color: rgba(0, 217, 255, 0.3);
        }
        
        .stMetric {
            background-color: #1a1f3a;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #00d9ff;
        }
        
        .stMetricLabel {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .stMetricValue {
            color: #00d9ff;
        }
        
        .stSelectbox, .stMultiSelect, .stSlider {
            color: #ffffff;
        }
        
        /* Header Gradient */
        .gradient-header {
            background: linear-gradient(90deg, #6A2D84 0%, #4A5FBF 50%, #00d9ff 100%);
            padding: 40px 20px;
            color: white;
            margin: -100px -50px 30px -50px;
            text-align: left;
            border-radius: 0 0 15px 15px;
        }
        
        /* Stats Cards */
        .stat-card {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1528 100%);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }
        
        .stat-value {
            color: #00d9ff;
            font-size: 2em;
            font-weight: 800;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        /* Player Cards */
        .player-card {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1528 100%);
            border: 2px solid rgba(0, 217, 255, 0.4);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .player-card:hover {
            border-color: #00d9ff;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
        }
        
        .player-name {
            color: #00d9ff;
            font-size: 1.3em;
            font-weight: 700;
            margin: 10px 0;
        }
        
        /* Section Headers */
        .section-header {
            color: #00d9ff;
            font-size: 1.5em;
            font-weight: 700;
            margin: 30px 0 15px 0;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.2);
            border-bottom: 2px solid rgba(0, 217, 255, 0.3);
            padding-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

LEAGUE_COLORS = {
    'Spain La Liga': '#FFC000',
    'England Premier League': '#3D195B',
    'Germany Bundesliga': '#DD0000',
    'Italy Serie A': '#003DA5',
    'France Ligue 1': '#004FD5',
    'UEFA Champions League': '#002399',
    'UEFA Europa League': '#f39200',
    'UEFA Conference League': '#6D4C41'
}

# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def load_data():
    """Load player statistics from GitHub repository"""
    try:
        url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
        df = pd.read_csv(url)
        df = df.fillna(0)
        return df
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# Get unique values
all_players = sorted(df['player'].unique().tolist())
all_teams = sorted(df['team'].unique().tolist())
all_leagues = sorted(df['league_name'].unique().tolist())
all_seasons = sorted(df['season_year'].unique().tolist())

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - FILTERS
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("<div class='sidebar-header'>🔍 FILTERS</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# League Filter
selected_leagues = st.sidebar.multiselect(
    "🏆 Leagues",
    options=all_leagues,
    default=all_leagues[:3],
    key="leagues_filter"
)

# Season Filter
selected_seasons = st.sidebar.multiselect(
    "📅 Seasons",
    options=all_seasons,
    default=[all_seasons[-1]],
    key="seasons_filter"
)

# Team Filter
selected_teams = st.sidebar.multiselect(
    "🏢 Teams",
    options=all_teams,
    default=None,
    key="teams_filter"
)

st.sidebar.markdown("---")

# Filter dataframe
filtered_df = df[
    (df['league_name'].isin(selected_leagues)) &
    (df['season_year'].isin(selected_seasons))
]

if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

filtered_players = sorted(filtered_df['player'].unique().tolist())

# Display filter stats
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style='background-color: #1a1f3a; padding: 12px; border-radius: 8px; border-left: 3px solid #00d9ff;'>
    <b>📊 Data Summary</b><br>
    <span style='color: #00d9ff; font-weight: 700;'>{len(filtered_df)}</span> records<br>
    <span style='color: #00d9ff; font-weight: 700;'>{len(filtered_players)}</span> players<br>
    <span style='color: #00d9ff; font-weight: 700;'>{len(selected_leagues)}</span> leagues
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER WITH GRADIENT
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="gradient-header">
        <h1>⚽ EUROPEAN FOOTBALL ANALYTICS 2020-2025</h1>
        <div style="font-size: 1em; color: rgba(255, 255, 255, 0.95); margin-top: 10px; font-weight: 500;">Top 5 Leagues + European Competitions | Real-Time Player Statistics</div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚔️ ATTACK", "🛡️ DEFENCE", "🎯 PASSING", "🥅 GOALKEEPER", "👥 PLAYER COMPARISON"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: ATTACK STATS
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<h2 class='section-header'>⚔️ Attacking Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💥 Avg Goals", f"{filtered_df['goals'].mean():.2f}", delta=f"{filtered_df['goals'].std():.2f}")
    with col2:
        st.metric("🎯 Avg Shots", f"{filtered_df['totalShots'].mean():.2f}", delta=f"{filtered_df['shotsOnTarget'].mean():.2f}")
    with col3:
        st.metric("✨ Avg Assists", f"{filtered_df['assists'].mean():.2f}", delta=f"{filtered_df['bigChancesCreated'].mean():.2f}")
    with col4:
        st.metric("📲 Pass Accuracy", f"{filtered_df['accuratePassesPercentage'].mean():.1f}%", delta=f"{filtered_df['keyPasses'].mean():.2f}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        goals_by_league = filtered_df.groupby('league_name')['goals'].agg(['mean', 'count']).reset_index()
        goals_by_league = goals_by_league.sort_values('mean', ascending=False)
        
        fig_goals = go.Figure(data=go.Bar(
            x=goals_by_league['league_name'],
            y=goals_by_league['mean'],
            marker=dict(color=goals_by_league['mean'], colorscale='Viridis', showscale=True),
            text=goals_by_league['mean'].round(2),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Avg Goals: %{y:.2f}<extra></extra>'
        ))
        fig_goals.update_layout(
            title="⚽ Average Goals by League", xaxis_title="League", yaxis_title="Goals",
            template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    with col2:
        shot_data = filtered_df.groupby('league_name').agg({
            'totalShots': 'mean',
            'shotsOnTarget': 'mean'
        }).reset_index().sort_values('totalShots', ascending=False)
        
        fig_shots = go.Figure()
        fig_shots.add_trace(go.Bar(name='Total Shots', x=shot_data['league_name'], y=shot_data['totalShots'], marker_color='#00d9ff'))
        fig_shots.add_trace(go.Bar(name='Shots on Target', x=shot_data['league_name'], y=shot_data['shotsOnTarget'], marker_color='#ff0080'))
        fig_shots.update_layout(
            title="🎯 Shots Analysis by League", barmode='group', template="plotly_dark",
            height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
        )
        st.plotly_chart(fig_shots, use_container_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Replaced position-level touches with League-level averages
        touches_by_league = filtered_df.groupby('league_name')['touches'].mean().reset_index().sort_values('touches', ascending=False)
        fig_touches = go.Figure(data=go.Bar(
            x=touches_by_league['league_name'], y=touches_by_league['touches'],
            marker_color='#00d9ff', text=touches_by_league['touches'].round(1), textposition='auto'
        ))
        fig_touches.update_layout(title="👆 Average Touches by League", template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_touches, use_container_width=True)
        
    with col2:
        # Replaced position-level goals inside/outside box with League-level averages
        box_data = filtered_df.groupby('league_name').agg({
            'goalsFromInsideTheBox': 'mean',
            'goalsFromOutsideTheBox': 'mean'
        }).reset_index()
        fig_box = go.Figure(data=[
            go.Bar(name='Inside Box', x=box_data['league_name'], y=box_data['goalsFromInsideTheBox'], marker_color='#00d9ff'),
            go.Bar(name='Outside Box', x=box_data['league_name'], y=box_data['goalsFromOutsideTheBox'], marker_color='#ff0080'),
        ])
        fig_box.update_layout(title="📍 Goals Location Analysis by League", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.markdown("<h3 class='section-header'>🏆 Top 10 Scorers</h3>", unsafe_allow_html=True)
    top_scorers = filtered_df.nlargest(10, 'goals')[['player', 'team', 'league_name', 'goals', 'assists', 'totalShots', 'shotsOnTarget']]
    top_scorers.columns = ['Player', 'Team', 'League', 'Goals', 'Assists', 'Shots', 'On Target']
    st.dataframe(top_scorers, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2: DEFENCE STATS
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2 class='section-header'>🛡️ Defensive Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("🤝 Avg Tackles", f"{filtered_df['tackles'].mean():.2f}")
    with col2: st.metric("👁️ Avg Interceptions", f"{filtered_df['interceptions'].mean():.2f}")
    with col3: st.metric("🟩 Avg Blocks", f"{filtered_df['outfielderBlocks'].mean():.2f}")
    with col4: st.metric("🧹 Avg Clearances", f"{filtered_df['clearances'].mean():.2f}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        defence_by_league = filtered_df.groupby('league_name').agg({
            'tackles': 'mean',
            'interceptions': 'mean',
            'outfielderBlocks': 'mean'
        }).reset_index()
        
        fig_defence = go.Figure()
        fig_defence.add_trace(go.Bar(name='Tackles', x=defence_by_league['league_name'], y=defence_by_league['tackles'], marker_color='#00d9ff'))
        fig_defence.add_trace(go.Bar(name='Interceptions', x=defence_by_league['league_name'], y=defence_by_league['interceptions'], marker_color='#ff0080'))
        fig_defence.add_trace(go.Bar(name='Blocks', x=defence_by_league['league_name'], y=defence_by_league['outfielderBlocks'], marker_color='#00ff88'))
        fig_defence.update_layout(title="🛡️ Defensive Actions by League", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_defence, use_container_width=True)
    
    with col2:
        duels_by_league = filtered_df.groupby('league_name').agg({
            'aerialDuelsWon': 'mean',
            'groundDuelsWon': 'mean'
        }).reset_index()
        
        fig_duels = go.Figure()
        fig_duels.add_trace(go.Bar(name='Aerial Duels Won', x=duels_by_league['league_name'], y=duels_by_league['aerialDuelsWon'], marker_color='#00d9ff'))
        fig_duels.add_trace(go.Bar(name='Ground Duels Won', x=duels_by_league['league_name'], y=duels_by_league['groundDuelsWon'], marker_color='#ff0080'))
        fig_duels.update_layout(title="⚔️ Duels Won by League", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_duels, use_container_width=True)
    
    st.markdown("---")
    st.markdown("<h3 class='section-header'>🏆 Top 10 Defenders (by Tackles)</h3>", unsafe_allow_html=True)
    top_defenders = filtered_df.nlargest(10, 'tackles')[['player', 'team', 'league_name', 'tackles', 'interceptions', 'outfielderBlocks', 'clearances']]
    top_defenders.columns = ['Player', 'Team', 'League', 'Tackles', 'Interceptions', 'Blocks', 'Clearances']
    st.dataframe(top_defenders, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PASSING STATS
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<h2 class='section-header'>🎯 Passing Statistics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📲 Pass Accuracy %", f"{filtered_df['accuratePassesPercentage'].mean():.1f}%")
    with col2: st.metric("⚡ Avg Key Passes", f"{filtered_df['keyPasses'].mean():.2f}")
    with col3: st.metric("🎁 Avg Assists", f"{filtered_df['assists'].mean():.2f}")
    with col4: st.metric("✨ Big Chances Created", f"{filtered_df['bigChancesCreated'].mean():.2f}")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        pass_by_league = filtered_df.groupby('league_name')['accuratePassesPercentage'].mean().reset_index().sort_values('accuratePassesPercentage', ascending=False)
        fig_pass = go.Figure(data=go.Bar(
            x=pass_by_league['league_name'], y=pass_by_league['accuratePassesPercentage'],
            marker=dict(color=pass_by_league['accuratePassesPercentage'], colorscale='Plasma', showscale=True),
            text=pass_by_league['accuratePassesPercentage'].round(1), textposition='auto'
        ))
        fig_pass.update_layout(title="📲 Pass Accuracy % by League", template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_pass, use_container_width=True)
    
    with col2:
        assists_data = filtered_df.groupby('league_name').agg({
            'assists': 'mean',
            'bigChancesCreated': 'mean',
            'keyPasses': 'mean'
        }).reset_index()
        
        fig_assists = go.Figure()
        fig_assists.add_trace(go.Bar(name='Assists', x=assists_data['league_name'], y=assists_data['assists'], marker_color='#00d9ff'))
        fig_assists.add_trace(go.Bar(name='Big Chances', x=assists_data['league_name'], y=assists_data['bigChancesCreated'], marker_color='#ff0080'))
        fig_assists.add_trace(go.Bar(name='Key Passes', x=assists_data['league_name'], y=assists_data['keyPasses'], marker_color='#00ff88'))
        fig_assists.update_layout(title="🎁 Creativity Stats by League", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
        st.plotly_chart(fig_assists, use_container_width=True)
        
    st.markdown("---")
    st.markdown("<h3 class='section-header'>🏆 Top 10 Playmakers</h3>", unsafe_allow_html=True)
    top_creators = filtered_df.nlargest(10, 'assists')[['player', 'team', 'league_name', 'assists', 'keyPasses', 'bigChancesCreated', 'accuratePassesPercentage']]
    top_creators.columns = ['Player', 'Team', 'League', 'Assists', 'Key Passes', 'Big Chances', 'Pass %']
    st.dataframe(top_creators, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4: GOALKEEPER STATS
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<h2 class='section-header'>🥅 Goalkeeper Statistics</h2>", unsafe_allow_html=True)
    
    # Auto-identifies goalkeepers by isolating records where made saves > 0
    gk_data = filtered_df[filtered_df['saves'] > 0]
    
    if len(gk_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("🙌 Avg Saves", f"{gk_data['saves'].mean():.2f}")
        with col2: st.metric("🟩 Avg Clean Sheets", f"{gk_data['cleanSheet'].mean():.2f}")
        with col3: st.metric("✋ Avg Parry Saves", f"{gk_data['savesParried'].mean():.2f}")
        with col4: st.metric("⚠️ Errors to Goal", f"{gk_data['errorLeadToGoal'].mean():.2f}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            saves_by_league = gk_data.groupby('league_name').agg({'saves': 'mean', 'cleanSheet': 'mean'}).reset_index()
            fig_saves = go.Figure()
            fig_saves.add_trace(go.Bar(name='Saves', x=saves_by_league['league_name'], y=saves_by_league['saves'], marker_color='#00d9ff'))
            fig_saves.add_trace(go.Bar(name='Clean Sheets', x=saves_by_league['league_name'], y=saves_by_league['cleanSheet'], marker_color='#00ff88'))
            fig_saves.update_layout(title="🙌 GK Performance by League", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
            st.plotly_chart(fig_saves, use_container_width=True)
        
        with col2:
            gk_dist = gk_data.groupby('league_name').agg({'saves': 'mean', 'savesParried': 'mean', 'highClaims': 'mean'}).reset_index()
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(name='Saves', x=gk_dist['league_name'], y=gk_dist['saves'], marker_color='#00d9ff'))
            fig_dist.add_trace(go.Bar(name='Parried', x=gk_dist['league_name'], y=gk_dist['savesParried'], marker_color='#ff0080'))
            fig_dist.add_trace(go.Bar(name='High Claims', x=gk_dist['league_name'], y=gk_dist['highClaims'], marker_color='#00ff88'))
            fig_dist.update_layout(title="🥊 GK Shot-Stopping Distribution", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        st.markdown("---")
        st.markdown("<h3 class='section-header'>🏆 Top 10 Goalkeepers</h3>", unsafe_allow_html=True)
        top_gk = gk_data.nlargest(10, 'saves')[['player', 'team', 'league_name', 'saves', 'cleanSheet', 'savesParried', 'errorLeadToGoal']]
        top_gk.columns = ['Player', 'Team', 'League', 'Saves', 'Clean Sheets', 'Parried', 'Errors']
        st.dataframe(top_gk, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ No goalkeeper statistics extracted matching current league selections.")

# ═══════════════════════════════════════════════════════════════
# TAB 5: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<h2 class='section-header'>👥 Player Comparison</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: player1 = st.selectbox("Select Player 1:", options=[None] + filtered_players, key="p1")
    with col2: player2 = st.selectbox("Select Player 2:", options=[None] + filtered_players, key="p2")
    
    st.markdown("---")
    
    if player1 and player2:
        p1_data = filtered_df[filtered_df['player'] == player1].iloc[0]
        p2_data = filtered_df[filtered_df['player'] == player2].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='player-card'>
                    <div class='player-name'>{player1}</div>
                    <div class='player-meta'>{p1_data['team']} | {p1_data['league_name']}</div>
                    <div style='margin-top: 15px;'>
                        <div class='stat-card'><div class='stat-value'>{int(p1_data['goals'])}</div><div class='stat-label'>GOALS</div></div>
                        <div class='stat-card'><div class='stat-value'>{int(p1_data['assists'])}</div><div class='stat-label'>ASSISTS</div></div>
                        <div class='stat-card'><div class='stat-value'>{int(p1_data['tackles'])}</div><div class='stat-label'>TACKLES</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='player-card'>
                    <div class='player-name'>{player2}</div>
                    <div class='player-meta'>{p2_data['team']} | {p2_data['league_name']}</div>
                    <div style='margin-top: 15px;'>
                        <div class='stat-card'><div class='stat-value'>{int(p2_data['goals'])}</div><div class='stat-label'>GOALS</div></div>
                        <div class='stat-card'><div class='stat-value'>{int(p2_data['assists'])}</div><div class='stat-label'>ASSISTS</div></div>
                        <div class='stat-card'><div class='stat-value'>{int(p2_data['tackles'])}</div><div class='stat-label'>TACKLES</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            comparison_stats = {
                'Goals': [int(p1_data['goals']), int(p2_data['goals'])],
                'Assists': [int(p1_data['assists']), int(p2_data['assists'])],
                'Shots': [int(p1_data['totalShots']), int(p2_data['totalShots'])],
                'Tackles': [int(p1_data['tackles']), int(p2_data['tackles'])],
                'Interceptions': [int(p1_data['interceptions']), int(p2_data['interceptions'])],
            }
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Bar(name=player1, x=list(comparison_stats.keys()), y=[v[0] for v in comparison_stats.values()], marker_color='#00d9ff'))
            fig_compare.add_trace(go.Bar(name=player2, x=list(comparison_stats.keys()), y=[v[1] for v in comparison_stats.values()], marker_color='#ff0080'))
            fig_compare.update_layout(title="📊 Key Stats Comparison", barmode='group', template="plotly_dark", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
            st.plotly_chart(fig_compare, use_container_width=True)
        
        with col2:
            categories = ['Goals', 'Assists', 'Shots', 'Tackles', 'Pass %']
            p1_values = [int(p1_data['goals']), int(p1_data['assists']), int(p1_data['totalShots']), int(p1_data['tackles']), p1_data['accuratePassesPercentage']]
            p2_values = [int(p2_data['goals']), int(p2_data['assists']), int(p2_data['totalShots']), int(p2_data['tackles']), p2_data['accuratePassesPercentage']]
            
            max_vals = [max(p1_values[i], p2_values[i], 1) for i in range(len(categories))]
            p1_norm = [p1_values[i]/max_vals[i]*100 for i in range(len(categories))]
            p2_norm = [p2_values[i]/max_vals[i]*100 for i in range(len(categories))]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=p1_norm, theta=categories, fill='toself', name=player1, line_color='#00d9ff'))
            fig_radar.add_trace(go.Scatterpolar(r=p2_norm, theta=categories, fill='toself', name=player2, line_color='#ff0080'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark", title="🎯 Player Profile Radar", height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27")
            st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown("---")
        st.markdown("<h3 class='section-header'>📋 Detailed Metrics</h3>", unsafe_allow_html=True)
        detailed_comparison = pd.DataFrame({
            'Metric': ['Goals', 'Assists', 'Shots', 'Shots on Target', 'Pass Accuracy %', 'Tackles', 'Interceptions', 'Blocks', 'Appearances', 'Minutes', 'Big Chances Created', 'Key Passes', 'Yellow Cards', 'Red Cards'],
            player1: [int(p1_data['goals']), int(p1_data['assists']), int(p1_data['totalShots']), int(p1_data['shotsOnTarget']), round(p1_data['accuratePassesPercentage'], 2), int(p1_data['tackles']), int(p1_data['interceptions']), int(p1_data['outfielderBlocks']), int(p1_data['appearances']), int(p1_data['minutesPlayed']), int(p1_data['bigChancesCreated']), int(p1_data['keyPasses']), int(p1_data['yellowCards']), int(p1_data['redCards'])],
            player2: [int(p2_data['goals']), int(p2_data['assists']), int(p2_data['totalShots']), int(p2_data['shotsOnTarget']), round(p2_data['accuratePassesPercentage'], 2), int(p2_data['tackles']), int(p2_data['interceptions']), int(p2_data['outfielderBlocks']), int(p2_data['appearances']), int(p2_data['minutesPlayed']), int(p2_data['bigChancesCreated']), int(p2_data['keyPasses']), int(p2_data['yellowCards']), int(p2_data['redCards'])],
        })
        st.dataframe(detailed_comparison, use_container_width=True, hide_index=True)
    else:
        st.info("👥 Select two players to view detailed comparison options.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.5); margin-top: 40px; padding: 20px;'>
        <small>⚽ Football Analytics Dashboard | Powered by Streamlit & Plotly</small><br>
        <small>European Leagues Data | Top 5 Leagues + European Competitions</small>
    </div>
""", unsafe_allow_html=True)
