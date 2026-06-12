import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
# DARK THEME CSS & TYPOGRAPHY - TACTICAL SCOUTING PLATFORM
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            --bg-primary: #030B12;
            --bg-secondary: #041018;
            --bg-sidebar: #08131A;
            --bg-card: #0D1C25;
            --bg-card-hover: #132733;

            --accent-primary: #0E7C86;
            --accent-secondary: #63AEB5;
            --accent-tertiary: #AFC3D2;
            --accent-muted: #145D6D;

            --text-primary: #F5F7FA;
            --text-secondary: #A7BAC6;
            --text-muted: #6C8594;
        }

        html, body, [class*="st-"] {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stApp, .stAppViewContainer, .stAppViewBlockContainer, .main, .block-container {
            background-color: transparent !important;
        }

        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--accent-muted) !important;
        }
        [data-testid="stSidebarHeader"], [data-testid="stSidebarContent"] {
            background-color: var(--bg-sidebar) !important;
        }

        h1, h2, h3, h4, h5, h6, .st-emotion-cache-10trblm h1 {
            font-family: 'Bebas Neue', sans-serif !important;
            letter-spacing: 1.5px;
            color: var(--text-primary);
            font-weight: 400;
            text-transform: uppercase;
        }

        /* Filters & Inputs Tactical Styling */
        div[data-baseweb="select"] > div {
            background-color: var(--bg-sidebar) !important;
            border: 1px solid var(--accent-muted) !important;
            color: var(--text-primary) !important;
        }
        div[data-baseweb="popover"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted) !important;
        }
        li[role="option"] {
            background-color: var(--bg-card) !important;
            color: var(--text-primary) !important;
        }
        li[role="option"]:hover {
            background-color: var(--accent-muted) !important;
        }
        span[data-baseweb="tag"] {
            background-color: var(--accent-primary) !important;
            color: white !important;
            border: none !important;
        }

        /* KPI Cards */
        [data-testid="stMetric"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted);
            border-radius: 0px !important;
            padding: 16px;
            box-shadow: none;
            border-left: 3px solid var(--accent-primary);
            transition: all 0.2s ease;
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
            color: var(--text-primary);
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2.5rem;
            line-height: 1.1;
        }

        /* Tabs */
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
            background-color: rgba(14, 124, 134, 0.1) !important;
        }
        
        /* Table Styling */
        [data-testid="stDataFrame"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted) !important;
            border-radius: 0px !important;
        }
        [data-testid="stDataFrame"] > div, 
        [data-testid="stDataFrame"] table, 
        [data-testid="stDataFrame"] th, 
        [data-testid="stDataFrame"] td {
            background-color: var(--bg-card) !important;
            color: var(--text-primary) !important;
            font-family: 'JetBrains Mono', monospace !important;
            border-color: var(--accent-muted) !important;
            font-size: 0.85rem;
        }
        [data-testid="stDataFrame"] th {
            color: var(--accent-secondary) !important;
            text-transform: uppercase;
        }

        .tactical-header {
            font-family: 'Bebas Neue', sans-serif;
            color: var(--text-primary);
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
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATA LAYER (OPTIMIZED & CACHED)
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_and_preprocess_data():
    """Load and preprocess dataset once to maximize performance."""
    try:
        url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
        df = pd.read_csv(url).fillna(0)
        # Precompute expensive metrics globally
        df['big_chance_conv'] = np.where(
            df['bigChancesCreated'] > 0, 
            (df['goals'] / df['bigChancesCreated']) * 100, 
            0
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def identify_gk_players(df):
    return df[(df['saves'] > 0) | (df['savesParried'] > 0) | (df['punches'] > 0) | (df['highClaims'] > 0)]

def hex_to_rgba(hex_color, opacity):
    h = hex_color.lstrip('#')
    if len(h) == 3: h = ''.join([c*2 for c in h])
    if len(h) != 6: return f'rgba(0, 0, 0, {opacity})'
    r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {opacity})'

# ═══════════════════════════════════════════════════════════════
# CHART FACTORIES
# ═══════════════════════════════════════════════════════════════
def apply_sofascore_radar_layout(fig, title):
    """Applies strict SofaScore tactical design template to a radar chart."""
    fig.update_layout(
        polar=dict(
            bgcolor="#041018",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#ffffff", family="JetBrains Mono", size=10)
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(family="Bebas Neue", size=16, color="#ffffff")
            )
        ),
        paper_bgcolor="#030B12",
        plot_bgcolor="#030B12",
        font=dict(color="#F5F7FA"),
        title=dict(
            text=title, 
            font=dict(family="Bebas Neue", size=22, color="#F5F7FA"),
            y=0.95, x=0.05, xanchor='left', yanchor='top'
        ),
        height=450,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1,
            font=dict(family="Inter", size=12, color="#A7BAC6")
        ),
        margin=dict(l=60, r=160, t=80, b=60)
    )
    return fig

