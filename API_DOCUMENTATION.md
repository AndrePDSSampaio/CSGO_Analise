# 📚 CS:GO Analysis Dashboard - API Documentation

## Overview

This document provides comprehensive documentation for all public APIs, functions, and components in the CS:GO Player Analysis Dashboard. The application is built using Streamlit and provides interactive data analysis capabilities for CS:GO professional player statistics.

## Table of Contents

- [Data Models](#data-models)
- [Core Functions](#core-functions)
- [Visualization Functions](#visualization-functions)
- [Utility Functions](#utility-functions)
- [Streamlit Components](#streamlit-components)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)

## Data Models

### Player Data Schema

The CS:GO player dataset follows this structure:

```python
{
    "name": str,           # Player nickname/handle
    "country": str,        # Country of origin
    "teams": str,          # JSON string of team affiliations
    "total_maps": int,     # Total competitive maps played
    "total_rounds": int,   # Total rounds participated in
    "kd_diff": int,        # Kill-Death difference
    "kd": float,           # Kill-Death ratio
    "rating": float        # Overall performance rating
}
```

#### Field Descriptions

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `name` | string | - | Unique player identifier/nickname |
| `country` | string | - | ISO country name or standard country name |
| `teams` | string | - | JSON array of team names as string |
| `total_maps` | integer | 0+ | Number of competitive maps played |
| `total_rounds` | integer | 0+ | Total rounds across all maps |
| `kd_diff` | integer | - | Difference between kills and deaths |
| `kd` | float | 0.0+ | Kill/Death ratio (kills ÷ deaths) |
| `rating` | float | 1.0+ | Professional performance rating |

## Core Functions

### Data Loading

#### `load_data()`

```python
@st.cache_data
def load_data() -> pd.DataFrame | None
```

**Purpose**: Loads and preprocesses CS:GO player data from CSV file.

**Returns**: 
- `pd.DataFrame`: Cleaned dataset with player statistics
- `None`: If file not found or loading error

**Features**:
- Automatic data caching for performance
- Data cleaning (removes null values)
- Error handling with user feedback

**Example Usage**:
```python
df = load_data()
if df is not None:
    print(f"Loaded {len(df)} players")
    print(f"Countries: {df['country'].nunique()}")
else:
    print("Failed to load data")
```

**Error Conditions**:
- `FileNotFoundError`: CSV file missing
- `pd.errors.ParserError`: Malformed CSV data
- `KeyError`: Missing required columns

### Statistical Analysis

#### `create_statistics_overview(df, column)`

```python
def create_statistics_overview(df: pd.DataFrame, column: str) -> dict
```

**Purpose**: Generates comprehensive statistical summary for any numerical column.

**Parameters**:
- `df` (pd.DataFrame): Input dataframe
- `column` (str): Column name for analysis

**Returns**: Dictionary with statistical measures:
```python
{
    'mean': float,     # Arithmetic mean
    'min': float,      # Minimum value
    'max': float,      # Maximum value
    'median': float,   # Median value
    'std': float       # Standard deviation
}
```

**Example Usage**:
```python
# Analyze player ratings
rating_stats = create_statistics_overview(df, 'rating')
print(f"Average rating: {rating_stats['mean']:.3f}")
print(f"Rating range: {rating_stats['min']:.2f} - {rating_stats['max']:.2f}")

# Analyze maps played
map_stats = create_statistics_overview(df, 'total_maps')
print(f"Experience range: {map_stats['min']} - {map_stats['max']} maps")
```

**Supported Columns**:
- `rating`: Player performance rating
- `kd`: Kill/Death ratio
- `total_maps`: Maps played
- `total_rounds`: Rounds played
- `kd_diff`: Kill/Death difference

## Visualization Functions

### Statistical Charts

#### `plot_statistics_bar_chart(df, column, title, ylabel, color)`

```python
def plot_statistics_bar_chart(
    df: pd.DataFrame, 
    column: str, 
    title: str, 
    ylabel: str, 
    color: str = 'blue'
) -> go.Figure
```

**Purpose**: Creates interactive bar chart showing statistical measures.

**Parameters**:
- `df`: Source dataframe
- `column`: Numerical column to analyze
- `title`: Chart title
- `ylabel`: Y-axis label
- `color`: Bar color (default: 'blue')

**Returns**: Plotly Figure object with interactive features

**Features**:
- Automatic value annotations on bars
- Responsive design
- Interactive hover tooltips

**Example Usage**:
```python
# K/D ratio statistics
fig_kd = plot_statistics_bar_chart(
    df=player_data,
    column='kd',
    title='Kill/Death Ratio Statistics',
    ylabel='K/D Ratio',
    color='crimson'
)
st.plotly_chart(fig_kd, use_container_width=True)

# Maps played statistics
fig_maps = plot_statistics_bar_chart(
    df=player_data,
    column='total_maps',
    title='Maps Played Distribution',
    ylabel='Number of Maps',
    color='steelblue'
)
```

### Distribution Analysis

#### `plot_country_distribution(df)`

```python
def plot_country_distribution(df: pd.DataFrame) -> go.Figure
```

**Purpose**: Visualizes player distribution across countries.

**Parameters**:
- `df`: Player dataframe

**Returns**: Interactive bar chart showing country-wise player counts

**Features**:
- Automatic value labels
- Sorted by player count (descending)
- Responsive layout
- Country name rotation for readability

**Example Usage**:
```python
fig_countries = plot_country_distribution(filtered_players)
st.plotly_chart(fig_countries, use_container_width=True)

# Get country statistics
country_counts = df['country'].value_counts()
print(f"Top country: {country_counts.index[0]} ({country_counts.iloc[0]} players)")
```

#### `plot_rating_distribution(df)`

```python
def plot_rating_distribution(df: pd.DataFrame) -> go.Figure
```

**Purpose**: Creates histogram showing rating distribution patterns.

**Parameters**:
- `df`: Player dataframe

**Returns**: Interactive histogram with rating distribution

**Features**:
- Automatic bin calculation (30 bins)
- Semi-transparent bars for overlapping data
- Statistical distribution insights

**Example Usage**:
```python
fig_rating = plot_rating_distribution(top_players)
st.plotly_chart(fig_rating, use_container_width=True)

# Analyze distribution
ratings = df['rating']
print(f"Rating distribution: μ={ratings.mean():.3f}, σ={ratings.std():.3f}")
```

### Correlation Analysis

#### `plot_kd_vs_rating_scatter(df, title_suffix, top_n, min_maps)`

```python
def plot_kd_vs_rating_scatter(
    df: pd.DataFrame, 
    title_suffix: str = "", 
    top_n: int = None, 
    min_maps: int = None
) -> go.Figure
```

**Purpose**: Creates scatter plot analyzing K/D vs Rating relationship.

**Parameters**:
- `df`: Player dataframe
- `title_suffix`: Additional text for chart title
- `top_n`: Limit to top N players (optional)
- `min_maps`: Minimum maps filter (optional)

**Returns**: Interactive scatter plot with correlation analysis

**Features**:
- Player name annotations (for top 20 or fewer)
- Trend line for small datasets
- Hover tooltips with player details
- Correlation visualization

**Example Usage**:
```python
# All players correlation
fig_all = plot_kd_vs_rating_scatter(df)

# Top 20 players with names
fig_top20 = plot_kd_vs_rating_scatter(
    df, 
    title_suffix=" (Elite Players)", 
    top_n=20
)

# Experienced players (750+ maps)
experienced_df = df[df['total_maps'] > 750]
fig_exp = plot_kd_vs_rating_scatter(
    experienced_df, 
    title_suffix=" (Experienced Players)",
    min_maps=750,
    top_n=20
)

st.plotly_chart(fig_exp, use_container_width=True)
```

**Insights Provided**:
- Performance correlation patterns
- Outlier identification
- Player classification (aggressive vs. supportive)

## Utility Functions

### Insights Generation

#### `display_player_insights(df)`

```python
def display_player_insights(df: pd.DataFrame) -> None
```

**Purpose**: Generates and displays automated insights about player data.

**Parameters**:
- `df`: Player dataframe

**Side Effects**: Renders Streamlit components with insights

**Generated Insights**:
- K/D vs Rating correlation coefficient
- Geographic diversity statistics
- Performance pattern identification
- Dataset composition analysis

**Example Usage**:
```python
# Display insights for current dataset
display_player_insights(filtered_players)

# Manual correlation calculation
correlation = df['kd'].corr(df['rating'])
print(f"K/D-Rating correlation: {correlation:.3f}")
```

## Streamlit Components

### Page Configuration

```python
st.set_page_config(
    page_title="CS:GO Player Analysis Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Features**:
- Wide layout for better data visualization
- Gaming-themed icon and title
- Expanded sidebar for controls

### Interactive Controls

#### Sidebar Filters

```python
# Analysis type selection
analysis_type = st.sidebar.selectbox(
    "Selecione o tipo de análise:",
    ["Visão Geral", "Análise por País", "Distribuição de Rating", 
     "Relação K/D vs Rating", "Análise de Top Players"]
)

# Numerical filters
min_maps = st.sidebar.slider("Mínimo de mapas jogados:", 0, max_maps, 0)
min_rating = st.sidebar.slider("Rating mínimo:", min_rating, max_rating, min_rating)
```

#### Dynamic Metrics

```python
# Real-time metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Jogadores", len(filtered_df))
with col2:
    st.metric("Rating Médio", f"{filtered_df['rating'].mean():.3f}")
with col3:
    st.metric("K/D Médio", f"{filtered_df['kd'].mean():.3f}")
with col4:
    st.metric("Países Representados", filtered_df['country'].nunique())
```

### Analysis Views

#### 1. Overview Analysis
- Key performance metrics
- Statistical summaries
- Top player tables

#### 2. Country Analysis
- Geographic distribution
- Country-wise statistics
- International comparison

#### 3. Rating Distribution
- Histogram visualization
- Performance ranges
- Player concentration analysis

#### 4. K/D vs Rating Correlation
- Scatter plot analysis
- Multiple view options
- Performance insights

#### 5. Top Players Analysis
- Elite player comparison
- Customizable top-N analysis
- Detailed statistics

## Configuration

### Styling Configuration

```python
# Custom CSS styling
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
</style>
""", unsafe_allow_html=True)
```

### Chart Configuration

Default Plotly configuration:
```python
# Standard chart settings
fig.update_layout(
    height=400,                    # Standard height
    showlegend=False,             # Hide legend by default
    xaxis_tickangle=-45,          # Rotate x-axis labels
    margin=dict(l=0, r=0, t=40, b=0)  # Minimal margins
)
```

## Error Handling

### Data Loading Errors

```python
try:
    df = pd.read_csv("csgo_dados.csv")
    df = df.dropna()
    return df
except FileNotFoundError:
    st.error("❌ Data file 'csgo_dados.csv' not found.")
    return None
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    return None
```

### Visualization Errors

```python
try:
    fig = create_visualization(data)
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"❌ Error creating visualization: {str(e)}")
    st.info("Please check your data and try again.")
```

### Filter Validation

```python
# Validate filtered data
if len(filtered_df) == 0:
    st.warning("⚠️ No players match the current filters.")
    st.info("Try adjusting the filter values.")
else:
    # Proceed with analysis
    display_analysis(filtered_df)
```

## Performance Considerations

### Data Caching

```python
@st.cache_data
def load_data():
    """Cache data loading for better performance."""
    return pd.read_csv("csgo_dados.csv")

@st.cache_data
def expensive_calculation(df):
    """Cache expensive computations."""
    return df.groupby('country').agg({'rating': 'mean'})
```

### Optimization Tips

1. **Data Filtering**:
   ```python
   # Filter before visualization
   filtered_df = df[df['total_maps'] > threshold]
   fig = create_chart(filtered_df)  # Faster rendering
   ```

2. **Lazy Loading**:
   ```python
   # Only load visualization when needed
   if analysis_type == "Specific Analysis":
       fig = expensive_visualization(df)
       st.plotly_chart(fig)
   ```

3. **Memory Management**:
   ```python
   # Use efficient data types
   df['rating'] = pd.to_numeric(df['rating'], downcast='float')
   df['country'] = df['country'].astype('category')
   ```

### Recommended Limits

- **Maximum players for scatter plots**: 1000 points
- **Country distribution**: All countries (typically <50)
- **Top player analysis**: 5-50 players
- **Histogram bins**: 20-50 bins

## Usage Examples

### Basic Analysis Workflow

```python
# 1. Load data
df = load_data()
if df is None:
    st.stop()

# 2. Apply filters
min_rating = 1.05
experienced_players = df[df['rating'] >= min_rating]

# 3. Generate insights
stats = create_statistics_overview(experienced_players, 'rating')
st.write(f"High-rated players: {len(experienced_players)}")
st.write(f"Average rating: {stats['mean']:.3f}")

# 4. Create visualization
fig = plot_kd_vs_rating_scatter(experienced_players, " (High Rated)")
st.plotly_chart(fig)

# 5. Display detailed analysis
display_player_insights(experienced_players)
```

### Custom Analysis Example

```python
# Custom country-specific analysis
def analyze_country_performance(df, country):
    """Analyze performance for specific country."""
    country_players = df[df['country'] == country]
    
    if len(country_players) == 0:
        return None
    
    analysis = {
        'player_count': len(country_players),
        'avg_rating': country_players['rating'].mean(),
        'avg_kd': country_players['kd'].mean(),
        'top_player': country_players.loc[country_players['rating'].idxmax()]['name'],
        'total_experience': country_players['total_maps'].sum()
    }
    
    return analysis

# Usage
brazil_analysis = analyze_country_performance(df, 'Brazil')
if brazil_analysis:
    st.write(f"Brazil has {brazil_analysis['player_count']} top players")
    st.write(f"Average rating: {brazil_analysis['avg_rating']:.3f}")
```

This comprehensive API documentation provides all the information needed to understand, use, and extend the CS:GO Player Analysis Dashboard.