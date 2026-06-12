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
    page_title="⚽ Player Comparison - Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM STYLING - DARK THEME WITH GRADIENT HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        body {
            background-color: #0a0e27;
            color: #ffffff;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            background-color: #0a0e27;
            padding: 0;
        }
        
        /* GRADIENT HEADER */
        .gradient-header {
            background: linear-gradient(90deg, #6A2D84 0%, #4A5FBF 50%, #00d9ff 100%);
            padding: 40px 20px;
            color: white;
            margin: -70px -30px 0 -30px;
            text-align: left;
        }
        
        .gradient-header h1 {
            font-size: 3em;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 10px rgba(0, 217, 255, 0.2);
        }
        
        .gradient-header .subtitle {
            font-size: 0.95em;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 10px;
            font-weight: 500;
        }
        
        /* NAVIGATION TABS */
        .nav-tabs {
            display: flex;
            gap: 20px;
            padding: 15px 20px;
            background: linear-gradient(90deg, rgba(106, 45, 132, 0.3) 0%, rgba(74, 95, 191, 0.3) 50%, rgba(0, 217, 255, 0.2) 100%);
            border-bottom: 1px solid rgba(0, 217, 255, 0.2);
            margin: 0 -30px;
            font-size: 0.95em;
        }
        
        .nav-tabs a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-tabs a:hover {
            color: #00d9ff;
        }
        
        .nav-tabs a.active {
            color: #00d9ff;
            font-weight: 600;
            border-bottom: 2px solid #00d9ff;
        }
        
        /* PLAYER SLOT CARD */
        .player-slot {
            background: linear-gradient(135deg, rgba(45, 45, 45, 0.8) 0%, rgba(31, 31, 31, 0.8) 100%);
            border: 2px solid rgba(0, 217, 255, 0.3);
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            min-height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .player-slot:hover {
            border-color: #00d9ff;
            background: linear-gradient(135deg, rgba(45, 45, 45, 1) 0%, rgba(31, 31, 31, 1) 100%);
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
        }
        
        .player-slot .plus-icon {
            font-size: 3em;
            color: #00d9ff;
            margin-bottom: 15px;
        }
        
        .player-slot .placeholder-text {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1em;
            font-weight: 500;
        }
        
        /* FILLED PLAYER CARD */
        .player-card-filled {
            background: linear-gradient(135deg, rgba(45, 45, 45, 0.8) 0%, rgba(31, 31, 31, 0.8) 100%);
            border: 2px solid #00d9ff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            min-height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .player-name {
            color: #00d9ff;
            font-size: 1.5em;
            font-weight: 700;
            margin: 15px 0 5px 0;
        }
        
        .player-info {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
            margin: 5px 0;
        }
        
        .player-stats {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.85em;
            margin-top: 15px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            text-align: left;
        }
        
        .stat-item {
            background: rgba(0, 217, 255, 0.05);
            padding: 8px;
            border-radius: 6px;
            border-left: 2px solid #00d9ff;
        }
        
        .stat-value {
            color: #00d9ff;
            font-weight: 700;
            font-size: 1.1em;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.75em;
            margin-top: 2px;
        }
        
        /* POPULAR PLAYERS GRID */
        .popular-section {
            margin-top: 40px;
        }
        
        .popular-title {
            color: #00d9ff;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.2);
        }
        
        .player-card {
            background: linear-gradient(135deg, rgba(45, 45, 45, 0.6) 0%, rgba(31, 31, 31, 0.6) 100%);
            border: 1px solid rgba(0, 217, 255, 0.2);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        
        .player-card:hover {
            border-color: #00d9ff;
            background: linear-gradient(135deg, rgba(45, 45, 45, 1) 0%, rgba(31, 31, 31, 1) 100%);
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0, 217, 255, 0.15);
        }
        
        .player-card-emoji {
            font-size: 2.5em;
        }
        
        .player-card-name {
            color: #ffffff;
            font-weight: 700;
            font-size: 0.95em;
        }
        
        .player-card-meta {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8em;
        }
        
        /* COMPARISON SECTION */
        .comparison-header {
            color: #00d9ff;
            font-size: 1.5em;
            font-weight: 700;
            margin: 30px 0 20px 0;
            text-align: center;
        }
        
        .stats-table {
            background: rgba(31, 31, 31, 0.5);
            border: 1px solid rgba(0, 217, 255, 0.2);
            border-radius: 8px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        /* METRIC CARDS */
        .metric-mini {
            background: rgba(31, 31, 31, 0.5);
            border-left: 3px solid #00d9ff;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
        
        .metric-mini-value {
            color: #00d9ff;
            font-size: 1.3em;
            font-weight: 700;
        }
        
        .metric-mini-label {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8em;
            margin-top: 3px;
        }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def load_data():
    """Load player statistics from GitHub repository"""
    try:
        # Load from GitHub raw content
        url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
        df = pd.read_csv(url)
        
        # Clean up - handle missing values
        df = df.fillna(0)
        
        # Create a unique identifier for display
        df['player_display'] = df['player'] + ' (' + df['team'] + ')'
        
        return df
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        st.info("💡 Make sure your GitHub repo is public and the CSV file exists.")
        return None

df = load_data()

# Get unique players
all_players = sorted(df['player'].unique().tolist())
all_teams = sorted(df['team'].unique().tolist())
all_leagues = sorted(df['league_name'].unique().tolist())
all_seasons = sorted(df['season_year'].unique().tolist())

# ═══════════════════════════════════════════════════════════════
# HEADER WITH GRADIENT
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="gradient-header">
        <h1>⚽ Stats Centre</h1>
        <div class="subtitle">European Football Analytics | Top 5 Leagues + European Competitions</div>
    </div>
""", unsafe_allow_html=True)

# Navigation tabs
st.markdown("""
    <div class="nav-tabs">
        <a>Dashboard</a>
        <a>Player</a>
        <a>Club</a>
        <a>All-time Stats</a>
        <a>Records</a>
        <a class="active">Player Comparison</a>
        <a>Head-to-head</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔍 Filters")
    st.markdown("---")
    
    selected_leagues = st.multiselect(
        "Leagues",
        options=all_leagues,
        default=all_leagues[:3]
    )
    
    selected_seasons = st.multiselect(
        "Seasons",
        options=all_seasons,
        default=all_seasons[-1:]
    )
    
    selected_teams = st.multiselect(
        "Teams",
        options=all_teams,
        default=None
    )

# Filter data
filtered_df = df[
    (df['league_name'].isin(selected_leagues)) &
    (df['season_year'].isin(selected_seasons))
]

if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

filtered_players = sorted(filtered_df['player'].unique().tolist())

# ═══════════════════════════════════════════════════════════════
# PLAYER SELECTION SECTION
# ═══════════════════════════════════════════════════════════════
st.markdown("### Player Comparison")
st.markdown("---")

# Use session state to track selected players
if 'player1' not in st.session_state:
    st.session_state.player1 = None
if 'player2' not in st.session_state:
    st.session_state.player2 = None

# Two-column layout for player selection
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Player 1**")
    player1_name = st.selectbox(
        "Select Player 1",
        options=[None] + filtered_players,
        key="p1_select",
        label_visibility="collapsed",
        index=0
    )
    if player1_name:
        st.session_state.player1 = player1_name

with col2:
    st.markdown("**Player 2**")
    player2_name = st.selectbox(
        "Select Player 2",
        options=[None] + filtered_players,
        key="p2_select",
        label_visibility="collapsed",
        index=0
    )
    if player2_name:
        st.session_state.player2 = player2_name

st.markdown("---")
st.markdown("<small style='color: rgba(255, 255, 255, 0.5);'>📊 Some statistics are not available for all seasons. Select players to compare detailed metrics.</small>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# POPULAR PLAYERS SUGGESTIONS
# ═══════════════════════════════════════════════════════════════
st.markdown("<div class='popular-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='popular-title'>Popular player comparisons</h2>", unsafe_allow_html=True)

# Get top scorers as popular players
popular_players = filtered_df.nlargest(8, 'goals')[['player', 'team', 'goals', 'assists']].drop_duplicates(subset=['player'])

cols = st.columns(4)
for idx, (_, player_data) in enumerate(popular_players.iterrows()):
    with cols[idx % 4]:
        if st.button(
            f"👤\n{player_data['player']}\n{player_data['team']}",
            key=f"pop_{idx}",
            use_container_width=True,
            help=f"Goals: {int(player_data['goals'])}, Assists: {int(player_data['assists'])}"
        ):
            if idx % 2 == 0:
                st.session_state.player1 = player_data['player']
            else:
                st.session_state.player2 = player_data['player']
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# COMPARISON VIEW
# ═══════════════════════════════════════════════════════════════
if player1_name and player2_name:
    st.markdown("---")
    st.markdown("<h2 class='comparison-header'>📊 Detailed Comparison</h2>", unsafe_allow_html=True)
    
    # Get player data
    p1_data = filtered_df[filtered_df['player'] == player1_name].iloc[0]
    p2_data = filtered_df[filtered_df['player'] == player2_name].iloc[0]
    
    # Player Info Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='player-card-filled'>
                <div style='flex-grow: 1;'>
                    <div class='player-name'>{player1_name}</div>
                    <div class='player-info'>{p1_data['team']}</div>
                    <div class='player-info'>{p1_data['league_name']}</div>
                    <div style='margin-top: 20px;'>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p1_data['goals'])}</div>
                            <div class='stat-label'>GOALS</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p1_data['assists'])}</div>
                            <div class='stat-label'>ASSISTS</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p1_data['tackles'])}</div>
                            <div class='stat-label'>TACKLES</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p1_data['appearances'])}</div>
                            <div class='stat-label'>APPEARANCES</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='player-card-filled'>
                <div style='flex-grow: 1;'>
                    <div class='player-name'>{player2_name}</div>
                    <div class='player-info'>{p2_data['team']}</div>
                    <div class='player-info'>{p2_data['league_name']}</div>
                    <div style='margin-top: 20px;'>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p2_data['goals'])}</div>
                            <div class='stat-label'>GOALS</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p2_data['assists'])}</div>
                            <div class='stat-label'>ASSISTS</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p2_data['tackles'])}</div>
                            <div class='stat-label'>TACKLES</div>
                        </div>
                        <div class='metric-mini'>
                            <div class='stat-value'>{int(p2_data['appearances'])}</div>
                            <div class='stat-label'>APPEARANCES</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Detailed Stats Comparison
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Attacking Stats")
        attack_metrics = {
            'Goals': (int(p1_data['goals']), int(p2_data['goals'])),
            'Assists': (int(p1_data['assists']), int(p2_data['assists'])),
            'Shots': (int(p1_data['totalShots']), int(p2_data['totalShots'])),
            'Shots on Target': (int(p1_data['shotsOnTarget']), int(p2_data['shotsOnTarget'])),
            'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
            'Key Passes': (int(p1_data['keyPasses']), int(p2_data['keyPasses'])),
        }
        
        fig_attack = go.Figure()
        fig_attack.add_trace(go.Bar(
            name=player1_name,
            x=list(attack_metrics.keys()),
            y=[v[0] for v in attack_metrics.values()],
            marker_color='#00d9ff'
        ))
        fig_attack.add_trace(go.Bar(
            name=player2_name,
            x=list(attack_metrics.keys()),
            y=[v[1] for v in attack_metrics.values()],
            marker_color='#ff0080'
        ))
        fig_attack.update_layout(
            template="plotly_dark",
            barmode='group',
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        st.plotly_chart(fig_attack, use_container_width=True)
    
    with col2:
        st.markdown("#### Defensive Stats")
        defence_metrics = {
            'Tackles': (int(p1_data['tackles']), int(p2_data['tackles'])),
            'Interceptions': (int(p1_data['interceptions']), int(p2_data['interceptions'])),
            'Blocks': (int(p1_data['outfielderBlocks']), int(p2_data['outfielderBlocks'])),
            'Clearances': (int(p1_data['clearances']), int(p2_data['clearances'])),
            'Aerial Won': (int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
        }
        
        fig_defence = go.Figure()
        fig_defence.add_trace(go.Bar(
            name=player1_name,
            x=list(defence_metrics.keys()),
            y=[v[0] for v in defence_metrics.values()],
            marker_color='#00d9ff'
        ))
        fig_defence.add_trace(go.Bar(
            name=player2_name,
            x=list(defence_metrics.keys()),
            y=[v[1] for v in defence_metrics.values()],
            marker_color='#ff0080'
        ))
        fig_defence.update_layout(
            template="plotly_dark",
            barmode='group',
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        st.plotly_chart(fig_defence, use_container_width=True)
    
    # Radar Chart Comparison
    st.markdown("---")
    
    categories = ['Goals', 'Assists', 'Tackles', 'Pass Success %', 'Appearances']
    
    # Normalize values for radar (0-100 scale for better visualization)
    max_goals = max(int(p1_data['goals']), int(p2_data['goals']), 1)
    max_assists = max(int(p1_data['assists']), int(p2_data['assists']), 1)
    max_tackles = max(int(p1_data['tackles']), int(p2_data['tackles']), 1)
    max_apps = max(int(p1_data['appearances']), int(p2_data['appearances']), 1)
    
    p1_values = [
        (int(p1_data['goals']) / max_goals) * 100,
        (int(p1_data['assists']) / max_assists) * 100,
        (int(p1_data['tackles']) / max_tackles) * 100,
        p1_data['accuratePassesPercentage'],
        (int(p1_data['appearances']) / max_apps) * 100,
    ]
    
    p2_values = [
        (int(p2_data['goals']) / max_goals) * 100,
        (int(p2_data['assists']) / max_assists) * 100,
        (int(p2_data['tackles']) / max_tackles) * 100,
        p2_data['accuratePassesPercentage'],
        (int(p2_data['appearances']) / max_apps) * 100,
    ]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=p1_values,
        theta=categories,
        fill='toself',
        name=player1_name,
        line_color='#00d9ff'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=p2_values,
        theta=categories,
        fill='toself',
        name=player2_name,
        line_color='#ff0080'
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_dark",
        height=500,
        showlegend=True
    )
    
    st.markdown("#### 🎯 Player Profile Radar")
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Detailed Stats Table
    st.markdown("---")
    st.markdown("#### 📋 All Detailed Metrics")
    
    comparison_data = {
        'Metric': [
            'Goals', 'Assists', 'Shots', 'Shots on Target', 'Pass Accuracy %',
            'Tackles', 'Interceptions', 'Blocks', 'Aerial Duels Won',
            'Appearances', 'Minutes Played', 'Clean Sheets', 'Yellow Cards', 'Red Cards'
        ],
        player1_name: [
            int(p1_data['goals']),
            int(p1_data['assists']),
            int(p1_data['totalShots']),
            int(p1_data['shotsOnTarget']),
            round(p1_data['accuratePassesPercentage'], 2),
            int(p1_data['tackles']),
            int(p1_data['interceptions']),
            int(p1_data['outfielderBlocks']),
            int(p1_data['aerialDuelsWon']),
            int(p1_data['appearances']),
            int(p1_data['minutesPlayed']),
            int(p1_data['cleanSheet']),
            int(p1_data['yellowCards']),
            int(p1_data['redCards']),
        ],
        player2_name: [
            int(p2_data['goals']),
            int(p2_data['assists']),
            int(p2_data['totalShots']),
            int(p2_data['shotsOnTarget']),
            round(p2_data['accuratePassesPercentage'], 2),
            int(p2_data['tackles']),
            int(p2_data['interceptions']),
            int(p2_data['outfielderBlocks']),
            int(p2_data['aerialDuelsWon']),
            int(p2_data['appearances']),
            int(p2_data['minutesPlayed']),
            int(p2_data['cleanSheet']),
            int(p2_data['yellowCards']),
            int(p2_data['redCards']),
        ],
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

else:
    st.markdown("<p style='text-align: center; color: rgba(255, 255, 255, 0.5); margin-top: 40px;'>👥 Select two players to view detailed comparison</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.4); margin-top: 40px; padding: 20px;'>
        <small>⚽ Football Analytics Dashboard | Powered by Streamlit</small><br>
        <small style='font-size: 0.8em;'>European Leagues Data | Season: {}</small>
    </div>
""".format(', '.join(selected_seasons)), unsafe_allow_html=True)