def create_ranked_scouting_bar(df_subset, value_col, label_col, title):
    """Creates a custom horizontal bar chart matching the 5-step gradient palette constraint."""
    gradient_palette = ['#0E7C86', '#63AEB5', '#AFC3D2', '#D0D7DD', '#E8ECEF']
    
    sorted_df = df_subset.nlargest(5, value_col)
    metrics = sorted_df[label_col].tolist()
    values = sorted_df[value_col].tolist()
    
    metrics_rev = list(reversed(metrics))
    values_rev = list(reversed(values))
    
    bar_colors = [gradient_palette[len(metrics_rev) - 1 - i] for i in range(len(metrics_rev))]
    
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
        title=dict(
            text=title, 
            font=dict(family="Bebas Neue", size=20, color="#F5F7FA"),
            y=0.9, x=0.0, xanchor='left', yanchor='top'
        ),
        xaxis=dict(
            title=dict(text="METRIC OUTPUT", font=dict(family="JetBrains Mono", size=10, color="#6C8594")),
            tickfont=dict(family="JetBrains Mono", color="#6C8594", size=10),
            gridcolor="#145D6D",
            gridwidth=0.5,
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(family="Inter", color="#F5F7FA", size=12, weight="bold")
        ),
        paper_bgcolor="#0D1C25",
        plot_bgcolor="#0D1C25",
        font=dict(color="#F5F7FA"),
        height=320,
        showlegend=False,
        margin=dict(l=150, r=20, t=70, b=40)
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# APPLICATION STATE & FILTERS
# ═══════════════════════════════════════════════════════════════
df = load_and_preprocess_data()
if df.empty:
    st.error("Failed to load analytics data.")
    st.stop()

all_players = sorted(df['player'].unique().tolist())
all_teams = sorted(df['team'].unique().tolist())
all_leagues = sorted(df['league_name'].unique().tolist())
all_seasons = sorted(df['season_year'].unique().tolist())

