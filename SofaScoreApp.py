import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="European Football Analytics Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# DARK THEME CSS & TYPOGRAPHY - UNIFIED TACTICAL WORKSPACE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            /* BACKGROUNDS */
            --bg-primary: #030B12;
            --bg-secondary: #07141C;
            --bg-sidebar: #08131A;
            --bg-card: #0D1C25;
            --bg-card-hover: #132733;

            /* ACCENTS */
            --accent-primary: #00B8C9;
            --accent-secondary: #37E6F7;
            --accent-tertiary: #E8F5E9;
            --accent-muted: #145D6D;

            /* TEXT */
            --text-primary: #F5F7FA;
            --text-secondary: #A7BAC6;
            --text-muted: #6C8594;
        }

        /* CORE LAYOUT OVERRIDES (KILLING ALL WHITE BACKGROUNDS) */
        html, body {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stApp, .stAppViewContainer, .stAppViewBlockContainer {
            background-color: var(--bg-primary) !important;
        }
        
        .main, .block-container, [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }

        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--accent-muted) !important;
        }
        [data-testid="stSidebarHeader"], [data-testid="stSidebarContent"] {
            background-color: var(--bg-sidebar) !important;
        }

        /* Main Headers */
        h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm h1 {
            font-family: 'Bebas Neue', sans-serif !important;
            letter-spacing: 1.5px;
            color: var(--text-primary);
            font-weight: 400;
            text-transform: uppercase;
        }

        /* KPI Cards Styling */
        [data-testid="stMetric"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted);
            border-radius: 0px !important;
            padding: 16px;
            box-shadow: none;
            border-left: 3px solid var(--accent-muted);
            transition: all 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            background-color: var(--bg-card-hover) !important;
            border-left: 3px solid var(--accent-primary);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-secondary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        [data-testid="stMetricValue"] {
            color: var(--accent-primary);
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2.5rem;
            line-height: 1.1;
        }

        /* Tabs Styling */
        [data-testid="stTabs"] button {
            background-color: transparent !important;
            border: none !important;
            border-bottom: 2px solid var(--accent-muted) !important;
            border-radius: 0 !important;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.4rem;
            letter-spacing: 1px;
            color: var(--text-muted) !important;
            padding: 10px 24px;
            transition: all 0.2s;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            border-bottom: 3px solid var(--accent-primary) !important;
            color: var(--text-primary) !important;
            background-color: rgba(0, 184, 201, 0.05) !important;
        }
        
        [data-testid="stTabContent"] {
            background-color: transparent !important;
        }

        /* DataFrames Styling */
        [data-testid="stDataFrame"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted) !important;
            border-radius: 0px !important;
        }
        [data-testid="stDataFrame"] > div {
            background-color: var(--bg-card) !important;
        }

        .stDataFrame {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
        }
        
        /* Tactical Subheaders */
        .tactical-header {
            font-family: 'Bebas Neue', sans-serif;
            color: var(--accent-primary);
            border-bottom: 1px solid var(--accent-muted);
            padding-bottom: 6px;
            margin-bottom: 20px;
            margin-top: 40px;
            font-size: 1.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        hr {
            border-color: var(--accent-muted);
            opacity: 0.4;
            margin: 2.5rem 0;
        }
        
        /* General input overrides to match dark theme */
        .stSelectbox > div > div { background-color: var(--bg-card) !important; color: var(--text-primary) !important; border: 1px solid var(--accent-muted) !important; }
        .stMultiSelect > div > div { background-color: var(--bg-card) !important; color: var(--text-primary) !important; border: 1px solid var(--accent-muted) !important; }
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
    try:
        g = float(goals)
        bc = float(big_chances)
    except Exception:
        return 0
    if bc == 0 or np.isnan(bc) or np.isnan(g):
        return 0
    return (g / bc) * 100

def hex_to_rgba(hex_color, opacity):
    """Convert hex color to rgba string for Plotly"""
    if not isinstance(hex_color, str):
        return f'rgba(0, 0, 0, {opacity})'
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join([c*2 for c in h])
    if len(h) != 6:
        return f'rgba(0, 0, 0, {opacity})'
    try:
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return f'rgba(0, 0, 0, {opacity})'
    try:
        o = float(opacity)
    except Exception:
        o = 1.0
    o = max(0.0, min(1.0, o))
    return f'rgba({r}, {g}, {b}, {o})'

# ═══════════════════════════════════════════════════════════════
# SCOUTING RADAR STYLER (SOFASCORE STYLE SPECIFICATION)
# ═══════════════════════════════════════════════════════════════
def apply_sofascore_radar_layout(fig, title):
    """Applies a strict SofaScore tactical design template to a multi-player radar chart."""
    fig.update_layout(
        polar=dict(
            bgcolor="#041018",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(20, 93, 109, 0.2)",
                linecolor="rgba(20, 93, 109, 0.2)",
                tickfont=dict(color="#6C8594", family="JetBrains Mono", size=9)
            ),
            angularaxis=dict(
                gridcolor="rgba(20, 93, 109, 0.2)",
                linecolor="rgba(20, 93, 109, 0.2)",
                tickfont=dict(family="Bebas Neue", size=14, color="#F5F7FA")
            )
        ),
        paper_bgcolor="#0D1C25",
        plot_bgcolor="#0D1C25",
        font=dict(color="#F5F7FA"),
        title=dict(text=title, font=dict(family="Bebas Neue", size=20, color="#F5F7FA")),
        height=500,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(family="Inter", size=11, color="#A7BAC6")
        ),
        margin=dict(l=50, r=150, t=60, b=50)
    )
    return fig

