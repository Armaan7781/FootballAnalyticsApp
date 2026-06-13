import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import warnings
import unicodedata

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="European Football Analytics Hub",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        header[data-testid="stHeader"] { background-color: transparent !important; }
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--accent-muted) !important;
        }
        [data-testid="stSidebarHeader"], [data-testid="stSidebarContent"] {
            background-color: var(--bg-sidebar) !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Bebas Neue', sans-serif !important;
            letter-spacing: 1.5px;
            color: var(--text-primary);
            font-weight: 400;
            text-transform: uppercase;
        }
        div[data-baseweb="select"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted) !important;
            color: var(--text-primary) !important;
            border-radius: 6px !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s ease !important;
        }

    /* ── SELECTED TAGS (Clean, readable spacing with no text clipping) ── */
        span[data-baseweb="tag"] {
            display: inline-flex !important;
            align-items: center !important;
            gap: 4px !important;
            background-color: rgba(14, 124, 134, 0.3) !important;
            color: var(--accent-secondary) !important;
            border: 1px solid var(--accent-primary) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            border-radius: 4px !important;
            margin: 4px !important;
            padding: 0 4px !important;
            white-space: nowrap !important;
            box-sizing: border-box !important;
        }

        /* Remove the inner solid background and normalize tag content spacing */
        span[data-baseweb="tag"] span {
            background-color: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
            display: inline-flex !important;
            align-items: center !important;
        }

        /* Disable the Streamlit gradient mask on tag text */
        span[data-baseweb="tag"] span::before,
        span[data-baseweb="tag"] span::after {
            display: none !important;
        }

        /* Fix inner text clipping & strip systemic dark boxes */
        span[data-baseweb="tag"] * {
            background-color: transparent !important;
            overflow: visible !important;
        }

        span[data-baseweb="tag"] > div:first-child {
            padding-left: 4px !important;
            padding-right: 4px !important;
        }

        li[role="option"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
        }
        li[role="option"]:hover { background-color: rgba(14, 124, 134, 0.2) !important; }
        [data-testid="stMetric"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted);
            border-radius: 6px !important;
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

        /* ── CUSTOM TABLE STYLES ── */
        .scout-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #145D6D;
            margin-bottom: 16px;
        }
        .scout-table thead tr {
            background: linear-gradient(90deg, #0E7C86 0%, #0a5a62 100%);
        }
        .scout-table thead th {
            padding: 11px 14px;
            text-align: left;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: #F5F7FA;
            border: none;
        }
        .scout-table tbody tr {
            border-bottom: 1px solid rgba(20, 93, 109, 0.4);
            transition: background 0.15s ease;
        }
        .scout-table tbody tr:last-child { border-bottom: none; }
        .scout-table tbody tr:nth-child(odd)  { background-color: #0D1C25; }
        .scout-table tbody tr:nth-child(even) { background-color: #0a1820; }
        .scout-table tbody tr:hover { background-color: #132733; }
        .scout-table tbody td {
            padding: 10px 14px;
            color: #F5F7FA;
            vertical-align: middle;
        }
        .scout-table tbody td:first-child {
            font-weight: 600;
            color: #63AEB5;
        }
        .scout-table tbody td:not(:first-child) {
            font-family: 'JetBrains Mono', monospace;
            color: #AFC3D2;
        }
        .rank-badge {
            display: inline-block;
            width: 22px; height: 22px;
            line-height: 22px;
            text-align: center;
            border-radius: 50%;
            background: rgba(14, 124, 134, 0.25);
            border: 1px solid #0E7C86;
            color: #00D9FF;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            margin-right: 6px;
        }

        .tactical-header {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: #63AEB5;
            border-bottom: 1px solid var(--accent-muted);
            padding-bottom: 6px;
            margin-bottom: 20px;
            margin-top: 40px;
            font-size: 0.85rem;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        hr {
            border-color: var(--accent-muted);
            opacity: 0.4;
            margin: 2.5rem 0;
        }
        .section-label {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: #F5F7FA;
            font-size: 0.8rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            border-bottom: 1px solid #145D6D;
            padding-bottom: 5px;
            margin-bottom: 14px;
        }
        .sub-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: #0E7C86;
            font-weight: 700;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_and_preprocess_data():
    try:
        url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
        df = pd.read_csv(url).fillna(0)
        
        # Normalize text to remove special characters
        df['player'] = df['player'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        # FIX: Append team name to player name to create a unique identifier
        df['player'] = df['player'] + ' (' + df['team'] + ')'
        
        # Identify goalkeepers
        df['is_gk'] = (df['saves'] > 0) | (df['savesParried'] > 0) | (df['punches'] > 0) | (df['highClaims'] > 0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def aggregate_player_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    agg_dict = {col: 'sum' for col in numeric_cols}
    agg_dict.update({'team': 'first', 'league_name': 'first', 'is_gk': 'max'})
    for col in ['season_year', 'accuratePassesPercentage']:
        agg_dict.pop(col, None)
    agg_df = df.groupby('player').agg(agg_dict).reset_index()
    matches_played = df.groupby('player').size().reset_index(name='matches_played')
    agg_df = pd.merge(agg_df, matches_played, on='player', how='left')
    if len(agg_df) >= 10:
        top_10_threshold = agg_df['goals'].nlargest(10).iloc[-1]
    else:
        top_10_threshold = float('inf')
    agg_df['goal_conversion'] = np.where(
        agg_df['totalShots'] > 0,
        np.where(agg_df['goals'] >= top_10_threshold, np.clip((agg_df['goals'] / agg_df['totalShots']) * 100, 0, 100), 0),
        0
    )
    if 'accuratePasses' in agg_df.columns and 'totalPasses' in agg_df.columns:
        agg_df['accuratePassesPercentage'] = np.where(
            agg_df['totalPasses'] > 0, np.clip((agg_df['accuratePasses'] / agg_df['totalPasses']) * 100, 0, 100), 0
        )
    elif 'accuratePassesPercentage' in df.columns:
        pass_acc = df.groupby('player')['accuratePassesPercentage'].mean().reset_index()
        agg_df = pd.merge(agg_df, pass_acc, on='player', how='left')
    return agg_df

def aggregate_team_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    agg_dict = {col: 'sum' for col in numeric_cols}
    for col in ['season_year', 'accuratePassesPercentage']:
        agg_dict.pop(col, None)
    return df.groupby('team').agg(agg_dict).reset_index()

def hex_to_rgba(hex_color, opacity):
    h = hex_color.lstrip('#')
    if len(h) == 3: h = ''.join([c*2 for c in h])
    if len(h) != 6: return f'rgba(0, 0, 0, {opacity})'
    r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {opacity})'

def df_to_scout_table(df, col_rename=None):
    """Ranked table with numbered badges — used in top-5 lists."""
    if col_rename:
        df = df.rename(columns=col_rename)
    cols = df.columns.tolist()
    header = "".join(f"<th>{c}</th>" for c in cols)
    rows_html = ""
    for i, (_, row) in enumerate(df.iterrows()):
        cells = ""
        for j, c in enumerate(cols):
            val = row[c]
            if j == 0:
                cells += f"<td><span class='rank-badge'>{i+1}</span>{val}</td>"
            elif isinstance(val, float):
                cells += f"<td>{val:.1f}</td>"
            else:
                cells += f"<td>{val}</td>"
        rows_html += f"<tr>{cells}</tr>"
    return f"<table class='scout-table'><thead><tr>{header}</tr></thead><tbody>{rows_html}</tbody></table>"

def df_to_plain_table(df):
    """Comparison table without rank badges — used in H2H dossier."""
    cols = df.columns.tolist()
    header = "".join(f"<th>{c}</th>" for c in cols)
    rows_html = ""
    for _, row in df.iterrows():
        cells = ""
        for j, c in enumerate(cols):
            val = row[c]
            if j == 0:
                cells += f"<td style='color:#63AEB5;font-weight:600;'>{val}</td>"
            elif isinstance(val, float):
                cells += f"<td>{val:.2f}</td>"
            else:
                cells += f"<td>{val}</td>"
        rows_html += f"<tr>{cells}</tr>"
    return f"<table class='scout-table'><thead><tr>{header}</tr></thead><tbody>{rows_html}</tbody></table>"

# ═══════════════════════════════════════════════════════════════
# CHART FACTORIES
# ═══════════════════════════════════════════════════════════════
RADAR_COLORS = ['#00D9FF', '#00FF88', '#FF006E', '#FFB700', '#7E5BEF']

def apply_sofascore_radar_layout(fig, title):
    fig.update_layout(
        polar=dict(
            bgcolor="#041018",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#ffffff", family="JetBrains Mono", size=10)
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(family="Inter", size=11, color="#A7BAC6", weight="bold")
            )
        ),
        paper_bgcolor="#030B12",
        plot_bgcolor="#030B12",
        font=dict(color="#F5F7FA"),
        title=dict(
            text=title,
            font=dict(family="Inter", size=13, color="#63AEB5", weight="bold"),
            y=0.97, x=0.04, xanchor='left', yanchor='top'
        ),
        height=450,
        legend=dict(
            orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1,
            font=dict(family="Inter", size=11, color="#A7BAC6")
        ),
        margin=dict(l=60, r=160, t=60, b=60)
    )
    return fig

def create_ranked_scouting_bar(df_subset, value_col, label_col, title):
    gradient_palette = ['#0E7C86', '#63AEB5', '#AFC3D2', '#D0D7DD', '#E8ECEF']
    sorted_df = df_subset.nlargest(5, value_col)
    metrics = sorted_df[label_col].tolist()
    values = sorted_df[value_col].tolist()
    metrics_rev = list(reversed(metrics))
    values_rev = list(reversed(values))
    bar_colors = [gradient_palette[len(metrics_rev) - 1 - i] for i in range(len(metrics_rev))]
    fig = go.Figure(data=[
        go.Bar(
            y=metrics_rev, x=values_rev, orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f'{v:.1f}' if isinstance(v, float) else f'{v}' for v in values_rev],
            textposition='auto',
            textfont=dict(family="JetBrains Mono", color="#030B12", weight="bold"),
            hovertemplate='<b style="font-family:Inter;color:#F5F7FA;">%{y}</b><br><span style="font-family:JetBrains Mono;color:#F5F7FA;">%{x:.2f}</span><extra></extra>'
        )
    ])
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter", size=13, color="#63AEB5", weight="bold"),
            y=0.96, x=0.0, xanchor='left', yanchor='top'
        ),
        xaxis=dict(
            title=dict(text="METRIC OUTPUT", font=dict(family="JetBrains Mono", size=10, color="#6C8594")),
            tickfont=dict(family="JetBrains Mono", color="#6C8594", size=10),
            gridcolor="#145D6D", gridwidth=0.5, zeroline=False
        ),
        yaxis=dict(tickfont=dict(family="Inter", color="#F5F7FA", size=12, weight="bold")),
        paper_bgcolor="#0D1C25",
        plot_bgcolor="#0D1C25",
        font=dict(color="#F5F7FA"),
        height=320,
        showlegend=False,
        margin=dict(l=150, r=20, t=60, b=40)
    )
    return fig

# ═══════════════════════════════════════════════════════════════
# APP STATE & FILTERS
# ═══════════════════════════════════════════════════════════════
raw_df = load_and_preprocess_data()
if raw_df.empty:
    st.error("Failed to load analytics data.")
    st.stop()

all_leagues = sorted(raw_df['league_name'].unique().tolist())
all_seasons = sorted(raw_df['season_year'].unique().tolist())
all_teams   = sorted(raw_df['team'].unique().tolist())

st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, rgba(14,124,134,0.1) 0%, rgba(99,174,181,0.05) 100%);
                border: 1px solid #145D6D; border-radius: 8px; padding: 20px; margin-bottom: 20px;'>
        <div style='font-family: Inter; font-weight:700; color: #0E7C86; letter-spacing: 2px; margin: 0 0 20px 0; font-size: 0.85rem; text-transform:uppercase;'>
            ⚙️ INTELLIGENCE FILTERS
        </div>
    </div>
""", unsafe_allow_html=True)

selected_leagues = st.sidebar.multiselect("COMPETITION", options=all_leagues, default=all_leagues, key="leagues_filter")
selected_seasons = st.sidebar.multiselect("SEASON", options=all_seasons, default=[all_seasons[-1]], key="seasons_filter")
selected_teams   = st.sidebar.multiselect("CLUB ROSTER", options=all_teams, default=None, key="teams_filter")
st.sidebar.markdown("<hr style='margin: 20px 0; border-color: #145D6D;'>", unsafe_allow_html=True)

filtered_df = raw_df[(raw_df['league_name'].isin(selected_leagues)) & (raw_df['season_year'].isin(selected_seasons))]
if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]
if filtered_df.empty:
    st.warning("NO DATA AVAILABLE FOR SELECTED SCOUTING PARAMETERS. ADJUST FILTERS TO CONTINUE.")
    st.stop()

player_agg_df   = aggregate_player_stats(filtered_df)
gk_agg_df       = player_agg_df[player_agg_df['is_gk'] == 1]
outfield_agg_df = player_agg_df[player_agg_df['is_gk'] == 0]

st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #0D1C25 0%, #132733 100%);
                padding: 18px; border: 1px solid var(--accent-primary);
                border-left: 4px solid #00D9FF; font-family: Inter, sans-serif; border-radius: 8px;
                box-shadow: 0 4px 12px rgba(14,124,134,0.15);'>
        <div style='font-family: Inter; font-weight:700; color: #00D9FF; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 14px; text-transform: uppercase;'>
            📊 DATA VOLUME
        </div>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 12px;'>
            <div style='background: rgba(0,217,255,0.08); padding: 10px; border-radius: 4px; border: 1px solid rgba(0,217,255,0.2);'>
                <span style='color: var(--text-secondary); font-size: 0.7rem; font-family: JetBrains Mono; text-transform: uppercase; display: block; margin-bottom: 4px;'>Records</span>
                <span style='color: #00D9FF; font-family: JetBrains Mono; font-weight: 700; font-size: 1.3rem;'>{}</span>
            </div>
            <div style='background: rgba(0,255,136,0.08); padding: 10px; border-radius: 4px; border: 1px solid rgba(0,255,136,0.2);'>
                <span style='color: var(--text-secondary); font-size: 0.7rem; font-family: JetBrains Mono; text-transform: uppercase; display: block; margin-bottom: 4px;'>Players</span>
                <span style='color: #00FF88; font-family: JetBrains Mono; font-weight: 700; font-size: 1.3rem;'>{}</span>
            </div>
            <div style='background: rgba(255,183,0,0.08); padding: 10px; border-radius: 4px; border: 1px solid rgba(255,183,0,0.2);'>
                <span style='color: var(--text-secondary); font-size: 0.7rem; font-family: JetBrains Mono; text-transform: uppercase; display: block; margin-bottom: 4px;'>Competitions</span>
                <span style='color: #FFB700; font-family: JetBrains Mono; font-weight: 700; font-size: 1.3rem;'>{}</span>
            </div>
            <div style='background: rgba(126,91,239,0.08); padding: 10px; border-radius: 4px; border: 1px solid rgba(126,91,239,0.2);'>
                <span style='color: var(--text-secondary); font-size: 0.7rem; font-family: JetBrains Mono; text-transform: uppercase; display: block; margin-bottom: 4px;'>Seasons</span>
                <span style='color: #7E5BEF; font-family: JetBrains Mono; font-weight: 700; font-size: 1.3rem;'>{}</span>
            </div>
        </div>
    </div>
""".format(len(filtered_df), len(player_agg_df), len(selected_leagues), len(selected_seasons)), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style="background-color: #030B12; padding: 40px 30px; border: 1px solid #145D6D; border-left: 6px solid #0E7C86; margin-bottom: 40px; border-radius: 4px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #6C8594; letter-spacing: 2px; margin-bottom: 10px;">PRO-LEVEL SCOUTING SUITE // V.3.3</div>
        <h1 style="font-family: 'Bebas Neue', sans-serif; font-size: 4rem; font-weight: 400; letter-spacing: 3px; color: #F5F7FA; margin: 0 0 10px 0; line-height: 1;">EUROPEAN FOOTBALL ANALYTICS HUB</h1>
        <div style="display: flex; gap: 20px; font-size: 0.85rem; color: #63AEB5; font-family: 'JetBrains Mono', monospace; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
            <span>[+] Elite Global Leagues</span>
            <span style="color: #145D6D;">|</span>
            <span>[+] League Level Analysis</span>
            <span style="color: #145D6D;">|</span>
            <span style="color: #AFC3D2;">[+] Tactical Radar Profiling</span>
        </div>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["LEAGUE LEVEL ANALYSIS", "CLUB TACTICAL PROFILES", "PLAYER COMPARION"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: League Level Analysis
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='tactical-header'>ATTACKING WINDOW — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'goals', 'player', "GOALS REGISTERED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'totalShots', 'player', "SHOT VOLUME"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'expectedGoals', 'player', "EXPECTED GOALS (xG)"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'goal_conversion', 'player', "GOAL CONVERSION %"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>PLAYMAKING & CREATIVITY — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'keyPasses', 'player', "KEY PASSES VOLUME"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'bigChancesCreated', 'player', "BIG CHANCES CREATED"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'successfulDribbles', 'player', "SUCCESSFUL TAKE-ONS"), use_container_width=True)
    with col2:
        top_creators_df = outfield_agg_df.nlargest(5, 'bigChancesCreated')
        max_bcc  = max(top_creators_df['bigChancesCreated'].max(), 1)
        max_drb  = max(top_creators_df['successfulDribbles'].max(), 1)
        max_pf3  = max(top_creators_df['accurateFinalThirdPasses'].max() if 'accurateFinalThirdPasses' in top_creators_df.columns else 1, 1)
        max_pob  = max(top_creators_df['totalOppositionHalfPasses'].max() if 'totalOppositionHalfPasses' in top_creators_df.columns else 1, 1)
        max_foul = max(top_creators_df['wasFouled'].max() if 'wasFouled' in top_creators_df.columns else 1, 1)
        fig_pm_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_creators_df.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            pf3  = p_row['accurateFinalThirdPasses'] if 'accurateFinalThirdPasses' in p_row else 0
            pob  = p_row['totalOppositionHalfPasses'] if 'totalOppositionHalfPasses' in p_row else 0
            foul = p_row['wasFouled'] if 'wasFouled' in p_row else 0
            fig_pm_radar.add_trace(go.Scatterpolar(
                r=[(p_row['bigChancesCreated']/max_bcc*100), (p_row['successfulDribbles']/max_drb*100),
                   (pf3/max_pf3*100), (pob/max_pob*100), (foul/max_foul*100)],
                theta=['Big Chances', 'Dribbles', 'Passes Final 3rd', 'Passes Opp Box', 'Was Fouled'],
                fill='toself', name=p_row['player'],
                line=dict(color=color, width=3), fillcolor=hex_to_rgba(color, 0.2)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_pm_radar, "PLAYMAKING MATRIX"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>POSSESSION & RETENTION — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'accuratePasses', 'player', "COMPLETED PASSES"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'touches', 'player', "TOTAL TOUCHES"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'accuratePassesPercentage', 'player', "PASS COMPLETION ACCURACY %"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>DEFENDING & TACTICAL GRIT — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'tackles', 'player', "TACKLES WON"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'interceptions', 'player', "INTERCEPTIONS"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'aerialDuelsWon', 'player', "AERIAL DUELS WON"), use_container_width=True)
    with col2:
        top_defenders_df = outfield_agg_df.nlargest(5, 'tackles')
        max_tck = max(top_defenders_df['tackles'].max(), 1)
        max_int = max(top_defenders_df['interceptions'].max(), 1)
        max_aer = max(top_defenders_df['aerialDuelsWon'].max(), 1)
        max_grd = max(top_defenders_df['groundDuelsWon'].max(), 1)
        max_rec = max(top_defenders_df['ballRecovery'].max() if 'ballRecovery' in top_defenders_df.columns else 1, 1)
        fig_def_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_defenders_df.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            rec = p_row['ballRecovery'] if 'ballRecovery' in p_row else 0
            fig_def_radar.add_trace(go.Scatterpolar(
                r=[(p_row['tackles']/max_tck*100), (p_row['interceptions']/max_int*100),
                   (p_row['aerialDuelsWon']/max_aer*100), (p_row['groundDuelsWon']/max_grd*100), (rec/max_rec*100)],
                theta=['Tackles Won', 'Interceptions', 'Aerial Duels', 'Ground Duels', 'Ball Recovery'],
                fill='toself', name=p_row['player'],
                line=dict(color=color, width=3), fillcolor=hex_to_rgba(color, 0.2)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_def_radar, "DEFENSIVE EFFICIENCY MATRIX"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>GOALKEEPING SECURITY — TOP 5 PLAYERS</div>", unsafe_allow_html=True)
    if len(gk_agg_df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(gk_agg_df, 'saves', 'player', "SAVES EXECUTED"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(gk_agg_df, 'cleanSheet', 'player', "CLEAN SHEETS"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(gk_agg_df, 'highClaims', 'player', "HIGH CLAIMS"), use_container_width=True)
    else:
        st.info("NO ACTIVE GOALKEEPER DATA IN THIS FILTER RANGE.")

# ═══════════════════════════════════════════════════════════════
# TAB 2: CLUB TACTICAL PROFILES  — radars stacked vertically
# ═══════════════════════════════════════════════════════════════
with tab2:
    selected_team_tab2 = st.selectbox(
        "ISOLATE CLUB ROSTER OR COMPARE TEAMS:",
        options=["All Teams"] + sorted(filtered_df['team'].unique().tolist()),
        key="club_filter_tab2"
    )

    if selected_team_tab2 == "All Teams":
        team_agg = aggregate_team_stats(filtered_df)

        st.markdown("<div class='tactical-header'>TEAM BENCHMARKS (TOP 5)</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'goals', 'team', "TEAM GOALS"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'totalShots', 'team', "TEAM SHOTS"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'expectedGoals', 'team', "TEAM xG"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'bigChancesCreated', 'team', "TEAM BIG CHANCES CREATED"), use_container_width=True)

        st.markdown("---")
        st.markdown("<div class='tactical-header'>TEAM PERFORMANCE - RADAR (TOP 5 TEAMS BY METRIC)</div>", unsafe_allow_html=True)

        # ── PASSING RADAR ──────────────────────────────────────
        top_passing_teams = team_agg.nlargest(5, 'accuratePasses')
        max_ap    = max(top_passing_teams['accuratePasses'].max(), 1)
        max_t     = max(top_passing_teams['touches'].max(), 1)
        max_alb   = max(top_passing_teams['accurateLongBalls'].max() if 'accurateLongBalls' in top_passing_teams.columns else 1, 1)
        max_bcc_t = max(top_passing_teams['bigChancesCreated'].max(), 1)
        max_kp_t  = max(top_passing_teams['keyPasses'].max(), 1)
        fig_team_pass = go.Figure()
        for idx, (_, t_row) in enumerate(top_passing_teams.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            alb = t_row['accurateLongBalls'] if 'accurateLongBalls' in t_row else 0
            fig_team_pass.add_trace(go.Scatterpolar(
                r=[(t_row['accuratePasses']/max_ap*100), (t_row['touches']/max_t*100),
                   (alb/max_alb*100), (t_row['bigChancesCreated']/max_bcc_t*100), (t_row['keyPasses']/max_kp_t*100)],
                theta=['Accurate Passes', 'Touches', 'Long Balls', 'BCC', 'Key Passes'],
                fill='toself', name=t_row['team'],
                line=dict(color=color, width=3), fillcolor=hex_to_rgba(color, 0.2)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_team_pass, "PASSING TEAMS MATRIX"), use_container_width=True)

        # ── DEFENSIVE RADAR ────────────────────────────────────
        top_def_teams = team_agg.nlargest(5, 'tackles')
        max_tck_t = max(top_def_teams['tackles'].max(), 1)
        max_int_t = max(top_def_teams['interceptions'].max(), 1)
        max_aer_t = max(top_def_teams['aerialDuelsWon'].max(), 1)
        max_grd_t = max(top_def_teams['groundDuelsWon'].max(), 1)
        max_rec_t = max(top_def_teams['ballRecovery'].max() if 'ballRecovery' in top_def_teams.columns else 1, 1)
        fig_team_def = go.Figure()
        for idx, (_, t_row) in enumerate(top_def_teams.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            rec = t_row['ballRecovery'] if 'ballRecovery' in t_row else 0
            fig_team_def.add_trace(go.Scatterpolar(
                r=[(t_row['tackles']/max_tck_t*100), (t_row['interceptions']/max_int_t*100),
                   (t_row['aerialDuelsWon']/max_aer_t*100), (t_row['groundDuelsWon']/max_grd_t*100), (rec/max_rec_t*100)],
                theta=['Tackles Won', 'Interceptions', 'Aerial Duels', 'Ground Duels', 'Ball Recovery'],
                fill='toself', name=t_row['team'],
                line=dict(color=color, width=3), fillcolor=hex_to_rgba(color, 0.2)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_team_def, "DEFENSIVE TEAMS MATRIX"), use_container_width=True)

        # ── GK RADAR ──────────────────────────────────────────
        top_gk_teams = team_agg.nlargest(5, 'saves')
        max_sv     = max(top_gk_teams['saves'].max(), 1)
        max_cs     = max(top_gk_teams['cleanSheet'].max(), 1)
        max_alb_gk = max(top_gk_teams['accurateLongBalls'].max() if 'accurateLongBalls' in top_gk_teams.columns else 1, 1)
        max_err    = max(top_gk_teams['errorLeadToGoal'].max(), 1)
        fig_team_gk = go.Figure()
        for idx, (_, t_row) in enumerate(top_gk_teams.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            alb_gk = t_row['accurateLongBalls'] if 'accurateLongBalls' in t_row else 0
            fig_team_gk.add_trace(go.Scatterpolar(
                r=[(t_row['saves']/max_sv*100), (t_row['cleanSheet']/max_cs*100),
                   (alb_gk/max_alb_gk*100), ((max_err - t_row['errorLeadToGoal'])/max_err*100)],
                theta=['Saves', 'Clean Sheets', 'Long Balls', 'Error Avoidance'],
                fill='toself', name=t_row['team'],
                line=dict(color=color, width=3), fillcolor=hex_to_rgba(color, 0.2)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_team_gk, "GOALKEEPER TEAMS MATRIX"), use_container_width=True)

    else:
        team_df       = player_agg_df[player_agg_df['team'] == selected_team_tab2]
        team_outfield = team_df[team_df['is_gk'] == 0]
        team_gk       = team_df[team_df['is_gk'] == 1]

        st.markdown(f"<div class='tactical-header'>[{selected_team_tab2}] TEAM SCOUTING REPORT</div>", unsafe_allow_html=True)

        st.markdown("<p class='sub-label'>ATTACK — TOP 5 PLAYERS</p>", unsafe_allow_html=True)
        att_df = team_outfield.nlargest(5, 'goals')[['player', 'goals', 'expectedGoals', 'totalShots']].copy()
        st.markdown(df_to_scout_table(att_df, {'player':'Player','goals':'Goals','expectedGoals':'xG','totalShots':'Shots'}), unsafe_allow_html=True)

        st.markdown("<p class='sub-label' style='margin-top:20px;'>CREATION — TOP 5 PLAYERS</p>", unsafe_allow_html=True)
        pm_df = team_outfield.nlargest(5, 'bigChancesCreated')[['player', 'keyPasses', 'bigChancesCreated', 'successfulDribbles']].copy()
        st.markdown(df_to_scout_table(pm_df, {'player':'Player','keyPasses':'Key Passes','bigChancesCreated':'BCC','successfulDribbles':'Dribbles'}), unsafe_allow_html=True)

        st.markdown("<p class='sub-label' style='margin-top:20px;'>POSSESSION — TOP 5 PLAYERS</p>", unsafe_allow_html=True)
        pos_df = team_outfield.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']].copy()
        pos_df['accuratePassesPercentage'] = pos_df['accuratePassesPercentage'].round(1)
        st.markdown(df_to_scout_table(pos_df, {'player':'Player','accuratePasses':'Passes Completed','touches':'Touches','accuratePassesPercentage':'Pass Acc %'}), unsafe_allow_html=True)

        st.markdown("<p class='sub-label' style='margin-top:20px;'>DEFENCE — TOP 5 PLAYERS</p>", unsafe_allow_html=True)
        def_df = team_outfield.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'aerialDuelsWon']].copy()
        st.markdown(df_to_scout_table(def_df, {'player':'Player','tackles':'Tackles','interceptions':'Interceptions','aerialDuelsWon':'Aerial Duels'}), unsafe_allow_html=True)

        if len(team_gk) > 0:
            st.markdown("<p class='sub-label' style='margin-top:20px;'>GOALKEEPING</p>", unsafe_allow_html=True)
            gk_df = team_gk.nlargest(5, 'saves')[['player', 'saves', 'cleanSheet', 'highClaims']].copy()
            st.markdown(df_to_scout_table(gk_df, {'player':'Player','saves':'Saves','cleanSheet':'Clean Sheets','highClaims':'Claims'}), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='tactical-header'>PLAYER COMPARISON</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("ISOLATE TARGET (A):", options=[None] + sorted(player_agg_df['player'].tolist()), key="p1")
    with col2:
        player2 = st.selectbox("ISOLATE TARGET (B):", options=[None] + sorted(player_agg_df['player'].tolist()), key="p2")

    st.markdown("---")

    if player1 and player2:
        p1_data = player_agg_df[player_agg_df['player'] == player1].iloc[0]
        p2_data = player_agg_df[player_agg_df['player'] == player2].iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            p1_type = "GOALKEEPER" if p1_data['is_gk'] else "OUTFIELD"
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #00D9FF; padding: 25px; margin-bottom: 20px; border-radius: 4px;'>
                    <div style='color: #00D9FF; font-family: JetBrains Mono; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // A ({p1_type})</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player1}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p1_data['team']} | {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            p2_type = "GOALKEEPER" if p2_data['is_gk'] else "OUTFIELD"
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #00FF88; padding: 25px; margin-bottom: 20px; border-radius: 4px;'>
                    <div style='color: #00FF88; font-family: JetBrains Mono; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // B ({p2_type})</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player2}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p2_data['team']} | {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)

        is_p1_gk = p1_data['is_gk']
        is_p2_gk = p2_data['is_gk']

        if not is_p1_gk and not is_p2_gk:
            # ── OFFENSE ─────────────────────────────
            st.markdown("<p class='section-label'>// OFFENSE</p>", unsafe_allow_html=True)
            attacking_metrics = {
                'Goals Registered':    (int(p1_data['goals']),           int(p2_data['goals'])),
                'Assists':             (int(p1_data['assists']),          int(p2_data['assists'])),
                'Shot Volume':         (int(p1_data['totalShots']),       int(p2_data['totalShots'])),
                'Shots on Target':     (int(p1_data['shotsOnTarget']),    int(p2_data['shotsOnTarget'])),
                'BCC (Big Chances)':   (int(p1_data['bigChancesCreated']),int(p2_data['bigChancesCreated'])),
                'Expected Goals (xG)': (float(p1_data['expectedGoals']),  float(p2_data['expectedGoals'])),
            }
            att_cmp_df = pd.DataFrame({'Performance Metric': list(attacking_metrics.keys()),
                                       player1: [v[0] for v in attacking_metrics.values()],
                                       player2: [v[1] for v in attacking_metrics.values()]})
            st.markdown(df_to_plain_table(att_cmp_df), unsafe_allow_html=True)
            st.markdown("---")

            # ── PLAYMAKING AUDIT ─────────────────────────────────
            st.markdown("<p class='section-label'>// PLAYMAKING AUDIT</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                p1_pf3  = p1_data['accurateFinalThirdPasses'] if 'accurateFinalThirdPasses' in p1_data else 0
                p2_pf3  = p2_data['accurateFinalThirdPasses'] if 'accurateFinalThirdPasses' in p2_data else 0
                p1_pob  = p1_data['totalOppositionHalfPasses'] if 'totalOppositionHalfPasses' in p1_data else 0
                p2_pob  = p2_data['totalOppositionHalfPasses'] if 'totalOppositionHalfPasses' in p2_data else 0
                p1_foul = p1_data['wasFouled'] if 'wasFouled' in p1_data else 0
                p2_foul = p2_data['wasFouled'] if 'wasFouled' in p2_data else 0
                playmaking_metrics = {
                    'Big Chances Created':   (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                    'Dribbles (Successful)': (int(p1_data['successfulDribbles']),int(p2_data['successfulDribbles'])),
                    'Passes in Final 3rd':   (int(p1_pf3), int(p2_pf3)),
                    'Passes in Opp Box':     (int(p1_pob), int(p2_pob)),
                    'Times Fouled':          (int(p1_foul),int(p2_foul)),
                }
                pm_cmp_df = pd.DataFrame({'Playmaking Metric': list(playmaking_metrics.keys()),
                                          player1: [v[0] for v in playmaking_metrics.values()],
                                          player2: [v[1] for v in playmaking_metrics.values()]})
                st.markdown(df_to_plain_table(pm_cmp_df), unsafe_allow_html=True)
            with col2:
                max_bcc  = max(p1_data['bigChancesCreated'],  p2_data['bigChancesCreated'],  1)
                max_drb  = max(p1_data['successfulDribbles'], p2_data['successfulDribbles'],  1)
                max_pf3  = max(p1_pf3, p2_pf3, 1)
                max_pob  = max(p1_pob, p2_pob, 1)
                max_foul = max(p1_foul, p2_foul, 1)
                fig_playmaking = go.Figure()
                fig_playmaking.add_trace(go.Scatterpolar(
                    r=[(p1_data['bigChancesCreated']/max_bcc*100), (p1_data['successfulDribbles']/max_drb*100),
                       (p1_pf3/max_pf3*100), (p1_pob/max_pob*100), (p1_foul/max_foul*100)],
                    theta=['Big Chances','Dribbles','Final 3rd Passes','Opp Box Passes','Was Fouled'],
                    fill='toself', name=player1,
                    line=dict(color='#00D9FF', width=3), fillcolor=hex_to_rgba('#00D9FF', 0.2)
                ))
                fig_playmaking.add_trace(go.Scatterpolar(
                    r=[(p2_data['bigChancesCreated']/max_bcc*100), (p2_data['successfulDribbles']/max_drb*100),
                       (p2_pf3/max_pf3*100), (p2_pob/max_pob*100), (p2_foul/max_foul*100)],
                    theta=['Big Chances','Dribbles','Final 3rd Passes','Opp Box Passes','Was Fouled'],
                    fill='toself', name=player2,
                    line=dict(color='#00FF88', width=3), fillcolor=hex_to_rgba('#00FF88', 0.2)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_playmaking, "PLAYMAKING MATRIX"), use_container_width=True)
            st.markdown("---")

# ── PASSING PROFILE ─────────────────────────────
            st.markdown("<p class='section-label'>// PASSING PROFILE</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                p1_alb = p1_data['accurateLongBalls'] if 'accurateLongBalls' in p1_data else 0
                p2_alb = p2_data['accurateLongBalls'] if 'accurateLongBalls' in p2_data else 0
                passing_metrics = {
                    'Touches':             (int(p1_data['touches']),        int(p2_data['touches'])),
                    'Key Passes':          (int(p1_data['keyPasses']),      int(p2_data['keyPasses'])),
                    'Accurate Passes':     (int(p1_data['accuratePasses']), int(p2_data['accuratePasses'])),
                    'Accurate Long Balls': (int(p1_alb),                    int(p2_alb)),
                }
                pass_cmp_df = pd.DataFrame({'Passing Metric': list(passing_metrics.keys()),
                                            player1: [v[0] for v in passing_metrics.values()],
                                            player2: [v[1] for v in passing_metrics.values()]})
                st.markdown(df_to_plain_table(pass_cmp_df), unsafe_allow_html=True)
            with col2:
                max_tch = max(p1_data['touches'],        p2_data['touches'],        1)
                max_kp  = max(p1_data['keyPasses'],      p2_data['keyPasses'],      1)
                max_ap  = max(p1_data['accuratePasses'], p2_data['accuratePasses'], 1)
                max_alb = max(p1_alb, p2_alb, 1)
                
                fig_passing = go.Figure()
                fig_passing.add_trace(go.Scatterpolar(
                    r=[(p1_data['touches']/max_tch*100), (p1_data['keyPasses']/max_kp*100),
                       (p1_data['accuratePasses']/max_ap*100), (p1_alb/max_alb*100)],
                    theta=['Touches', 'Key Passes', 'Accurate Passes', 'Long Balls'],
                    fill='toself', name=player1,
                    line=dict(color='#00D9FF', width=3), fillcolor=hex_to_rgba('#00D9FF', 0.2)
                ))
                fig_passing.add_trace(go.Scatterpolar(
                    r=[(p2_data['touches']/max_tch*100), (p2_data['keyPasses']/max_kp*100),
                       (p2_data['accuratePasses']/max_ap*100), (p2_alb/max_alb*100)],
                    theta=['Touches', 'Key Passes', 'Accurate Passes', 'Long Balls'],
                    fill='toself', name=player2,
                    line=dict(color='#00FF88', width=3), fillcolor=hex_to_rgba('#00FF88', 0.2)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_passing, "PASSING PROFILE RADAR"), use_container_width=True)
            st.markdown("---")

            # ── DEFENSIVE ACTIONS ─────────────────────────────────
            st.markdown("<p class='section-label'>// DEFENSIVE ACTIONS</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                rec1 = p1_data['ballRecovery'] if 'ballRecovery' in p1_data else 0
                rec2 = p2_data['ballRecovery'] if 'ballRecovery' in p2_data else 0
                defence_metrics = {
                    'Tackles Won':     (int(p1_data['tackles']),        int(p2_data['tackles'])),
                    'Interceptions':   (int(p1_data['interceptions']),  int(p2_data['interceptions'])),
                    'Aerial Duels Won':(int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
                    'Ground Duels Won':(int(p1_data['groundDuelsWon']), int(p2_data['groundDuelsWon'])),
                    'Ball Recovery':   (int(rec1), int(rec2)),
                }
                def_cmp_df = pd.DataFrame({'Defensive Action': list(defence_metrics.keys()),
                                           player1: [v[0] for v in defence_metrics.values()],
                                           player2: [v[1] for v in defence_metrics.values()]})
                st.markdown(df_to_plain_table(def_cmp_df), unsafe_allow_html=True)
            with col2:
                max_tck = max(p1_data['tackles'],        p2_data['tackles'],        1)
                max_int = max(p1_data['interceptions'],  p2_data['interceptions'],  1)
                max_aer = max(p1_data['aerialDuelsWon'], p2_data['aerialDuelsWon'], 1)
                max_grd = max(p1_data['groundDuelsWon'], p2_data['groundDuelsWon'], 1)
                max_rec = max(rec1, rec2, 1)
                fig_defence = go.Figure()
                fig_defence.add_trace(go.Scatterpolar(
                    r=[(p1_data['tackles']/max_tck*100), (p1_data['interceptions']/max_int*100),
                       (p1_data['aerialDuelsWon']/max_aer*100), (p1_data['groundDuelsWon']/max_grd*100), (rec1/max_rec*100)],
                    theta=['Tackles','Interceptions','Aerials','Ground Duels','Ball Recovery'],
                    fill='toself', name=player1,
                    line=dict(color='#00D9FF', width=3), fillcolor=hex_to_rgba('#00D9FF', 0.2)
                ))
                fig_defence.add_trace(go.Scatterpolar(
                    r=[(p2_data['tackles']/max_tck*100), (p2_data['interceptions']/max_int*100),
                       (p2_data['aerialDuelsWon']/max_aer*100), (p2_data['groundDuelsWon']/max_grd*100), (rec2/max_rec*100)],
                    theta=['Tackles','Interceptions','Aerials','Ground Duels','Ball Recovery'],
                    fill='toself', name=player2,
                    line=dict(color='#00FF88', width=3), fillcolor=hex_to_rgba('#00FF88', 0.2)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_defence, "DEFENSIVE MATRIX RADAR"), use_container_width=True)

        elif is_p1_gk and is_p2_gk:
            st.markdown("<p class='section-label'>// SHOT STOPPING DOSSIER</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                alb1 = p1_data['accurateLongBalls'] if 'accurateLongBalls' in p1_data else 0
                alb2 = p2_data['accurateLongBalls'] if 'accurateLongBalls' in p2_data else 0
                gk_metrics = {
                    'Total Saves':        (int(p1_data['saves']),           int(p2_data['saves'])),
                    'Clean Sheets':       (int(p1_data['cleanSheet']),      int(p2_data['cleanSheet'])),
                    'Accurate Long Balls':(int(alb1),                      int(alb2)),
                    'Errors Led To Goal': (int(p1_data['errorLeadToGoal']), int(p2_data['errorLeadToGoal'])),
                }
                gk_cmp_df = pd.DataFrame({'Goalkeeper Metric': list(gk_metrics.keys()),
                                          player1: [v[0] for v in gk_metrics.values()],
                                          player2: [v[1] for v in gk_metrics.values()]})
                st.markdown(df_to_plain_table(gk_cmp_df), unsafe_allow_html=True)
            with col2:
                max_sv  = max(p1_data['saves'],           p2_data['saves'],           1)
                max_cs  = max(p1_data['cleanSheet'],       p2_data['cleanSheet'],       1)
                max_alb = max(alb1, alb2, 1)
                max_err = max(p1_data['errorLeadToGoal'], p2_data['errorLeadToGoal'],  1)
                fig_gk = go.Figure()
                fig_gk.add_trace(go.Scatterpolar(
                    r=[(p1_data['saves']/max_sv*100), (p1_data['cleanSheet']/max_cs*100),
                       (alb1/max_alb*100), ((max_err-p1_data['errorLeadToGoal'])/max_err*100)],
                    theta=['Saves','Clean Sheets','Long Balls','Error Avoidance'],
                    fill='toself', name=player1,
                    line=dict(color='#00D9FF', width=3), fillcolor=hex_to_rgba('#00D9FF', 0.2)
                ))
                fig_gk.add_trace(go.Scatterpolar(
                    r=[(p2_data['saves']/max_sv*100), (p2_data['cleanSheet']/max_cs*100),
                       (alb2/max_alb*100), ((max_err-p2_data['errorLeadToGoal'])/max_err*100)],
                    theta=['Saves','Clean Sheets','Long Balls','Error Avoidance'],
                    fill='toself', name=player2,
                    line=dict(color='#00FF88', width=3), fillcolor=hex_to_rgba('#00FF88', 0.2)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_gk, "GOALKEEPER RADAR"), use_container_width=True)
        else:
            st.warning("⚠️ YOU HAVE SELECTED ONE OUTFIELD PLAYER AND ONE GOALKEEPER. DIRECT METRIC COMPARISON IS NOT RECOMMENDED FOR DIFFERENT ROLES.")
    else:
        st.info("SELECT TWO TARGET PROFILES TO INITIATE HEAD-TO-HEAD DOSSIER COMPARISON.")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style='text-align: center; color: var(--text-muted); margin-top: 50px; padding: 20px; font-family: JetBrains Mono, monospace; font-size: 0.75rem; border-top: 1px solid #145D6D;'>
        <span style='color: var(--accent-primary); font-weight: 700; letter-spacing: 2px;'>EUROPEAN FOOTBALL ANALYTICS HUB</span><br>
        <div style='margin-top: 10px; color: #6C8594;'>TACTICAL RECRUITMENT INTELLIGENCE & SEASON LEVEL ANALYSIS</div>
    </div>
""", unsafe_allow_html=True)
