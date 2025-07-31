import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="CS:GO Player Analysis Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #004E89;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #FF6B35;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        border-left: 4px solid #004E89;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """
    Load and preprocess CS:GO player data.
    
    Returns:
        pd.DataFrame: Processed CS:GO player statistics
    """
    try:
        df = pd.read_csv("csgo_dados.csv")
        # Clean and preprocess data
        df = df.dropna()
        return df
    except FileNotFoundError:
        st.error("❌ Data file 'csgo_dados.csv' not found. Please ensure the file exists in the project directory.")
        return None

def create_statistics_overview(df, column):
    """
    Create statistical overview for a given column.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
        column (str): The column name to analyze
        
    Returns:
        dict: Dictionary containing statistical measures
    """
    return {
        'mean': df[column].mean(),
        'min': df[column].min(),
        'max': df[column].max(),
        'median': df[column].median(),
        'std': df[column].std()
    }

def plot_statistics_bar_chart(df, column, title, ylabel, color='blue'):
    """
    Create a bar chart showing statistical measures for a column.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
        column (str): The column name to analyze
        title (str): Title for the chart
        ylabel (str): Y-axis label
        color (str): Color for the bars
        
    Returns:
        plotly.graph_objects.Figure: Interactive bar chart
    """
    stats = create_statistics_overview(df, column)
    
    fig = go.Figure(data=[
        go.Bar(
            x=['Média', 'Mínimo', 'Máximo', 'Mediana'],
            y=[stats['mean'], stats['min'], stats['max'], stats['median']],
            marker_color=color,
            text=[f'{val:.2f}' for val in [stats['mean'], stats['min'], stats['max'], stats['median']]],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Estatísticas",
        yaxis_title=ylabel,
        showlegend=False,
        height=400
    )
    
    return fig

def plot_country_distribution(df):
    """
    Create a bar chart showing player distribution by country.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
        
    Returns:
        plotly.graph_objects.Figure: Interactive country distribution chart
    """
    country_counts = df['country'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=country_counts.index,
            y=country_counts.values,
            marker_color='green',
            text=country_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Distribuição de Jogadores por País",
        xaxis_title="Países",
        yaxis_title="Número de Jogadores",
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig

def plot_rating_distribution(df):
    """
    Create a histogram showing rating distribution.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
        
    Returns:
        plotly.graph_objects.Figure: Interactive rating distribution chart
    """
    fig = go.Figure(data=[
        go.Histogram(
            x=df['rating'],
            nbinsx=30,
            marker_color='lightblue',
            opacity=0.7
        )
    ])
    
    fig.update_layout(
        title="Distribuição de Rating dos Jogadores",
        xaxis_title="Rating",
        yaxis_title="Número de Jogadores",
        height=400
    )
    
    return fig

def plot_kd_vs_rating_scatter(df, title_suffix="", top_n=None, min_maps=None):
    """
    Create a scatter plot showing KD vs Rating relationship.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
        title_suffix (str): Additional text for the title
        top_n (int): Number of top players to show
        min_maps (int): Minimum number of maps filter
        
    Returns:
        plotly.graph_objects.Figure: Interactive scatter plot
    """
    plot_df = df.copy()
    
    if min_maps:
        plot_df = plot_df[plot_df['total_maps'] > min_maps]
    
    if top_n:
        plot_df = plot_df.head(top_n)
    
    fig = go.Figure()
    
    # Add scatter plot
    fig.add_trace(go.Scatter(
        x=plot_df['kd'],
        y=plot_df['rating'],
        mode='markers+text',
        text=plot_df['name'] if top_n and top_n <= 20 else "",
        textposition='top center',
        marker=dict(
            size=8,
            color='darkblue',
            opacity=0.7
        ),
        hovertemplate='<b>%{text}</b><br>K/D: %{x:.2f}<br>Rating: %{y:.2f}<extra></extra>'
    ))
    
    # Add trend line for top players
    if top_n and top_n <= 20:
        fig.add_trace(go.Scatter(
            x=[plot_df['kd'].min(), plot_df['kd'].max()],
            y=[plot_df['rating'].min(), plot_df['rating'].max()],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Linha de Tendência'
        ))
    
    fig.update_layout(
        title=f"K/D vs Rating{title_suffix}",
        xaxis_title="K/D",
        yaxis_title="Rating",
        height=500,
        showlegend=True if top_n and top_n <= 20 else False
    )
    
    return fig

def display_player_insights(df):
    """
    Display insights about player performance patterns.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data
    """
    st.markdown('<div class="section-header">🎯 Insights da Análise</div>', unsafe_allow_html=True)
    
    top_20 = df.head(20)
    
    # Calculate correlation
    correlation = df['kd'].corr(df['rating'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <h4>📊 Correlação K/D vs Rating</h4>
        <p>A correlação entre K/D e Rating é de <strong>{correlation:.3f}</strong>, 
        indicando uma relação positiva forte entre eficiência em kills/deaths e rating geral.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
        <h4>🌍 Diversidade Global</h4>
        <p>O dataset inclui jogadores de <strong>{df['country'].nunique()}</strong> países diferentes, 
        com {df['country'].value_counts().iloc[0]} jogadores do país mais representado ({df['country'].value_counts().index[0]}).</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """
    Main Streamlit application function.
    """
    # Header
    st.markdown('<div class="main-header">🎮 CS:GO Player Analysis Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 📋 Sobre esta Análise
    
    Esta aplicação analisa dados de jogadores profissionais de Counter-Strike: Global Offensive com rating acima de 1.00 
    entre os anos de 2015-2020. O dataset inclui informações detalhadas sobre performance, países, times e estatísticas de jogo.
    """)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controles da Análise")
    
    # Analysis selection
    analysis_type = st.sidebar.selectbox(
        "Selecione o tipo de análise:",
        ["Visão Geral", "Análise por País", "Distribuição de Rating", "Relação K/D vs Rating", "Análise de Top Players"]
    )
    
    # Filters
    st.sidebar.subheader("🔍 Filtros")
    min_maps = st.sidebar.slider("Mínimo de mapas jogados:", 0, int(df['total_maps'].max()), 0)
    min_rating = st.sidebar.slider("Rating mínimo:", float(df['rating'].min()), float(df['rating'].max()), float(df['rating'].min()))
    
    # Apply filters
    filtered_df = df[(df['total_maps'] >= min_maps) & (df['rating'] >= min_rating)]
    
    # Display filtered data info
    st.sidebar.markdown(f"**Jogadores após filtros:** {len(filtered_df)}")
    
    # Main content based on selection
    if analysis_type == "Visão Geral":
        st.markdown('<div class="section-header">📊 Estatísticas Gerais</div>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Jogadores", len(filtered_df))
        with col2:
            st.metric("Rating Médio", f"{filtered_df['rating'].mean():.3f}")
        with col3:
            st.metric("K/D Médio", f"{filtered_df['kd'].mean():.3f}")
        with col4:
            st.metric("Países Representados", filtered_df['country'].nunique())
        
        # Statistics charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_maps = plot_statistics_bar_chart(filtered_df, 'total_maps', 
                                                'Estatísticas de Mapas Jogados', 'Mapas Jogados', 'blue')
            st.plotly_chart(fig_maps, use_container_width=True)
        
        with col2:
            fig_kd = plot_statistics_bar_chart(filtered_df, 'kd', 
                                             'Estatísticas de K/D', 'Relação K/D', 'red')
            st.plotly_chart(fig_kd, use_container_width=True)
        
        # Data table
        st.markdown('<div class="section-header">📋 Top 20 Jogadores</div>', unsafe_allow_html=True)
        st.dataframe(filtered_df.head(20)[['name', 'country', 'total_maps', 'kd', 'rating']], use_container_width=True)
    
    elif analysis_type == "Análise por País":
        st.markdown('<div class="section-header">🌍 Distribuição por País</div>', unsafe_allow_html=True)
        
        fig_country = plot_country_distribution(filtered_df)
        st.plotly_chart(fig_country, use_container_width=True)
        
        # Country statistics
        country_stats = filtered_df.groupby('country').agg({
            'rating': ['mean', 'max', 'count'],
            'kd': 'mean'
        }).round(3)
        
        country_stats.columns = ['Rating Médio', 'Rating Máximo', 'Número de Jogadores', 'K/D Médio']
        country_stats = country_stats.sort_values('Rating Médio', ascending=False)
        
        st.markdown("### 📊 Estatísticas por País")
        st.dataframe(country_stats, use_container_width=True)
    
    elif analysis_type == "Distribuição de Rating":
        st.markdown('<div class="section-header">📈 Distribuição de Rating</div>', unsafe_allow_html=True)
        
        fig_rating = plot_rating_distribution(filtered_df)
        st.plotly_chart(fig_rating, use_container_width=True)
        
        # Rating analysis
        rating_ranges = pd.cut(filtered_df['rating'], bins=5, precision=2)
        rating_counts = rating_ranges.value_counts().sort_index()
        
        st.markdown("### 📊 Jogadores por Faixa de Rating")
        for range_val, count in rating_counts.items():
            st.write(f"**{range_val}**: {count} jogadores")
    
    elif analysis_type == "Relação K/D vs Rating":
        st.markdown('<div class="section-header">⚡ Relação K/D vs Rating</div>', unsafe_allow_html=True)
        
        view_option = st.radio(
            "Selecione a visualização:",
            ["Todos os jogadores", "Top 50", "Top 20", "Top 20 com +750 mapas"]
        )
        
        if view_option == "Todos os jogadores":
            fig = plot_kd_vs_rating_scatter(filtered_df)
        elif view_option == "Top 50":
            fig = plot_kd_vs_rating_scatter(filtered_df, " (Top 50)", top_n=50)
        elif view_option == "Top 20":
            fig = plot_kd_vs_rating_scatter(filtered_df, " (Top 20)", top_n=20)
        else:  # Top 20 with +750 maps
            high_exp_df = filtered_df[filtered_df['total_maps'] > 750]
            fig = plot_kd_vs_rating_scatter(high_exp_df, " (Top 20, +750 mapas)", top_n=20)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display insights
        display_player_insights(filtered_df)
    
    elif analysis_type == "Análise de Top Players":
        st.markdown('<div class="section-header">🏆 Análise de Top Players</div>', unsafe_allow_html=True)
        
        top_n = st.slider("Número de top players para analisar:", 5, 50, 20)
        top_players = filtered_df.head(top_n)
        
        # Player comparison
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=top_players['name'],
            y=top_players['rating'],
            mode='markers+lines',
            name='Rating',
            line=dict(color='blue'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"Rating dos Top {top_n} Jogadores",
            xaxis_title="Jogadores",
            yaxis_title="Rating",
            xaxis_tickangle=-45,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed player table
        st.markdown(f"### 📋 Detalhes dos Top {top_n} Jogadores")
        st.dataframe(top_players[['name', 'country', 'teams', 'total_maps', 'total_rounds', 'kd', 'rating']], 
                    use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("📊 **CS:GO Player Analysis Dashboard** - Análise interativa de dados de jogadores profissionais")

if __name__ == "__main__":
    main()