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
        
        .subsection-header {
            color: #00ff88;
            font-size: 1.2em;
            font-weight: 600;
            margin: 20px 0 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# STAT CATEGORIES DEFINITION
# ═══════════════════════════════════════════════════════════════

ATTACKING_STATS = {
    'Goals': 'goals',
    'Assists': 'assists',
    'Total Shots': 'totalShots',
    'Shots on Target': 'shotsOnTarget',
    'Goals Inside Box': 'goalsFromInsideTheBox',
    'Goals Outside Box': 'goalsFromOutsideTheBox',
    'Big Chances Created': 'bigChancesCreated',
    'Expected Goals': 'expectedGoals',
    'Goal Conversion %': 'goalConversionPercentage',
    'Headed Goals': 'headedGoals',
    'Left Foot Goals': 'leftFootGoals',
    'Right Foot Goals': 'rightFootGoals',
}

PASSING_STATS = {
    'Pass Accuracy %': 'accuratePassesPercentage',
    'Key Passes': 'keyPasses',
    'Assists': 'assists',
    'Big Chances Created': 'bigChancesCreated',
    'Expected Assists': 'expectedAssists',
    'Accurate Passes': 'accuratePasses',
    'Total Passes': 'totalPasses',
    'Accurate Crosses': 'accurateCrosses',
    'Long Balls': 'accurateLongBalls',
}

DEFENCE_STATS = {
    'Tackles': 'tackles',
    'Tackles Won': 'tacklesWon',
    'Interceptions': 'interceptions',
    'Blocks': 'outfielderBlocks',
    'Clearances': 'clearances',
    'Aerial Duels Won': 'aerialDuelsWon',
    'Ground Duels Won': 'groundDuelsWon',
    'Fouls': 'fouls',
    'Blocked Shots': 'blockedShots',
    'Dispossessed': 'dispossessed',
}

GK_STATS = {
    'Saves': 'saves',
    'Clean Sheets': 'cleanSheet',
    'Saves Parried': 'savesParried',
    'Saves Caught': 'savesCaught',
    'Punches': 'punches',
    'High Claims': 'highClaims',
    'Goals Conceded': 'goalsConceded',
    'Penalty Saves': 'penaltySave',
    'Errors to Goal': 'errorLeadToGoal',
}

GK_RADAR_STATS = {
    'Saves': 'saves',
    'Clean Sheets': 'cleanSheet',
    'High Claims': 'highClaims',
    'Penalty Saves': 'penaltySave',
    'Pass %': 'accuratePassesPercentage',
}

OTHER_STATS = {
    'Appearances': 'appearances',
    'Matches Started': 'matchesStarted',
    'Minutes Played': 'minutesPlayed',
    'Touches': 'touches',
    'Ball Recovery': 'ballRecovery',
    'Rating': 'rating',
    'Yellow Cards': 'yellowCards',
    'Red Cards': 'redCards',
    'Offsides': 'offsides',
    'Own Goals': 'ownGoals',
}

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
tab1, tab2, tab3 = st.tabs(["🏆 LEAGUE-WISE", "🏢 CLUB-WISE", "👥 PLAYER COMPARISON"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: LEAGUE-WISE DATA
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<h2 class='section-header'>🏆 League-Wise Statistics</h2>", unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💥 Avg Goals", f"{filtered_df['goals'].mean():.2f}")
    with col2:
        st.metric("🎯 Avg Shots", f"{filtered_df['totalShots'].mean():.2f}")
    with col3:
        st.metric("✨ Avg Assists", f"{filtered_df['assists'].mean():.2f}")
    with col4:
        st.metric("🛡️ Avg Tackles", f"{filtered_df['tackles'].mean():.2f}")
    
    st.markdown("---")
    
    # League Comparison Charts
    col1, col2 = st.columns(2)
    
    with col1:
        league_goals = filtered_df.groupby('league_name').agg({
            'goals': 'mean',
            'assists': 'mean',
            'totalShots': 'mean'
        }).reset_index().sort_values('goals', ascending=False)
        
        fig_attack = go.Figure()
        fig_attack.add_trace(go.Bar(name='Goals', x=league_goals['league_name'], y=league_goals['goals'], marker_color='#00d9ff'))
        fig_attack.add_trace(go.Bar(name='Assists', x=league_goals['league_name'], y=league_goals['assists'], marker_color='#00ff88'))
        fig_attack.add_trace(go.Bar(name='Shots', x=league_goals['league_name'], y=league_goals['totalShots'], marker_color='#ff0080'))
        fig_attack.update_layout(
            title="⚔️ Attacking Stats by League", barmode='group', template="plotly_dark",
            height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
        )
        st.plotly_chart(fig_attack, use_container_width=True)
    
    with col2:
        league_defence = filtered_df.groupby('league_name').agg({
            'tackles': 'mean',
            'interceptions': 'mean',
            'outfielderBlocks': 'mean'
        }).reset_index()
        
        fig_defence = go.Figure()
        fig_defence.add_trace(go.Bar(name='Tackles', x=league_defence['league_name'], y=league_defence['tackles'], marker_color='#00d9ff'))
        fig_defence.add_trace(go.Bar(name='Interceptions', x=league_defence['league_name'], y=league_defence['interceptions'], marker_color='#ff0080'))
        fig_defence.add_trace(go.Bar(name='Blocks', x=league_defence['league_name'], y=league_defence['outfielderBlocks'], marker_color='#00ff88'))
        fig_defence.update_layout(
            title="🛡️ Defensive Stats by League", barmode='group', template="plotly_dark",
            height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
        )
        st.plotly_chart(fig_defence, use_container_width=True)
    
    st.markdown("---")
    
    # League Summary Table
    st.markdown("<h3 class='subsection-header'>📊 League Summary Statistics</h3>", unsafe_allow_html=True)
    league_summary = filtered_df.groupby('league_name').agg({
        'player': 'count',
        'goals': 'mean',
        'assists': 'mean',
        'tackles': 'mean',
        'accuratePassesPercentage': 'mean',
        'totalShots': 'mean',
    }).reset_index().sort_values('goals', ascending=False)
    
    league_summary.columns = ['League', 'Players', 'Avg Goals', 'Avg Assists', 'Avg Tackles', 'Pass %', 'Avg Shots']
    league_summary['Avg Goals'] = league_summary['Avg Goals'].round(2)
    league_summary['Avg Assists'] = league_summary['Avg Assists'].round(2)
    league_summary['Avg Tackles'] = league_summary['Avg Tackles'].round(2)
    league_summary['Pass %'] = league_summary['Pass %'].round(1)
    league_summary['Avg Shots'] = league_summary['Avg Shots'].round(2)
    
    st.dataframe(league_summary, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 2: CLUB-WISE DATA
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2 class='section-header'>🏢 Club-Wise Statistics</h2>", unsafe_allow_html=True)
    
    # Team Selection
    selected_team_filter = st.selectbox(
        "Select a team to view details:",
        options=["All Teams"] + sorted(filtered_df['team'].unique().tolist()),
        key="club_filter"
    )
    
    if selected_team_filter == "All Teams":
        club_data = filtered_df
    else:
        club_data = filtered_df[filtered_df['team'] == selected_team_filter]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💥 Avg Goals", f"{club_data['goals'].mean():.2f}")
    with col2:
        st.metric("🎯 Avg Shots", f"{club_data['totalShots'].mean():.2f}")
    with col3:
        st.metric("✨ Avg Assists", f"{club_data['assists'].mean():.2f}")
    with col4:
        st.metric("🛡️ Avg Tackles", f"{club_data['tackles'].mean():.2f}")
    
    st.markdown("---")
    
    # Club Summary Table
    st.markdown("<h3 class='subsection-header'>📊 Club Summary Statistics</h3>", unsafe_allow_html=True)
    
    if selected_team_filter == "All Teams":
        club_summary = filtered_df.groupby('team').agg({
            'league_name': 'first',
            'player': 'count',
            'goals': 'mean',
            'assists': 'mean',
            'tackles': 'mean',
            'accuratePassesPercentage': 'mean',
            'totalShots': 'mean',
            'interceptions': 'mean'
        }).reset_index().sort_values('goals', ascending=False)
        
        club_summary.columns = ['Team', 'League', 'Players', 'Avg Goals', 'Avg Assists', 'Avg Tackles', 'Pass %', 'Avg Shots', 'Avg Interceptions']
        club_summary['Avg Goals'] = club_summary['Avg Goals'].round(2)
        club_summary['Avg Assists'] = club_summary['Avg Assists'].round(2)
        club_summary['Avg Tackles'] = club_summary['Avg Tackles'].round(2)
        club_summary['Pass %'] = club_summary['Pass %'].round(1)
        club_summary['Avg Shots'] = club_summary['Avg Shots'].round(2)
        club_summary['Avg Interceptions'] = club_summary['Avg Interceptions'].round(2)
        
        st.dataframe(club_summary, use_container_width=True, hide_index=True)
    else:
        # Top Players in Selected Team
        team_players = club_data.nlargest(10, 'goals')[['player', 'goals', 'assists', 'totalShots', 'tackles', 'accuratePassesPercentage', 'minutesPlayed']]
        team_players.columns = ['Player', 'Goals', 'Assists', 'Shots', 'Tackles', 'Pass %', 'Minutes']
        team_players['Pass %'] = team_players['Pass %'].round(1)
        
        st.markdown(f"<h3 class='subsection-header'>👥 Top Players - {selected_team_filter}</h3>", unsafe_allow_html=True)
        st.dataframe(team_players, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<h2 class='section-header'>👥 Player Comparison</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select Player 1:", options=[None] + filtered_players, key="p1")
    with col2:
        player2 = st.selectbox("Select Player 2:", options=[None] + filtered_players, key="p2")
    
    st.markdown("---")
    
    if player1 and player2:
        p1_data = filtered_df[filtered_df['player'] == player1].iloc[0]
        p2_data = filtered_df[filtered_df['player'] == player2].iloc[0]
        
        # Player Header Cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='player-card'>
                    <div class='player-name'>{player1}</div>
                    <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.95em;'>{p1_data['team']} | {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='player-card'>
                    <div class='player-name'>{player2}</div>
                    <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.95em;'>{p2_data['team']} | {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # ATTACKING STATS TABLE
        # ═══════════════════════════════════════════════════════════════
        st.markdown("<h3 class='subsection-header'>⚔️ Attacking Statistics</h3>", unsafe_allow_html=True)
        
        attacking_data = {metric: [
            int(p1_data[col]) if col in p1_data.index and isinstance(p1_data[col], (int, float)) else 0,
            int(p2_data[col]) if col in p2_data.index and isinstance(p2_data[col], (int, float)) else 0
        ] for metric, col in ATTACKING_STATS.items()}
        
        attacking_df = pd.DataFrame(attacking_data, index=[player1, player2]).T
        attacking_df.columns = ['Player 1', 'Player 2']
        st.dataframe(attacking_df, use_container_width=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # PASSING STATS WITH RADAR CHART
        # ═══════════════════════════════════════════════════════════════
        st.markdown("<h3 class='subsection-header'>🎯 Passing Metrics</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            passing_data = {metric: [
                float(p1_data[col]) if col in p1_data.index else 0,
                float(p2_data[col]) if col in p2_data.index else 0
            ] for metric, col in PASSING_STATS.items()}
            
            passing_df = pd.DataFrame(passing_data, index=[player1, player2]).T
            passing_df.columns = ['Player 1', 'Player 2']
            passing_df = passing_df.round(2)
            st.dataframe(passing_df, use_container_width=True)
        
        with col2:
            # Radar chart for passing
            radar_categories = ['Pass %', 'Key Passes', 'Assists', 'Big Chances', 'Expected Assists']
            p1_radar_vals = [
                p1_data['accuratePassesPercentage'],
                min(p1_data['keyPasses'], 100),
                min(p1_data['assists'] * 10, 100),
                min(p1_data['bigChancesCreated'] * 10, 100),
                min(p1_data['expectedAssists'] * 10, 100)
            ]
            p2_radar_vals = [
                p2_data['accuratePassesPercentage'],
                min(p2_data['keyPasses'], 100),
                min(p2_data['assists'] * 10, 100),
                min(p2_data['bigChancesCreated'] * 10, 100),
                min(p2_data['expectedAssists'] * 10, 100)
            ]
            
            fig_radar_pass = go.Figure()
            fig_radar_pass.add_trace(go.Scatterpolar(
                r=p1_radar_vals, theta=radar_categories, fill='toself', 
                name=player1, line_color='#00d9ff', fillcolor='rgba(0, 217, 255, 0.3)'
            ))
            fig_radar_pass.add_trace(go.Scatterpolar(
                r=p2_radar_vals, theta=radar_categories, fill='toself',
                name=player2, line_color='#ff0080', fillcolor='rgba(255, 0, 128, 0.3)'
            ))
            fig_radar_pass.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                template="plotly_dark", title="📊 Passing Profile",
                height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
            )
            st.plotly_chart(fig_radar_pass, use_container_width=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # DEFENCE STATS TABLE
        # ═══════════════════════════════════════════════════════════════
        st.markdown("<h3 class='subsection-header'>🛡️ Defensive Statistics</h3>", unsafe_allow_html=True)
        
        defence_data = {metric: [
            int(p1_data[col]) if col in p1_data.index and isinstance(p1_data[col], (int, float)) else 0,
            int(p2_data[col]) if col in p2_data.index and isinstance(p2_data[col], (int, float)) else 0
        ] for metric, col in DEFENCE_STATS.items()}
        
        defence_df = pd.DataFrame(defence_data, index=[player1, player2]).T
        defence_df.columns = ['Player 1', 'Player 2']
        st.dataframe(defence_df, use_container_width=True)
        
        st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # GOALKEEPER STATS (if applicable)
        # ═══════════════════════════════════════════════════════════════
        if p1_data['saves'] > 0 or p2_data['saves'] > 0:
            st.markdown("<h3 class='subsection-header'>🥅 Goalkeeper Statistics</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                gk_data = {metric: [
                    int(p1_data[col]) if col in p1_data.index and isinstance(p1_data[col], (int, float)) else 0,
                    int(p2_data[col]) if col in p2_data.index and isinstance(p2_data[col], (int, float)) else 0
                ] for metric, col in GK_STATS.items()}
                
                gk_df = pd.DataFrame(gk_data, index=[player1, player2]).T
                gk_df.columns = ['Player 1', 'Player 2']
                st.dataframe(gk_df, use_container_width=True)
            
            with col2:
                # Radar chart for GK
                gk_radar_cats = list(GK_RADAR_STATS.keys())
                p1_gk_radar = [
                    min(p1_data[GK_RADAR_STATS[cat]], 100) if GK_RADAR_STATS[cat] in p1_data.index else 0
                    for cat in gk_radar_cats
                ]
                p2_gk_radar = [
                    min(p2_data[GK_RADAR_STATS[cat]], 100) if GK_RADAR_STATS[cat] in p2_data.index else 0
                    for cat in gk_radar_cats
                ]
                
                fig_radar_gk = go.Figure()
                fig_radar_gk.add_trace(go.Scatterpolar(
                    r=p1_gk_radar, theta=gk_radar_cats, fill='toself',
                    name=player1, line_color='#00d9ff', fillcolor='rgba(0, 217, 255, 0.3)'
                ))
                fig_radar_gk.add_trace(go.Scatterpolar(
                    r=p2_gk_radar, theta=gk_radar_cats, fill='toself',
                    name=player2, line_color='#ff0080', fillcolor='rgba(255, 0, 128, 0.3)'
                ))
                fig_radar_gk.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    template="plotly_dark", title="🥊 GK Profile",
                    height=400, paper_bgcolor="#0a0e27", plot_bgcolor="#0a0e27"
                )
                st.plotly_chart(fig_radar_gk, use_container_width=True)
            
            st.markdown("---")
        
        # ═══════════════════════════════════════════════════════════════
        # OTHER STATISTICS TABLE
        # ═══════════════════════════════════════════════════════════════
        st.markdown("<h3 class='subsection-header'>📋 Other Statistics</h3>", unsafe_allow_html=True)
        
        other_data = {metric: [
            int(p1_data[col]) if col in p1_data.index and isinstance(p1_data[col], (int, float)) else 0,
            int(p2_data[col]) if col in p2_data.index and isinstance(p2_data[col], (int, float)) else 0
        ] for metric, col in OTHER_STATS.items()}
        
        other_df = pd.DataFrame(other_data, index=[player1, player2]).T
        other_df.columns = ['Player 1', 'Player 2']
        st.dataframe(other_df, use_container_width=True)
        
    else:
        st.info("👥 Select two players to view detailed comparison.")

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
