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
        
        /* ── SIDEBAR STYLING ── */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--accent-muted) !important;
            padding-top: 1rem;
        }
        [data-testid="stSidebarHeader"], [data-testid="stSidebarContent"] {
            background-color: var(--bg-sidebar) !important;
        }
        .sidebar-title {
            font-family: 'Bebas Neue', sans-serif;
            color: var(--accent-secondary);
            letter-spacing: 2px;
            font-size: 1.4rem;
            margin-bottom: 10px;
            text-transform: uppercase;
            border-bottom: 1px solid var(--accent-muted);
            padding-bottom: 10px;
        }
        .stMultiSelect label p {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            color: var(--text-secondary) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 2px !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Bebas Neue', sans-serif !important;
            letter-spacing: 1.5px;
            color: var(--text-primary);
            font-weight: 400;
            text-transform: uppercase;
        }
        
        /* ── CUSTOM DROPDOWN STYLES ── */
        div[data-baseweb="select"] > div {
            background-color: rgba(13, 28, 37, 0.6) !important;
            border: 1px solid var(--accent-muted) !important;
            color: var(--text-primary) !important;
            border-radius: 4px !important;
            min-height: 34px !important;
            padding: 2px !important;
        }
        div[data-baseweb="popover"] > div {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted) !important;
            border-radius: 4px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] span {
            color: var(--text-primary) !important;
            background-color: transparent !important;
        }
        li[role="option"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
        }
        li[role="option"]:hover {
            background-color: rgba(14, 124, 134, 0.2) !important;
        }

        /* ── SELECTED TAGS ── */
        span[data-baseweb="tag"] {
            background-color: rgba(14, 124, 134, 0.15) !important;
            border: 1px solid var(--accent-primary) !important;
            border-radius: 4px !important;
            margin: 2px !important;
        }
        span[data-baseweb="tag"] span {
            background-color: transparent !important;
            color: var(--accent-tertiary) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.75rem !important;
        }
        span[data-baseweb="tag"] svg {
            fill: var(--accent-tertiary) !important;
        }
        span[data-baseweb="tag"] span::before,
        span[data-baseweb="tag"] span::after {
            display: none !important;
        }
        span[data-baseweb="tag"] * {
            background-color: transparent !important;
            overflow: visible !important;
        }
        span[data-baseweb="tag"] > div:first-child {
            padding-left: 6px !important;
            padding-right: 6px !important;
        }

        /* ── METRICS & TABS ── */
        [data-testid="stMetric"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--accent-muted);
            border-radius: 4px !important;
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
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid #145D6D;
            margin-bottom: 16px;
        }
        .scout-table thead tr {
            background-color: #0D1C25;
            border-bottom: 1px solid #145D6D;
        }
        .scout-table thead th {
            padding: 12px 14px;
            text-align: left;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-secondary);
            border: none;
        }
        .scout-table tbody tr {
            border-bottom: 1px solid rgba(20, 93, 109, 0.3);
            background-color: transparent;
            transition: background 0.15s ease;
        }
        .scout-table tbody tr:last-child { border-bottom: none; }
        .scout-table tbody tr:hover { background-color: #132733; }
        .scout-table tbody td {
            padding: 12px 14px;
            color: var(--text-primary);
            vertical-align: middle;
        }
        .scout-table tbody td:first-child {
            font-weight: 600;
            color: var(--accent-secondary);
        }
        .scout-table tbody td:not(:first-child) {
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-tertiary);
        }
        .rank-badge {
            display: inline-block;
            width: 22px; height: 22px;
            line-height: 22px;
            text-align: center;
            border-radius: 2px;
            background: rgba(14, 124, 134, 0.15);
            border: 1px solid #0E7C86;
            color: var(--accent-secondary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            margin-right: 8px;
        }

        .tactical-header {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: var(--accent-secondary);
            border-bottom: 1px solid var(--accent-muted);
            padding-bottom: 6px;
            margin-bottom: 20px;
            margin-top: 40px;
            font-size: 0.95rem;
            letter-spacing: 2px;
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
            color: var(--text-primary);
            font-size: 0.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            border-bottom: 1px solid #145D6D;
            padding-bottom: 6px;
            margin-bottom: 16px;
        }
        .opt-summary {
            background-color: #041018;
            border: 1px solid #145D6D;
            border-radius: 4px;
            padding: 16px;
            margin-top: 20px;
        }
        .opt-summary-title {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .opt-summary-row {
            display: flex;
            justify-content: space-between;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        .opt-summary-row span.val {
            color: var(--accent-secondary);
            font-weight: 700;
        }
        .opt-summary-row .dots {
            flex-grow: 1;
            border-bottom: 1px dotted var(--accent-muted);
            margin: 0 8px 5px 8px;
            opacity: 0.5;
        }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_and_preprocess_data():
    try:
        url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
        df = pd.read_csv(url).fillna(0)
        
        df['player'] = df['player'].apply(
            lambda name: ''.join(
                c for c in unicodedata.normalize('NFD', str(name))
                if unicodedata.category(c) != 'Mn'
            )
        )
        df['player'] = df['player'] + ' (' + df['team'] + ')'
        df['is_gk'] = (df['saves'] > 0) | (df['savesParried'] > 0) | (df['punches'] > 0) | (df['highClaims'] > 0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def aggregate_player_stats(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    agg_dict = {col: 'sum' for col in numeric_cols}
    agg_dict.update({'team': 'first', 'league_name': 'first', 'is_gk': 'max'})
    for col in ['season_year', 'accuratePassesPercentage']:
        agg_dict.pop(col, None)
    
    agg_df = df.groupby('player').agg(agg_dict).reset_index()
        
    if len(agg_df) > 0:
        top_20_goals = agg_df.nlargest(20, 'goals')
        agg_df['goal_conversion'] = 0.0
        mask = agg_df['player'].isin(top_20_goals['player']) & (agg_df['totalShots'] > 0)
        agg_df.loc[mask, 'goal_conversion'] = np.clip((agg_df.loc[mask, 'goals'] / agg_df.loc[mask, 'totalShots']) * 100, 0, 100)
        
    if 'accuratePasses' in agg_df.columns and 'totalPasses' in agg_df.columns:
        agg_df['accuratePassesPercentage'] = np.where(
            agg_df['totalPasses'] > 0, np.clip((agg_df['accuratePasses'] / agg_df['totalPasses']) * 100, 0, 100), 0
        )
    elif 'accuratePassesPercentage' in df.columns:
        pass_acc = df.groupby('player')['accuratePassesPercentage'].mean().reset_index()
        agg_df = pd.merge(agg_df, pass_acc, on='player', how='left')
        
    return agg_df

@st.cache_data(show_spinner=False)
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
RADAR_COLORS = ['#00B4D8', '#0096C7', '#90BE6D', '#F9C74F', '#F98444', '#F94144', '#577590']
BAR_RANK_COLORS = ["#0E7C86", "#3B99A3", "#6EB6BD", "#A7D2D7", "#DCECEF"]

def apply_sofascore_radar_layout(fig, title):
    fig.update_layout(
        polar=dict(
            bgcolor="#041018",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#6C8594", family="JetBrains Mono", size=10)
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="rgba(255,255,255,0.1)",
                tickfont=dict(family="Inter", size=13, color="#F5F7FA", weight=700) 
            )
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F5F7FA"),
        title=dict(
            text=title,
            font=dict(family="Inter", size=16, color="#F5F7FA", weight=700), 
            y=0.96, x=0.04, xanchor='left', yanchor='top'
        ),
        height=480,
        legend=dict(
            orientation="v", yanchor="top", y=1, xanchor="left", x=1.15,
            font=dict(family="Inter", size=12, color="#A7BAC6")
        ),
        margin=dict(l=80, r=180, t=70, b=60)
    )
    return fig

def create_ranked_scouting_bar(df_subset, value_col, label_col, title):
    sorted_df = df_subset.nlargest(5, value_col)
    metrics = sorted_df[label_col].tolist()
    values = sorted_df[value_col].tolist()
    metrics_rev = list(reversed(metrics))
    values_rev = list(reversed(values))
    bar_colors_rev = [BAR_RANK_COLORS[len(metrics_rev) - 1 - i] for i in range(len(metrics_rev))]
    
    fig = go.Figure(data=[
        go.Bar(
            y=metrics_rev, x=values_rev, orientation='h',
            marker=dict(color=bar_colors_rev, line=dict(width=0)),
            text=[f'{v:.1f}' if isinstance(v, float) else f'{v}' for v in values_rev],
            textposition='auto',
            textfont=dict(family="JetBrains Mono", color="#030B12", weight="bold"),
            hovertemplate='<b style="font-family:Inter;color:#F5F7FA;">%{y}</b><br><span style="font-family:JetBrains Mono;color:#F5F7FA;">%{x:.2f}</span><extra></extra>'
        )
    ])
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter", size=16, color="#F5F7FA", weight=700), 
            y=0.96, x=0.0, xanchor='left', yanchor='top'
        ),
        xaxis=dict(
            title=dict(text="OUTPUT", font=dict(family="JetBrains Mono", size=10, color="#6C8594")),
            tickfont=dict(family="JetBrains Mono", color="#6C8594", size=10),
            gridcolor="#145D6D", gridwidth=0.5, zeroline=False
        ),
        yaxis=dict(tickfont=dict(family="Inter", color="#F5F7FA", size=12, weight=600)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
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

default_top_5 = [l for l in all_leagues if any(x in l for x in ['Premier League', 'LaLiga', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1'])]
if len(default_top_5) == 0: default_top_5 = all_leagues[:5]

st.sidebar.markdown("<div class='sidebar-title'>SCOUTING PARAMETERS</div>", unsafe_allow_html=True)

selected_leagues = st.sidebar.multiselect("COMPETITION", options=all_leagues, default=default_top_5, key="leagues_filter")
selected_seasons = st.sidebar.multiselect("SEASON", options=all_seasons, default=[all_seasons[-1]], key="seasons_filter")
selected_teams   = st.sidebar.multiselect("CLUB ROSTER", options=all_teams, default=None, key="teams_filter")

filtered_df = raw_df[(raw_df['league_name'].isin(selected_leagues)) & (raw_df['season_year'].isin(selected_seasons))]
if selected_teams:
    filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]

if filtered_df.empty:
    st.warning("NO DATA AVAILABLE FOR CURRENT FILTER COMBINATION.")
    st.stop()

player_agg_df   = aggregate_player_stats(filtered_df)
gk_agg_df       = player_agg_df[player_agg_df['is_gk'] == 1]
outfield_agg_df = player_agg_df[player_agg_df['is_gk'] == 0]

st.sidebar.markdown(f"""
    <div class="opt-summary">
        <div class="opt-summary-title">SCOUTING SUMMARY</div>
        <div class="opt-summary-row"><span>Records</span><div class="dots"></div><span class="val">{len(filtered_df):,}</span></div>
        <div class="opt-summary-row"><span>Players</span><div class="dots"></div><span class="val">{len(player_agg_df):,}</span></div>
        <div class="opt-summary-row"><span>Competitions</span><div class="dots"></div><span class="val">{len(selected_leagues):,}</span></div>
        <div class="opt-summary-row"><span>Seasons</span><div class="dots"></div><span class="val">{len(selected_seasons):,}</span></div>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# MAIN HUB
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div style="background-color: #030B12; padding: 30px 25px; border: 1px solid #145D6D; border-left: 6px solid #0E7C86; margin-bottom: 30px; border-radius: 4px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #6C8594; letter-spacing: 2px; margin-bottom: 10px;">PRO-LEVEL SCOUTING SUITE</div>
        <h1 style="font-family: 'Bebas Neue', sans-serif; font-size: 3.5rem; letter-spacing: 2px; color: #F5F7FA; margin: 0 0 10px 0; line-height: 1;">EUROPEAN FOOTBALL ANALYTICS HUB</h1>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["LEAGUE ANALYSIS", "CLUB TACTICAL PROFILES", "PLAYER COMPARISON"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: LEAGUE ANALYSIS
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='tactical-header'>ATTACKING PRODUCTION</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'goals', 'player', "Goals Registered"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'totalShots', 'player', "Shot Volume"), use_container_width=True)
    with col2:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'expectedGoals', 'player', "Expected Goals (xG)"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'goal_conversion', 'player', "Best Goal Conversion Rate"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>PLAYMAKING & CREATIVITY</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'keyPasses', 'player', "Key Passes"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'bigChancesCreated', 'player', "Big Chances Created"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'successfulDribbles', 'player', "Successful Dribbles"), use_container_width=True)
    with col2:
        top_creators_df = outfield_agg_df.nlargest(5, 'bigChancesCreated')
        max_drb  = max(top_creators_df['successfulDribbles'].max() if len(top_creators_df) else 1, 1)
        max_foul = max(top_creators_df.get('wasFouled', pd.Series([0])).max(), 1)
        max_bcc  = max(top_creators_df['bigChancesCreated'].max() if len(top_creators_df) else 1, 1)
        max_pf3  = max(top_creators_df.get('accurateFinalThirdPasses', pd.Series([0])).max(), 1)
        
        fig_pm_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_creators_df.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            drb  = p_row.get('successfulDribbles', 0)
            foul = p_row.get('wasFouled', 0)
            bcc  = p_row.get('bigChancesCreated', 0)
            pf3  = p_row.get('accurateFinalThirdPasses', 0)
            
            fig_pm_radar.add_trace(go.Scatterpolar(
                r=[(drb/max_drb*100), (foul/max_foul*100), (bcc/max_bcc*100), (pf3/max_pf3*100)],
                theta=['Successful Dribbles', 'Was Fouled', 'Big Chances Created', 'Passes In Final Third'],
                fill='toself', name=p_row['player'],
                line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_pm_radar, "Playmaking Radar"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>POSSESSION & PASSING</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'accuratePasses', 'player', "Passes Completed"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'touches', 'player', "Touches"), use_container_width=True)
    with col2:
        top_passing_df = outfield_agg_df.nlargest(5, 'accuratePasses')
        max_kp  = max(top_passing_df['keyPasses'].max() if len(top_passing_df) else 1, 1)
        max_ap  = max(top_passing_df['accuratePasses'].max() if len(top_passing_df) else 1, 1)
        max_alb = max(top_passing_df.get('accurateLongBalls', pd.Series([0])).max(), 1)
        max_tch = max(top_passing_df['touches'].max() if len(top_passing_df) else 1, 1)
        max_pob = max(top_passing_df.get('totalOppositionHalfPasses', pd.Series([0])).max(), 1)
        
        fig_pass_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_passing_df.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            kp  = p_row.get('keyPasses', 0)
            ap  = p_row.get('accuratePasses', 0)
            alb = p_row.get('accurateLongBalls', 0)
            tch = p_row.get('touches', 0)
            pob = p_row.get('totalOppositionHalfPasses', 0)
            
            fig_pass_radar.add_trace(go.Scatterpolar(
                r=[(kp/max_kp*100), (ap/max_ap*100), (alb/max_alb*100), (tch/max_tch*100), (pob/max_pob*100)],
                theta=['Key Passes', 'Accurate Passes', 'Accurate Long Balls', 'Touches', 'Passes In Opp Box'],
                fill='toself', name=p_row['player'],
                line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_pass_radar, "Passing Radar"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>DEFENSIVE ACTIONS</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'tackles', 'player', "Tackles"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'interceptions', 'player', "Interceptions"), use_container_width=True)
        st.plotly_chart(create_ranked_scouting_bar(outfield_agg_df, 'clearances', 'player', "Clearances"), use_container_width=True)
    with col2:
        top_defenders_df = outfield_agg_df.nlargest(5, 'tackles')
        max_tck = max(top_defenders_df['tackles'].max() if len(top_defenders_df) else 1, 1)
        max_int = max(top_defenders_df['interceptions'].max() if len(top_defenders_df) else 1, 1)
        max_clr = max(top_defenders_df['clearances'].max() if len(top_defenders_df) else 1, 1)
        max_aer = max(top_defenders_df['aerialDuelsWon'].max() if len(top_defenders_df) else 1, 1)
        max_rec = max(top_defenders_df.get('ballRecovery', pd.Series([1])).max(), 1)
        
        fig_def_radar = go.Figure()
        for idx, (_, p_row) in enumerate(top_defenders_df.iterrows()):
            color = RADAR_COLORS[idx % len(RADAR_COLORS)]
            rec = p_row.get('ballRecovery', 0)
            fig_def_radar.add_trace(go.Scatterpolar(
                r=[(p_row['tackles']/max_tck*100), (p_row['interceptions']/max_int*100),
                   (p_row['clearances']/max_clr*100), (p_row['aerialDuelsWon']/max_aer*100), (rec/max_rec*100)],
                theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ball Recovery'],
                fill='toself', name=p_row['player'],
                line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
            ))
        st.plotly_chart(apply_sofascore_radar_layout(fig_def_radar, "Defensive Radar"), use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='tactical-header'>GOALKEEPING</div>", unsafe_allow_html=True)
    if len(gk_agg_df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(gk_agg_df, 'saves', 'player', "Saves"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(gk_agg_df, 'cleanSheet', 'player', "Clean Sheets"), use_container_width=True)
        with col2:
            top_gk_df = gk_agg_df.nlargest(5, 'saves')
            max_sv  = max(top_gk_df['saves'].max() if len(top_gk_df) else 1, 1)
            max_cs  = max(top_gk_df['cleanSheet'].max() if len(top_gk_df) else 1, 1)
            max_alb = max(top_gk_df.get('accurateLongBalls', pd.Series([0])).max(), 1)
            max_svc = max(top_gk_df.get('savesCaught', pd.Series([0])).max(), 1)
            max_pen = max(top_gk_df.get('penaltySave', pd.Series([0])).max(), 1)
            
            fig_gk_radar = go.Figure()
            for idx, (_, p_row) in enumerate(top_gk_df.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                sv  = p_row.get('saves', 0)
                cs  = p_row.get('cleanSheet', 0)
                alb = p_row.get('accurateLongBalls', 0)
                svc = p_row.get('savesCaught', 0)
                pen = p_row.get('penaltySave', 0)
                
                fig_gk_radar.add_trace(go.Scatterpolar(
                    r=[(sv/max_sv*100), (cs/max_cs*100), (alb/max_alb*100), (svc/max_svc*100), (pen/max_pen*100)],
                    theta=['Saves', 'Clean Sheets', 'Accurate Long Balls', 'Saves Caught', 'Penalty Saves'],
                    fill='toself', name=p_row['player'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_gk_radar, "Goalkeeper Radar"), use_container_width=True)
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
        team_agg = aggregate_team_stats(filtered_df)

        st.markdown("<div class='tactical-header'>TEAM BENCHMARKS</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'goals', 'team', "Team Goals"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'totalShots', 'team', "Team Shots"), use_container_width=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'expectedGoals', 'team', "Team xG"), use_container_width=True)
            st.plotly_chart(create_ranked_scouting_bar(team_agg, 'bigChancesCreated', 'team', "Team Big Chances Created"), use_container_width=True)

        st.markdown("---")
        st.markdown("<div class='tactical-header'>TEAM PERFORMANCE RADARS</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            # ── PASSING RADAR ──
            top_passing_teams = team_agg.nlargest(5, 'accuratePasses')
            max_kp  = max(top_passing_teams['keyPasses'].max() if len(top_passing_teams) else 1, 1)
            max_ap  = max(top_passing_teams['accuratePasses'].max() if len(top_passing_teams) else 1, 1)
            max_alb = max(top_passing_teams.get('accurateLongBalls', pd.Series([1])).max(), 1)
            max_tch = max(top_passing_teams['touches'].max() if len(top_passing_teams) else 1, 1)
            max_pob = max(top_passing_teams.get('totalOppositionHalfPasses', pd.Series([1])).max(), 1)
            
            fig_team_pass = go.Figure()
            for idx, (_, t_row) in enumerate(top_passing_teams.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                kp  = t_row.get('keyPasses', 0)
                ap  = t_row.get('accuratePasses', 0)
                alb = t_row.get('accurateLongBalls', 0)
                tch = t_row.get('touches', 0)
                pob = t_row.get('totalOppositionHalfPasses', 0)
                
                fig_team_pass.add_trace(go.Scatterpolar(
                    r=[(kp/max_kp*100), (ap/max_ap*100), (alb/max_alb*100), (tch/max_tch*100), (pob/max_pob*100)],
                    theta=['Key Passes', 'Accurate Passes', 'Accurate Long Balls', 'Touches', 'Passes In Opp Box'],
                    fill='toself', name=t_row['team'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_pass, "Passing Radar (Top 5 Teams)"), use_container_width=True)

        with col2:
            # ── PLAYMAKING RADAR ──
            top_creative_teams = team_agg.nlargest(5, 'bigChancesCreated')
            max_drb  = max(top_creative_teams['successfulDribbles'].max() if len(top_creative_teams) else 1, 1)
            max_foul = max(top_creative_teams.get('wasFouled', pd.Series([1])).max(), 1)
            max_bcc  = max(top_creative_teams['bigChancesCreated'].max() if len(top_creative_teams) else 1, 1)
            max_pf3  = max(top_creative_teams.get('accurateFinalThirdPasses', pd.Series([1])).max(), 1)
            
            fig_team_pm = go.Figure()
            for idx, (_, t_row) in enumerate(top_creative_teams.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                drb  = t_row.get('successfulDribbles', 0)
                foul = t_row.get('wasFouled', 0)
                bcc  = t_row.get('bigChancesCreated', 0)
                pf3  = t_row.get('accurateFinalThirdPasses', 0)
                
                fig_team_pm.add_trace(go.Scatterpolar(
                    r=[(drb/max_drb*100), (foul/max_foul*100), (bcc/max_bcc*100), (pf3/max_pf3*100)],
                    theta=['Successful Dribbles', 'Was Fouled', 'Big Chances Created', 'Passes In Final Third'],
                    fill='toself', name=t_row['team'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_pm, "Playmaking Radar (Top 5 Teams)"), use_container_width=True)
            
        col3, col4 = st.columns(2)
        with col3:
            # ── DEFENSIVE RADAR ──
            top_def_teams = team_agg.nlargest(5, 'tackles')
            max_tck_t = max(top_def_teams['tackles'].max() if len(top_def_teams) else 1, 1)
            max_int_t = max(top_def_teams['interceptions'].max() if len(top_def_teams) else 1, 1)
            max_clr_t = max(top_def_teams['clearances'].max() if len(top_def_teams) else 1, 1)
            max_aer_t = max(top_def_teams['aerialDuelsWon'].max() if len(top_def_teams) else 1, 1)
            max_rec_t = max(top_def_teams.get('ballRecovery', pd.Series([1])).max(), 1)
            
            fig_team_def = go.Figure()
            for idx, (_, t_row) in enumerate(top_def_teams.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                rec = t_row.get('ballRecovery', 0)
                fig_team_def.add_trace(go.Scatterpolar(
                    r=[(t_row['tackles']/max_tck_t*100), (t_row['interceptions']/max_int_t*100),
                       (t_row['clearances']/max_clr_t*100), (t_row['aerialDuelsWon']/max_aer_t*100), (rec/max_rec_t*100)],
                    theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ball Recovery'],
                    fill='toself', name=t_row['team'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_def, "Defensive Radar (Top 5 Teams)"), use_container_width=True)
            
        with col4:
            # ── GK RADAR ──
            top_gk_teams = team_agg.nlargest(5, 'saves')
            max_sv     = max(top_gk_teams['saves'].max() if len(top_gk_teams) else 1, 1)
            max_cs     = max(top_gk_teams['cleanSheet'].max() if len(top_gk_teams) else 1, 1)
            max_alb_gk = max(top_gk_teams.get('accurateLongBalls', pd.Series([1])).max(), 1)
            max_svc    = max(top_gk_teams.get('savesCaught', pd.Series([1])).max(), 1)
            max_pen    = max(top_gk_teams.get('penaltySave', pd.Series([1])).max(), 1)
            
            fig_team_gk = go.Figure()
            for idx, (_, t_row) in enumerate(top_gk_teams.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                sv  = t_row.get('saves', 0)
                cs  = t_row.get('cleanSheet', 0)
                alb = t_row.get('accurateLongBalls', 0)
                svc = t_row.get('savesCaught', 0)
                pen = t_row.get('penaltySave', 0)
                
                fig_team_gk.add_trace(go.Scatterpolar(
                    r=[(sv/max_sv*100), (cs/max_cs*100), (alb/max_alb_gk*100), (svc/max_svc*100), (pen/max_pen*100)],
                    theta=['Saves', 'Clean Sheets', 'Accurate Long Balls', 'Saves Caught', 'Penalty Saves'],
                    fill='toself', name=t_row['team'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_gk, "Goalkeeper Radar (Top 5 Teams)"), use_container_width=True)

    else:
        team_df       = player_agg_df[player_agg_df['team'] == selected_team_tab2]
        team_outfield = team_df[team_df['is_gk'] == 0]
        team_gk       = team_df[team_df['is_gk'] == 1]

        st.markdown(f"<div class='tactical-header'>[{selected_team_tab2}] TEAM SCOUTING REPORT</div>", unsafe_allow_html=True)

        st.markdown("<p class='section-label'>ATTACK</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            att_df = team_outfield.nlargest(5, 'goals')[['player', 'goals', 'expectedGoals', 'totalShots']].copy()
            st.markdown(df_to_scout_table(att_df, {'player':'Player','goals':'Goals','expectedGoals':'xG','totalShots':'Shots'}), unsafe_allow_html=True)
        with col2:
            st.plotly_chart(create_ranked_scouting_bar(team_outfield, 'goals', 'player', "Goals"), use_container_width=True)

        st.markdown("<p class='section-label' style='margin-top:20px;'>CREATION</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            pm_df = team_outfield.nlargest(5, 'bigChancesCreated')[['player', 'keyPasses', 'bigChancesCreated', 'successfulDribbles']].copy()
            st.markdown(df_to_scout_table(pm_df, {'player':'Player','keyPasses':'Key Passes','bigChancesCreated':'BCC','successfulDribbles':'Dribbles'}), unsafe_allow_html=True)
        with col2:
            top_team_creators = team_outfield.nlargest(5, 'bigChancesCreated')
            max_drb  = max(top_team_creators['successfulDribbles'].max() if len(top_team_creators) else 1, 1)
            max_foul = max(top_team_creators.get('wasFouled', pd.Series([1])).max(), 1)
            max_bcc  = max(top_team_creators['bigChancesCreated'].max() if len(top_team_creators) else 1, 1)
            max_pf3  = max(top_team_creators.get('accurateFinalThirdPasses', pd.Series([1])).max(), 1)
            
            fig_team_pm_rad = go.Figure()
            for idx, (_, p_row) in enumerate(top_team_creators.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                drb  = p_row.get('successfulDribbles', 0)
                foul = p_row.get('wasFouled', 0)
                bcc  = p_row.get('bigChancesCreated', 0)
                pf3  = p_row.get('accurateFinalThirdPasses', 0)
                fig_team_pm_rad.add_trace(go.Scatterpolar(
                    r=[(drb/max_drb*100), (foul/max_foul*100), (bcc/max_bcc*100), (pf3/max_pf3*100)],
                    theta=['Successful Dribbles', 'Was Fouled', 'Big Chances Created', 'Passes In Final Third'],
                    fill='toself', name=p_row['player'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_pm_rad, "Playmaking Radar"), use_container_width=True)

        st.markdown("<p class='section-label' style='margin-top:20px;'>POSSESSION</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            pos_df = team_outfield.nlargest(5, 'accuratePasses')[['player', 'accuratePasses', 'touches', 'accuratePassesPercentage']].copy()
            pos_df['accuratePassesPercentage'] = pos_df['accuratePassesPercentage'].round(1)
            st.markdown(df_to_scout_table(pos_df, {'player':'Player','accuratePasses':'Passes','touches':'Touches','accuratePassesPercentage':'Pass Acc %'}), unsafe_allow_html=True)
        with col2:
            top_team_passers = team_outfield.nlargest(5, 'accuratePasses')
            max_kp  = max(top_team_passers['keyPasses'].max() if len(top_team_passers) else 1, 1)
            max_ap  = max(top_team_passers['accuratePasses'].max() if len(top_team_passers) else 1, 1)
            max_alb = max(top_team_passers.get('accurateLongBalls', pd.Series([1])).max(), 1)
            max_tch = max(top_team_passers['touches'].max() if len(top_team_passers) else 1, 1)
            max_pob = max(top_team_passers.get('totalOppositionHalfPasses', pd.Series([1])).max(), 1)
            
            fig_team_pass_rad = go.Figure()
            for idx, (_, p_row) in enumerate(top_team_passers.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                kp  = p_row.get('keyPasses', 0)
                ap  = p_row.get('accuratePasses', 0)
                alb = p_row.get('accurateLongBalls', 0)
                tch = p_row.get('touches', 0)
                pob = p_row.get('totalOppositionHalfPasses', 0)
                fig_team_pass_rad.add_trace(go.Scatterpolar(
                    r=[(kp/max_kp*100), (ap/max_ap*100), (alb/max_alb*100), (tch/max_tch*100), (pob/max_pob*100)],
                    theta=['Key Passes', 'Accurate Passes', 'Accurate Long Balls', 'Touches', 'Passes In Opp Box'],
                    fill='toself', name=p_row['player'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_pass_rad, "Passing Radar"), use_container_width=True)

        st.markdown("<p class='section-label' style='margin-top:20px;'>DEFENCE</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            def_df = team_outfield.nlargest(5, 'tackles')[['player', 'tackles', 'interceptions', 'clearances']].copy()
            st.markdown(df_to_scout_table(def_df, {'player':'Player','tackles':'Tackles','interceptions':'Interceptions','clearances':'Clearances'}), unsafe_allow_html=True)
        with col2:
            top_team_defenders = team_outfield.nlargest(5, 'tackles')
            max_tck = max(top_team_defenders['tackles'].max() if len(top_team_defenders) else 1, 1)
            max_int = max(top_team_defenders['interceptions'].max() if len(top_team_defenders) else 1, 1)
            max_clr = max(top_team_defenders['clearances'].max() if len(top_team_defenders) else 1, 1)
            max_aer = max(top_team_defenders['aerialDuelsWon'].max() if len(top_team_defenders) else 1, 1)
            max_rec = max(top_team_defenders.get('ballRecovery', pd.Series([1])).max(), 1)
            
            fig_team_def_rad = go.Figure()
            for idx, (_, p_row) in enumerate(top_team_defenders.iterrows()):
                color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                rec = p_row.get('ballRecovery', 0)
                fig_team_def_rad.add_trace(go.Scatterpolar(
                    r=[(p_row['tackles']/max_tck*100), (p_row['interceptions']/max_int*100),
                       (p_row['clearances']/max_clr*100), (p_row['aerialDuelsWon']/max_aer*100), (rec/max_rec*100)],
                    theta=['Tackles', 'Interceptions', 'Clearances', 'Aerial Duels', 'Ball Recovery'],
                    fill='toself', name=p_row['player'],
                    line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                ))
            st.plotly_chart(apply_sofascore_radar_layout(fig_team_def_rad, "Defensive Radar"), use_container_width=True)

        if len(team_gk) > 0:
            st.markdown("<p class='section-label' style='margin-top:20px;'>GOALKEEPING</p>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                gk_df = team_gk.nlargest(5, 'saves')[['player', 'saves', 'cleanSheet']].copy()
                st.markdown(df_to_scout_table(gk_df, {'player':'Player','saves':'Saves','cleanSheet':'Clean Sheets'}), unsafe_allow_html=True)
            with col2:
                top_team_gk = team_gk.nlargest(5, 'saves')
                max_sv  = max(top_team_gk['saves'].max() if len(top_team_gk) else 1, 1)
                max_cs  = max(top_team_gk['cleanSheet'].max() if len(top_team_gk) else 1, 1)
                max_alb = max(top_team_gk.get('accurateLongBalls', pd.Series([1])).max(), 1)
                max_svc = max(top_team_gk.get('savesCaught', pd.Series([1])).max(), 1)
                max_pen = max(top_team_gk.get('penaltySave', pd.Series([1])).max(), 1)
                
                fig_team_gk_rad = go.Figure()
                for idx, (_, p_row) in enumerate(top_team_gk.iterrows()):
                    color = RADAR_COLORS[idx % len(RADAR_COLORS)]
                    sv  = p_row.get('saves', 0)
                    cs  = p_row.get('cleanSheet', 0)
                    alb = p_row.get('accurateLongBalls', 0)
                    svc = p_row.get('savesCaught', 0)
                    pen = p_row.get('penaltySave', 0)
                    
                    fig_team_gk_rad.add_trace(go.Scatterpolar(
                        r=[(sv/max_sv*100), (cs/max_cs*100), (alb/max_alb*100), (svc/max_svc*100), (pen/max_pen*100)],
                        theta=['Saves', 'Clean Sheets', 'Accurate Long Balls', 'Saves Caught', 'Penalty Saves'],
                        fill='toself', name=p_row['player'],
                        line=dict(color=color, width=4), fillcolor=hex_to_rgba(color, 0.1)
                    ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_team_gk_rad, "Goalkeeper Radar"), use_container_width=True)

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
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #00B4D8; padding: 25px; margin-bottom: 20px; border-radius: 4px;'>
                    <div style='color: #00B4D8; font-family: JetBrains Mono; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // A ({p1_type})</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player1}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p1_data['team']} | {p1_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            p2_type = "GOALKEEPER" if p2_data['is_gk'] else "OUTFIELD"
            st.markdown(f"""
                <div style='background-color: var(--bg-card); border: 1px solid var(--accent-muted); border-left: 6px solid #90BE6D; padding: 25px; margin-bottom: 20px; border-radius: 4px;'>
                    <div style='color: #90BE6D; font-family: JetBrains Mono; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 8px;'>TARGET DOSSIER // B ({p2_type})</div>
                    <div style='color: var(--text-primary); font-family: Bebas Neue; font-size: 2.5rem; letter-spacing: 1.5px; margin-bottom: 5px; line-height: 1;'>{player2}</div>
                    <div style='color: var(--text-secondary); font-size: 0.9em; font-family: JetBrains Mono; text-transform: uppercase;'>{p2_data['team']} | {p2_data['league_name']}</div>
                </div>
            """, unsafe_allow_html=True)

        is_p1_gk = p1_data['is_gk']
        is_p2_gk = p2_data['is_gk']

        if not is_p1_gk and not is_p2_gk:
            # ── OFFENSE ─────────────────────────────
            st.markdown("<p class='section-label'>OFFENSE</p>", unsafe_allow_html=True)
            p1_conv = (p1_data['goals'] / p1_data['totalShots'] * 100) if p1_data['totalShots'] > 0 else 0
            p2_conv = (p2_data['goals'] / p2_data['totalShots'] * 100) if p2_data['totalShots'] > 0 else 0
            
            attacking_metrics = {
                'Goals Registered':    (int(p1_data['goals']),           int(p2_data['goals'])),
                'Assists':             (int(p1_data['assists']),           int(p2_data['assists'])),
                'Shot Volume':         (int(p1_data['totalShots']),       int(p2_data['totalShots'])),
                'Shots on Target':     (int(p1_data['shotsOnTarget']),    int(p2_data['shotsOnTarget'])),
                'Goal Conversion Rate (%)': (float(p1_conv),              float(p2_conv)),
                'Expected Goals (xG)': (float(p1_data['expectedGoals']),  float(p2_data['expectedGoals'])),
            }
            att_cmp_df = pd.DataFrame({'Metric': list(attacking_metrics.keys()),
                                       player1: [v[0] for v in attacking_metrics.values()],
                                       player2: [v[1] for v in attacking_metrics.values()]})
            st.markdown(df_to_plain_table(att_cmp_df), unsafe_allow_html=True)
            st.markdown("---")

            # ── PLAYMAKING ─────────────────────────────────
            st.markdown("<p class='section-label'>PLAYMAKING</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                p1_pf3  = p1_data.get('accurateFinalThirdPasses', 0)
                p2_pf3  = p2_data.get('accurateFinalThirdPasses', 0)
                p1_foul = p1_data.get('wasFouled', 0)
                p2_foul = p2_data.get('wasFouled', 0)
                
                playmaking_metrics = {
                    'Successful Dribbles':   (int(p1_data['successfulDribbles']),int(p2_data['successfulDribbles'])),
                    'Was Fouled':            (int(p1_foul), int(p2_foul)),
                    'Big Chances Created':   (int(p1_data['bigChancesCreated']), int(p2_data['bigChancesCreated'])),
                    'Passes In Final Third': (int(p1_pf3), int(p2_pf3))
                }
                pm_cmp_df = pd.DataFrame({'Metric': list(playmaking_metrics.keys()),
                                          player1: [v[0] for v in playmaking_metrics.values()],
                                          player2: [v[1] for v in playmaking_metrics.values()]})
                st.markdown(df_to_plain_table(pm_cmp_df), unsafe_allow_html=True)
            with col2:
                max_drb  = max(p1_data['successfulDribbles'], p2_data['successfulDribbles'],  1)
                max_foul = max(p1_foul, p2_foul, 1)
                max_bcc  = max(p1_data['bigChancesCreated'],  p2_data['bigChancesCreated'],  1)
                max_pf3  = max(p1_pf3, p2_pf3, 1)
                
                fig_playmaking = go.Figure()
                fig_playmaking.add_trace(go.Scatterpolar(
                    r=[(p1_data['successfulDribbles']/max_drb*100), (p1_foul/max_foul*100),
                       (p1_data['bigChancesCreated']/max_bcc*100), (p1_pf3/max_pf3*100)],
                    theta=['Successful Dribbles', 'Was Fouled', 'Big Chances Created', 'Passes In Final Third'],
                    fill='toself', name=player1,
                    line=dict(color='#00B4D8', width=4), fillcolor=hex_to_rgba('#00B4D8', 0.1)
                ))
                fig_playmaking.add_trace(go.Scatterpolar(
                    r=[(p2_data['successfulDribbles']/max_drb*100), (p2_foul/max_foul*100),
                       (p2_data['bigChancesCreated']/max_bcc*100), (p2_pf3/max_pf3*100)],
                    theta=['Successful Dribbles', 'Was Fouled', 'Big Chances Created', 'Passes In Final Third'],
                    fill='toself', name=player2,
                    line=dict(color='#90BE6D', width=4), fillcolor=hex_to_rgba('#90BE6D', 0.1)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_playmaking, "Playmaking Radar"), use_container_width=True)
            st.markdown("---")

            # ── PASSING PROFILE ─────────────────────────────
            st.markdown("<p class='section-label'>PASSING</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                p1_alb = p1_data.get('accurateLongBalls', 0)
                p2_alb = p2_data.get('accurateLongBalls', 0)
                p1_pob = p1_data.get('totalOppositionHalfPasses', 0)
                p2_pob = p2_data.get('totalOppositionHalfPasses', 0)
                
                passing_metrics = {
                    'Key Passes':               (int(p1_data['keyPasses']),      int(p2_data['keyPasses'])),
                    'Accurate Passes':          (int(p1_data['accuratePasses']), int(p2_data['accuratePasses'])),
                    'Accurate Long Balls':      (int(p1_alb),                    int(p2_alb)),
                    'Touches':                  (int(p1_data['touches']),        int(p2_data['touches'])),
                    'Passes In Opposition Box': (int(p1_pob),                    int(p2_pob)),
                }
                pass_cmp_df = pd.DataFrame({'Metric': list(passing_metrics.keys()),
                                            player1: [v[0] for v in passing_metrics.values()],
                                            player2: [v[1] for v in passing_metrics.values()]})
                st.markdown(df_to_plain_table(pass_cmp_df), unsafe_allow_html=True)
            with col2:
                max_kp  = max(p1_data['keyPasses'],      p2_data['keyPasses'],      1)
                max_ap  = max(p1_data['accuratePasses'], p2_data['accuratePasses'], 1)
                max_alb = max(p1_alb, p2_alb, 1)
                max_tch = max(p1_data['touches'],        p2_data['touches'],        1)
                max_pob = max(p1_pob, p2_pob, 1)
                
                fig_passing = go.Figure()
                fig_passing.add_trace(go.Scatterpolar(
                    r=[(p1_data['keyPasses']/max_kp*100), (p1_data['accuratePasses']/max_ap*100),
                       (p1_alb/max_alb*100), (p1_data['touches']/max_tch*100), (p1_pob/max_pob*100)],
                    theta=['Key Passes', 'Accurate Passes', 'Accurate Long Balls', 'Touches', 'Passes In Opp Box'],
                    fill='toself', name=player1,
                    line=dict(color='#00B4D8', width=4), fillcolor=hex_to_rgba('#00B4D8', 0.1)
                ))
                fig_passing.add_trace(go.Scatterpolar(
                    r=[(p2_data['keyPasses']/max_kp*100), (p2_data['accuratePasses']/max_ap*100),
                       (p2_alb/max_alb*100), (p2_data['touches']/max_tch*100), (p2_pob/max_pob*100)],
                    theta=['Key Passes', 'Accurate Passes', 'Accurate Long Balls', 'Touches', 'Passes In Opp Box'],
                    fill='toself', name=player2,
                    line=dict(color='#90BE6D', width=4), fillcolor=hex_to_rgba('#90BE6D', 0.1)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_passing, "Passing Radar"), use_container_width=True)
            st.markdown("---")

            # ── DEFENSIVE ACTIONS ─────────────────────────────────
            st.markdown("<p class='section-label'>DEFENCE</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                rec1 = p1_data.get('ballRecovery', 0)
                rec2 = p2_data.get('ballRecovery', 0)
                defence_metrics = {
                    'Tackles Won':     (int(p1_data['tackles']),        int(p2_data['tackles'])),
                    'Interceptions':   (int(p1_data['interceptions']),  int(p2_data['interceptions'])),
                    'Clearances':      (int(p1_data['clearances']),     int(p2_data['clearances'])),
                    'Aerial Duels Won':(int(p1_data['aerialDuelsWon']), int(p2_data['aerialDuelsWon'])),
                    'Ball Recovery':   (int(rec1), int(rec2)),
                }
                def_cmp_df = pd.DataFrame({'Metric': list(defence_metrics.keys()),
                                           player1: [v[0] for v in defence_metrics.values()],
                                           player2: [v[1] for v in defence_metrics.values()]})
                st.markdown(df_to_plain_table(def_cmp_df), unsafe_allow_html=True)
            with col2:
                max_tck = max(p1_data['tackles'],        p2_data['tackles'],        1)
                max_int = max(p1_data['interceptions'],  p2_data['interceptions'],  1)
                max_clr = max(p1_data['clearances'],     p2_data['clearances'],     1)
                max_aer = max(p1_data['aerialDuelsWon'], p2_data['aerialDuelsWon'], 1)
                max_rec = max(rec1, rec2, 1)
                
                fig_defence = go.Figure()
                fig_defence.add_trace(go.Scatterpolar(
                    r=[(p1_data['tackles']/max_tck*100), (p1_data['interceptions']/max_int*100),
                       (p1_data['clearances']/max_clr*100), (p1_data['aerialDuelsWon']/max_aer*100), (rec1/max_rec*100)],
                    theta=['Tackles','Interceptions','Clearances','Aerial Duels','Ball Recovery'],
                    fill='toself', name=player1,
                    line=dict(color='#00B4D8', width=4), fillcolor=hex_to_rgba('#00B4D8', 0.1)
                ))
                fig_defence.add_trace(go.Scatterpolar(
                    r=[(p2_data['tackles']/max_tck*100), (p2_data['interceptions']/max_int*100),
                       (p2_data['clearances']/max_clr*100), (p2_data['aerialDuelsWon']/max_aer*100), (rec2/max_rec*100)],
                    theta=['Tackles','Interceptions','Clearances','Aerial Duels','Ball Recovery'],
                    fill='toself', name=player2,
                    line=dict(color='#90BE6D', width=4), fillcolor=hex_to_rgba('#90BE6D', 0.1)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_defence, "Defensive Radar"), use_container_width=True)

        elif is_p1_gk and is_p2_gk:
            st.markdown("<p class='section-label'>GOALKEEPING</p>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                p1_alb = p1_data.get('accurateLongBalls', 0)
                p2_alb = p2_data.get('accurateLongBalls', 0)
                p1_svc = p1_data.get('savesCaught', 0)
                p2_svc = p2_data.get('savesCaught', 0)
                p1_pen = p1_data.get('penaltySave', 0)
                p2_pen = p2_data.get('penaltySave', 0)

                gk_metrics = {
                    'Saves':               (int(p1_data['saves']),           int(p2_data['saves'])),
                    'Clean Sheets':        (int(p1_data['cleanSheet']),      int(p2_data['cleanSheet'])),
                    'Accurate Long Balls': (int(p1_alb),                     int(p2_alb)),
                    'Saves Caught':        (int(p1_svc),                     int(p2_svc)),
                    'Penalty Saves':       (int(p1_pen),                     int(p2_pen))
                }
                gk_cmp_df = pd.DataFrame({'Metric': list(gk_metrics.keys()),
                                          player1: [v[0] for v in gk_metrics.values()],
                                          player2: [v[1] for v in gk_metrics.values()]})
                st.markdown(df_to_plain_table(gk_cmp_df), unsafe_allow_html=True)
            with col2:
                max_sv  = max(p1_data['saves'],      p2_data['saves'],      1)
                max_cs  = max(p1_data['cleanSheet'], p2_data['cleanSheet'], 1)
                max_alb = max(p1_alb, p2_alb, 1)
                max_svc = max(p1_svc, p2_svc, 1)
                max_pen = max(p1_pen, p2_pen, 1)
                
                fig_gk = go.Figure()
                fig_gk.add_trace(go.Scatterpolar(
                    r=[(p1_data['saves']/max_sv*100), (p1_data['cleanSheet']/max_cs*100),
                       (p1_alb/max_alb*100), (p1_svc/max_svc*100), (p1_pen/max_pen*100)],
                    theta=['Saves', 'Clean Sheets', 'Accurate Long Balls', 'Saves Caught', 'Penalty Saves'],
                    fill='toself', name=player1,
                    line=dict(color='#00B4D8', width=4), fillcolor=hex_to_rgba('#00B4D8', 0.1)
                ))
                fig_gk.add_trace(go.Scatterpolar(
                    r=[(p2_data['saves']/max_sv*100), (p2_data['cleanSheet']/max_cs*100),
                       (p2_alb/max_alb*100), (p2_svc/max_svc*100), (p2_pen/max_pen*100)],
                    theta=['Saves', 'Clean Sheets', 'Accurate Long Balls', 'Saves Caught', 'Penalty Saves'],
                    fill='toself', name=player2,
                    line=dict(color='#90BE6D', width=4), fillcolor=hex_to_rgba('#90BE6D', 0.1)
                ))
                st.plotly_chart(apply_sofascore_radar_layout(fig_gk, "Goalkeeper Radar"), use_container_width=True)
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
        <div style='margin-top: 10px; color: #6C8594;'>TACTICAL RECRUITMENT INTELLIGENCE</div>
    </div>
""", unsafe_allow_html=True)
