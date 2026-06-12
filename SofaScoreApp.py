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
# DARK THEME CSS
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
        
        .gradient-header {
            background: linear-gradient(90deg, #6A2D84 0%, #4A5FBF 50%, #00d9ff 100%);
            padding: 40px 20px;
            color: white;
            margin: -100px -50px 30px -50px;
            text-align: left;
            border-radius: 0 0 15px 15px;
        }
        
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

def identify_gk_players(df):
    """Identify goalkeepers by statistical pattern"""
    gk_candidates = df[
        (df['saves'] > 0) | 
        (df['savesParried'] > 0) | 
        (df['punches'] > 0) | 
        (df['highClaims'] > 0)
    ].copy()
    return gk_candidates

def calculate_big_chance_conversion(goals, big_chances):
    """Calculate big chance conversion rate"""
    if big_chances == 0:
        return 0
    return (goals / big_chances) * 100

# ═══════════════════════════════════════════════════════════════
# CREATE HORIZONTAL BAR CHART WITH CONDITIONAL FORMATTING
# ═══════════════════════════════════════════════════════════════
def create_horizontal_bar_chart(data_dict, title, colors_list=None):
    """Create horizontal bar chart with conditional formatting"""
    if colors_list is None:
        colors_list = ['#00d9ff', '#00ff88', '#ff0080', '#ffd700', '#ff6b9d']
    
    metrics = list(data_dict.keys())
    values = list(data_dict.values())
    
    # Assign colors to each metric
    bar_colors = [colors_list[i % len(colors_list)] for i in range(len(metrics))]
    
    fig = go.Figure(data=[
        go.Bar(
            y=metrics,
            x=values,
            orientation='h',
            marker=dict(color=bar_colors),
            text=[f'{v:.1f}' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>%{x:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Value",
        template="plotly_dark",
        height=400,
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27",
        showlegend=False,
        margin=dict(l=200)
    )
    
    return fig

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

selected_leagues = st.sidebar.multiselect(
    "🏆 Leagues",
    options=all_leagues,
    default=all_leagues[:3],
    key="leagues_filter"
)

selected_seasons = st.sidebar.multiselect(
    "📅 Seasons",
    options=all_seasons,
    default=[all_seasons[-1]],
    key="seasons_filter"
)

selected_teams = st.sidebar.multiselect(
    "🏢 Teams",
    options=all_teams,
    default=None,
    key="teams_filter"
)

st.sidebar.markdown("---")

filtered_df = df[
    (df['league_name'].isin(selected_leagues)) &
    (df['season_year'].isin(selected_seasons))
]

if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

filtered_players = sorted(filtered_df['player'].unique().tolist())

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
# HEADER
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
    
    # Calculate league aggregates
    league_stats = filtered_df.groupby('league_name').agg({
        'goals': 'sum',
        'expectedGoals': 'sum',
        'bigChancesCreated': 'sum',
        'bigChancesMissed': 'sum',
        'tackles': 'sum',
        'saves': 'sum',
        'cleanSheet': 'sum'
    }).reset_index()
    
    # KPI Cards - Per League (showing aggregates)
    st.markdown("<h3 class='subsection-header'>📊 League Totals</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.metric("⚽ Goals", f"{league_stats['goals'].sum():.0f}")
    with col2:
        st.metric("📈 xG Generated", f"{league_stats['expectedGoals'].sum():.1f}")
    with col3:
        st.metric("🎯 Big Chances Created", f"{league_stats['bigChancesCreated'].sum():.0f}")
    with col4:
        st.metric("❌ Big Chances Missed", f"{league_stats['bigChancesMissed'].sum():.0f}")
    with col5:
        st.metric("🛡️ Tackles", f"{league_stats['tackles'].sum():.0f}")
    with col6:
        st.metric("🙌 Saves", f"{league_stats['saves'].sum():.0f}")
    with col7:
        st.metric("🟩 Clean Sheets", f"{league_stats['cleanSheet'].sum():.0f}")
    
    st.markdown("---")
    
    # ATTACK SECTION
    st.markdown("<h3 class='subsection-header'>⚔️ Attack Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Goals horizontal bar chart
        goals_by_league = filtered_df.groupby('league_name')['goals'].sum().sort_values(ascending=True)
        fig_goals = create_horizontal_bar_chart(
            dict(goals_by_league),
            "⚽ Goals by League",
            colors_list=['#00d9ff']
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    with col2:
        # xG horizontal bar chart
        xg_by_league = filtered_df.groupby('league_name')['expectedGoals'].sum().sort_values(ascending=True)
        fig_xg = create_horizontal_bar_chart(
            dict(xg_by_league),
            "📈 Expected Goals (xG) by League",
            colors_list=['#00ff88']
        )
        st.plotly_chart(fig_xg, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Shots horizontal bar chart
        shots_by_league = filtered_df.groupby('league_name')['totalShots'].sum().sort_values(ascending=True)
        fig_shots = create_horizontal_bar_chart(
            dict(shots_by_league),
            "🎯 Total Shots by League",
            colors_list=['#ff0080']
        )
        st.plotly_chart(fig_shots, use_container_width=True)
    
    with col2:
        # Big Chance Conversion horizontal bar chart
        bcc_by_league = filtered_df.groupby('league_name').apply(
            lambda x: calculate_big_chance_conversion(x['goals'].sum(), x['bigChancesCreated'].sum())
        ).sort_values(ascending=True)
        fig_bcc = create_horizontal_bar_chart(
            dict(bcc_by_league),
            "📊 Big Chance Conversion % by League",
            colors_list=['#ffd700']
        )
        st.plotly_chart(fig_bcc, use_container_width=True)
    
    st.markdown("---")
    
    # PLAYMAKING SECTION
    st.markdown("<h3 class='subsection-header'>🎯 Playmaking (Radar Chart)</h3>", unsafe_allow_html=True)
    
    playmaking_by_league = filtered_df.groupby('league_name').agg({
        'bigChancesCreated': 'sum',
        'keyPasses': 'sum',
        'successfulDribbles': 'sum'
    }).reset_index()
    
    # Normalize for radar chart (0-100 scale)
    max_bcc = playmaking_by_league['bigChancesCreated'].max()
    max_kp = playmaking_by_league['keyPasses'].max()
    max_drb = playmaking_by_league['successfulDribbles'].max()
    
    fig_radar_playmaking = go.Figure()
    
    for idx, row in playmaking_by_league.iterrows():
        fig_radar_playmaking.add_trace(go.Scatterpolar(
            r=[
                (row['bigChancesCreated'] / max_bcc * 100) if max_bcc > 0 else 0,
                (row['keyPasses'] / max_kp * 100) if max_kp > 0 else 0,
                (row['successfulDribbles'] / max_drb * 100) if max_drb > 0 else 0
            ],
            theta=['Big Chances Created', 'Key Passes', 'Successful Dribbles'],
            fill='toself',
            name=row['league_name'],
            line_color=['#00d9ff', '#00ff88', '#ff0080'][idx % 3]
        ))
    
    fig_radar_playmaking.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_dark",
        title="🎯 Playmaking Metrics by League",
        height=500,
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27"
    )
    
    st.plotly_chart(fig_radar_playmaking, use_container_width=True)
    
    st.markdown("---")
    
    # PASSING SECTION
    st.markdown("<h3 class='subsection-header'>📲 Passing Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Accurate Passes horizontal bar chart
        acc_passes_by_league = filtered_df.groupby('league_name')['accuratePasses'].sum().sort_values(ascending=True)
        fig_acc_passes = create_horizontal_bar_chart(
            dict(acc_passes_by_league),
            "✅ Accurate Passes by League",
            colors_list=['#00d9ff']
        )
        st.plotly_chart(fig_acc_passes, use_container_width=True)
    
    with col2:
        # Touches horizontal bar chart
        touches_by_league = filtered_df.groupby('league_name')['touches'].sum().sort_values(ascending=True)
        fig_touches = create_horizontal_bar_chart(
            dict(touches_by_league),
            "👆 Touches by League",
            colors_list=['#00ff88']
        )
        st.plotly_chart(fig_touches, use_container_width=True)
    
    # Pass Accuracy %
    col1, col2 = st.columns(2)
    with col1:
        pass_acc_by_league = filtered_df.groupby('league_name')['accuratePassesPercentage'].mean().sort_values(ascending=True)
        fig_pass_acc = create_horizontal_bar_chart(
            dict(pass_acc_by_league),
            "📲 Pass Accuracy % by League",
            colors_list=['#ff0080']
        )
        st.plotly_chart(fig_pass_acc, use_container_width=True)
    
    st.markdown("---")
    
    # DEFENCE SECTION
    st.markdown("<h3 class='subsection-header'>🛡️ Defensive Metrics (Radar Chart)</h3>", unsafe_allow_html=True)
    
    defence_by_league = filtered_df.groupby('league_name').agg({
        'tackles': 'sum',
        'interceptions': 'sum',
        'clearances': 'sum',
        'aerialDuelsWon': 'sum',
        'groundDuelsWon': 'sum'
    }).reset_index()
    
    # Normalize for radar chart
    max_tck = defence_by_league['tackles'].max()
    max_int = defence_by_league['interceptions'].max()
    max_clr = defence_by_league['clearances'].max()
    max_aer = defence_by_league['aerialDuelsWon'].max()
    max_grd = defence_by_league['groundDuelsWon'].max()
    
    fig_radar_defence = go.Figure()
    
    defense_colors = ['#00d9ff', '#00ff88', '#ff0080', '#ffd700', '#ff6b9d']
    
    for idx, row in defence_by_league.iterrows():
        fig_radar_defence.add_trace(go.Scatterpolar(
            r=[
                (row['tackles'] / max_tck * 100) if max_tck > 0 else 0,
                (row['interceptions'] / max_int * 100) if max_int > 0 else 0,
                (row['clearances'] / max_clr * 100) if max_clr > 0 else 0,
                (row['aerialDuelsWon'] / max_aer * 100) if max_aer > 0 else 0,
                (row['groundDuelsWon'] / max_grd * 100) if max_grd > 0 else 0
            ],
            theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels Won', 'Ground Duels Won'],
            fill='toself',
            name=row['league_name'],
            line_color=defense_colors[idx % len(defense_colors)]
        ))
    
    fig_radar_defence.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_dark",
        title="🛡️ Defensive Profile by League",
        height=500,
        paper_bgcolor="#0a0e27",
        plot_bgcolor="#0a0e27"
    )
    
    st.plotly_chart(fig_radar_defence, use_container_width=True)
    
    st.markdown("---")
    
    # GOALKEEPER SECTION
    st.markdown("<h3 class='subsection-header'>🥅 Goalkeeper Metrics</h3>", unsafe_allow_html=True)
    
    gk_data = identify_gk_players(filtered_df)
    gk_by_league = gk_data.groupby('league_name').agg({
        'saves': 'sum',
        'cleanSheet': 'sum',
        'highClaims': 'sum',
        'errorLeadToGoal': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Saves horizontal bar chart
        saves_by_league = gk_by_league.set_index('league_name')['saves'].sort_values(ascending=True)
        fig_saves = create_horizontal_bar_chart(
            dict(saves_by_league),
            "🙌 Saves by League",
            colors_list=['#00d9ff']
        )
        st.plotly_chart(fig_saves, use_container_width=True)
    
    with col2:
        # Clean Sheets horizontal bar chart
        cs_by_league = gk_by_league.set_index('league_name')['cleanSheet'].sort_values(ascending=True)
        fig_cs = create_horizontal_bar_chart(
            dict(cs_by_league),
            "🟩 Clean Sheets by League",
            colors_list=['#00ff88']
        )
        st.plotly_chart(fig_cs, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # High Claims horizontal bar chart
        claims_by_league = gk_by_league.set_index('league_name')['highClaims'].sort_values(ascending=True)
        fig_claims = create_horizontal_bar_chart(
            dict(claims_by_league),
            "🎯 High Claims by League",
            colors_list=['#ff0080']
        )
        st.plotly_chart(fig_claims, use_container_width=True)
    
    with col2:
        # Errors to Goal horizontal bar chart
        errors_by_league = gk_by_league.set_index('league_name')['errorLeadToGoal'].sort_values(ascending=True)
        fig_errors = create_horizontal_bar_chart(
            dict(errors_by_league),
            "⚠️ Errors Led to Goal by League",
            colors_list=['#ffd700']
        )
        st.plotly_chart(fig_errors, use_container_width=True)
    
    st.markdown("---")
    
    # TOP PLAYERS TABLES BY LEAGUE
    st.markdown("<h3 class='subsection-header'>🏆 Top 5 Players Per League</h3>", unsafe_allow_html=True)
    
    for league in selected_leagues:
        league_df = filtered_df[filtered_df['league_name'] == league]
        
        st.markdown(f"#### {league}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⚔️ Top 5 Attackers**")
            top_attackers = league_df.nlargest(5, 'goals')[['player', 'team', 'goals', 'assists', 'totalShots']]
            top_attackers.columns = ['Player', 'Team', 'Goals', 'Assists', 'Shots']
            st.dataframe(top_attackers, use_container_width=True, hide_index=True)
            
            st.markdown("**🎯 Top 5 Playmakers**")
            top_playmakers = league_df.nlargest(5, 'bigChancesCreated')[['player', 'team', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
            top_playmakers.columns = ['Player', 'Team', 'Big Chances', 'Key Passes', 'Dribbles']
            st.dataframe(top_playmakers, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**📲 Top 5 Passers**")
            top_passers = league_df.nlargest(5, 'accuratePasses')[['player', 'team', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
            top_passers.columns = ['Player', 'Team', 'Accurate Passes', 'Touches', 'Pass %']
            top_passers['Pass %'] = top_passers['Pass %'].round(1)
            st.dataframe(top_passers, use_container_width=True, hide_index=True)
            
            st.markdown("**🛡️ Top 5 Defenders**")
            top_defenders = league_df.nlargest(5, 'tackles')[['player', 'team', 'tackles', 'interceptions', 'clearances']]
            top_defenders.columns = ['Player', 'Team', 'Tackles', 'Interceptions', 'Clearances']
            st.dataframe(top_defenders, use_container_width=True, hide_index=True)
        
        # GK Table
        gk_league = identify_gk_players(league_df)
        if len(gk_league) > 0:
            st.markdown("**🥅 Top 5 Goalkeepers**")
            top_gk = gk_league.nlargest(5, 'saves')[['player', 'team', 'saves', 'cleanSheet', 'highClaims', 'errorLeadToGoal']]
            top_gk.columns = ['Player', 'Team', 'Saves', 'Clean Sheets', 'High Claims', 'Errors']
            st.dataframe(top_gk, use_container_width=True, hide_index=True)
        
        st.markdown("---")

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
        club_list = sorted(filtered_df['team'].unique().tolist())
    else:
        club_data = filtered_df[filtered_df['team'] == selected_team_filter]
        club_list = [selected_team_filter]
    
    # For "All Teams" view, show aggregates
    if selected_team_filter == "All Teams":
        club_stats = club_data.groupby('team').agg({
            'goals': 'sum',
            'expectedGoals': 'sum',
            'bigChancesCreated': 'sum',
            'bigChancesMissed': 'sum',
            'tackles': 'sum',
            'saves': 'sum',
            'cleanSheet': 'sum'
        }).reset_index()
        
        # KPI Cards - Club Totals
        st.markdown("<h3 class='subsection-header'>📊 Club Totals</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        
        with col1:
            st.metric("⚽ Goals", f"{club_stats['goals'].sum():.0f}")
        with col2:
            st.metric("📈 xG Generated", f"{club_stats['expectedGoals'].sum():.1f}")
        with col3:
            st.metric("🎯 Big Chances Created", f"{club_stats['bigChancesCreated'].sum():.0f}")
        with col4:
            st.metric("❌ Big Chances Missed", f"{club_stats['bigChancesMissed'].sum():.0f}")
        with col5:
            st.metric("🛡️ Tackles", f"{club_stats['tackles'].sum():.0f}")
        with col6:
            st.metric("🙌 Saves", f"{club_stats['saves'].sum():.0f}")
        with col7:
            st.metric("🟩 Clean Sheets", f"{club_stats['cleanSheet'].sum():.0f}")
        
        st.markdown("---")
        
        # ATTACK CHARTS FOR ALL CLUBS
        st.markdown("<h3 class='subsection-header'>⚔️ Attack Metrics (All Clubs)</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            goals_by_club = club_data.groupby('team')['goals'].sum().sort_values(ascending=True).tail(10)
            fig_goals = create_horizontal_bar_chart(
                dict(goals_by_club),
                "⚽ Goals by Club (Top 10)",
                colors_list=['#00d9ff']
            )
            st.plotly_chart(fig_goals, use_container_width=True)
        
        with col2:
            xg_by_club = club_data.groupby('team')['expectedGoals'].sum().sort_values(ascending=True).tail(10)
            fig_xg = create_horizontal_bar_chart(
                dict(xg_by_club),
                "📈 Expected Goals (xG) by Club (Top 10)",
                colors_list=['#00ff88']
            )
            st.plotly_chart(fig_xg, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            shots_by_club = club_data.groupby('team')['totalShots'].sum().sort_values(ascending=True).tail(10)
            fig_shots = create_horizontal_bar_chart(
                dict(shots_by_club),
                "🎯 Total Shots by Club (Top 10)",
                colors_list=['#ff0080']
            )
            st.plotly_chart(fig_shots, use_container_width=True)
        
        with col2:
            bcc_by_club = club_data.groupby('team').apply(
                lambda x: calculate_big_chance_conversion(x['goals'].sum(), x['bigChancesCreated'].sum())
            ).sort_values(ascending=True).tail(10)
            fig_bcc = create_horizontal_bar_chart(
                dict(bcc_by_club),
                "📊 Big Chance Conversion % by Club (Top 10)",
                colors_list=['#ffd700']
            )
            st.plotly_chart(fig_bcc, use_container_width=True)
        
        st.markdown("---")
        
        # PLAYMAKING FOR ALL CLUBS
        st.markdown("<h3 class='subsection-header'>🎯 Playmaking (All Clubs)</h3>", unsafe_allow_html=True)
        
        playmaking_by_club = club_data.groupby('team').agg({
            'bigChancesCreated': 'sum',
            'keyPasses': 'sum',
            'successfulDribbles': 'sum'
        }).reset_index()
        
        max_bcc = playmaking_by_club['bigChancesCreated'].max()
        max_kp = playmaking_by_club['keyPasses'].max()
        max_drb = playmaking_by_club['successfulDribbles'].max()
        
        fig_radar_playmaking = go.Figure()
        
        colors_for_clubs = ['#00d9ff', '#00ff88', '#ff0080', '#ffd700', '#ff6b9d']
        for idx, row in playmaking_by_club.iterrows():
            fig_radar_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (row['bigChancesCreated'] / max_bcc * 100) if max_bcc > 0 else 0,
                    (row['keyPasses'] / max_kp * 100) if max_kp > 0 else 0,
                    (row['successfulDribbles'] / max_drb * 100) if max_drb > 0 else 0
                ],
                theta=['Big Chances Created', 'Key Passes', 'Successful Dribbles'],
                fill='toself',
                name=row['team'],
                line_color=colors_for_clubs[idx % len(colors_for_clubs)],
                visible='legendonly' if idx > 4 else True  # Show only first 5 by default
            ))
        
        fig_radar_playmaking.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template="plotly_dark",
            title="🎯 Playmaking Metrics (All Clubs)",
            height=500,
            paper_bgcolor="#0a0e27",
            plot_bgcolor="#0a0e27"
        )
        
        st.plotly_chart(fig_radar_playmaking, use_container_width=True)
        
        st.markdown("---")
        
        # PASSING FOR ALL CLUBS
        st.markdown("<h3 class='subsection-header'>📲 Passing Metrics (All Clubs)</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            acc_passes_by_club = club_data.groupby('team')['accuratePasses'].sum().sort_values(ascending=True).tail(10)
            fig_acc = create_horizontal_bar_chart(
                dict(acc_passes_by_club),
                "✅ Accurate Passes by Club (Top 10)",
                colors_list=['#00d9ff']
            )
            st.plotly_chart(fig_acc, use_container_width=True)
        
        with col2:
            touches_by_club = club_data.groupby('team')['touches'].sum().sort_values(ascending=True).tail(10)
            fig_tch = create_horizontal_bar_chart(
                dict(touches_by_club),
                "👆 Touches by Club (Top 10)",
                colors_list=['#00ff88']
            )
            st.plotly_chart(fig_tch, use_container_width=True)
        
        st.markdown("---")
        
        # DEFENCE FOR ALL CLUBS
        st.markdown("<h3 class='subsection-header'>🛡️ Defensive Metrics (All Clubs)</h3>", unsafe_allow_html=True)
        
        defence_by_club = club_data.groupby('team').agg({
            'tackles': 'sum',
            'interceptions': 'sum',
            'clearances': 'sum',
            'aerialDuelsWon': 'sum',
            'groundDuelsWon': 'sum'
        }).reset_index()
        
        max_tck = defence_by_club['tackles'].max()
        max_int = defence_by_club['interceptions'].max()
        max_clr = defence_by_club['clearances'].max()
        max_aer = defence_by_club['aerialDuelsWon'].max()
        max_grd = defence_by_club['groundDuelsWon'].max()
        
        fig_radar_def = go.Figure()
        
        for idx, row in defence_by_club.iterrows():
            fig_radar_def.add_trace(go.Scatterpolar(
                r=[
                    (row['tackles'] / max_tck * 100) if max_tck > 0 else 0,
                    (row['interceptions'] / max_int * 100) if max_int > 0 else 0,
                    (row['clearances'] / max_clr * 100) if max_clr > 0 else 0,
                    (row['aerialDuelsWon'] / max_aer * 100) if max_aer > 0 else 0,
                    (row['groundDuelsWon'] / max_grd * 100) if max_grd > 0 else 0
                ],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels Won', 'Ground Duels Won'],
                fill='toself',
                name=row['team'],
                line_color=colors_for_clubs[idx % len(colors_for_clubs)],
                visible='legendonly' if idx > 4 else True
            ))
        
        fig_radar_def.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            template="plotly_dark",
            title="🛡️ Defensive Profile (All Clubs)",
            height=500,
            paper_bgcolor="#0a0e27",
            plot_bgcolor="#0a0e27"
        )
        
        st.plotly_chart(fig_radar_def, use_container_width=True)
        
        st.markdown("---")
        
        # TOP PLAYERS BY CLUB - Show for each selected league
        st.markdown("<h3 class='subsection-header'>🏆 Top 5 Players Per Club (Per League)</h3>", unsafe_allow_html=True)
        
        for league in selected_leagues:
            league_club_df = club_data[club_data['league_name'] == league]
            league_clubs = sorted(league_club_df['team'].unique().tolist())
            
            if league_clubs:
                st.markdown(f"#### {league}")
                
                for club in league_clubs:
                    club_specific_df = league_club_df[league_club_df['team'] == club]
                    
                    st.markdown(f"**{club}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**⚔️ Top Attackers**")
                        top_att = club_specific_df.nlargest(5, 'goals')[['player', 'goals', 'assists', 'totalShots']]
                        top_att.columns = ['Player', 'Goals', 'Assists', 'Shots']
                        st.dataframe(top_att, use_container_width=True, hide_index=True)
                        
                        st.write("**🎯 Top Playmakers**")
                        top_pm = club_specific_df.nlargest(5, 'bigChancesCreated')[['player', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
                        top_pm.columns = ['Player', 'Big Chances', 'Key Passes', 'Dribbles']
                        st.dataframe(top_pm, use_container_width=True, hide_index=True)
                    
                    with col2:
                        st.write("**📲 Top Passers**")
                        top_ps = club_specific_df.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
                        top_ps.columns = ['Player', 'Accurate Passes', 'Touches', 'Pass %']
                        top_ps['Pass %'] = top_ps['Pass %'].round(1)
                        st.dataframe(top_ps, use_container_width=True, hide_index=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**🛡️ Top Defenders**")
                        top_df = club_specific_df.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']]
                        top_df.columns = ['Player', 'Tackles', 'Interceptions', 'Clearances']
                        st.dataframe(top_df, use_container_width=True, hide_index=True)
                    
                    with col2:
                        gk_club = identify_gk_players(club_specific_df)
                        if len(gk_club) > 0:
                            st.write("**🥅 Goalkeeper(s)**")
                            top_gk_club = gk_club.nlargest(3, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims']]
                            top_gk_club.columns = ['Player', 'Saves', 'Clean Sheets', 'High Claims']
                            st.dataframe(top_gk_club, use_container_width=True, hide_index=True)
                
                st.markdown("---")
    
    else:
        # Selected Team View
        team_stats = club_data.agg({
            'goals': 'sum',
            'expectedGoals': 'sum',
            'bigChancesCreated': 'sum',
            'bigChancesMissed': 'sum',
            'tackles': 'sum',
            'saves': 'sum',
            'cleanSheet': 'sum'
        })
        
        st.markdown(f"<h3 class='subsection-header'>📊 {selected_team_filter} - Statistics</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        
        with col1:
            st.metric("⚽ Goals", f"{team_stats['goals']:.0f}")
        with col2:
            st.metric("📈 xG Generated", f"{team_stats['expectedGoals']:.1f}")
        with col3:
            st.metric("🎯 Big Chances Created", f"{team_stats['bigChancesCreated']:.0f}")
        with col4:
            st.metric("❌ Big Chances Missed", f"{team_stats['bigChancesMissed']:.0f}")
        with col5:
            st.metric("🛡️ Tackles", f"{team_stats['tackles']:.0f}")
        with col6:
            st.metric("🙌 Saves", f"{team_stats['saves']:.0f}")
        with col7:
            st.metric("🟩 Clean Sheets", f"{team_stats['cleanSheet']:.0f}")
        
        st.markdown("---")
        
        st.markdown(f"<h3 class='subsection-header'>👥 {selected_team_filter} - Squad</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⚔️ Top Attackers**")
            top_att = club_data.nlargest(5, 'goals')[['player', 'goals', 'assists', 'totalShots']]
            top_att.columns = ['Player', 'Goals', 'Assists', 'Shots']
            st.dataframe(top_att, use_container_width=True, hide_index=True)
            
            st.markdown("**🎯 Top Playmakers**")
            top_pm = club_data.nlargest(5, 'bigChancesCreated')[['player', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
            top_pm.columns = ['Player', 'Big Chances', 'Key Passes', 'Dribbles']
            st.dataframe(top_pm, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**📲 Top Passers**")
            top_ps = club_data.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
            top_ps.columns = ['Player', 'Accurate Passes', 'Touches', 'Pass %']
            top_ps['Pass %'] = top_ps['Pass %'].round(1)
            st.dataframe(top_ps, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🛡️ Top Defenders**")
            top_df = club_data.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']]
            top_df.columns = ['Player', 'Tackles', 'Interceptions', 'Clearances']
            st.dataframe(top_df, use_container_width=True, hide_index=True)
        
        with col2:
            gk_team = identify_gk_players(club_data)
            if len(gk_team) > 0:
                st.markdown("**🥅 Goalkeepers**")
                top_gk_team = gk_team.nlargest(3, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims', 'errorLeadToGoal']]
                top_gk_team.columns = ['Player', 'Saves', 'Clean Sheets', 'High Claims', 'Errors']
                st.dataframe(top_gk_team, use_container_width=True, hide_index=True)

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
                <div style='background-color: #1a1f3a; border: 2px solid #00d9ff; border-radius: 12px; padding: 20px; text-align: center;'>
                    <div style='color: #00d9ff; font-size: 1.3em; font-weight: 700; margin-bottom: 10px;'>{player1}</div>
                    <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.95em;'>{p1_data['team']} | {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: #1a1f3a; border: 2px solid #ff0080; border-radius: 12px; padding: 20px; text-align: center;'>
                    <div style='color: #ff0080; font-size: 1.3em; font-weight: 700; margin-bottom: 10px;'>{player2}</div>
                    <div style='color: rgba(255, 255, 255, 0.7); font-size: 0.95em;'>{p2_data['team']} | {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ATTACKING STATS TABLE
        st.markdown("<h3 class='subsection-header'>⚔️ Attacking Statistics</h3>", unsafe_allow_html=True)
        
        attacking_metrics = {
            'Goals': (int(p1_data['goals']), int(p2_data['goals'])),
            'Assists': (int(p1_data['assists']), int(p2_data['assists'])),
            'Total Shots': (int(p1_data['totalShots']), int(p2_data['totalShots'])),
            'Shots on Target': (int(p1_data['shotsOnTarget']), int(p2_data['shotsOnTarget'])),
            'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
            'Expected Goals': (float(p1_data['expectedGoals']), float(p2_data['expectedGoals'])),
        }
        
        attacking_df = pd.DataFrame({
            'Metric': attacking_metrics.keys(),
            player1: [attacking_metrics[m][0] for m in attacking_metrics.keys()],
            player2: [attacking_metrics[m][1] for m in attacking_metrics.keys()]
        })
        
        st.dataframe(attacking_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # PASSING WITH RADAR
        st.markdown("<h3 class='subsection-header'>🎯 Passing Metrics & Playmaking</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            passing_metrics = {
                'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                'Key Passes': (int(p1_data['keyPasses']), int(p2_data['keyPasses'])),
                'Successful Dribbles': (int(p1_data['successfulDribbles']), int(p2_data['successfulDribbles'])),
            }
            
            passing_df = pd.DataFrame({
                'Metric': passing_metrics.keys(),
                player1: [passing_metrics[m][0] for m in passing_metrics.keys()],
                player2: [passing_metrics[m][1] for m in passing_metrics.keys()]
            })
            
            st.markdown("**Playmaking Table**")
            st.dataframe(passing_df, use_container_width=True, hide_index=True)
        
        with col2:
            # Radar for playmaking
            max_bcc = max(p1_data['bigChancesCreated'], p2_data['bigChancesCreated'], 1)
            max_kp = max(p1_data['keyPasses'], p2_data['keyPasses'], 1)
            max_drb = max(p1_data['successfulDribbles'], p2_data['successfulDribbles'], 1)
            
            fig_playmaking = go.Figure()
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (p1_data['bigChancesCreated'] / max_bcc * 100),
                    (p1_data['keyPasses'] / max_kp * 100),
                    (p1_data['successfulDribbles'] / max_drb * 100)
                ],
                theta=['Big Chances', 'Key Passes', 'Dribbles'],
                fill='toself',
                name=player1,
                line_color='#00d9ff',
                fillcolor='rgba(0, 217, 255, 0.3)'
            ))
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (p2_data['bigChancesCreated'] / max_bcc * 100),
                    (p2_data['keyPasses'] / max_kp * 100),
                    (p2_data['successfulDribbles'] / max_drb * 100)
                ],
                theta=['Big Chances', 'Key Passes', 'Dribbles'],
                fill='toself',
                name=player2,
                line_color='#ff0080',
                fillcolor='rgba(255, 0, 128, 0.3)'
            ))
            fig_playmaking.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                template="plotly_dark",
                title="🎯 Playmaking Profile",
                height=400,
                paper_bgcolor="#0a0e27",
                plot_bgcolor="#0a0e27"
            )
            st.plotly_chart(fig_playmaking, use_container_width=True)
        
        st.markdown("---")
        
        # PASSING ACCURACY TABLE
        st.markdown("<h3 class='subsection-header'>📲 Passing Accuracy</h3>", unsafe_allow_html=True)
        
        passing_acc_metrics = {
            'Accurate Passes': (int(p1_data['accuratePasses']), int(p2_data['accuratePasses'])),
            'Touches': (int(p1_data['touches']), int(p2_data['touches'])),
            'Pass Accuracy %': (round(p1_data['accuratePassesPercentage'], 1), round(p2_data['accuratePassesPercentage'], 1)),
        }
        
        passing_acc_df = pd.DataFrame({
            'Metric': passing_acc_metrics.keys(),
            player1: [passing_acc_metrics[m][0] for m in passing_acc_metrics.keys()],
            player2: [passing_acc_metrics[m][1] for m in passing_acc_metrics.keys()]
        })
        
        st.dataframe(passing_acc_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # DEFENCE TABLE
        st.markdown("<h3 class='subsection-header'>🛡️ Defensive Statistics</h3>", unsafe_allow_html=True)
        
        defence_metrics = {
            'Tackles': (int(p1_data['tackles']), int(p2_data['tackles'])),
            'Interceptions': (int(p1_data['interceptions']), int(p2_data['interceptions'])),
            'Clearances': (int(p1_data['clearances']), int(p2_data['clearances'])),
            'Aerial Duels Won': (int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
            'Ground Duels Won': (int(p1_data['groundDuelsWon']), int(p2_data['groundDuelsWon'])),
        }
        
        defence_df = pd.DataFrame({
            'Metric': defence_metrics.keys(),
            player1: [defence_metrics[m][0] for m in defence_metrics.keys()],
            player2: [defence_metrics[m][1] for m in defence_metrics.keys()]
        })
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.dataframe(defence_df, use_container_width=True, hide_index=True)
        
        with col2:
            # Radar for defence
            max_tck = max(p1_data['tackles'], p2_data['tackles'], 1)
            max_int = max(p1_data['interceptions'], p2_data['interceptions'], 1)
            max_clr = max(p1_data['clearances'], p2_data['clearances'], 1)
            max_aer = max(p1_data['aerialDuelsWon'], p2_data['aerialDuelsWon'], 1)
            max_grd = max(p1_data['groundDuelsWon'], p2_data['groundDuelsWon'], 1)
            
            fig_defence = go.Figure()
            fig_defence.add_trace(go.Scatterpolar(
                r=[
                    (p1_data['tackles'] / max_tck * 100),
                    (p1_data['interceptions'] / max_int * 100),
                    (p1_data['clearances'] / max_clr * 100),
                    (p1_data['aerialDuelsWon'] / max_aer * 100),
                    (p1_data['groundDuelsWon'] / max_grd * 100)
                ],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ground Duels'],
                fill='toself',
                name=player1,
                line_color='#00d9ff',
                fillcolor='rgba(0, 217, 255, 0.3)'
            ))
            fig_defence.add_trace(go.Scatterpolar(
                r=[
                    (p2_data['tackles'] / max_tck * 100),
                    (p2_data['interceptions'] / max_int * 100),
                    (p2_data['clearances'] / max_clr * 100),
                    (p2_data['aerialDuelsWon'] / max_aer * 100),
                    (p2_data['groundDuelsWon'] / max_grd * 100)
                ],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ground Duels'],
                fill='toself',
                name=player2,
                line_color='#ff0080',
                fillcolor='rgba(255, 0, 128, 0.3)'
            ))
            fig_defence.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                template="plotly_dark",
                title="🛡️ Defensive Profile",
                height=400,
                paper_bgcolor="#0a0e27",
                plot_bgcolor="#0a0e27"
            )
            st.plotly_chart(fig_defence, use_container_width=True)
        
        st.markdown("---")
        
        # GK STATS (if applicable)
        if p1_data['saves'] > 0 or p2_data['saves'] > 0:
            st.markdown("<h3 class='subsection-header'>🥅 Goalkeeper Statistics</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                gk_metrics = {
                    'Saves': (int(p1_data['saves']), int(p2_data['saves'])),
                    'Clean Sheets': (int(p1_data['cleanSheet']), int(p2_data['cleanSheet'])),
                    'High Claims': (int(p1_data['highClaims']), int(p2_data['highClaims'])),
                    'Errors Led to Goal': (int(p1_data['errorLeadToGoal']), int(p2_data['errorLeadToGoal'])),
                }
                
                gk_df = pd.DataFrame({
                    'Metric': gk_metrics.keys(),
                    player1: [gk_metrics[m][0] for m in gk_metrics.keys()],
                    player2: [gk_metrics[m][1] for m in gk_metrics.keys()]
                })
                
                st.dataframe(gk_df, use_container_width=True, hide_index=True)
            
            with col2:
                # Radar for GK
                max_sv = max(p1_data['saves'], p2_data['saves'], 1)
                max_cs = max(p1_data['cleanSheet'], p2_data['cleanSheet'], 1)
                max_hc = max(p1_data['highClaims'], p2_data['highClaims'], 1)
                max_err = max(p1_data['errorLeadToGoal'], p2_data['errorLeadToGoal'], 1)
                
                fig_gk = go.Figure()
                fig_gk.add_trace(go.Scatterpolar(
                    r=[
                        (p1_data['saves'] / max_sv * 100),
                        (p1_data['cleanSheet'] / max_cs * 100),
                        (p1_data['highClaims'] / max_hc * 100),
                        ((max_err - p1_data['errorLeadToGoal']) / max_err * 100),  # Inverse for errors
                    ],
                    theta=['Saves', 'Clean Sheets', 'High Claims', 'Errors (Lower Better)'],
                    fill='toself',
                    name=player1,
                    line_color='#00d9ff',
                    fillcolor='rgba(0, 217, 255, 0.3)'
                ))
                fig_gk.add_trace(go.Scatterpolar(
                    r=[
                        (p2_data['saves'] / max_sv * 100),
                        (p2_data['cleanSheet'] / max_cs * 100),
                        (p2_data['highClaims'] / max_hc * 100),
                        ((max_err - p2_data['errorLeadToGoal']) / max_err * 100),
                    ],
                    theta=['Saves', 'Clean Sheets', 'High Claims', 'Errors (Lower Better)'],
                    fill='toself',
                    name=player2,
                    line_color='#ff0080',
                    fillcolor='rgba(255, 0, 128, 0.3)'
                ))
                fig_gk.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    template="plotly_dark",
                    title="🥅 Goalkeeper Profile",
                    height=400,
                    paper_bgcolor="#0a0e27",
                    plot_bgcolor="#0a0e27"
                )
                st.plotly_chart(fig_gk, use_container_width=True)
            
            st.markdown("---")
    
    else:
        st.info("👥 Select two players to compare.")

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
