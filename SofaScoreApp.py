import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# PAGE CONFIG
st.set_page_config(
    page_title="⚽ Europe Football Analytics - 2020s",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM DARK THEME & CSS
st.markdown("""
    <style>
        :root {
            --primary-color: #1f1f1f;
            --secondary-color: #2d2d2d;
            --accent-color: #00d9ff;
            --text-color: #ffffff;
        }
        
        body {
            background-color: #0a0e27;
            color: #ffffff;
        }
        
        .main {
            background-color: #0a0e27;
            padding: 20px;
        }
        
        .sidebar .sidebar-content {
            background-color: #1f1f1f;
            border-right: 2px solid #00d9ff;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background-color: #2d2d2d;
            color: #ffffff;
            border-radius: 8px;
            padding: 10px 20px;
            margin: 5px;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #00d9ff;
            color: #0a0e27;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #2d2d2d 0%, #1f1f1f 100%);
            border: 1px solid #00d9ff;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        h1, h2, h3 {
            color: #00d9ff;
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }
        
        .filter-header {
            background: linear-gradient(135deg, #00d9ff 0%, #0099cc 100%);
            color: #0a0e27;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# LEAGUE COLOR MAPPING (Real League Colors)
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

LEAGUE_LOGOS = {
    'Spain La Liga': '🇪🇸',
    'England Premier League': '🇬🇧',
    'Germany Bundesliga': '🇩🇪',
    'Italy Serie A': '🇮🇹',
    'France Ligue 1': '🇫🇷',
    'UEFA Champions League': '🏆',
    'UEFA Europa League': '🎯',
    'UEFA Conference League': '⭐'
}

POSITIONS = ['ST', 'CF', 'LW', 'RW', 'CM', 'CAM', 'CDM', 'LM', 'RM', 'CB', 'LB', 'RB', 'GK', 'All']

# LOAD OR GENERATE SAMPLE DATA
@st.cache_resource
def load_data():
    """Load sample football data - replace with your actual CSV from the pipeline"""
    # This generates sample data matching the pipeline output structure
    np.random.seed(42)
    
    leagues = list(LEAGUE_COLORS.keys())
    positions = POSITIONS[:-1]  # Exclude 'All'
    countries = ['Spain', 'England', 'Germany', 'Italy', 'France', 'Portugal', 'Netherlands', 'Belgium', 'Argentina', 'Brazil']
    
    n_records = 5000
    
    data = {
        'player_name': [f"Player_{i}" for i in range(n_records)],
        'league_name': np.random.choice(leagues, n_records),
        'club_name': [f"Club_{i}" for i in range(n_records)],
        'position': np.random.choice(positions, n_records),
        'player_country': np.random.choice(countries, n_records),
        'season_year': np.random.choice(['20/21', '21/22', '22/23', '23/24', '24/25'], n_records),
        
        # Attack Stats
        'goals': np.random.poisson(5, n_records),
        'presses': np.random.poisson(20, n_records),
        'xG': np.random.uniform(0, 15, n_records),
        'shots': np.random.poisson(8, n_records),
        'shots_on_target': np.random.poisson(3, n_records),
        'big_chances_missed': np.random.poisson(2, n_records),
        'fouls_won': np.random.poisson(5, n_records),
        'goals_inside_box': np.random.poisson(3, n_records),
        'goals_outside_box': np.random.poisson(1, n_records),
        'shots_inside_box': np.random.poisson(5, n_records),
        'shots_outside_box': np.random.poisson(2, n_records),
        
        # Passing Stats
        'progressive_passes': np.random.poisson(5, n_records),
        'passes_in_opp_box': np.random.poisson(3, n_records),
        'big_chances_created': np.random.poisson(2, n_records),
        'assists': np.random.poisson(2, n_records),
        'crosses': np.random.poisson(4, n_records),
        'long_balls': np.random.poisson(6, n_records),
        'pass_success_rate': np.random.uniform(60, 95, n_records),
        'touches': np.random.poisson(60, n_records),
        'duels_won': np.random.poisson(10, n_records),
        'set_pieces': np.random.poisson(2, n_records),
        
        # Defence Stats
        'tackles': np.random.poisson(8, n_records),
        'interceptions': np.random.poisson(6, n_records),
        'aerial_duels': np.random.poisson(8, n_records),
        'ground_duels': np.random.poisson(12, n_records),
        'clearances': np.random.poisson(5, n_records),
        'fouls': np.random.poisson(3, n_records),
        'clean_sheets': np.random.poisson(2, n_records),
        'blocks': np.random.poisson(4, n_records),
        'recoveries': np.random.poisson(15, n_records),
        'errors_led_to_goal': np.random.poisson(0.5, n_records),
        
        # GK Stats
        'saves': np.random.poisson(5, n_records),
        'parry_saves': np.random.poisson(2, n_records),
        'punches': np.random.poisson(3, n_records),
        'catches': np.random.poisson(4, n_records),
        'goal_kicks': np.random.poisson(30, n_records),
        'long_balls_gk': np.random.poisson(8, n_records),
        'clearances_gk': np.random.poisson(5, n_records),
        'pen_saves': np.random.poisson(0.3, n_records),
    }
    
    df = pd.DataFrame(data)
    return df

# LOAD DATA
df = load_data()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - INTERACTIVE FILTER PANEL
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("<div class='filter-header'>⚙️ FILTERS & CONTROLS</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# League Filter
selected_leagues = st.sidebar.multiselect(
    "🏆 League Selection",
    options=sorted(df['league_name'].unique()),
    default=sorted(df['league_name'].unique())[:3],
    key="leagues"
)

# Position Filter
selected_positions = st.sidebar.multiselect(
    "👤 Position",
    options=POSITIONS,
    default=['All'] if 'All' in POSITIONS else POSITIONS,
    key="positions"
)

# Country Filter
selected_countries = st.sidebar.multiselect(
    "🌍 Player Country",
    options=sorted(df['player_country'].unique()),
    default=sorted(df['player_country'].unique())[:3],
    key="countries"
)

# Season Filter
selected_seasons = st.sidebar.multiselect(
    "📅 Season",
    options=sorted(df['season_year'].unique()),
    default=sorted(df['season_year'].unique()),
    key="seasons"
)

st.sidebar.markdown("---")

# Apply Filters
@st.cache_data
def filter_data(leagues, positions, countries, seasons):
    filtered = df[
        (df['league_name'].isin(leagues)) &
        ((df['position'].isin(positions)) if 'All' not in positions else True) &
        (df['player_country'].isin(countries)) &
        (df['season_year'].isin(seasons))
    ]
    return filtered

filtered_df = filter_data(selected_leagues, selected_positions, selected_countries, selected_seasons)

# Display filter stats
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style='background-color: #2d2d2d; padding: 10px; border-radius: 8px; border-left: 3px solid #00d9ff;'>
    <b>📊 Data Summary</b><br>
    Total Records: <span style='color: #00d9ff;'>{len(filtered_df)}</span><br>
    Leagues: <span style='color: #00d9ff;'>{len(selected_leagues)}</span><br>
    Countries: <span style='color: #00d9ff;'>{len(selected_countries)}</span>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# MAIN HEADER
# ═══════════════════════════════════════════════════════════════
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>⚽ EUROPE'S TOP FOOTBALL ANALYTICS 2020-2025</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; color: #00d9ff; margin-bottom: 20px;'>
    <small>Top 5 Leagues + European Competitions | Champions League | Europa League | Conference League</small>
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
    st.markdown("### ⚔️ Attack Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💥 Avg Goals", f"{filtered_df['goals'].mean():.2f}", delta=f"{filtered_df['goals'].std():.2f}")
    with col2:
        st.metric("🎯 Avg Shots", f"{filtered_df['shots'].mean():.2f}", delta=f"{filtered_df['shots_on_target'].mean():.2f}")
    with col3:
        st.metric("📊 Avg xG", f"{filtered_df['xG'].mean():.2f}", delta=f"{filtered_df['xG'].std():.2f}")
    with col4:
        st.metric("🏃 Avg Presses", f"{filtered_df['presses'].mean():.2f}", delta=f"{filtered_df['presses'].std():.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Goals Distribution by League
    with col1:
        goals_by_league = filtered_df.groupby('league_name')['goals'].agg(['mean', 'count']).reset_index()
        fig_goals = go.Figure()
        fig_goals.add_trace(go.Bar(
            x=goals_by_league['league_name'],
            y=goals_by_league['mean'],
            marker=dict(color=[LEAGUE_COLORS.get(l, '#00d9ff') for l in goals_by_league['league_name']]),
            text=goals_by_league['mean'].round(2),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Avg Goals: %{y:.2f}<extra></extra>'
        ))
        fig_goals.update_layout(
            title="⚽ Average Goals by League",
            xaxis_title="League",
            yaxis_title="Goals",
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    # xG vs Goals Scatter
    with col2:
        fig_xg = px.scatter(
            filtered_df.sample(min(500, len(filtered_df))),
            x='xG',
            y='goals',
            color='league_name',
            size='shots',
            hover_data=['player_name', 'position'],
            color_discrete_map=LEAGUE_COLORS,
            title="📊 xG vs Actual Goals (Size = Shots)",
            labels={'xG': 'Expected Goals (xG)', 'goals': 'Actual Goals'},
            height=400
        )
        fig_xg.update_layout(template="plotly_dark", hovermode='closest')
        st.plotly_chart(fig_xg, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Shots Distribution
    with col1:
        shot_data = filtered_df.groupby('position').agg({
            'shots': 'mean',
            'shots_on_target': 'mean',
            'big_chances_missed': 'mean'
        }).reset_index().sort_values('shots', ascending=False)
        
        fig_shots = go.Figure(data=[
            go.Bar(name='Shots', x=shot_data['position'], y=shot_data['shots']),
            go.Bar(name='Shots on Target', x=shot_data['position'], y=shot_data['shots_on_target']),
        ])
        fig_shots.update_layout(
            title="🎯 Shots Analysis by Position",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_shots, use_container_width=True)
    
    # Inside vs Outside Box
    with col2:
        box_data = filtered_df.groupby('position').agg({
            'goals_inside_box': 'mean',
            'goals_outside_box': 'mean'
        }).reset_index().sort_values('goals_inside_box', ascending=False)
        
        fig_box = go.Figure(data=[
            go.Bar(name='Inside Box', x=box_data['position'], y=box_data['goals_inside_box'], marker_color='#00d9ff'),
            go.Bar(name='Outside Box', x=box_data['position'], y=box_data['goals_outside_box'], marker_color='#ff0080'),
        ])
        fig_box.update_layout(
            title="📍 Goals Location Analysis",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Attack Stats Table
    st.subheader("📋 Detailed Attack Statistics by League")
    attack_stats = filtered_df.groupby('league_name').agg({
        'goals': 'mean',
        'shots': 'mean',
        'shots_on_target': 'mean',
        'xG': 'mean',
        'big_chances_missed': 'mean',
        'fouls_won': 'mean',
        'presses': 'mean'
    }).round(2).reset_index()
    
    attack_stats.columns = ['League', 'Avg Goals', 'Avg Shots', 'Shots on Target', 'xG', 'Big Chances Missed', 'Fouls Won', 'Presses']
    
    st.dataframe(
        attack_stats,
        use_container_width=True,
        column_config={
            "League": st.column_config.TextColumn(),
            "Avg Goals": st.column_config.NumberColumn(format="%.2f"),
            "Avg Shots": st.column_config.NumberColumn(format="%.2f"),
            "Shots on Target": st.column_config.NumberColumn(format="%.2f"),
            "xG": st.column_config.NumberColumn(format="%.2f"),
            "Big Chances Missed": st.column_config.NumberColumn(format="%.2f"),
            "Fouls Won": st.column_config.NumberColumn(format="%.2f"),
            "Presses": st.column_config.NumberColumn(format="%.2f"),
        }
    )

# ═══════════════════════════════════════════════════════════════
# TAB 2: DEFENCE STATS
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🛡️ Defence Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🤝 Avg Tackles", f"{filtered_df['tackles'].mean():.2f}")
    with col2:
        st.metric("👁️ Avg Interceptions", f"{filtered_df['interceptions'].mean():.2f}")
    with col3:
        st.metric("🟩 Avg Blocks", f"{filtered_df['blocks'].mean():.2f}")
    with col4:
        st.metric("🧹 Avg Clearances", f"{filtered_df['clearances'].mean():.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Defence by League
    with col1:
        defence_by_league = filtered_df.groupby('league_name').agg({
            'tackles': 'mean',
            'interceptions': 'mean',
            'blocks': 'mean',
            'clearances': 'mean'
        }).reset_index()
        
        fig_defence = go.Figure()
        fig_defence.add_trace(go.Bar(name='Tackles', x=defence_by_league['league_name'], y=defence_by_league['tackles']))
        fig_defence.add_trace(go.Bar(name='Interceptions', x=defence_by_league['league_name'], y=defence_by_league['interceptions']))
        fig_defence.add_trace(go.Bar(name='Blocks', x=defence_by_league['league_name'], y=defence_by_league['blocks']))
        
        fig_defence.update_layout(
            title="🛡️ Defensive Actions by League",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_defence, use_container_width=True)
    
    # Duels Analysis
    with col2:
        duels_by_pos = filtered_df.groupby('position').agg({
            'aerial_duels': 'mean',
            'ground_duels': 'mean',
            'duels_won': 'mean'
        }).reset_index().sort_values('duels_won', ascending=False)
        
        fig_duels = go.Figure()
        fig_duels.add_trace(go.Bar(name='Aerial Duels', x=duels_by_pos['position'], y=duels_by_pos['aerial_duels']))
        fig_duels.add_trace(go.Bar(name='Ground Duels', x=duels_by_pos['position'], y=duels_by_pos['ground_duels']))
        
        fig_duels.update_layout(
            title="⚔️ Duels by Position",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_duels, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Clean Sheets
    with col1:
        clean_sheets = filtered_df.groupby('league_name')['clean_sheets'].mean().reset_index()
        clean_sheets = clean_sheets.sort_values('clean_sheets', ascending=False)
        
        fig_cs = go.Figure(data=go.Bar(
            x=clean_sheets['league_name'],
            y=clean_sheets['clean_sheets'],
            marker=dict(color=[LEAGUE_COLORS.get(l, '#00d9ff') for l in clean_sheets['league_name']]),
            text=clean_sheets['clean_sheets'].round(2),
            textposition='auto'
        ))
        fig_cs.update_layout(
            title="🟩 Average Clean Sheets by League",
            xaxis_title="League",
            yaxis_title="Clean Sheets",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_cs, use_container_width=True)
    
    # Recoveries vs Tackles
    with col2:
        recovery_data = filtered_df.sample(min(500, len(filtered_df)))
        fig_recovery = px.scatter(
            recovery_data,
            x='tackles',
            y='recoveries',
            color='position',
            size='interceptions',
            hover_data=['player_name', 'league_name'],
            title="🔄 Recoveries vs Tackles (Size = Interceptions)",
            labels={'tackles': 'Tackles', 'recoveries': 'Recoveries'},
            height=400
        )
        fig_recovery.update_layout(template="plotly_dark", hovermode='closest')
        st.plotly_chart(fig_recovery, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Defence Stats
    st.subheader("📋 Detailed Defence Statistics by Position")
    defence_stats = filtered_df.groupby('position').agg({
        'tackles': 'mean',
        'interceptions': 'mean',
        'blocks': 'mean',
        'clearances': 'mean',
        'aerial_duels': 'mean',
        'ground_duels': 'mean',
        'clean_sheets': 'mean',
        'errors_led_to_goal': 'mean'
    }).round(2).reset_index()
    
    defence_stats.columns = ['Position', 'Tackles', 'Interceptions', 'Blocks', 'Clearances', 'Aerial Duels', 'Ground Duels', 'Clean Sheets', 'Errors to Goal']
    
    st.dataframe(defence_stats, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: PASSING STATS
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🎯 Passing Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📲 Avg Pass Success %", f"{filtered_df['pass_success_rate'].mean():.1f}%")
    with col2:
        st.metric("⚡ Avg Progressive Passes", f"{filtered_df['progressive_passes'].mean():.2f}")
    with col3:
        st.metric("🎁 Avg Assists", f"{filtered_df['assists'].mean():.2f}")
    with col4:
        st.metric("✨ Avg Big Chances Created", f"{filtered_df['big_chances_created'].mean():.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Pass Success Rate by League
    with col1:
        pass_by_league = filtered_df.groupby('league_name')['pass_success_rate'].mean().reset_index()
        pass_by_league = pass_by_league.sort_values('pass_success_rate', ascending=False)
        
        fig_pass = go.Figure(data=go.Bar(
            x=pass_by_league['league_name'],
            y=pass_by_league['pass_success_rate'],
            marker=dict(color=[LEAGUE_COLORS.get(l, '#00d9ff') for l in pass_by_league['league_name']]),
            text=pass_by_league['pass_success_rate'].round(1),
            textposition='auto'
        ))
        fig_pass.update_layout(
            title="📲 Pass Success Rate by League",
            xaxis_title="League",
            yaxis_title="Success Rate (%)",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_pass, use_container_width=True)
    
    # Big Chances Created vs Assists (Scatter)
    with col2:
        scatter_data = filtered_df.sample(min(500, len(filtered_df)))
        fig_chances = px.scatter(
            scatter_data,
            x='big_chances_created',
            y='assists',
            color='league_name',
            size='progressive_passes',
            hover_data=['player_name', 'position'],
            color_discrete_map=LEAGUE_COLORS,
            title="🎁 Big Chances Created vs Assists (Club Level)",
            labels={'big_chances_created': 'Big Chances Created', 'assists': 'Assists'},
            height=400
        )
        fig_chances.update_layout(template="plotly_dark", hovermode='closest')
        st.plotly_chart(fig_chances, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    # Passing Stats by Position
    with col1:
        pass_by_pos = filtered_df.groupby('position').agg({
            'progressive_passes': 'mean',
            'passes_in_opp_box': 'mean',
            'crosses': 'mean',
            'long_balls': 'mean'
        }).reset_index().sort_values('progressive_passes', ascending=False)
        
        fig_pass_pos = go.Figure()
        fig_pass_pos.add_trace(go.Bar(name='Progressive Passes', x=pass_by_pos['position'], y=pass_by_pos['progressive_passes']))
        fig_pass_pos.add_trace(go.Bar(name='Passes in Opp Box', x=pass_by_pos['position'], y=pass_by_pos['passes_in_opp_box']))
        
        fig_pass_pos.update_layout(
            title="📊 Passing Distribution by Position",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_pass_pos, use_container_width=True)
    
    # Crosses and Long Balls
    with col2:
        cross_data = filtered_df.groupby('league_name').agg({
            'crosses': 'mean',
            'long_balls': 'mean',
            'set_pieces': 'mean'
        }).reset_index()
        
        fig_cross = go.Figure()
        fig_cross.add_trace(go.Bar(name='Crosses', x=cross_data['league_name'], y=cross_data['crosses']))
        fig_cross.add_trace(go.Bar(name='Long Balls', x=cross_data['league_name'], y=cross_data['long_balls']))
        fig_cross.add_trace(go.Bar(name='Set Pieces', x=cross_data['league_name'], y=cross_data['set_pieces']))
        
        fig_cross.update_layout(
            title="🎯 Crossing & Long Balls by League",
            barmode='group',
            template="plotly_dark",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_cross, use_container_width=True)
    
    st.markdown("---")
    
    # Touches and Ball Involvement
    col1, col2 = st.columns(2)
    
    with col1:
        touches_data = filtered_df.groupby('position')['touches'].mean().reset_index().sort_values('touches', ascending=False)
        
        fig_touches = go.Figure(data=go.Bar(
            x=touches_data['position'],
            y=touches_data['touches'],
            marker_color='#00d9ff',
            text=touches_data['touches'].round(1),
            textposition='auto'
        ))
        fig_touches.update_layout(
            title="👆 Average Touches by Position",
            xaxis_title="Position",
            yaxis_title="Touches",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_touches, use_container_width=True)
    
    with col2:
        duels_won = filtered_df.groupby('position')['duels_won'].mean().reset_index().sort_values('duels_won', ascending=False)
        
        fig_duels_won = go.Figure(data=go.Bar(
            x=duels_won['position'],
            y=duels_won['duels_won'],
            marker_color='#ff0080',
            text=duels_won['duels_won'].round(1),
            textposition='auto'
        ))
        fig_duels_won.update_layout(
            title="⚔️ Average Duels Won by Position",
            xaxis_title="Position",
            yaxis_title="Duels Won",
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_duels_won, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 4: GOALKEEPER STATS
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🥅 Goalkeeper Statistics")
    
    # Filter GK data
    gk_data = filtered_df[filtered_df['position'] == 'GK']
    
    if len(gk_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🙌 Avg Saves", f"{gk_data['saves'].mean():.2f}")
        with col2:
            st.metric("🟩 Avg Clean Sheets", f"{gk_data['clean_sheets'].mean():.2f}")
        with col3:
            st.metric("✋ Avg Parry Saves", f"{gk_data['parry_saves'].mean():.2f}")
        with col4:
            st.metric("💿 Avg Punches", f"{gk_data['punches'].mean():.2f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # Saves by League
        with col1:
            saves_by_league = gk_data.groupby('league_name').agg({
                'saves': 'mean',
                'clean_sheets': 'mean'
            }).reset_index()
            
            fig_saves = go.Figure()
            fig_saves.add_trace(go.Bar(
                name='Saves',
                x=saves_by_league['league_name'],
                y=saves_by_league['saves'],
                marker_color='#00d9ff'
            ))
            fig_saves.add_trace(go.Bar(
                name='Clean Sheets',
                x=saves_by_league['league_name'],
                y=saves_by_league['clean_sheets'],
                marker_color='#00ff00'
            ))
            
            fig_saves.update_layout(
                title="🙌 Saves & Clean Sheets by League",
                barmode='group',
                template="plotly_dark",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_saves, use_container_width=True)
        
        # GK Distribution
        with col2:
            gk_dist = gk_data.groupby('league_name').agg({
                'parry_saves': 'mean',
                'punches': 'mean',
                'catches': 'mean'
            }).reset_index()
            
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Bar(name='Parry Saves', x=gk_dist['league_name'], y=gk_dist['parry_saves']))
            fig_dist.add_trace(go.Bar(name='Punches', x=gk_dist['league_name'], y=gk_dist['punches']))
            fig_dist.add_trace(go.Bar(name='Catches', x=gk_dist['league_name'], y=gk_dist['catches']))
            
            fig_dist.update_layout(
                title="🥊 GK Shot-Stopping Distribution",
                barmode='group',
                template="plotly_dark",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # Distribution Stats
        with col1:
            dist_stats = gk_data.groupby('league_name').agg({
                'goal_kicks': 'mean',
                'long_balls_gk': 'mean',
                'clearances_gk': 'mean'
            }).reset_index()
            
            fig_dist_stats = go.Figure()
            fig_dist_stats.add_trace(go.Bar(name='Goal Kicks', x=dist_stats['league_name'], y=dist_stats['goal_kicks']))
            fig_dist_stats.add_trace(go.Bar(name='Long Balls', x=dist_stats['league_name'], y=dist_stats['long_balls_gk']))
            fig_dist_stats.add_trace(go.Bar(name='Clearances', x=dist_stats['league_name'], y=dist_stats['clearances_gk']))
            
            fig_dist_stats.update_layout(
                title="🦶 Distribution Stats by League",
                barmode='group',
                template="plotly_dark",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_dist_stats, use_container_width=True)
        
        # Saves vs Errors
        with col2:
            gk_scatter = gk_data.sample(min(200, len(gk_data)))
            fig_error = px.scatter(
                gk_scatter,
                x='saves',
                y='errors_led_to_goal',
                color='league_name',
                size='clean_sheets',
                hover_data=['player_name'],
                color_discrete_map=LEAGUE_COLORS,
                title="⚠️ Saves vs Errors (Size = Clean Sheets)",
                labels={'saves': 'Saves', 'errors_led_to_goal': 'Errors Led to Goal'},
                height=400
            )
            fig_error.update_layout(template="plotly_dark", hovermode='closest')
            st.plotly_chart(fig_error, use_container_width=True)
        
        st.markdown("---")
        
        # GK Detailed Stats
        st.subheader("📋 Detailed GK Statistics by League")
        gk_stats = gk_data.groupby('league_name').agg({
            'saves': 'mean',
            'clean_sheets': 'mean',
            'parry_saves': 'mean',
            'punches': 'mean',
            'catches': 'mean',
            'goal_kicks': 'mean',
            'long_balls_gk': 'mean',
            'pen_saves': 'mean',
            'errors_led_to_goal': 'mean'
        }).round(2).reset_index()
        
        gk_stats.columns = ['League', 'Saves', 'Clean Sheets', 'Parry Saves', 'Punches', 'Catches', 'Goal Kicks', 'Long Balls', 'Pen Saves', 'Errors to Goal']
        
        st.dataframe(gk_stats, use_container_width=True)
    else:
        st.warning("⚠️ No goalkeeper data available with current filters.")

# ═══════════════════════════════════════════════════════════════
# TAB 5: PLAYER COMPARISON
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 👥 Player Comparison Analysis")
    
    comparison_mode = st.radio(
        "Choose Comparison Mode:",
        ["One vs One (Player vs Player)", "Profile vs Profile (Position Averages)", "Player vs League Average"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if comparison_mode == "One vs One (Player vs Player)":
        col1, col2 = st.columns(2)
        
        available_players = sorted(filtered_df['player_name'].unique())
        
        with col1:
            player1 = st.selectbox(
                "Select Player 1:",
                options=available_players,
                key="p1"
            )
        
        with col2:
            player2 = st.selectbox(
                "Select Player 2:",
                options=available_players,
                key="p2",
                index=min(1, len(available_players)-1)
            )
        
        if player1 and player2:
            p1_data = filtered_df[filtered_df['player_name'] == player1].iloc[0]
            p2_data = filtered_df[filtered_df['player_name'] == player2].iloc[0]
            
            st.markdown("---")
            
            # Player Info Cards
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>{player1}</h3>
                    <p><b>Position:</b> {p1_data['position']}</p>
                    <p><b>League:</b> {p1_data['league_name']}</p>
                    <p><b>Club:</b> {p1_data['club_name']}</p>
                    <p><b>Country:</b> {p1_data['player_country']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>{player2}</h3>
                    <p><b>Position:</b> {p2_data['position']}</p>
                    <p><b>League:</b> {p2_data['league_name']}</p>
                    <p><b>Club:</b> {p2_data['club_name']}</p>
                    <p><b>Country:</b> {p2_data['player_country']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Comparison Charts
            col1, col2 = st.columns(2)
            
            with col1:
                comparison_stats = pd.DataFrame({
                    player1: [
                        p1_data['goals'],
                        p1_data['assists'],
                        p1_data['tackles'],
                        p1_data['interceptions'],
                        p1_data['pass_success_rate']
                    ],
                    player2: [
                        p2_data['goals'],
                        p2_data['assists'],
                        p2_data['tackles'],
                        p2_data['interceptions'],
                        p2_data['pass_success_rate']
                    ]
                }, index=['Goals', 'Assists', 'Tackles', 'Interceptions', 'Pass Success %'])
                
                fig_compare = go.Figure()
                fig_compare.add_trace(go.Bar(name=player1, x=comparison_stats.index, y=comparison_stats[player1]))
                fig_compare.add_trace(go.Bar(name=player2, x=comparison_stats.index, y=comparison_stats[player2]))
                
                fig_compare.update_layout(
                    title="📊 Key Stats Comparison",
                    barmode='group',
                    template="plotly_dark",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_compare, use_container_width=True)
            
            # Radar Chart
            with col2:
                categories = ['Goals', 'Assists', 'Shots', 'Tackles', 'Pass Success %']
                
                p1_values = [
                    p1_data['goals'],
                    p1_data['assists'],
                    p1_data['shots'],
                    p1_data['tackles'],
                    p1_data['pass_success_rate']
                ]
                
                p2_values = [
                    p2_data['goals'],
                    p2_data['assists'],
                    p2_data['shots'],
                    p2_data['tackles'],
                    p2_data['pass_success_rate']
                ]
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=p1_values,
                    theta=categories,
                    fill='toself',
                    name=player1,
                    line_color='#00d9ff'
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=p2_values,
                    theta=categories,
                    fill='toself',
                    name=player2,
                    line_color='#ff0080'
                ))
                
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(max(p1_values), max(p2_values))*1.2])),
                    template="plotly_dark",
                    title="🎯 Player Profile Radar",
                    height=400
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Detailed Comparison Table
            st.markdown("---")
            st.subheader("📋 Detailed Metrics Comparison")
            
            detailed_comparison = pd.DataFrame({
                'Metric': ['Goals', 'Assists', 'Shots', 'Shots on Target', 'xG', 'Tackles', 'Interceptions',
                          'Blocks', 'Pass Success %', 'Progressive Passes', 'Touches', 'Duels Won', 'Clean Sheets'],
                player1: [
                    p1_data['goals'], p1_data['assists'], p1_data['shots'], p1_data['shots_on_target'],
                    p1_data['xG'], p1_data['tackles'], p1_data['interceptions'], p1_data['blocks'],
                    p1_data['pass_success_rate'], p1_data['progressive_passes'], p1_data['touches'],
                    p1_data['duels_won'], p1_data['clean_sheets']
                ],
                player2: [
                    p2_data['goals'], p2_data['assists'], p2_data['shots'], p2_data['shots_on_target'],
                    p2_data['xG'], p2_data['tackles'], p2_data['interceptions'], p2_data['blocks'],
                    p2_data['pass_success_rate'], p2_data['progressive_passes'], p2_data['touches'],
                    p2_data['duels_won'], p2_data['clean_sheets']
                ],
                'Difference': [0]*13
            })
            
            detailed_comparison['Difference'] = (detailed_comparison[player1] - detailed_comparison[player2]).round(2)
            detailed_comparison = detailed_comparison.round(2)
            
            st.dataframe(detailed_comparison, use_container_width=True)
    
    elif comparison_mode == "Profile vs Profile (Position Averages)":
        col1, col2 = st.columns(2)
        
        with col1:
            pos1 = st.selectbox(
                "Select Position 1:",
                options=POSITIONS[:-1],
                key="pos1"
            )
            league1 = st.selectbox(
                "Select League 1:",
                options=sorted(filtered_df['league_name'].unique()),
                key="league1"
            )
        
        with col2:
            pos2 = st.selectbox(
                "Select Position 2:",
                options=POSITIONS[:-1],
                key="pos2",
                index=1 if len(POSITIONS) > 1 else 0
            )
            league2 = st.selectbox(
                "Select League 2:",
                options=sorted(filtered_df['league_name'].unique()),
                key="league2",
                index=min(1, len(sorted(filtered_df['league_name'].unique()))-1)
            )
        
        st.markdown("---")
        
        # Get profile averages
        profile1 = filtered_df[(filtered_df['position'] == pos1) & (filtered_df['league_name'] == league1)]
        profile2 = filtered_df[(filtered_df['position'] == pos2) & (filtered_df['league_name'] == league2)]
        
        if len(profile1) > 0 and len(profile2) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>{pos1} - {league1}</h3>
                    <p><b>Sample Size:</b> {len(profile1)} players</p>
                    <p><b>Avg Goals:</b> {profile1['goals'].mean():.2f}</p>
                    <p><b>Avg Assists:</b> {profile1['assists'].mean():.2f}</p>
                    <p><b>Avg Tackles:</b> {profile1['tackles'].mean():.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>{pos2} - {league2}</h3>
                    <p><b>Sample Size:</b> {len(profile2)} players</p>
                    <p><b>Avg Goals:</b> {profile2['goals'].mean():.2f}</p>
                    <p><b>Avg Assists:</b> {profile2['assists'].mean():.2f}</p>
                    <p><b>Avg Tackles:</b> {profile2['tackles'].mean():.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Radar comparison
            categories = ['Goals', 'Assists', 'Shots', 'Tackles', 'Pass Success %', 'Touches']
            
            p1_values = [
                profile1['goals'].mean(),
                profile1['assists'].mean(),
                profile1['shots'].mean(),
                profile1['tackles'].mean(),
                profile1['pass_success_rate'].mean(),
                profile1['touches'].mean() / 10  # Scale for visualization
            ]
            
            p2_values = [
                profile2['goals'].mean(),
                profile2['assists'].mean(),
                profile2['shots'].mean(),
                profile2['tackles'].mean(),
                profile2['pass_success_rate'].mean(),
                profile2['touches'].mean() / 10
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=p1_values,
                theta=categories,
                fill='toself',
                name=f"{pos1} ({league1})",
                line_color='#00d9ff'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=p2_values,
                theta=categories,
                fill='toself',
                name=f"{pos2} ({league2})",
                line_color='#ff0080'
            ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                template="plotly_dark",
                title="⭐ Position & League Profile Comparison",
                height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.warning("⚠️ Not enough data for selected profiles.")
    
    else:  # Player vs League Average
        selected_player = st.selectbox(
            "Select Player:",
            options=sorted(filtered_df['player_name'].unique())
        )
        
        if selected_player:
            player_stats = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
            player_league = player_stats['league_name']
            player_position = player_stats['position']
            
            # League average for same position
            league_avg = filtered_df[
                (filtered_df['league_name'] == player_league) &
                (filtered_df['position'] == player_position)
            ]
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>{selected_player}</h3>
                    <p><b>Position:</b> {player_position}</p>
                    <p><b>League:</b> {player_league}</p>
                    <p><b>Club:</b> {player_stats['club_name']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>League Average</h3>
                    <p><b>Position:</b> {player_position}</p>
                    <p><b>League:</b> {player_league}</p>
                    <p><b>Sample:</b> {len(league_avg)} players</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                percentile = (filtered_df[filtered_df['goals'] <= player_stats['goals']].shape[0] / len(filtered_df)) * 100
                st.markdown(f"""
                    <div class='metric-card'>
                    <h3>Stats Percentile</h3>
                    <p><b>Goals Percentile:</b> {percentile:.1f}%</p>
                    <p><b>vs League Avg:</b> {player_stats['goals'] - league_avg['goals'].mean():.2f} goals</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Comparison visualization
            col1, col2 = st.columns(2)
            
            with col1:
                stats_comparison = pd.DataFrame({
                    selected_player: [
                        player_stats['goals'],
                        player_stats['assists'],
                        player_stats['shots'],
                        player_stats['tackles'],
                        player_stats['pass_success_rate']
                    ],
                    f"{player_position} Avg ({player_league})": [
                        league_avg['goals'].mean(),
                        league_avg['assists'].mean(),
                        league_avg['shots'].mean(),
                        league_avg['tackles'].mean(),
                        league_avg['pass_success_rate'].mean()
                    ]
                }, index=['Goals', 'Assists', 'Shots', 'Tackles', 'Pass Success %'])
                
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Bar(
                    name=selected_player,
                    x=stats_comparison.index,
                    y=stats_comparison[selected_player],
                    marker_color='#00d9ff'
                ))
                fig_comp.add_trace(go.Bar(
                    name="League Average",
                    x=stats_comparison.index,
                    y=stats_comparison[f"{player_position} Avg ({player_league})"],
                    marker_color='#ff0080'
                ))
                
                fig_comp.update_layout(
                    title="📊 Player vs League Average",
                    barmode='group',
                    template="plotly_dark",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig_comp, use_container_width=True)
            
            with col2:
                # Distribution visualization
                goals_dist = filtered_df[
                    (filtered_df['league_name'] == player_league) &
                    (filtered_df['position'] == player_position)
                ]['goals']
                
                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(
                    x=goals_dist,
                    name='Goals Distribution',
                    marker_color='#2d2d2d',
                    nbinsx=20,
                    opacity=0.7
                ))
                fig_dist.add_vline(
                    x=player_stats['goals'],
                    line_dash="dash",
                    line_color="#00d9ff",
                    annotation_text=f"{selected_player}: {player_stats['goals']:.1f}",
                    annotation_position="top right"
                )
                fig_dist.add_vline(
                    x=league_avg['goals'].mean(),
                    line_dash="dash",
                    line_color="#ff0080",
                    annotation_text=f"League Avg: {league_avg['goals'].mean():.1f}",
                    annotation_position="top left"
                )
                
                fig_dist.update_layout(
                    title="📈 Goals Distribution in League",
                    xaxis_title="Goals",
                    yaxis_title="Number of Players",
                    template="plotly_dark",
                    height=400
                )
                st.plotly_chart(fig_dist, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #00d9ff; margin-top: 40px;'>
    <small>⚽ Football Analytics Dashboard 2020-2025 | Powered by Streamlit & Plotly</small><br>
    <small>Data Source: ScraperFC | Europe's Top 5 Leagues + European Competitions</small>
    </div>
""", unsafe_allow_html=True)
