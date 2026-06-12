# ─────────────────────────────────────────────────────────────────────────────
#   FOOTBALL ANALYTICS – EUROPEAN LEAGUES
#   Streamlit + Plotly – professional dark theme (OPTA / StatsBomb style)
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
#   PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ Football Analytics – European Leagues",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#   GLOBAL COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
PALETTE = {
    "bg_primary": "#0f1419",
    "bg_secondary": "#151d2a",
    "bg_tertiary": "#1e2738",
    "accent_1": "#2dd4bf",   # petrol‑blue / teal
    "accent_2": "#0ea5e9",   # bright teal
    "accent_3": "#06b6d4",   # lighter teal
    "orange": "#ff6b35",
    "green": "#00d084",
    "red": "#ef4444",
    "text_primary": "#ffffff",
    "text_secondary": "#d4d9e3",
    "text_muted": "#8b92a3",
}
# -------------------------------------------------------------------------
#   CSS – professional dark theme (inspired by OPTA / StatsBomb)
# -------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        :root {{
            --bg-primary: {PALETTE["bg_primary"]};
            --bg-secondary: {PALETTE["bg_secondary"]};
            --bg-tertiary: {PALETTE["bg_tertiary"]};
            --accent-1: {PALETTE["accent_1"]};
            --accent-2: {PALETTE["accent_2"]};
            --accent-3: {PALETTE["accent_3"]};
            --orange: {PALETTE["orange"]};
            --green: {PALETTE["green"]};
            --red: {PALETTE["red"]};
            --text-primary: {PALETTE["text_primary"]};
            --text-secondary: {PALETTE["text_secondary"]};
            --text-muted: {PALETTE["text_muted"]};
        }}

        * {{margin:0; padding:0;}}
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: var(--bg-secondary) !important;
            border-right: 1px solid rgba(45,212,191,0.1);
        }}

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: var(--accent-1);
            border-bottom: 2px solid var(--accent-1);
        }}

        .stMetric {{background-color: var(--bg-tertiary); border-left:3px solid var(--accent-1);}}
        .stMetricLabel {{color: var(--text-muted);}}
        .stMetricValue {{color: var(--accent-1);}}

        .header-container {{
            background: linear-gradient(135deg,var(--bg-secondary) 0%,var(--bg-tertiary) 50%,#0d1117 100%);
            padding:48px 40px;
            margin:-60px -40px 40px -40px;
            border-bottom:2px solid var(--accent-1);
            border-radius:0 0 16px 16px;
        }}
        .header-eyebrow {{color:var(--accent-1);font-weight:700;letter-spacing:1px;}}
        .header-subtitle {{color:var(--text-muted);font-size:.95em;}}
        .section-header {{color:var(--text-primary);font-size:1.6em;font-weight:800;}}
        .section-eyebrow {{color:var(--accent-1);font-size:.75em;font-weight:800;letter-spacing:1.5px;}}
        .section-divider {{height:1px;background:linear-gradient(90deg,rgba(45,212,191,0.2),transparent);margin:32px 0;}}
        .subsection-header {{color:var(--text-primary);font-size:1.2em;font-weight:700;margin:24px 0 16px;}}
        .stat-card {{background:{PALETTE["bg_tertiary"]};border:1px solid rgba(45,212,191,0.15);
                     border-radius:8px;padding:16px;transition:all .3s;}}
        .stat-card:hover {{border-color:rgba(45,212,191,0.3);background:#232f3d;}}
        .sidebar-header {{color:var(--accent-1);font-weight:800;letter-spacing:1px;}}
        [data-baseweb="input"], .stSelectbox > div, .stMultiSelect {{
            background:{PALETTE["bg_tertiary"]} !important;
            border:1px solid rgba(45,212,191,0.2) !important;
            border-radius:6px !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
#   DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_data() -> pd.DataFrame:
    """Load the CSV from the public GitHub repo."""
    url = "https://raw.githubusercontent.com/Armaan7781/FootballAnalyticsApp/main/Historical%20Data.csv"
    df = pd.read_csv(url).fillna(0)
    return df


df = load_data()
if df.empty:
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
#   HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def identify_goalkeepers(df: pd.DataFrame) -> pd.DataFrame:
    """Goalkeepers are identified by any non‑zero goalkeeper‑specific stat."""
    gk = df[
        (df["saves"] > 0)
        | (df["savesParried"] > 0)
        | (df["punches"] > 0)
        | (df["highClaims"] > 0)
    ].copy()
    return gk


def big_chance_conversion(goals: float, big_chances: float) -> float:
    """% of big chances that resulted in a goal."""
    return (goals / big_chances) * 100 if big_chances else 0.0


def top5_metric_per_league(
    df: pd.DataFrame, metric: str, n: int = 5
) -> dict[str, float]:
    """Sum of the *metric* for the top‑n players in each league."""
    out = {}
    for league in df["league_name"].unique():
        sub = df[df["league_name"] == league]
        out[league] = sub.nlargest(n, metric)[metric].sum()
    return out


def top5_metric_overall(df: pd.DataFrame, metric: str, n: int = 5) -> float:
    """Sum of the *metric* for the top‑n players across the whole filtered set."""
    return df.nlargest(n, metric)[metric].sum()


def gradient_color(value: float, max_val: float, palette: list[str]) -> str:
    """Return a colour from *palette* based on normalised *value*."""
    if max_val == 0:
        return palette[0]
    norm = value / max_val
    idx = int(norm * (len(palette) - 1))
    return palette[idx]


# -------------------------------------------------------------------------
#   BAR CHART (light → dark gradient)
# -------------------------------------------------------------------------
def bar_chart(
    data: dict,
    title: str,
    metric_type: str = "attack",
    eyebrow: str = "",
) -> go.Figure:
    """Horizontal bar chart with a gradient that matches the metric type."""
    # ---- colour palettes per metric type -----------------------------------
    palettes = {
        "attack": ["#ffffff", "#e0f7f6", "#a0e4df", "#60cec5", "#2dd4bf", "#1da39a"],
        "playmaking": ["#ffffff", "#e0f2fe", "#a0e2ff", "#60d0ff", "#0ea5e9", "#0284c7"],
        "passing": ["#ffffff", "#ddf4f5", "#aae5e9", "#77d6dd", "#44c7d1", "#1db5c0"],
        "defense": ["#ffffff", "#e8e8ff", "#c4c4ff", "#a0a0ff", "#7c7cff", "#5858ff"],
        "goalkeeper": ["#ffffff", "#ffe8d6", "#ffd4ad", "#ffc084", "#ffac5b", "#ff9832"],
    }
    palette = palettes.get(metric_type, palettes["attack"])

    # ---- build figure ----------------------------------------------------
    metrics = list(data.keys())
    values = list(data.values())
    max_val = max(values) if values else 1

    colors = [gradient_color(v, max_val, palette) for v in values]

    fig = go.Figure(
        data=[
            go.Bar(
                y=metrics,
                x=values,
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"{v:.1f}" if v % 1 else f"{int(v)}" for v in values],
                textposition="auto",
                textfont=dict(size=12, color=PALETTE["bg_tertiary"]),
                hovertemplate="<b>%{y}</b><br>%{x:.2f}<extra></extra>",
                showlegend=False,
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=14, color=PALETTE["text_primary"]),
            x=0,
            xanchor="left",
        ),
        xaxis=dict(showgrid=True, gridcolor="rgba(45,212,191,0.05)", color=PALETTE["text_muted"]),
        yaxis=dict(showgrid=False, color=PALETTE["text_primary"], tickfont=dict(size=11)),
        template="plotly_dark",
        height=350,
        paper_bgcolor=PALETTE["bg_tertiary"],
        plot_bgcolor=PALETTE["bg_secondary"],
        margin=dict(l=180, r=20, t=20, b=20),
    )
    return fig


# -------------------------------------------------------------------------
#   RADAR CHART (re‑used for play‑making, defence & goal‑keeping)
# -------------------------------------------------------------------------
def radar_chart(
    data: dict[str, list[float]],
    title: str,
    metric_type: str = "playmaking",
) -> go.Figure:
    """Professional radar chart – each series gets a distinct colour."""
    # colour cycle – keep it consistent with the bar charts
    colours = [
        PALETTE["accent_1"],
        PALETTE["accent_2"],
        PALETTE["accent_3"],
        PALETTE["orange"],
        PALETTE["green"],
    ]

    fig = go.Figure()
    for i, (name, values) in enumerate(data.items()):
        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=list(data[name].keys()) if isinstance(values, dict) else list(data[name]),
                fill="toself",
                name=name,
                line_color=colours[i % len(colours)],
                fillcolor=f"rgba(45,212,191,0.15)",
                hovertemplate="<b>%{name}</b><br>%{theta}: %{r:.1f}<extra></extra>",
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(45,212,191,0.1)",
                tickfont=dict(color=PALETTE["text_muted"], size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(45,212,191,0.1)",
                tickfont=dict(color=PALETTE["text_primary"], size=11),
            ),
        ),
        template="plotly_dark",
        title=dict(text=f"<b>{title}</b>", font=dict(size=14, color=PALETTE["text_primary"]), x=0, xanchor="left"),
        height=470,
        paper_bgcolor=PALETTE["bg_tertiary"],
        plot_bgcolor=PALETTE["bg_secondary"],
        legend=dict(x=1.05, y=1, bgcolor="rgba(0,0,0,0)"),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#   SIDEBAR – FILTERS
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("<span class='sidebar-header'>🔍 FILTERS</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

all_leagues = sorted(df["league_name"].unique())
all_seasons = sorted(df["season_year"].unique())
all_teams   = sorted(df["team"].unique())
all_players = sorted(df["player"].unique())

selected_leagues = st.sidebar.multiselect(
    "🏆 Leagues",
    options=all_leagues,
    default=all_leagues[:3],
    key="leagues",
)

selected_seasons = st.sidebar.multiselect(
    "📅 Seasons",
    options=all_seasons,
    default=[all_seasons[-1]],
    key="seasons",
)

selected_teams = st.sidebar.multiselect(
    "🏢 Teams",
    options=all_teams,
    default=None,
    key="teams",
)

# Apply filters ------------------------------------------------------------
filtered = df[
    (df["league_name"].isin(selected_leagues))
    & (df["season_year"].isin(selected_seasons))
]

if selected_teams:
    filtered = filtered[filtered["team"].isin(selected_teams)]

filtered_players = sorted(filtered["player"].unique())

# -------------------------------------------------------------------------
#   HEADER
# -------------------------------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <div class="header-eyebrow">⚽ EUROPEAN FOOTBALL INTELLIGENCE</div>
        <h1>League Analytics Dashboard</h1>
        <div class="header-subtitle">
            In‑depth performance metrics across Europe’s top five leagues & continental cups (2020‑2025)
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
#   TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_league, tab_club, tab_player = st.tabs(
    ["🏆 LEAGUE ANALYSIS", "🏢 CLUB COMPARISON", "👥 PLAYER MATCHUP"]
)

# -------------------------------------------------------------------------
#   TAB 1 – LEAGUE ANALYSIS (TOP‑5‑PLAYER METRICS)
# -------------------------------------------------------------------------
with tab_league:
    st.markdown(
        """
        <span class="section-eyebrow">⚽ PERFORMANCE BREAKDOWN</span>
        <h2 class="section-header">League‑wide Metrics (Top‑5 Players)</h2>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------
    #   Overall KPI row (sum of top‑5 across all selected leagues)
    # -----------------------------------------------------------------
    col = st.columns(7)
    with col[0]:
        st.metric("⚽ Goals", f"{top5_metric_overall(filtered, 'goals'):.0f}")
    with col[1]:
        st.metric("📈 xG", f"{top5_metric_overall(filtered, 'expectedGoals'):.1f}")
    with col[2]:
        st.metric("🎯 Big Chances", f"{top5_metric_overall(filtered, 'bigChancesCreated'):.0f}")
    with col[3]:
        st.metric("❌ Missed", f"{top5_metric_overall(filtered, 'bigChancesMissed'):.0f}")
    with col[4]:
        st.metric("🛡️ Tackles", f"{top5_metric_overall(filtered, 'tackles'):.0f}")
    with col[5]:
        st.metric("🙌 Saves", f"{top5_metric_overall(filtered, 'saves'):.0f}")
    with col[6]:
        st.metric("🟩 Clean Sheets", f"{top5_metric_overall(filtered, 'cleanSheet'):.0f}")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   ATTACK – BAR CHARTS
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">⚔️ ATTACK</span>
        <h2 class="section-header">Scoring & Finishing</h2>
        """,
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        goals = top5_metric_per_league(filtered, "goals")
        st.plotly_chart(bar_chart(goals, "Goals – Top 5 Players", "attack"), use_container_width=True)

    with col_b:
        xg = top5_metric_per_league(filtered, "expectedGoals")
        st.plotly_chart(bar_chart(xg, "Expected Goals – Top 5 Players", "attack"), use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        shots = top5_metric_per_league(filtered, "totalShots")
        st.plotly_chart(bar_chart(shots, "Shots – Top 5 Players", "attack"), use_container_width=True)

    with col_d:
        # Big‑chance conversion = goals / big chances created
        conversion = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            top5 = league_df.nlargest(5, "goals")
            conv = big_chance_conversion(top5["goals"].sum(), top5["bigChancesCreated"].sum())
            conversion[league] = conv
        st.plotly_chart(bar_chart(conversion, "Big‑Chance Conversion % – Top 5", "attack"), use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   PLAYMAKING – RADAR
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">🎯 PLAYMAKING</span>
        <h2 class="section-header">Chance Creation & Progression</h2>
        """,
        unsafe_allow_html=True,
    )
    playmaking = {}
    # Normalise each metric against the absolute maximum in the filtered set
    max_bcc = filtered["bigChancesCreated"].max() or 1
    max_kp = filtered["keyPasses"].max() or 1
    max_drb = filtered["successfulDribbles"].max() or 1

    for league in selected_leagues:
        league_df = filtered[filtered["league_name"] == league]
        top5 = league_df.nlargest(5, "bigChancesCreated")
        playmaking[league] = [
            top5["bigChancesCreated"].sum() / max_bcc * 100,
            top5["keyPasses"].sum() / max_kp * 100,
            top5["successfulDribbles"].sum() / max_drb * 100,
        ]

    st.plotly_chart(
        radar_chart(
            playmaking,
            "Playmaking – Top 5 Players per League",
            metric_type="playmaking",
        ),
        use_container_width=True,
    )
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   PASSING – BAR CHARTS
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">📲 PASSING</span>
        <h2 class="section-header">Distribution & Accuracy</h2>
        """,
        unsafe_allow_html=True,
    )
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        acc_pass = top5_metric_per_league(filtered, "accuratePasses")
        st.plotly_chart(bar_chart(acc_pass, "Accurate Passes – Top 5", "passing"), use_container_width=True)

    with col_p2:
        touches = top5_metric_per_league(filtered, "touches")
        st.plotly_chart(bar_chart(touches, "Touches – Top 5", "passing"), use_container_width=True)

    col_p3, col_p4 = st.columns(2)
    with col_p3:
        # Pass accuracy % – we take the mean of the top‑5 players
        acc_pct = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            top5 = league_df.nlargest(5, "accuratePassesPercentage")
            acc_pct[league] = top5["accuratePassesPercentage"].mean()
        st.plotly_chart(bar_chart(acc_pct, "Pass Accuracy % – Top 5", "passing"), use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   DEFENCE – RADAR
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">🛡️ DEFENCE</span>
        <h2 class="section-header">Defensive Actions</h2>
        """,
        unsafe_allow_html=True,
    )
    defence = {}
    max_tck = filtered["tackles"].max() or 1
    max_int = filtered["interceptions"].max() or 1
    max_clr = filtered["clearances"].max() or 1
    max_aer = filtered["aerialDuelsWon"].max() or 1
    max_grd = filtered["groundDuelsWon"].max() or 1

    for league in selected_leagues:
        league_df = filtered[filtered["league_name"] == league]
        top5 = league_df.nlargest(5, "tackles")
        defence[league] = [
            top5["tackles"].sum() / max_tck * 100,
            top5["interceptions"].sum() / max_int * 100,
            top5["clearances"].sum() / max_clr * 100,
            top5["aerialDuelsWon"].sum() / max_aer * 100,
            top5["groundDuelsWon"].sum() / max_grd * 100,
        ]

    st.plotly_chart(
        radar_chart(defence, "Defence – Top 5 Players per League", metric_type="defense"),
        use_container_width=True,
    )
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   GOALKEEPING – BAR CHARTS
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">🥅 GOALKEEPING</span>
        <h2 class="section-header">Shot‑stopping & Distribution</h2>
        """,
        unsafe_allow_html=True,
    )
    col_gk1, col_gk2 = st.columns(2)
    with col_gk1:
        saves = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            gk = identify_goalkeepers(league_df)
            saves[league] = gk.nlargest(5, "saves")["saves"].sum()
        st.plotly_chart(bar_chart(saves, "Saves – Top 5 Keepers", "goalkeeper"), use_container_width=True)

    with col_gk2:
        cs = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            gk = identify_goalkeepers(league_df)
            cs[league] = gk.nlargest(5, "cleanSheet")["cleanSheet"].sum()
        st.plotly_chart(bar_chart(cs, "Clean Sheets – Top 5 Keepers", "goalkeeper"), use_container_width=True)

    col_gk3, col_gk4 = st.columns(2)
    with col_gk3:
        claims = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            gk = identify_goalkeepers(league_df)
            claims[league] = gk.nlargest(5, "highClaims")["highClaims"].sum()
        st.plotly_chart(bar_chart(claims, "High Claims – Top 5 Keepers", "goalkeeper"), use_container_width=True)

    with col_gk4:
        errors = {}
        for league in selected_leagues:
            league_df = filtered[filtered["league_name"] == league]
            gk = identify_goalkeepers(league_df)
            errors[league] = gk.nlargest(5, "errorLeadToGoal")["errorLeadToGoal"].sum()
        st.plotly_chart(bar_chart(errors, "Errors → Goals – Top 5 Keepers", "goalkeeper"), use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # -----------------------------------------------------------------
    #   TOP PERFORMERS TABLES (per league)
    # -----------------------------------------------------------------
    st.markdown(
        """
        <span class="section-eyebrow">🏅 RANKINGS</span>
        <h2 class="section-header">Elite Performers (Top 5 per league)</h2>
        """,
        unsafe_allow_html=True,
    )
    for league in selected_leagues:
        sub = filtered[filtered["league_name"] == league]
        st.markdown(f"<h3 class='subsection-header'>{league}</h3>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("**⚔️ Top Scorers**")
            top_scorers = sub.nlargest(5, "goals")[["player", "team", "goals", "assists", "totalShots"]]
            top_scorers.columns = ["Player", "Team", "Goals", "Assists", "Shots"]
            st.dataframe(top_scorers, use_container_width=True, hide_index=True)

            st.markdown("**🎯 Top Creators**")
            top_creators = sub.nlargest(5, "bigChancesCreated")[
                ["player", "team", "bigChancesCreated", "keyPasses", "successfulDribbles"]
            ]
            top_creators.columns = ["Player", "Team", "Chances", "Key Passes", "Dribbles"]
            st.dataframe(top_creators, use_container_width=True, hide_index=True)

        with col_right:
            st.markdown("**📲 Top Passers**")
            top_passers = sub.nlargest(5, "accuratePasses")[
                ["player", "team", "accuratePasses", "touches", "accuratePassesPercentage"]
            ]
            top_passers.columns = ["Player", "Team", "Passes", "Touches", "Acc %"]
            top_passers["Acc %"] = top_passers["Acc %"].round(1)
            st.dataframe(top_passers, use_container_width=True, hide_index=True)

            st.markdown("**🛡️ Top Defenders**")
            top_def = sub.nlargest(5, "tackles")[["player", "team", "tackles", "interceptions", "clearances"]]
            top_def.columns = ["Player", "Team", "Tackles", "Intercepts", "Clears"]
            st.dataframe(top_def, use_container_width=True, hide_index=True)

        # Goalkeepers (if any)
        gk_sub = identify_goalkeepers(sub)
        if not gk_sub.empty:
            st.markdown("**🥅 Top Keepers**")
            top_gk = gk_sub.nlargest(5, "saves")[["player", "team", "saves", "cleanSheet", "highClaims"]]
            top_gk.columns = ["Player", "Team", "Saves", "Clean Sheets", "Claims"]
            st.dataframe(top_gk, use_container_width=True, hide_index=True)

        st.markdown("---")

# -------------------------------------------------------------------------
#   TAB 2 – CLUB COMPARISON (same logic, refined style)
# -------------------------------------------------------------------------
with tab_club:
    st.markdown(
        """
        <span class="section-eyebrow">🏢 CLUB COMPARISON</span>
        <h2 class="section-header">Institutional Performance</h2>
        """,
        unsafe_allow_html=True,
    )
    club_choice = st.selectbox(
        "Select a club (or “All Clubs” for aggregate view)",
        ["All Clubs"] + sorted(filtered["team"].unique()),
    )
    if club_choice == "All Clubs":
        club_df = filtered
        st.info("📊 Aggregated metrics across all clubs – pick a specific club for a deep dive.")
    else:
        club_df = filtered[filtered["team"] == club_choice]
        st.markdown(
            f"<div class='stat-card'><b>{club_choice}</b> | {club_df['league_name'].iloc[0]}</div>",
            unsafe_allow_html=True,
        )

    # KPI row (same as in league tab but for the club)
    cols = st.columns(7)
    with cols[0]:
        st.metric("⚽ Goals", f"{club_df['goals'].sum():.0f}")
    with cols[1]:
        st.metric("📈 xG", f"{club_df['expectedGoals'].sum():.1f}")
    with cols[2]:
        st.metric("🎯 Chances", f"{club_df['bigChancesCreated'].sum():.0f}")
    with cols[3]:
        st.metric("❌ Missed", f"{club_df['bigChancesMissed'].sum():.0f}")
    with cols[4]:
        st.metric("🛡️ Tackles", f"{club_df['tackles'].sum():.0f}")
    with cols[5]:
        st.metric("🙌 Saves", f"{club_df['saves'].sum():.0f}")
    with cols[6]:
        st.metric("🟩 Clean Sheets", f"{club_df['cleanSheet'].sum():.0f}")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # You can add the same bar‑chart / radar‑chart blocks here for the selected club
    # (omitted for brevity – just copy‑paste the code from the league tab and replace `filtered`
    # with `club_df`).

# -------------------------------------------------------------------------
#   TAB 3 – PLAYER COMPARISON (clean UI, radar & tables)
# -------------------------------------------------------------------------
with tab_player:
    st.markdown(
        """
        <span class="section-eyebrow">👥 PLAYER MATCHUP</span>
        <h2 class="section-header">Head‑to‑Head Comparison</h2>
        """,
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns(2)
    with col_a:
        p1 = st.selectbox("Player 1", [None] + filtered_players, key="p1")
    with col_b:
        p2 = st.selectbox("Player 2", [None] + filtered_players, key="p2")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if p1 and p2:
        data1 = filtered[filtered["player"] == p1].iloc[0]
        data2 = filtered[filtered["player"] == p2].iloc[0]

        # ----- PLAYER CARDS ------------------------------------------------
        card_a, card_b = st.columns(2)
        with card_a:
            st.markdown(
                f"""
                <div class='stat-card'>
                    <div style='color:{PALETTE["accent_1"]};font-size:1.2em;font-weight:700;'>{p1}</div>
                    <div style='color:{PALETTE["text_muted"]};font-size:0.9em;'>{data1["team"]} • {data1["league_name"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with card_b:
            st.markdown(
                f"""
                <div class='stat-card'>
                    <div style='color:{PALETTE["accent_2"]};font-size:1.2em;font-weight:700;'>{p2}</div>
                    <div style='color:{PALETTE["text_muted"]};font-size:0.9em;'>{data2["team"]} • {data2["league_name"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ----- ATTACKING METRICS TABLE ------------------------------------
        st.markdown(
            """
            <span class="section-eyebrow">⚔️ ATTACKING</span>
            <h3 class="section-header">Finishing & Shooting</h3>
            """,
            unsafe_allow_html=True,
        )
        attack_metrics = {
            "Goals": (int(data1["goals"]), int(data2["goals"])),
            "Assists": (int(data1["assists"]), int(data2["assists"])),
            "Shots": (int(data1["totalShots"]), int(data2["totalShots"])),
            "Shots on Target": (int(data1["shotsOnTarget"]), int(data2["shotsOnTarget"])),
            "Big Chances Created": (int(data1["bigChancesCreated"]), int(data2["bigChancesCreated"])),
            "xG": (round(data1["expectedGoals"], 2), round(data2["expectedGoals"], 2)),
        }
        df_attack = pd.DataFrame(
            {
                "Metric": list(attack_metrics.keys()),
                p1: [v[0] for v in attack_metrics.values()],
                p2: [v[1] for v in attack_metrics.values()],
            }
        )
        st.dataframe(df_attack, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ----- PLAYMAKING RADAR -------------------------------------------
        st.markdown(
            """
            <span class="section-eyebrow">🎯 PLAYMAKING</span>
            <h3 class="section-header">Creativity & Progression</h3>
            """,
            unsafe_allow_html=True,
        )
        max_bcc = max(data1["bigChancesCreated"], data2["bigChancesCreated"], 1)
        max_kp = max(data1["keyPasses"], data2["keyPasses"], 1)
        max_drb = max(data1["successfulDribbles"], data2["successfulDribbles"], 1)

        radar_data = {
            p1: [
                data1["bigChancesCreated"] / max_bcc * 100,
                data1["keyPasses"] / max_kp * 100,
                data1["successfulDribbles"] / max_drb * 100,
            ],
            p2: [
                data2["bigChancesCreated"] / max_bcc * 100,
                data2["keyPasses"] / max_kp * 100,
                data2["successfulDribbles"] / max_drb * 100,
            ],
        }
        st.plotly_chart(
            radar_chart(radar_data, f"Playmaking – {p1} vs {p2}", metric_type="playmaking"),
            use_container_width=True,
        )
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ----- DEFENSIVE METRICS TABLE ------------------------------------
        st.markdown(
            """
            <span class="section-eyebrow">🛡️ DEFENCE</span>
            <h3 class="section-header">Duels & Clearances</h3>
            """,
            unsafe_allow_html=True,
        )
        defence_metrics = {
            "Tackles": (int(data1["tackles"]), int(data2["tackles"])),
            "Interceptions": (int(data1["interceptions"]), int(data2["interceptions"])),
            "Clearances": (int(data1["clearances"]), int(data2["clearances"])),
            "Aerial Duels Won": (int(data1["aerialDuelsWon"]), int(data2["aerialDuelsWon"])),
            "Ground Duels Won": (int(data1["groundDuelsWon"]), int(data2["groundDuelsWon"])),
        }
        df_def = pd.DataFrame(
            {
                "Metric": list(defence_metrics.keys()),
                p1: [v[0] for v in defence_metrics.values()],
                p2: [v[1] for v in defence_metrics.values()],
            }
        )
        st.dataframe(df_def, use_container_width=True, hide_index=True)

        # ----- DEFENCE RADAR -----------------------------------------------
        max_tck = max(data1["tackles"], data2["tackles"], 1)
        max_int = max(data1["interceptions"], data2["interceptions"], 1)
        max_clr = max(data1["clearances"], data2["clearances"], 1)
        max_aer = max(data1["aerialDuelsWon"], data2["aerialDuelsWon"], 1)
        max_grd = max(data1["groundDuelsWon"], data2["groundDuelsWon"], 1)

        radar_def = {
            p1: [
                data1["tackles"] / max_tck * 100,
                data1["interceptions"] / max_int * 100,
                data1["clearances"] / max_clr * 100,
                data1["aerialDuelsWon"] / max_aer * 100,
                data1["groundDuelsWon"] / max_grd * 100,
            ],
            p2: [
                data2["tackles"] / max_tck * 100,
                data2["interceptions"] / max_int * 100,
                data2["clearances"] / max_clr * 100,
                data2["aerialDuelsWon"] / max_aer * 100,
                data2["groundDuelsWon"] / max_grd * 100,
            ],
        }
        st.plotly_chart(
            radar_chart(radar_def, f"Defence – {p1} vs {p2}", metric_type="defense"),
            use_container_width=True,
        )

    else:
        st.info("⚡ Choose two players to see a side‑by‑side comparison.")

# -------------------------------------------------------------------------
#   FOOTER
# -------------------------------------------------------------------------
st.markdown(
    f"""
    <div style='text-align:center;color:{PALETTE["text_muted"]};margin-top:60px;padding:40px 20px;
                border-top:1px solid rgba(45,212,191,0.1);'>
        <div style='font-size:0.9em;font-weight:600;margin-bottom:8px;'>
            ⚽ European Football Intelligence Platform
        </div>
        <div style='font-size:0.8em;'>
            Advanced analytics across Europe’s elite competitions | 2020‑2025
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