# Determine Default Top 5 Leagues dynamically based on exact dataset strings
default_top_5 = [l for l in all_leagues if any(x in l for x in ['Premier League', 'LaLiga', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Primera Division'])]
if len(default_top_5) < 5: 
    default_top_5 = all_leagues[:5]

st.sidebar.markdown("<h2 style='font-family: Bebas Neue; color: #0E7C86; letter-spacing: 2px; margin-bottom: 0;'>SCOUTING PARAMETERS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin: 10px 0; border-color: #145D6D;'>", unsafe_allow_html=True)

selected_leagues = st.sidebar.multiselect("COMPETITION", options=all_leagues, default=default_top_5, key="leagues_filter")
selected_seasons = st.sidebar.multiselect("SEASON", options=all_seasons, default=[all_seasons[-1]], key="seasons_filter")
selected_teams = st.sidebar.multiselect("CLUB ROSTER", options=all_teams, default=None, key="teams_filter")

st.sidebar.markdown("<hr style='margin: 20px 0; border-color: #145D6D;'>", unsafe_allow_html=True)

# Optimized filtering
filtered_df = df[(df['league_name'].isin(selected_leagues)) & (df['season_year'].isin(selected_seasons))]
if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

# CRITICAL ISSUE 2: Empty Filter Crashes Prevention
if filtered_df.empty:
    st.warning("NO DATA AVAILABLE FOR SELECTED SCOUTING PARAMETERS. ADJUST FILTERS TO CONTINUE.")
    st.stop()

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
            <span style='color: var(--accent-secondary); font-family: JetBrains Mono; font-weight: 700;'>{len(filtered_players)}</span>
        </div>
        <div style='display: flex; justify-content: space-between;'>
            <span style='color: var(--text-secondary); font-size: 0.8rem; font-family: JetBrains Mono; text-transform: uppercase;'>Competitions:</span>
            <span style='color: var(--text-primary); font-family: JetBrains Mono; font-weight: 700;'>{len(selected_leagues)}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style="background-color: #030B12; padding: 40px 30px; border: 1px solid #145D6D; border-left: 6px solid #0E7C86; margin-bottom: 40px; position: relative; overflow: hidden;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #6C8594; letter-spacing: 2px; margin-bottom: 10px;">PRO-LEVEL SCOUTING SUITE // V.3.0</div>
        <h1 style="font-family: 'Bebas Neue', sans-serif; font-size: 4rem; font-weight: 400; letter-spacing: 3px; color: #F5F7FA; margin: 0 0 10px 0; line-height: 1;">EUROPEAN FOOTBALL ANALYTICS HUB</h1>
        <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #63AEB5; font-family: 'JetBrains Mono', monospace; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
            <span>[+] Elite Global Leagues</span>
            <span style="color: #145D6D;">|</span>
            <span>[+] Player-Centric Scouting</span>
            <span style="color: #145D6D;">|</span>
            <span style="color: #AFC3D2;">[+] Tactical Radar Profiling</span>
        </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["PLAYER-CENTRIC SCOUTING", "CLUB TACTICAL PROFILES", "HEAD-TO-HEAD DOSSIER"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: PLAYER-CENTRIC SCOUTING
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='tactical-header'>ATTACKING PRODUCTION — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'goals', 'player', "GOALS REGISTERED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'totalShots', 'player', "SHOT VOLUME"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'expectedGoals', 'player', "EXPECTED GOALS (xG)"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'big_chance_conv', 'player', "BIG CHANCE CONVERSION %"), use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("<div class='tactical-header'>PLAYMAKING & CREATIVITY — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'keyPasses', 'player', "KEY PASSES VOLUME"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'bigChancesCreated', 'player', "BIG CHANCES CREATED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'successfulDribbles', 'player', "SUCCESSFUL TAKE-ONS (DRIBBLES)"), use_container_width=True)
    with col2:
        top_creators_df = filtered_df.nlargest(5, 'bigChancesCreated')
        max_kp_c = max(top_creators_df['keyPasses'].max(), 1)
        max_bcc_c = max(top_creators_df['bigChancesCreated'].max(), 1)
        max_drb_c = max(top_creators_df['successfulDribbles'].max(), 1)
        
        fig_pm_radar = go.Figure()
        radar_palette = ['#0E7C86', '#63AEB5', '#AFC3D2', '#D0D7DD', '#E8ECEF']
        for idx, (_, p_row) in enumerate(top_creators_df.iterrows()):
            color = radar_palette[idx % len(radar_palette)]
            fig_pm_radar.add_trace(go.Scatterpolar(
                r=[
                    (p_row['keyPasses'] / max_kp_c * 100),
                    (p_row['bigChancesCreated'] / max_bcc_c * 100),
                    (p_row['successfulDribbles'] / max_drb_c * 100)
                ],
                theta=['Key Passes', 'Big Chances Created', 'Dribbles'],
                fill='toself',
                name=p_row['player'],
                line=dict(color=color, width=3),
                fillcolor=hex_to_rgba(color, 0.15)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_pm_radar, "CREATIVE ENGAGEMENT MATRIX"), use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("<div class='tactical-header'>POSSESSION & RETENTION — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'accuratePasses', 'player', "COMPLETED PASSES"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'touches', 'player', "TOTAL TOUCHES"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'accuratePassesPercentage', 'player', "PASS COMPLETION ACCURACY %"), use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("<div class='tactical-header'>DEFENDING & TACTICAL GRIT — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'tackles', 'player', "TACKLES WON"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'interceptions', 'player', "INTERCEPTIONS"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(filtered_df, 'clearances', 'player', "CLEARANCES"), use_container_width=True)
    with col2:
        top_defenders_df = filtered_df.nlargest(5, 'tackles')
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
        st.plotly_chart(apply_sofascore_radar_layout(fig_def_radar, "DEFENSIVE EFFICIENCY MATRIX"), use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("<div class='tactical-header'>GOALKEEPING SECURITY — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    gk_filtered_df = identify_gk_players(filtered_df)
    
    if len(gk_filtered_df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(gk_filtered_df, 'saves', 'player', "SAVES EXECUTED"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(gk_filtered_df, 'cleanSheet', 'player', "CLEAN SHEETS"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(gk_filtered_df, 'highClaims', 'player', "HIGH CLAIMS"), use_container_width=True)
    else:
        st.info("NO ACTIVE GOALKEEPER DATA IN THIS FILTER RANGE.")

# ═══════════════════════════════════════════════════════════════
# TAB 2: CLUB TACTICAL PROFILES
# ═══════════════════════════════════════════════════════════════
with tab2:
    selected_team_tab2 = st.selectbox(
        "ISOLATE CLUB ROSTER OR COMPARE TEAMS:",
        options=["All Teams"] + sorted(filtered_df['team'].unique().tolist()),
        key="club_filter_tab2"
    )
    
    if selected_team_tab2 == "All Teams":
        team_agg = filtered_df.groupby('team').sum(numeric_only=True).reset_index()
        
        st.markdown("<div class='tactical-header'>MACRO TEAM BENCHMARKS (TOP 5)</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'goals', 'team', "TEAM GOALS"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'totalShots', 'team', "TEAM SHOTS"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'expectedGoals', 'team', "TEAM xG"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'bigChancesCreated', 'team', "TEAM BIG CHANCES CREATED"), use_container_width=True)
            
        st.markdown("---")
        st.markdown("<div class='tactical-header'>TEAM RADAR DOSSIERS (TOP 5 TEAMS BY METRIC)</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            top_creative_teams = team_agg.nlargest(5, 'bigChancesCreated')
            max_bcc_t = max(top_creative_teams['bigChancesCreated'].max(), 1)
            max_kp_t = max(top_creative_teams['keyPasses'].max(), 1)
            max_drb_t = max(top_creative_teams['successfulDribbles'].max(), 1)
            
            fig_team_pm = go.Figure()
            radar_palette = ['#0E7C86', '#63AEB5', '#AFC3D2', '#D0D7DD', '#E8ECEF']
            for idx, (_, t_row) in enumerate(top_creative_teams.iterrows()):
                color = radar_palette[idx % len(radar_palette)]
                fig_team_pm.add_trace(go.Scatterpolar(
                    r=[
                        (t_row['bigChancesCreated'] / max_bcc_t * 100),
                        (t_row['keyPasses'] / max_kp_t * 100),
                        (t_row['successfulDribbles'] / max_drb_t * 100)
                    ],
                    theta=['BCC', 'Key Passes', 'Dribbles'],
                    fill='toself',
                    name=t_row['team'],
                    line=dict(color=color, width=3),
                    fillcolor=hex_to_rgba(color, 0.15)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_pm, "ELITE CREATIVE TEAMS MATRIX"), use_container_width=True)
            
        with col2:
            top_def_teams = team_agg.nlargest(5, 'tackles')
            max_tck_t = max(top_def_teams['tackles'].max(), 1)
            max_int_t = max(top_def_teams['interceptions'].max(), 1)
            max_clr_t = max(top_def_teams['clearances'].max(), 1)
            
            fig_team_def = go.Figure()
            for idx, (_, t_row) in enumerate(top_def_teams.iterrows()):
                color = radar_palette[idx % len(radar_palette)]
                fig_team_def.add_trace(go.Scatterpolar(
                    r=[
                        (t_row['tackles'] / max_tck_t * 100),
                        (t_row['interceptions'] / max_int_t * 100),
                        (t_row['clearances'] / max_clr_t * 100)
                    ],
                    theta=['Tackles Won', 'Interceptions', 'Clearances'],
                    fill='toself',
                    name=t_row['team'],
                    line=dict(color=color, width=3),
                    fillcolor=hex_to_rgba(color, 0.15)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_def, "ELITE DEFENSIVE TEAMS MATRIX"), use_container_width=True)

    else:
        team_df = filtered_df[filtered_df['team'] == selected_team_tab2]
        
        st.markdown(f"<div class='tactical-header'>[{selected_team_tab2}] TEAM SCOUTING REPORT</div>", unsafe_allow_html=True)
        
        st.markdown("#### ATTACK (TOP 5 PLAYERS)")
        att_df = team_df.nlargest(5, 'goals')[['player', 'goals', 'expectedGoals', 'totalShots']]
        att_df.columns = ['Player', 'Goals', 'xG', 'Shots']
        st.dataframe(att_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>#### CREATION (TOP 5 PLAYERS)", unsafe_allow_html=True)
        pm_df = team_df.nlargest(5, 'bigChancesCreated')[['player', 'keyPasses', 'bigChancesCreated', 'successfulDribbles']]
        pm_df.columns = ['Player', 'Key Passes', 'BCC', 'Dribbles']
        st.dataframe(pm_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>#### POSSESSION (TOP 5 PLAYERS)", unsafe_allow_html=True)
        pos_df = team_df.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']]
        pos_df.columns = ['Player', 'Passes Completed', 'Touches', 'Pass Acc %']
        pos_df['Pass Acc %'] = pos_df['Pass Acc %'].round(1)
        st.dataframe(pos_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>#### DEFENCE (TOP 5 PLAYERS)", unsafe_allow_html=True)
        def_df = team_df.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']]
        def_df.columns = ['Player', 'Tackles', 'Interceptions', 'Clearances']
        st.dataframe(def_df, use_container_width=True, hide_index=True)
        
        gk_team_df = identify_gk_players(team_df)
        if len(gk_team_df) > 0:
            st.markdown("<br>#### GOALKEEPING (TOP PLAYERS)", unsafe_allow_html=True)
            gk_df = gk_team_df.nlargest(5, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims']]
            gk_df.columns = ['Player', 'Saves', 'Clean Sheets', 'Claims']
            st.dataframe(gk_df, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: HEAD-TO-HEAD DOSSIER
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
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #0E7C86; padding: 25px; margin-bottom: 20px;'>
                    <div style='color: #0E7C86; font-family: JetBrains Mono, monospace; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // A</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue, sans-serif; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player1}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p1_data['team']} | {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #AFC3D2; padding: 25px; margin-bottom: 20px;'>
                    <div style='color: #AFC3D2; font-family: JetBrains Mono, monospace; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // B</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue, sans-serif; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player2}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p2_data['team']} | {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        
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
            'Performance Metric': list(attacking_metrics.keys()),
            player1: [v[0] for v in attacking_metrics.values()],
            player2: [v[1] for v in attacking_metrics.values()]
        })
        st.dataframe(attacking_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// PROGRESSION & DISTRIBUTION AUDIT</p>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            passing_metrics = {
                'Big Chances Created': (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                'Key Passes': (int(p1_data['keyPasses']), int(p2_data['keyPasses'])),
                'Successful Take-ons': (int(p1_data['successfulDribbles']), int(p2_data['successfulDribbles'])),
            }
            passing_df = pd.DataFrame({
                'Creative Output': list(passing_metrics.keys()),
                player1: [v[0] for v in passing_metrics.values()],
                player2: [v[1] for v in passing_metrics.values()]
            })
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #0E7C86; font-weight: 700;'>CREATION METRICS</p>", unsafe_allow_html=True)
            st.dataframe(passing_df, use_container_width=True, hide_index=True)
            
            passing_acc_metrics = {
                'Completed Passes': (int(p1_data['accuratePasses']), int(p2_data['accuratePasses'])),
                'Touch Volume': (int(p1_data['touches']), int(p2_data['touches'])),
                'Pass Completion %': (round(p1_data['accuratePassesPercentage'], 1), round(p2_data['accuratePassesPercentage'], 1)),
            }
            passing_acc_df = pd.DataFrame({
                'Ball Retention': list(passing_acc_metrics.keys()),
                player1: [v[0] for v in passing_acc_metrics.values()],
                player2: [v[1] for v in passing_acc_metrics.values()]
            })
            st.markdown("<br><p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #0E7C86; font-weight: 700;'>DISTRIBUTION METRICS</p>", unsafe_allow_html=True)
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
                line=dict(color='#0E7C86', width=3),
                fillcolor=hex_to_rgba('#0E7C86', 0.2)
            ))
            fig_playmaking.add_trace(go.Scatterpolar(
                r=[
                    (p2_data['bigChancesCreated'] / max_bcc * 100),
                    (p2_data['keyPasses'] / max_kp * 100),
                    (p2_data['successfulDribbles'] / max_drb * 100)
                ],
                theta=['BCC', 'Key Passes', 'Take-ons'],
                fill='toself',
                name=player2,
                line=dict(color='#AFC3D2', width=3),
                fillcolor=hex_to_rgba('#AFC3D2', 0.2)
            ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_playmaking, "CREATIVE INDEX RADAR"), use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("<p style='font-family: Bebas Neue; color: #F5F7FA; font-size: 1.4rem; letter-spacing: 2px; border-bottom: 1px solid #145D6D; padding-bottom: 5px;'>// DEFENSIVE ACTIONS</p>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            defence_metrics = {
                'Tackles Won': (int(p1_data['tackles']), int(p2_data['tackles'])),
                'Interceptions': (int(p1_data['interceptions']), int(p2_data['interceptions'])),
                'Clearances': (int(p1_data['clearances']), int(p2_data['clearances'])),
                'Aerial Duels Won': (int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
                'Ground Duels Won': (int(p1_data['groundDuelsWon']), int(p2_data['groundDuelsWon'])),
            }
            defence_df = pd.DataFrame({
                'Defensive Action': list(defence_metrics.keys()),
                player1: [v[0] for v in defence_metrics.values()],
                player2: [v[1] for v in defence_metrics.values()]
            })
            st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #0E7C86; font-weight: 700;'>TACKLING & SHAPE</p>", unsafe_allow_html=True)
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
                line=dict(color='#0E7C86', width=3),
                fillcolor=hex_to_rgba('#0E7C86', 0.2)
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
                line=dict(color='#AFC3D2', width=3),
                fillcolor=hex_to_rgba('#AFC3D2', 0.2)
            ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_defence, "DEFENSIVE INTENSITY RADAR"), use_container_width=True)
        
        st.markdown("---")
        
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
                    'Goalkeeper Metric': list(gk_metrics.keys()),
                    player1: [v[0] for v in gk_metrics.values()],
                    player2: [v[1] for v in gk_metrics.values()]
                })
                st.markdown("<p style='font-family: JetBrains Mono; font-size: 0.8rem; color: #0E7C86; font-weight: 700;'>GOALKEEPING OUTPUT</p>", unsafe_allow_html=True)
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
                    line=dict(color='#0E7C86', width=3),
                    fillcolor=hex_to_rgba('#0E7C86', 0.2)
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
                    line=dict(color='#AFC3D2', width=3),
                    fillcolor=hex_to_rgba('#AFC3D2', 0.2)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_gk, "SHOT STOPPING RADAR"), use_container_width=True)
            
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