# Shared palettes/utilities
radar_palette = ['#00B8C9', '#37E6F7', '#E8F5E9', '#A7BAC6', '#6C8594']


def create_horizontal_bar_chart(values_dict, title, colors):
    """Simple horizontal bar chart helper for club views."""
    labels = list(values_dict.keys())
    vals = list(values_dict.values())
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=vals,
        y=labels,
        orientation='h',
        marker=dict(color=colors[0] if colors else '#00B8C9'),
        text=[f"{v:.1f}" if isinstance(v, float) else f"{v}" for v in vals],
        textposition='auto'
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Bebas Neue", size=16, color="#F5F7FA")),
        paper_bgcolor="#0D1C25",
        plot_bgcolor="#0D1C25",
        font=dict(color="#F5F7FA"),
        height=360,
        margin=dict(l=140, r=20, t=50, b=40)
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# RANKING GRADIENT BAR CHART BUILDER
# ═══════════════════════════════════════════════════════════════
def create_ranked_scouting_bar(df_subset, value_col, label_col, title, inverse_rank=False):
    """Creates a custom horizontal bar chart matching the 5-step gradient palette constraint."""
    gradient_palette = ['#0E7C86', '#63AEB5', '#AFC3D2', '#D0D7DD', '#E8ECEF']
    
    sorted_df = df_subset.sort_values(by=value_col, ascending=inverse_rank).head(5)
    
    metrics = sorted_df[label_col].tolist()
    values = sorted_df[value_col].tolist()
    
    # Reverse loops for proper horizontal stack drawing hierarchy
    metrics_rev = list(reversed(metrics))
    values_rev = list(reversed(values))
    
    # If reversed, #1 is at the bottom of arrays, meaning it gets gradient index 0
    bar_colors = [gradient_palette[4 - i] for i in range(len(metrics_rev))]
    
    fig = go.Figure(data=[
        go.Bar(
            y=metrics_rev,
            x=values_rev,
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f'{v:.1f}' if isinstance(v, float) else f'{v}' for v in values_rev],
            textposition='auto',
            textfont=dict(family="JetBrains Mono", color="#030B12", weight="bold"),
            hovertemplate='<b style="font-family: Bebas Neue; color:#F5F7FA;">%{y}</b><br><span style="font-family: JetBrains Mono; color:#F5F7FA;">%{x:.2f}</span><extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(text=title, font=dict(family="Bebas Neue", size=18, color="#F5F7FA")),
        xaxis=dict(
            title=dict(text="OUTPUT TIER", font=dict(family="JetBrains Mono", size=9, color="#6C8594")),
            tickfont=dict(family="JetBrains Mono", color="#6C8594", size=9),
            gridcolor="#145D6D",
            gridwidth=0.5,
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(family="Inter", color="#F5F7FA", size=11, weight="bold")
        ),
        paper_bgcolor="#0D1C25",
        plot_bgcolor="#0D1C25",
        font=dict(color="#F5F7FA"),
        height=320,
        showlegend=False,
        margin=dict(l=140, r=20, t=50, b=40)
    )
    return fig

df = load_data()

# Safety: ensure horizontal bar helper exists in globals (guard against import/definition issues)
if 'create_horizontal_bar_chart' not in globals():
    def create_horizontal_bar_chart(values_dict, title, colors):
        labels = list(values_dict.keys())
        vals = list(values_dict.values())
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=vals,
            y=labels,
            orientation='h',
            marker=dict(color=colors[0] if colors else '#00B8C9'),
            text=[f"{v:.1f}" if isinstance(v, float) else f"{v}" for v in vals],
            textposition='auto'
        ))
        fig.update_layout(
            title=dict(text=title, font=dict(family="Bebas Neue", size=16, color="#F5F7FA")),
            paper_bgcolor="#0D1C25",
            plot_bgcolor="#0D1C25",
            font=dict(color="#F5F7FA"),
            height=360,
            margin=dict(l=140, r=20, t=50, b=40)
        )
        return fig

if df is None:
    st.stop()

# Cache global unique structures
all_players = sorted(df['player'].unique().tolist())
all_teams = sorted(df['team'].unique().tolist())
all_leagues = sorted(df['league_name'].unique().tolist())
all_seasons = sorted(df['season_year'].unique().tolist())

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - SCOUTING PARAMETERS
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("<h2 style='font-family: Bebas Neue; color: #00B8C9; letter-spacing: 2px; margin-bottom: 0;'>SCOUTING PARAMETERS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin: 10px 0; border-color: #145D6D;'>", unsafe_allow_html=True)

selected_leagues = st.sidebar.multiselect(
    "COMPETITION",
    options=all_leagues,
    default=all_leagues[:3],
    key="leagues_filter"
)

selected_seasons = st.sidebar.multiselect(
    "SEASON",
    options=all_seasons,
    default=[all_seasons[-1]],
    key="seasons_filter"
)

selected_teams = st.sidebar.multiselect(
    "CLUB ROSTER",
    options=all_teams,
    default=None,
    key="teams_filter"
)

st.sidebar.markdown("<hr style='margin: 20px 0; border-color: #145D6D;'>", unsafe_allow_html=True)

filtered_df = df[
    (df['league_name'].isin(selected_leagues)) &
    (df['season_year'].isin(selected_seasons))
]

if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

filtered_players = sorted(filtered_df['player'].unique().tolist())

