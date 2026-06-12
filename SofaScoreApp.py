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
# PROFESSIONAL DARK THEME CSS (Inspired by OPTA/StatsBomb)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
        :root {
            --bg-primary: #0f1419;
            --bg-secondary: #151d2a;
            --bg-tertiary: #1e2738;
            --accent-primary: #2dd4bf;
            --accent-secondary: #0ea5e9;
            --accent-tertiary: #06b6d4;
            --text-primary: #ffffff;
            --text-secondary: #d4d9e3;
            --text-muted: #8b92a3;
            --brand-orange: #ff6b35;
            --brand-green: #00d084;
            --brand-red: #ef4444;
        }
        
        * {
            margin: 0;
            padding: 0;
        }
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            background-color: #0f1419 !important;
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #151d2a !important;
            border-right: 1px solid rgba(45, 212, 191, 0.1);
        }
        
        [data-testid="stSidebarContent"] {
            background-color: #151d2a !important;
        }
        
        section[data-testid="stSidebar"] > div {
            background-color: #151d2a !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
            border-bottom: 1px solid rgba(45, 212, 191, 0.15);
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background-color: transparent;
            color: #8b92a3;
            border-radius: 0;
            padding: 16px 24px;
            margin: 0;
            font-weight: 600;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: transparent;
            color: #2dd4bf;
            font-weight: 700;
            border-bottom: 2px solid #2dd4bf;
        }
        
        .stMetric {
            background-color: #1e2738;
            padding: 16px;
            border-radius: 8px;
            border-left: 3px solid #2dd4bf;
        }
        
        .stMetricLabel {
            color: #8b92a3;
            font-size: 0.85em;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .stMetricValue {
            color: #2dd4bf;
            font-weight: 700;
            font-size: 1.8em;
        }
        
        /* PROFESSIONAL HEADER - Inspired by OPTA */
        .header-container {
            background: linear-gradient(135deg, #151d2a 0%, #1e2738 50%, #0d1117 100%);
            padding: 48px 40px;
            margin: -60px -40px 40px -40px;
            border-bottom: 2px solid #2dd4bf;
            border-radius: 0 0 16px 16px;
        }
        
        .header-container h1 {
            font-size: 2.4em;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: #ffffff;
            margin: 0 0 8px 0;
        }
        
        .header-eyebrow {
            color: #2dd4bf;
            font-size: 0.85em;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .header-subtitle {
            color: #8b92a3;
            font-size: 0.95em;
            font-weight: 500;
            margin-top: 12px;
        }
        
        /* SECTION HEADERS - Professional styling */
        .section-header {
            color: #ffffff;
            font-size: 1.6em;
            font-weight: 800;
            margin: 40px 0 8px 0;
            letter-spacing: -0.3px;
        }
        
        .section-eyebrow {
            color: #2dd4bf;
            font-size: 0.75em;
            font-weight: 800;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: block;
        }
        
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, rgba(45, 212, 191, 0.2) 0%, transparent 100%);
            margin: 32px 0;
        }
        
        .subsection-header {
            color: #ffffff;
            font-size: 1.2em;
            font-weight: 700;
            margin: 24px 0 16px 0;
            letter-spacing: -0.2px;
        }
        
        .data-label {
            color: #8b92a3;
            font-size: 0.8em;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        /* Card styling */
        .stat-card {
            background-color: #1e2738;
            border: 1px solid rgba(45, 212, 191, 0.15);
            border-radius: 8px;
            padding: 16px;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: rgba(45, 212, 191, 0.3);
            background-color: #232f3d;
        }
        
        /* Sidebar styling */
        .sidebar-header {
            color: #2dd4bf;
            font-size: 0.85em;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        
        [data-baseweb="input"] {
            background-color: #232f3d !important;
            border: 1px solid rgba(45, 212, 191, 0.2) !important;
            border-radius: 6px !important;
        }
        
        .stSelectbox > div {
            background-color: #1e2738;
        }
        
        .stMultiSelect {
            background-color: #1e2738;
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
        st.error(f"Error loading data: {e}")
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
# PROFESSIONAL COLOR GRADIENT GENERATOR
# ═══════════════════════════════════════════════════════════════
def get_color_gradient(metric_type, index, max_index):
    """Generate color gradients for different metrics (white to petrol blue)"""
    gradients = {
        'attack': ['#ffffff', '#e0f7f6', '#a0e4df', '#60cec5', '#2dd4bf', '#1da39a'],
        'playmaking': ['#ffffff', '#e0f2fe', '#a0e2ff', '#60d0ff', '#0ea5e9', '#0284c7'],
        'passing': ['#ffffff', '#ddf4f5', '#aae5e9', '#77d6dd', '#44c7d1', '#1db5c0'],
        'defense': ['#ffffff', '#e8e8ff', '#c4c4ff', '#a0a0ff', '#7c7cff', '#5858ff'],
        'goalkeeper': ['#ffffff', '#ffe8d6', '#ffd4ad', '#ffc084', '#ffac5b', '#ff9832']
    }
    
    color_list = gradients.get(metric_type, ['#2dd4bf', '#0ea5e9', '#06b6d4'])
    return color_list[min(index, len(color_list) - 1)]

# ═══════════════════════════════════════════════════════════════
# ENHANCED HORIZONTAL BAR CHART WITH GRADIENT
# ═══════════════════════════════════════════════════════════════
def create_gradient_bar_chart(data_dict, title, metric_type='attack', eyebrow=''):
    """Create professional horizontal bar chart with gradient coloring"""
    metrics = list(data_dict.keys())
    values = list(data_dict.values())
    
    # Normalize values for color mapping (0-1)
    max_val = max(values) if values else 1
    normalized = [v / max_val for v in values]
    
    # Generate gradient colors
    colors = [get_color_gradient(metric_type, int(norm * 5), 5) for norm in normalized]
    
    fig = go.Figure(data=[
        go.Bar(
            y=metrics,
            x=values,
            orientation='h',
            marker=dict(color=colors, line=dict(width=0)),
            text=[f'{v:.1f}' if v != int(v) else f'{int(v)}' for v in values],
            textposition='auto',
            textfont=dict(size=12, color='#1e2738'),
            hovertemplate='<b>%{y}</b><br>%{x:.2f}<extra></extra>',
            showlegend=False
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=14, color='#ffffff', family='Arial, sans-serif'),
            x=0,
            xanchor='left'
        ),
        xaxis_title="",
        yaxis_title="",
        template="plotly_dark",
        height=350,
        paper_bgcolor="#1e2738",
        plot_bgcolor="#151d2a",
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(45, 212, 191, 0.05)',
            zeroline=False,
            showline=False,
            color='#8b92a3'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            color='#ffffff',
            tickfont=dict(size=11)
        ),
        showlegend=False,
        margin=dict(l=180, r=20, t=20, b=20),
        hovermode='closest'
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════
# PROFESSIONAL RADAR CHART
# ═══════════════════════════════════════════════════════════════
def create_professional_radar(data_dict, title, metric_type='playmaking', eyebrow=''):
    """Create professional radar chart"""
    colors_map = {
        'playmaking': '#0ea5e9',
        'defense': '#06b6d4',
        'goalkeeper': '#ff9832',
        'passing': '#2dd4bf'
    }
    
    metrics = list(data_dict.keys())
    
    fig = go.Figure()
    
    for idx, (name, values) in enumerate(data_dict.items()):
        color = ['#0ea5e9', '#06b6d4', '#2dd4bf', '#ff6b35', '#00d084'][idx % 5]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics,
            fill='toself',
            name=name,
            line_color=color,
            fillcolor=f'rgba(45, 212, 191, 0.15)',
            hovertemplate='<b>%{name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(45, 212, 191, 0.1)',
                gridwidth=1,
                tickfont=dict(color='#8b92a3', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(45, 212, 191, 0.1)',
                tickfont=dict(color='#ffffff', size=11)
            )
        ),
        template="plotly_dark",
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=14, color='#ffffff'),
            x=0,
            xanchor='left'
        ),
        height=450,
        paper_bgcolor="#1e2738",
        plot_bgcolor="#151d2a",
        font=dict(family="Arial, sans-serif"),
        legend=dict(
            x=1.1,
            y=1,
            bgcolor='rgba(0, 0, 0, 0)',
            bordercolor='rgba(45, 212, 191, 0.2)',
            borderwidth=1
        )
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
st.sidebar.markdown("<span class='sidebar-header'>🔍 FILTERS</span>", unsafe_allow_html=True)
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
    <div style='background-color: #1e2738; padding: 16px; border-radius: 8px; border-left: 3px solid #2dd4bf;'>
    <div style='color: #8b92a3; font-size: 0.8em; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px;'>📊 Data Summary</div>
    <div style='color: #2dd4bf; font-weight: 700; margin-bottom: 4px;'>{len(filtered_df)}</div>
    <div style='color: #8b92a3; font-size: 0.85em;'>Total Records</div>
    <div style='color: #2dd4bf; font-weight: 700; margin: 8px 0 4px 0;'>{len(filtered_players)}</div>
    <div style='color: #8b92a3; font-size: 0.85em;'>Players</div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PROFESSIONAL HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="header-container">
        <div class="header-eyebrow">⚽ EUROPEAN FOOTBALL INTELLIGENCE</div>
        <h1>League Analytics Dashboard</h1>
        <div class="header-subtitle">In-depth performance metrics across Europe's top five leagues and continental competitions | 2020–2025</div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["LEAGUE ANALYSIS", "CLUB COMPARISON", "PLAYER MATCHUP"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: LEAGUE-WISE DATA - TOP 5 PLAYERS PER LEAGUE
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
        <span class="section-eyebrow">🏆 Performance Breakdown</span>
        <h2 class="section-header">League-Wide Metrics</h2>
    """, unsafe_allow_html=True)
    
    # Function to get top 5 players per league and their aggregated stats
    def get_top_players_stats(league_df, metric='goals', top_n=5):
        """Get top N players for a league by specific metric and aggregate their stats"""
        top_players = league_df.nlargest(top_n, metric)
        return top_players
    
    # ═════════════════════════════════════════
    # KEY METRICS - Overall from Top 5 per League
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="data-label">Overall Statistics</span>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    total_goals = filtered_df['goals'].sum()
    total_xg = filtered_df['expectedGoals'].sum()
    total_bcc = filtered_df['bigChancesCreated'].sum()
    total_bcm = filtered_df['bigChancesMissed'].sum()
    total_tackles = filtered_df['tackles'].sum()
    total_saves = filtered_df['saves'].sum()
    total_cs = filtered_df['cleanSheet'].sum()
    
    with col1:
        st.metric("⚽ Goals", f"{total_goals:.0f}")
    with col2:
        st.metric("📈 xG", f"{total_xg:.1f}")
    with col3:
        st.metric("🎯 Big Chances", f"{total_bcc:.0f}")
    with col4:
        st.metric("❌ Missed", f"{total_bcm:.0f}")
    with col5:
        st.metric("🛡️ Tackles", f"{total_tackles:.0f}")
    with col6:
        st.metric("🙌 Saves", f"{total_saves:.0f}")
    with col7:
        st.metric("🟩 Clean Sheets", f"{total_cs:.0f}")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # ATTACK METRICS - Top 5 Players per League
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">⚔️ Attacking</span>
        <h2 class="section-header">Offensive Performance</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        goals_by_league = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'goals')
            goals_by_league[league] = top_5['goals'].sum()
        
        fig = create_gradient_bar_chart(goals_by_league, "Goals Scored (Top 5 Players)", 'attack')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        xg_by_league = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'expectedGoals')
            xg_by_league[league] = top_5['expectedGoals'].sum()
        
        fig = create_gradient_bar_chart(xg_by_league, "Expected Goals (Top 5 Players)", 'attack')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        shots_by_league = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'totalShots')
            shots_by_league[league] = top_5['totalShots'].sum()
        
        fig = create_gradient_bar_chart(shots_by_league, "Total Shots (Top 5 Players)", 'attack')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        bcc_by_league = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'goals')
            total_goals = top_5['goals'].sum()
            total_bcc = top_5['bigChancesCreated'].sum()
            bcc_by_league[league] = calculate_big_chance_conversion(total_goals, total_bcc)
        
        fig = create_gradient_bar_chart(bcc_by_league, "Big Chance Conversion Rate % (Top 5 Players)", 'attack')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # PLAYMAKING - Radar Chart
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">🎯 Creation</span>
        <h2 class="section-header">Playmaking Profile</h2>
    """, unsafe_allow_html=True)
    
    playmaking_data = {}
    
    for league in selected_leagues:
        league_df = filtered_df[filtered_df['league_name'] == league]
        top_5 = league_df.nlargest(5, 'bigChancesCreated')
        
        max_bcc = filtered_df['bigChancesCreated'].max()
        max_kp = filtered_df['keyPasses'].max()
        max_drb = filtered_df['successfulDribbles'].max()
        
        playmaking_data[league] = [
            (top_5['bigChancesCreated'].sum() / max_bcc * 100) if max_bcc > 0 else 0,
            (top_5['keyPasses'].sum() / max_kp * 100) if max_kp > 0 else 0,
            (top_5['successfulDribbles'].sum() / max_drb * 100) if max_drb > 0 else 0
        ]
    
    fig_playmaking = go.Figure()
    
    colors = ['#0ea5e9', '#06b6d4', '#2dd4bf', '#ff6b35', '#00d084']
    for idx, (league, values) in enumerate(playmaking_data.items()):
        fig_playmaking.add_trace(go.Scatterpolar(
            r=values,
            theta=['Big Chances Created', 'Key Passes', 'Successful Dribbles'],
            fill='toself',
            name=league,
            line_color=colors[idx % len(colors)],
            fillcolor=f'rgba({45 + idx*30}, {212 - idx*20}, {191 + idx*10}, 0.15)',
            hovertemplate='<b>%{name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
    
    fig_playmaking.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(45, 212, 191, 0.1)'),
            angularaxis=dict(gridcolor='rgba(45, 212, 191, 0.1)', tickfont=dict(color='#ffffff'))
        ),
        template="plotly_dark",
        title=dict(text="<b>Top 5 Players - Playmaking Metrics</b>", font=dict(size=14, color='#ffffff'), x=0, xanchor='left'),
        height=500,
        paper_bgcolor="#1e2738",
        plot_bgcolor="#151d2a",
        legend=dict(x=1.05, y=1)
    )
    
    st.plotly_chart(fig_playmaking, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # PASSING - Horizontal Bar Charts
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">📲 Distribution</span>
        <h2 class="section-header">Passing Efficiency</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        acc_passes = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'accuratePasses')
            acc_passes[league] = top_5['accuratePasses'].sum()
        
        fig = create_gradient_bar_chart(acc_passes, "Accurate Passes (Top 5 Players)", 'passing')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        touches = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'touches')
            touches[league] = top_5['touches'].sum()
        
        fig = create_gradient_bar_chart(touches, "Total Touches (Top 5 Players)", 'passing')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        pass_acc = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            top_5 = league_df.nlargest(5, 'accuratePassesPercentage')
            pass_acc[league] = top_5['accuratePassesPercentage'].mean()
        
        fig = create_gradient_bar_chart(pass_acc, "Pass Accuracy % (Top 5 Players)", 'passing')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # DEFENSE - Radar Chart
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">🛡️ Resilience</span>
        <h2 class="section-header">Defensive Excellence</h2>
    """, unsafe_allow_html=True)
    
    defense_data = {}
    
    for league in selected_leagues:
        league_df = filtered_df[filtered_df['league_name'] == league]
        top_5 = league_df.nlargest(5, 'tackles')
        
        max_tck = filtered_df['tackles'].max()
        max_int = filtered_df['interceptions'].max()
        max_clr = filtered_df['clearances'].max()
        max_aer = filtered_df['aerialDuelsWon'].max()
        max_grd = filtered_df['groundDuelsWon'].max()
        
        defense_data[league] = [
            (top_5['tackles'].sum() / max_tck * 100) if max_tck > 0 else 0,
            (top_5['interceptions'].sum() / max_int * 100) if max_int > 0 else 0,
            (top_5['clearances'].sum() / max_clr * 100) if max_clr > 0 else 0,
            (top_5['aerialDuelsWon'].sum() / max_aer * 100) if max_aer > 0 else 0,
            (top_5['groundDuelsWon'].sum() / max_grd * 100) if max_grd > 0 else 0
        ]
    
    fig_defense = go.Figure()
    
    for idx, (league, values) in enumerate(defense_data.items()):
        fig_defense.add_trace(go.Scatterpolar(
            r=values,
            theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels Won', 'Ground Duels Won'],
            fill='toself',
            name=league,
            line_color=colors[idx % len(colors)],
            fillcolor=f'rgba({45 + idx*30}, {212 - idx*20}, {191 + idx*10}, 0.15)',
            hovertemplate='<b>%{name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
    
    fig_defense.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(45, 212, 191, 0.1)'),
            angularaxis=dict(gridcolor='rgba(45, 212, 191, 0.1)', tickfont=dict(color='#ffffff'))
        ),
        template="plotly_dark",
        title=dict(text="<b>Top 5 Players - Defensive Actions</b>", font=dict(size=14, color='#ffffff'), x=0, xanchor='left'),
        height=500,
        paper_bgcolor="#1e2738",
        plot_bgcolor="#151d2a",
        legend=dict(x=1.05, y=1)
    )
    
    st.plotly_chart(fig_defense, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # GOALKEEPER METRICS
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">🥅 Goalkeeping</span>
        <h2 class="section-header">Goalkeeper Performance</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        gk_saves = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            gk_league = identify_gk_players(league_df)
            top_5_gk = gk_league.nlargest(5, 'saves')
            gk_saves[league] = top_5_gk['saves'].sum()
        
        fig = create_gradient_bar_chart(gk_saves, "Saves (Top 5 Keepers)", 'goalkeeper')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        gk_cs = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            gk_league = identify_gk_players(league_df)
            top_5_gk = gk_league.nlargest(5, 'cleanSheet')
            gk_cs[league] = top_5_gk['cleanSheet'].sum()
        
        fig = create_gradient_bar_chart(gk_cs, "Clean Sheets (Top 5 Keepers)", 'goalkeeper')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        gk_claims = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            gk_league = identify_gk_players(league_df)
            top_5_gk = gk_league.nlargest(5, 'highClaims')
            gk_claims[league] = top_5_gk['highClaims'].sum()
        
        fig = create_gradient_bar_chart(gk_claims, "High Claims (Top 5 Keepers)", 'goalkeeper')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        gk_errors = {}
        for league in selected_leagues:
            league_df = filtered_df[filtered_df['league_name'] == league]
            gk_league = identify_gk_players(league_df)
            top_5_gk = gk_league.nlargest(5, 'errorLeadToGoal')
            gk_errors[league] = top_5_gk['errorLeadToGoal'].sum()
        
        fig = create_gradient_bar_chart(gk_errors, "Errors Led to Goals (Top 5 Keepers)", 'goalkeeper')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ═════════════════════════════════════════
    # TOP PERFORMERS TABLE
    # ═════════════════════════════════════════
    st.markdown("""
        <span class="section-eyebrow">🏅 Rankings</span>
        <h2 class="section-header">Elite Performers by League</h2>
    """, unsafe_allow_html=True)
    
    for league in selected_leagues:
        league_df = filtered_df[filtered_df['league_name'] == league]
        
        st.markdown(f"<h3 class='subsection-header'>{league}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⚔️ Top Scorers**")
            top_attackers = league_df.nlargest(5, 'goals')[['player', 'team', 'goals', 'assists', 'totalShots']]
            top_attackers.columns = ['Player', 'Team', 'Goals', 'Assists', 'Shots']
            st.dataframe(top_attackers, use_container_width=True, hide_index=True)
            
            st.markdown("**🎯 Top Creators**")
            top_playmakers = league_df.nlargest(5, 'bigChancesCreated')[['player', 'team', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
            top_playmakers.columns = ['Player', 'Team', 'Chances', 'Key Passes', 'Dribbles']
            st.dataframe(top_playmakers, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**📲 Top Passers**")
            top_passers = league_df.nlargest(5, 'accuratePasses')[['player', 'team', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
            top_passers.columns = ['Player', 'Team', 'Passes', 'Touches', 'Acc %']
            top_passers['Acc %'] = top_passers['Acc %'].round(1)
            st.dataframe(top_passers, use_container_width=True, hide_index=True)
            
            st.markdown("**🛡️ Top Defenders**")
            top_defenders = league_df.nlargest(5, 'tackles')[['player', 'team', 'tackles', 'interceptions', 'clearances']]
            top_defenders.columns = ['Player', 'Team', 'Tackles', 'Intercepts', 'Clears']
            st.dataframe(top_defenders, use_container_width=True, hide_index=True)
        
        gk_league = identify_gk_players(league_df)
        if len(gk_league) > 0:
            st.markdown("**🥅 Top Keepers**")
            top_gk = gk_league.nlargest(5, 'saves')[['player', 'team', 'saves', 'cleanSheet', 'highClaims']]
            top_gk.columns = ['Player', 'Team', 'Saves', 'Clean Sheets', 'Claims']
            st.dataframe(top_gk, use_container_width=True, hide_index=True)
        
        st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# TAB 2: CLUB-WISE DATA
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
        <span class="section-eyebrow">🏢 Institutional Performance</span>
        <h2 class="section-header">Club Comparison</h2>
    """, unsafe_allow_html=True)
    
    selected_team_filter = st.selectbox(
        "Select a club:",
        options=["All Clubs"] + sorted(filtered_df['team'].unique().tolist()),
        key="club_filter"
    )
    
    if selected_team_filter == "All Clubs":
        club_data = filtered_df
        st.info("👉 Showing aggregated metrics across all clubs. Select a specific club for detailed analysis.")
    else:
        club_data = filtered_df[filtered_df['team'] == selected_team_filter]
        st.markdown(f"<div class='stat-card'><b>{selected_team_filter}</b> | {club_data['league_name'].iloc[0]}</div>", unsafe_allow_html=True)
    
    # KPI Section
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.metric("⚽ Goals", f"{club_data['goals'].sum():.0f}")
    with col2:
        st.metric("📈 xG", f"{club_data['expectedGoals'].sum():.1f}")
    with col3:
        st.metric("🎯 Chances", f"{club_data['bigChancesCreated'].sum():.0f}")
    with col4:
        st.metric("❌ Missed", f"{club_data['bigChancesMissed'].sum():.0f}")
    with col5:
        st.metric("🛡️ Tackles", f"{club_data['tackles'].sum():.0f}")
    with col6:
        st.metric("🙌 Saves", f"{club_data['saves'].sum():.0f}")
    with col7:
        st.metric("🟩 Clean Sheets", f"{club_data['cleanSheet'].sum():.0f}")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
        <span class="section-eyebrow">👥 Head-to-Head</span>
        <h2 class="section-header">Player Comparison</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("Select first player:", options=[None] + filtered_players, key="p1")
    with col2:
        player2 = st.selectbox("Select second player:", options=[None] + filtered_players, key="p2")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if player1 and player2:
        p1_data = filtered_df[filtered_df['player'] == player1].iloc[0]
        p2_data = filtered_df[filtered_df['player'] == player2].iloc[0]
        
        # Player Cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='stat-card'>
                    <div style='color: #2dd4bf; font-size: 1.2em; font-weight: 700;'>{player1}</div>
                    <div style='color: #8b92a3; font-size: 0.9em;'>{p1_data['team']} • {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='stat-card'>
                    <div style='color: #0ea5e9; font-size: 1.2em; font-weight: 700;'>{player2}</div>
                    <div style='color: #8b92a3; font-size: 0.9em;'>{p2_data['team']} • {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Attacking Table
        st.markdown("""
            <span class="section-eyebrow">⚔️ Offensive</span>
            <h3 class="section-header">Attacking Statistics</h3>
        """, unsafe_allow_html=True)
        
        attacking_metrics = {
            'Goals': (int(p1_data['goals']), int(p2_data['goals'])),
            'Assists': (int(p1_data['assists']), int(p2_data['assists'])),
            'Total Shots': (int(p1_data['totalShots']), int(p2_data['totalShots'])),
            'Shots on Target': (int(p1_data['shotsOnTarget']), int(p2_data['shotsOnTarget'])),
            'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
            'Expected Goals': (round(p1_data['expectedGoals'], 2), round(p2_data['expectedGoals'], 2)),
        }
        
        attacking_df = pd.DataFrame({
            'Metric': attacking_metrics.keys(),
            player1: [attacking_metrics[m][0] for m in attacking_metrics.keys()],
            player2: [attacking_metrics[m][1] for m in attacking_metrics.keys()]
        })
        
        st.dataframe(attacking_df, use_container_width=True, hide_index=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Playmaking
        st.markdown("""
            <span class="section-eyebrow">🎯 Creation</span>
            <h3 class="section-header">Playmaking & Ball Progression</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            playmaking_metrics = {
                'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                'Key Passes': (int(p1_data['keyPasses']), int(p2_data['keyPasses'])),
                'Successful Dribbles': (int(p1_data['successfulDribbles']), int(p2_data['successfulDribbles'])),
            }
            
            playmaking_df = pd.DataFrame({
                'Metric': playmaking_metrics.keys(),
                player1: [playmaking_metrics[m][0] for m in playmaking_metrics.keys()],
                player2: [playmaking_metrics[m][1] for m in playmaking_metrics.keys()]
            })
            
            st.dataframe(playmaking_df, use_container_width=True, hide_index=True)
        
        with col2:
            max_bcc = max(p1_data['bigChancesCreated'], p2_data['bigChancesCreated'], 1)
            max_kp = max(p1_data['keyPasses'], p2_data['keyPasses'], 1)
            max_drb = max(p1_data['successfulDribbles'], p2_data['successfulDribbles'], 1)
            
            fig_playmaking = go.Figure()
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[(p1_data['bigChancesCreated'] / max_bcc * 100), (p1_data['keyPasses'] / max_kp * 100), (p1_data['successfulDribbles'] / max_drb * 100)],
                theta=['Big Chances', 'Key Passes', 'Dribbles'],
                fill='toself',
                name=player1,
                line_color='#2dd4bf',
                fillcolor='rgba(45, 212, 191, 0.2)'
            ))
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[(p2_data['bigChancesCreated'] / max_bcc * 100), (p2_data['keyPasses'] / max_kp * 100), (p2_data['successfulDribbles'] / max_drb * 100)],
                theta=['Big Chances', 'Key Passes', 'Dribbles'],
                fill='toself',
                name=player2,
                line_color='#0ea5e9',
                fillcolor='rgba(14, 165, 233, 0.2)'
            ))
            fig_playmaking.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(45, 212, 191, 0.1)')),
                template="plotly_dark",
                height=400,
                paper_bgcolor="#1e2738",
                plot_bgcolor="#151d2a"
            )
            st.plotly_chart(fig_playmaking, use_container_width=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Defense
        st.markdown("""
            <span class="section-eyebrow">🛡️ Defensive</span>
            <h3 class="section-header">Defensive Actions</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
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
            
            st.dataframe(defence_df, use_container_width=True, hide_index=True)
        
        with col2:
            max_tck = max(p1_data['tackles'], p2_data['tackles'], 1)
            max_int = max(p1_data['interceptions'], p2_data['interceptions'], 1)
            max_clr = max(p1_data['clearances'], p2_data['clearances'], 1)
            max_aer = max(p1_data['aerialDuelsWon'], p2_data['aerialDuelsWon'], 1)
            max_grd = max(p1_data['groundDuelsWon'], p2_data['groundDuelsWon'], 1)
            
            fig_defence = go.Figure()
            fig_defence.add_trace(go.Scatterpolar(
                r=[(p1_data['tackles'] / max_tck * 100), (p1_data['interceptions'] / max_int * 100), (p1_data['clearances'] / max_clr * 100), (p1_data['aerialDuelsWon'] / max_aer * 100), (p1_data['groundDuelsWon'] / max_grd * 100)],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ground Duels'],
                fill='toself',
                name=player1,
                line_color='#2dd4bf',
                fillcolor='rgba(45, 212, 191, 0.2)'
            ))
            fig_defence.add_trace(go.Scatterpolar(
                r=[(p2_data['tackles'] / max_tck * 100), (p2_data['interceptions'] / max_int * 100), (p2_data['clearances'] / max_clr * 100), (p2_data['aerialDuelsWon'] / max_aer * 100), (p2_data['groundDuelsWon'] / max_grd * 100)],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ground Duels'],
                fill='toself',
                name=player2,
                line_color='#0ea5e9',
                fillcolor='rgba(14, 165, 233, 0.2)'
            ))
            fig_defence.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(45, 212, 191, 0.1)')),
                template="plotly_dark",
                height=400,
                paper_bgcolor="#1e2738",
                plot_bgcolor="#151d2a"
            )
            st.plotly_chart(fig_defence, use_container_width=True)
    
    else:
        st.info("👉 Select two players to generate a detailed comparison.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style='text-align: center; color: #8b92a3; margin-top: 60px; padding: 40px 20px; border-top: 1px solid rgba(45, 212, 191, 0.1);'>
        <div style='font-size: 0.9em; font-weight: 600; margin-bottom: 8px;'>⚽ European Football Intelligence Platform</div>
        <div style='font-size: 0.8em;'>Advanced analytics across Europe's elite competitions | Data period: 2020–2025</div>
    </div>
""", unsafe_allow_html=True)