st.sidebar.markdown(f"""
    <div style='background-color: var(--bg-card); padding: 16px; border: 1px solid var(--accent-muted); border-left: 4px solid var(--accent-primary); font-family: Inter, sans-serif;'>
        <div style='font-family: Bebas Neue; color: var(--accent-primary); font-size: 1.4rem; letter-spacing: 1px; margin-bottom: 12px;'>DATA VOLUME SUMMARY</div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
            <span style='color: var(--text-secondary); font-size: 0.8rem; font-family: JetBrains Mono; text-transform: uppercase;'>Total Records:</span>
            <span style='color: var(--text-primary); font-family: JetBrains Mono; font-weight: 700;'>{len(filtered_df)}</span>
        </div>
        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
            <span style='color: var(--text-secondary); font-size: 0.8rem; font-family: JetBrains Mono; text-transform: uppercase;'>Unique Players:</span>
            <span style='color: var(--accent-tertiary); font-family: JetBrains Mono; font-weight: 700;'>{len(filtered_players)}</span>
        </div>
        <div style='display: flex; justify-content: space-between;'>
            <span style='color: var(--text-secondary); font-size: 0.8rem; font-family: JetBrains Mono; text-transform: uppercase;'>Competitions:</span>
            <span style='color: var(--text-primary); font-family: JetBrains Mono; font-weight: 700;'>{len(selected_leagues)}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO BANNER - COMMAND CENTER STYLE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style="background-color: #030B12; padding: 40px 30px; border: 1px solid #145D6D; border-left: 6px solid #00B8C9; margin-bottom: 40px; position: relative; overflow: hidden;">
        <div style="position: absolute; right: -50px; top: -50px; opacity: 0.03; font-size: 200px;">⚽</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #6C8594; letter-spacing: 2px; margin-bottom: 10px;">PRO-LEVEL SCOUTING SUITE // V.2.1</div>
        <h1 style="font-family: 'Bebas Neue', sans-serif; font-size: 4rem; font-weight: 400; letter-spacing: 3px; color: #F5F7FA; margin: 0 0 10px 0; line-height: 1;">EUROPEAN FOOTBALL ANALYTICS HUB</h1>
        <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #37E6F7; font-family: 'JetBrains Mono', monospace; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
            <span>[+] Top 5 Leagues & UEFA</span>
            <span style="color: #145D6D;">|</span>
            <span>[+] Season-Level Metrics</span>
            <span style="color: #145D6D;">|</span>
            <span style="color: #E8F5E9;">[+] 2020–2026 Decade Review</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# MAIN HUB NAVIGATION STRUCTURE
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["PLAYER-CENTRIC SCOUTING", "CLUB TACTICAL PROFILES", "HEAD-TO-HEAD DOSSIER"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: PLAYER-CENTRIC SCOUTING DASHBOARD (REBUILT LAYER)
# ═══════════════════════════════════════════════════════════════
with tab1:
    
    # -----------------------------------------------------------
    # DATA LAYER LOGIC FOR INTERCONNECTED RADARS/LEADERBOARDS
    # -----------------------------------------------------------
    # Enforce safe conversion computation array extensions
    scouting_base = filtered_df.copy()
    scouting_base['big_chance_conv'] = scouting_base.apply(
        lambda r: calculate_big_chance_conversion(r['goals'], r['bigChancesCreated']), axis=1
    )
    
    # 1. ATTACK SECTION
    st.markdown("<div class='tactical-header'>ATTACKING PRODUCTION — LEADERBOARDS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'goals', 'player', "GOALS REGISTERED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'totalShots', 'player', "SHOT VOLUME"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'expectedGoals', 'player', "EXPECTED GOALS (xG)"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'big_chance_conv', 'player', "BIG CHANCE CONVERSION %"), use_container_width=True)
        
    st.markdown("---")
    
    # 2. PLAYMAKING SECTION
    st.markdown("<div class='tactical-header'>PLAYMAKING & CREATIVITY PROFILE</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'keyPasses', 'player', "KEY PASSES VOLUME"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'bigChancesCreated', 'player', "BIG CHANCES CREATED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'successfulDribbles', 'player', "SUCCESSFUL TAKE-ONS (DRIBBLES)"), use_container_width=True)
    with col2:
        # Multi-player layout engine initialization for top creators
        top_creators_df = scouting_base.nlargest(5, 'bigChancesCreated')
        max_kp_c = max(top_creators_df['keyPasses'].max(), 1)
        max_bcc_c = max(top_creators_df['bigChancesCreated'].max(), 1)
        max_drb_c = max(top_creators_df['successfulDribbles'].max(), 1)
        
        fig_pm_radar = go.Figure()
        radar_palette = ['#00B8C9', '#37E6F7', '#E8F5E9', '#A7BAC6', '#6C8594']
        
        for idx, (_, p_row) in enumerate(top_creators_df.iterrows()):
            color = radar_palette[idx % len(radar_palette)]
            fig_pm_radar.add_trace(go.Scatterpolar(
                r=[
                    (p_row['keyPasses'] / max_kp_c * 100),
                    (p_row['bigChancesCreated'] / max_bcc_c * 100),
                    (p_row['successfulDribbles'] / max_drb_c * 100)
                ],
                theta=['Key Passes', 'Big Chances Created', 'Successful Dribbles'],
                fill='toself',
                name=p_row['player'],
                line=dict(color=color, width=3),
                fillcolor=hex_to_rgba(color, 0.15)
            ))
        fig_pm_radar = apply_sofascore_radar_layout(fig_pm_radar, "CREATIVE ENGAGEMENT MATRIX (TOP 5 CREATORS)")
        st.plotly_chart(fig_pm_radar, use_container_width=True)
        
    st.markdown("---")
    
    # 3. POSSESSION SECTION
    st.markdown("<div class='tactical-header'>POSSESSION & RETENTION HUBS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'accuratePasses', 'player', "COMPLETED DISTRIBUTION VOLUME"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'touches', 'player', "BALL ENGAGEMENT (TOUCHES)"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'accuratePassesPercentage', 'player', "PASS COMPLETION ACCURACY %"), use_container_width=True)
        
    st.markdown("---")
    
    # 4. DEFENDING SECTION
    st.markdown("<div class='tactical-header'>DEFENSIVE ARCHITECTURE & GRIT</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'tackles', 'player', "TACKLES STRUCTURALLY WON"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'interceptions', 'player', "INTERCEPTIONS), TURNOVER PROFILE"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(scouting_base, 'clearances', 'player', "TACTICAL CLEARANCES"), use_container_width=True)
    with col2:
        # Multi-player structural profile layout engine for top defensive assets
        top_defenders_df = scouting_base.nlargest(5, 'tackles')
        max_tck_d = max(top_defenders_df['tackles'].max(), 1)
        max_int_d = max(top_defenders_df['interceptions'].max(), 1)
        max_clr_d = max(top_defenders_df['clearances'].max(), 1)
        
        fig_def_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_defenders_df.iterrows()):
            color = radar_palette[idx % len(radar_palette)]
            fig_def_radar.add_trace(go.Scatterpolar(
                r=[
                    (p_row['tackles'] / max_tck_d * 100),
                    (p_row['interceptions'] / max_int_d * 100),
                    (p_row['clearances'] / max_clr_d * 100)
                ],
                theta=['Tackles Won', 'Interceptions', 'Clearances'],
                fill='toself',
                name=p_row['player'],
                line=dict(color=color, width=3),
                fillcolor=hex_to_rgba(color, 0.15)
            ))
        fig_def_radar = apply_sofascore_radar_layout(fig_def_radar, "DEFENSIVE EFFICIENCY MATRIX (TOP 5 DEFENDERS)")
        st.plotly_chart(fig_def_radar, use_container_width=True)
        
    st.markdown("---")
    
    # 5. GOALKEEPING SECTION
    st.markdown("<div class='tactical-header'>GOALKEEPING SECURITY LAYER</div>", unsafe_allow_html=True)
    gk_scouting_base = identify_gk_players(scouting_base)
    
    if len(gk_scouting_base) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(gk_scouting_base, 'saves', 'player', "SAVES EXECUTED"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(gk_scouting_base, 'cleanSheet', 'player', "CLEAN SHEETS SECURED"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(gk_scouting_base, 'highClaims', 'player', "HIGH CLAIMS (AERIAL CAPTURE)"), use_container_width=True)
    else:
        st.info("NO ACTIVE GOALKEEPER PATTERNS CAPTURED UNDER ISOLATED CRITERIA.")

# ═══════════════════════════════════════════════════════════════
# TAB 2: CLUB-WISE DATA
# ═══════════════════════════════════════════════════════════════
with tab2:
    selected_team_filter = st.selectbox(
        "ISOLATE CLUB ROSTER:",
        options=["All Teams"] + sorted(filtered_df['team'].unique().tolist()),
        key="club_filter"
    )
    
    if selected_team_filter == "All Teams":
        club_data = filtered_df
    else:
        club_data = filtered_df[filtered_df['team'] == selected_team_filter]
    
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
        
        st.markdown("<div class='tactical-header'>GLOBAL CLUB BENCHMARKS</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1: st.metric("TOTAL GLS", f"{club_stats['goals'].sum():.0f}")
        with col2: st.metric("TOTAL xG", f"{club_stats['expectedGoals'].sum():.1f}")
        with col3: st.metric("BCC VOL.", f"{club_stats['bigChancesCreated'].sum():.0f}")
        with col4: st.metric("BCM VOL.", f"{club_stats['bigChancesMissed'].sum():.0f}")
        with col5: st.metric("TACKLES WON", f"{club_stats['tackles'].sum():.0f}")
        with col6: st.metric("SAVES MADE", f"{club_stats['saves'].sum():.0f}")
        with col7: st.metric("CLEAN SHEETS", f"{club_stats['cleanSheet'].sum():.0f}")
        
        st.markdown("---")
        
        st.markdown("<div class='tactical-header'>OFFENSIVE METRICS (ELITE CLUBS)</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            goals_by_club = club_data.groupby('team')['goals'].sum().sort_values(ascending=True).tail(10)
            fig_goals = create_horizontal_bar_chart(dict(goals_by_club), "GOALS VOLUME (TOP 10)", ['#00B8C9'])
            st.plotly_chart(fig_goals, use_container_width=True)
        with col2:
            xg_by_club = club_data.groupby('team')['expectedGoals'].sum().sort_values(ascending=True).tail(10)
            fig_xg = create_horizontal_bar_chart(dict(xg_by_club), "EXPECTED GOALS [xG] (TOP 10)", ['#145D6D'])
            st.plotly_chart(fig_xg, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            shots_by_club = club_data.groupby('team')['totalShots'].sum().sort_values(ascending=True).tail(10)
            fig_shots = create_horizontal_bar_chart(dict(shots_by_club), "SHOT VOLUME (TOP 10)", ['#37E6F7'])
            st.plotly_chart(fig_shots, use_container_width=True)
        with col2:
            bcc_by_club = club_data.groupby('team').apply(
                lambda x: calculate_big_chance_conversion(x['goals'].sum(), x['bigChancesCreated'].sum())
            ).sort_values(ascending=True).tail(10)
            fig_bcc = create_horizontal_bar_chart(dict(bcc_by_club), "BCC CONVERSION RATE % (TOP 10)", ['#E8F5E9'])
            st.plotly_chart(fig_bcc, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<div class='tactical-header'>PROGRESSION & CREATIVITY</div>", unsafe_allow_html=True)
        
        playmaking_by_club = club_data.groupby('team').agg({
            'bigChancesCreated': 'sum',
            'keyPasses': 'sum',
            'successfulDribbles': 'sum'
        }).reset_index()
        
        max_bcc = playmaking_by_club['bigChancesCreated'].max()
        max_kp = playmaking_by_club['keyPasses'].max()
        max_drb = playmaking_by_club['successfulDribbles'].max()
        
        fig_radar_playmaking = go.Figure()
        colors_for_clubs = ['#00B8C9', '#37E6F7', '#E8F5E9', '#A7BAC6', '#6C8594']
        
        for idx, (_, row) in enumerate(playmaking_by_club.iterrows()):
            line_color = colors_for_clubs[idx % len(colors_for_clubs)]
            fill_color = hex_to_rgba(line_color, 0.1)
            
            fig_radar_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (row['bigChancesCreated'] / max_bcc * 100) if max_bcc > 0 else 0,
                    (row['keyPasses'] / max_kp * 100) if max_kp > 0 else 0,
                    (row['successfulDribbles'] / max_drb * 100) if max_drb > 0 else 0
                ],
                theta=['BCC', 'Key Passes', 'Take-ons'],
                fill='toself',
                name=row['team'],
                line_color=line_color,
                fillcolor=fill_color,
                visible='legendonly' if idx > 4 else True 
            ))
        
        fig_radar_playmaking.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)),
                angularaxis=dict(gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(family="Bebas Neue", size=16, color="#F5F7FA"))
            ),
            title=dict(text="CREATIVE INDEX RADAR", font=dict(family="Bebas Neue", size=22, color="#F5F7FA")),
            paper_bgcolor="#0D1C25",
            plot_bgcolor="#0D1C25",
            font=dict(color="#F5F7FA"),
            height=500,
            legend=dict(font=dict(family="Inter", color="#A7BAC6", size=11))
        )
        st.plotly_chart(fig_radar_playmaking, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<div class='tactical-header'>BALL RETENTION & DISTRIBUTION</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            acc_passes_by_club = club_data.groupby('team')['accuratePasses'].sum().sort_values(ascending=True).tail(10)
            fig_acc = create_horizontal_bar_chart(dict(acc_passes_by_club), "COMPLETED PASSES (TOP 10)", ['#00B8C9'])
            st.plotly_chart(fig_acc, use_container_width=True)
        with col2:
            touches_by_club = club_data.groupby('team')['touches'].sum().sort_values(ascending=True).tail(10)
            fig_tch = create_horizontal_bar_chart(dict(touches_by_club), "TOUCH VOLUME (TOP 10)", ['#145D6D'])
            st.plotly_chart(fig_tch, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<div class='tactical-header'>DEFENSIVE ARCHITECTURE</div>", unsafe_allow_html=True)
        
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
            line_color = colors_for_clubs[idx % len(colors_for_clubs)]
            fill_color = hex_to_rgba(line_color, 0.1)
            
            fig_radar_def.add_trace(go.Scatterpolar(
                r=[
                    (row['tackles'] / max_tck * 100) if max_tck > 0 else 0,
                    (row['interceptions'] / max_int * 100) if max_int > 0 else 0,
                    (row['clearances'] / max_clr * 100) if max_clr > 0 else 0,
                    (row['aerialDuelsWon'] / max_aer * 100) if max_aer > 0 else 0,
                    (row['groundDuelsWon'] / max_grd * 100) if max_grd > 0 else 0
                ],
                theta=['Tackles Won', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ground Duels'],
                fill='toself',
                name=row['team'],
                line_color=line_color,
                fillcolor=fill_color,
                visible='legendonly' if idx > 4 else True
            ))
        
        fig_radar_def.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)),
                angularaxis=dict(gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(family="Bebas Neue", size=16, color="#F5F7FA"))
            ),
            title=dict(text="DEFENSIVE INTENSITY RADAR", font=dict(family="Bebas Neue", size=22, color="#F5F7FA")),
            paper_bgcolor="#0D1C25",
            plot_bgcolor="#0D1C25",
            font=dict(color="#F5F7FA"),
            height=500,
            legend=dict(font=dict(family="Inter", color="#A7BAC6", size=11))
        )
        st.plotly_chart(fig_radar_def, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<div class='tactical-header'>SQUAD AUDIT BY COMPETITION</div>", unsafe_allow_html=True)
        for league in selected_leagues:
            league_club_df = club_data[club_data['league_name'] == league]
            league_clubs = sorted(league_club_df['team'].unique().tolist())
            
            if league_clubs:
                st.markdown(f"<h3 style='color: #E8F5E9; border-bottom: 2px solid #145D6D; display: inline-block; padding-bottom: 4px; margin-top: 30px;'>{league} INTERNAL AUDIT</h3>", unsafe_allow_html=True)
                for club in league_clubs:
                    club_specific_df = league_club_df[league_club_df['team'] == club]
                    st.markdown(f"<h4 style='color: #00B8C9; margin-top: 25px; font-family: Bebas Neue; letter-spacing: 1px;'>[{club}] ROSTER DATA</h4>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #6C8594; font-weight: 700; margin-bottom: 5px;'>// OFFENSIVE PRODUCTION</p>", unsafe_allow_html=True)
                        top_att = club_specific_df.nlargest(5, 'goals')[['player', 'goals', 'assists', 'totalShots']]
                        top_att.columns = ['Player', 'GLS', 'AST', 'SHT']
                        st.dataframe(top_att, use_container_width=True, hide_index=True)
                        
                        st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #6C8594; font-weight: 700; margin-top: 15px; margin-bottom: 5px;'>// CREATION HUB</p>", unsafe_allow_html=True)
                        top_pm = club_specific_df.nlargest(5, 'bigChancesCreated')[['player', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
                        top_pm.columns = ['Player', 'BCC', 'KP', 'DRB']
                        st.dataframe(top_pm, use_container_width=True, hide_index=True)
                    with col2:
                        st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #6C8594; font-weight: 700; margin-bottom: 5px;'>// DISTRIBUTION METRICS</p>", unsafe_allow_html=True)
                        top_ps = club_specific_df.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
                        top_ps.columns = ['Player', 'CMP', 'TCH', 'CMP%']
                        top_ps['CMP%'] = top_ps['CMP%'].round(1)
                        st.dataframe(top_ps, use_container_width=True, hide_index=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #6C8594; font-weight: 700; margin-top: 15px; margin-bottom: 5px;'>// DEFENSIVE ACTIONS</p>", unsafe_allow_html=True)
                        top_df = club_specific_df.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']]
                        top_df.columns = ['Player', 'TCK', 'INT', 'CLR']
                        st.dataframe(top_df, use_container_width=True, hide_index=True)
                    with col2:
                        gk_club = identify_gk_players(club_specific_df)
                        if len(gk_club) > 0:
                            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #6C8594; font-weight: 700; margin-top: 15px; margin-bottom: 5px;'>// SHOT STOPPING</p>", unsafe_allow_html=True)
                            top_gk_club = gk_club.nlargest(3, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims']]
                            top_gk_club.columns = ['Player', 'SV', 'CS', 'CLAIMS']
                            st.dataframe(top_gk_club, use_container_width=True, hide_index=True)
                    st.markdown("<hr style='border-top: 1px dashed #145D6D; margin: 15px 0;'>", unsafe_allow_html=True)
    
    else:
        team_stats = club_data.agg({
            'goals': 'sum',
            'expectedGoals': 'sum',
            'bigChancesCreated': 'sum',
            'bigChancesMissed': 'sum',
            'tackles': 'sum',
            'saves': 'sum',
            'cleanSheet': 'sum'
        })
        
        st.markdown(f"<div class='tactical-header'>[{selected_team_filter}] MACRO AGGREGATES</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1: st.metric("TOTAL GLS", f"{team_stats['goals']:.0f}")
        with col2: st.metric("CUMULATIVE xG", f"{team_stats['expectedGoals']:.1f}")
        with col3: st.metric("BCC VOL.", f"{team_stats['bigChancesCreated']:.0f}")
        with col4: st.metric("BCM VOL.", f"{team_stats['bigChancesMissed']:.0f}")
        with col5: st.metric("TACKLES WON", f"{team_stats['tackles']:.0f}")
        with col6: st.metric("SAVES MADE", f"{team_stats['saves']:.0f}")
        with col7: st.metric("CLEAN SHEETS", f"{team_stats['cleanSheet']:.0f}")
        
        st.markdown("---")
        
        st.markdown(f"<div class='tactical-header'>[{selected_team_filter}] INTERNAL ROSTER AUDIT</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #00B8C9; font-weight: 700;'>// OFFENSIVE PRODUCTION</p>", unsafe_allow_html=True)
            top_att = club_data.nlargest(5, 'goals')[['player', 'goals', 'assists', 'totalShots']]
            top_att.columns = ['Target Profile', 'GLS', 'AST', 'SHT']
            st.dataframe(top_att, use_container_width=True, hide_index=True)
            
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #00B8C9; font-weight: 700; margin-top: 20px;'>// CREATION HUB</p>", unsafe_allow_html=True)
            top_pm = club_data.nlargest(5, 'bigChancesCreated')[['player', 'bigChancesCreated', 'keyPasses', 'successfulDribbles']]
            top_pm.columns = ['Target Profile', 'BCC', 'KP', 'DRB']
            st.dataframe(top_pm, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #37E6F7; font-weight: 700;'>// DISTRIBUTION METRICS</p>", unsafe_allow_html=True)
            top_ps = club_data.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
            top_ps.columns = ['Target Profile', 'CMP', 'TCH', 'CMP%']
            top_ps['CMP%'] = top_ps['CMP%'].round(1)
            st.dataframe(top_ps, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #E8F5E9; font-weight: 700; margin-top: 20px;'>// DEFENSIVE ACTIONS</p>", unsafe_allow_html=True)
            top_df = club_data.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']]
            top_df.columns = ['Target Profile', 'TCK', 'INT', 'CLR']
            st.dataframe(top_df, use_container_width=True, hide_index=True)
        with col2:
            gk_team = identify_gk_players(club_data)
            if len(gk_team) > 0:
                st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.9rem; color: #A7BAC6; font-weight: 700; margin-top: 20px;'>// SHOT STOPPING</p>", unsafe_allow_html=True)
                top_gk_team = gk_team.nlargest(3, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims', 'errorLeadToGoal']]
                top_gk_team.columns = ['Target Profile', 'SV', 'CS', 'CLAIMS', 'ERR']
                st.dataframe(top_gk_team, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='tactical-header'>HEAD-TO-HEAD SCOUTING DOSSIER</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("ISOLATE TARGET (A):", options=[None] + filtered_players, key="p1")
    with col2:
        player2 = st.selectbox("ISOLATE TARGET (B):", options=[None] + filtered_players, key="p2")
    
    st.markdown("---")
    
    if player1 and player2:
        p1_data = filtered_df[filtered_df['player'] == player1].iloc[0]
        p2_data = filtered_df[filtered_df['player'] == player2].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid #145D6D; border-left: 6px solid #00B8C9; padding: 25px; margin-bottom: 20px;'>
                    <div style='color: #00B8C9; font-family: JetBrains Mono, monospace; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // A</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue, sans-serif; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player1}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p1_data['team']} <span style='color: #145D6D;'>|</span> {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid #145D6D; border-left: 6px solid #E8F5E9; padding: 25px; margin-bottom: 20px;'>
                    <div style='color: #E8F5E9; font-family: JetBrains Mono, monospace; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // B</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue, sans-serif; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player2}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p2_data['team']} <span style='color: #145D6D;'>|</span> {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # OFFENSIVE STATS TABLE
        st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// OFFENSIVE PRODUCTION</p>", unsafe_allow_html=True)
        
        attacking_metrics = {
            'Goals Registered': (int(p1_data['goals']), int(p2_data['goals'])),
            'Assists': (int(p1_data['assists']), int(p2_data['assists'])),
            'Shot Volume': (int(p1_data['totalShots']), int(p2_data['totalShots'])),
            'Shots on Target': (int(p1_data['shotsOnTarget']), int(p2_data['shotsOnTarget'])),
            'BCC (Big Chances)': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
            'Expected Goals (xG)': (float(p1_data['expectedGoals']), float(p2_data['expectedGoals'])),
        }
        
        attacking_df = pd.DataFrame({
            'Performance Metric': attacking_metrics.keys(),
            player1: [attacking_metrics[m][0] for m in attacking_metrics.keys()],
            player2: [attacking_metrics[m][1] for m in attacking_metrics.keys()]
        })
        st.dataframe(attacking_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # CREATION WITH RADAR
        st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// PROGRESSION & DISTRIBUTION AUDIT</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            passing_metrics = {
                'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                'Key Passes': (int(p1_data['keyPasses']), int(p2_data['keyPasses'])),
                'Successful Take-ons': (int(p1_data['successfulDribbles']), int(p2_data['successfulDribbles'])),
            }
            passing_df = pd.DataFrame({
                'Creative Output': passing_metrics.keys(),
                player1: [passing_metrics[m][0] for m in passing_metrics.keys()],
                player2: [passing_metrics[m][1] for m in passing_metrics.keys()]
            })
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #00B8C9; font-weight: 700;'>CREATION METRICS</p>", unsafe_allow_html=True)
            st.dataframe(passing_df, use_container_width=True, hide_index=True)
            
            passing_acc_metrics = {
                'Completed Passes': (int(p1_data['accuratePasses']), int(p2_data['accuratePasses'])),
                'Touch Volume': (int(p1_data['touches']), int(p2_data['touches'])),
                'Pass Completion %': (round(p1_data['accuratePassesPercentage'], 1), round(p2_data['accuratePassesPercentage'], 1)),
            }
            passing_acc_df = pd.DataFrame({
                'Ball Retention': passing_acc_metrics.keys(),
                player1: [passing_acc_metrics[m][0] for m in passing_acc_metrics.keys()],
                player2: [passing_acc_metrics[m][1] for m in passing_acc_metrics.keys()]
            })
            st.markdown("<br><p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #00B8C9; font-weight: 700;'>DISTRIBUTION METRICS</p>", unsafe_allow_html=True)
            st.dataframe(passing_acc_df, use_container_width=True, hide_index=True)
            
        with col2:
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
                theta=['BCC', 'Key Passes', 'Take-ons'],
                fill='toself',
                name=player1,
                line_color='#00B8C9',
                fillcolor=hex_to_rgba('#00B8C9', 0.2)
            ))
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (p1_data['bigChancesCreated'] / max_bcc * 100),
                    (p1_data['keyPasses'] / max_kp * 100),
                    (p1_data['successfulDribbles'] / max_drb * 100)
                ],
                theta=['BCC', 'Key Passes', 'Take-ons'],
                fill='toself',
                name=player2,
                line_color='#E8F5E9',
                fillcolor=hex_to_rgba('#E8F5E9', 0.2)
            ))
            fig_playmaking.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)),
                    angularaxis=dict(gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(family="Bebas Neue", size=14, color="#F5F7FA"))
                ),
                title=dict(text="CREATIVE INDEX RADAR", font=dict(family="Bebas Neue", size=18, color="#F5F7FA")),
                paper_bgcolor="#0D1C25",
                plot_bgcolor="#0D1C25",
                font=dict(color="#F5F7FA"),
                height=400,
                legend=dict(font=dict(family="Inter", color="#A7BAC6", size=11))
            )
            st.plotly_chart(fig_playmaking, use_container_width=True)
        
        st.markdown("---")
        
        # DEFENCE TABLE
        st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// DEFENSIVE ACTIONS</p>", unsafe_allow_html=True)
        
        defence_metrics = {
            'Tackles Won': (int(p1_data['tackles']), int(p2_data['tackles'])),
            'Interceptions': (int(p1_data['interceptions']), int(p2_data['interceptions'])),
            'Clearances': (int(p1_data['clearances']), int(p2_data['clearances'])),
            'Aerial Duels Won': (int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
            'Ground Duels Won': (int(p1_data['groundDuelsWon']), int(p2_data['groundDuelsWon'])),
        }
        
        defence_df = pd.DataFrame({
            'Defensive Action': defence_metrics.keys(),
            player1: [defence_metrics[m][0] for m in defence_metrics.keys()],
            player2: [defence_metrics[m][1] for m in defence_metrics.keys()]
        })
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #37E6F7; font-weight: 700;'>TACKLING & SHAPE</p>", unsafe_allow_html=True)
            st.dataframe(defence_df, use_container_width=True, hide_index=True)
            
        with col2:
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
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerials', 'Ground Duels'],
                fill='toself',
                name=player1,
                line_color='#00B8C9',
                fillcolor=hex_to_rgba('#00B8C9', 0.2)
            ))
            fig_defence.add_trace(go.Scatterpolar(
                r=[
                    (p2_data['tackles'] / max_tck * 100),
                    (p2_data['interceptions'] / max_int * 100),
                    (p2_data['clearances'] / max_clr * 100),
                    (p2_data['aerialDuelsWon'] / max_aer * 100),
                    (p2_data['groundDuelsWon'] / max_grd * 100)
                ],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerials', 'Ground Duels'],
                fill='toself',
                name=player2,
                line_color='#E8F5E9',
                fillcolor=hex_to_rgba('#E8F5E9', 0.2)
            ))
            fig_defence.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)),
                    angularaxis=dict(gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(family="Bebas Neue", size=14, color="#F5F7FA"))
                ),
                title=dict(text="DEFENSIVE INTENSITY RADAR", font=dict(family="Bebas Neue", size=18, color="#F5F7FA")),
                paper_bgcolor="#0D1C25",
                plot_bgcolor="#0D1C25",
                font=dict(color="#F5F7FA"),
                height=400,
                legend=dict(font=dict(family="Inter", color="#A7BAC6", size=11))
            )
            st.plotly_chart(fig_defence, use_container_width=True)
        
        st.markdown("---")
        
        # GK STATS (if applicable)
        if p1_data['saves'] > 0 or p2_data['saves'] > 0:
            st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// SHOT STOPPING DOSSIER</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                gk_metrics = {
                    'Total Saves': (int(p1_data['saves']), int(p2_data['saves'])),
                    'Clean Sheets': (int(p1_data['cleanSheet']), int(p2_data['cleanSheet'])),
                    'High Claims': (int(p1_data['highClaims']), int(p2_data['highClaims'])),
                    'Errors to Goals': (int(p1_data['errorLeadToGoal']), int(p2_data['errorLeadToGoal'])),
                }
                gk_df = pd.DataFrame({
                    'Goalkeeper Metric': gk_metrics.keys(),
                    player1: [gk_metrics[m][0] for m in gk_metrics.keys()],
                    player2: [gk_metrics[m][1] for m in gk_metrics.keys()]
                })
                st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #A7BAC6; font-weight: 700;'>GOALKEEPING OUTPUT</p>", unsafe_allow_html=True)
                st.dataframe(gk_df, use_container_width=True, hide_index=True)
                
            with col2:
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
                        ((max_err - p1_data['errorLeadToGoal']) / max_err * 100) if max_err > 0 else 0,
                    ],
                    theta=['Saves', 'Clean Sheets', 'High Claims', 'Error Avoidance'],
                    fill='toself',
                    name=player1,
                    line_color='#00B8C9',
                    fillcolor=hex_to_rgba('#00B8C9', 0.2)
                ))
                fig_gk.add_trace(go.Scatterpolar(
                    r=[
                        (p2_data['saves'] / max_sv * 100),
                        (p2_data['cleanSheet'] / max_cs * 100),
                        (p2_data['highClaims'] / max_hc * 100),
                        ((max_err - p2_data['errorLeadToGoal']) / max_err * 100) if max_err > 0 else 0,
                    ],
                    theta=['Saves', 'Clean Sheets', 'High Claims', 'Error Avoidance'],
                    fill='toself',
                    name=player2,
                    line_color='#E8F5E9',
                    fillcolor=hex_to_rgba('#E8F5E9', 0.2)
                ))
                fig_gk.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)),
                        angularaxis=dict(gridcolor="#145D6D", linecolor="#145D6D", tickfont=dict(family="Bebas Neue", size=14, color="#F5F7FA"))
                    ),
                    title=dict(text="SHOT STOPPING RADAR", font=dict(family="Bebas Neue", size=18, color="#F5F7FA")),
                    paper_bgcolor="#0D1C25",
                    plot_bgcolor="#0D1C25",
                    font=dict(color="#F5F7FA"),
                    height=400,
                    legend=dict(font=dict(family="Inter", color="#A7BAC6", size=11))
                )
                st.plotly_chart(fig_gk, use_container_width=True)
            
            st.markdown("---")
    
    else:
        st.info("SELECT TWO TARGET PROFILES TO INITIATE HEAD-TO-HEAD DOSSIER COMPARISON.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style='text-align: center; color: var(--text-muted); margin-top: 50px; padding: 20px; font-family: JetBrains Mono, monospace; font-size: 0.75rem; border-top: 1px solid #145D6D;'>
        <span style='color: var(--accent-primary); font-weight: 700; letter-spacing: 2px;'>EUROPEAN FOOTBALL ANALYTICS HUB</span><br>
        <div style='margin-top: 10px; color: #6C8594;'>TACTICAL RECRUITMENT INTELLIGENCE & MACRO SEASON AUDITING</div>
    </div>
""", unsafe_allow_html=True)
