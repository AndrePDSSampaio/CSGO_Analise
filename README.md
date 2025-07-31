# 🎮 CS:GO Player Analysis Dashboard

Uma aplicação interativa em Streamlit para análise de dados de jogadores profissionais de Counter-Strike: Global Offensive.

## 📋 Sobre o Projeto

Este projeto analisa um conjunto de dados que incluem jogadores de Counter Strike: Global Offensive com rating acima de 1.00 entre os anos de 2015-2020, considerado um padrão bom para o nível profissional do jogo.

### 📊 Dados Analisados

O arquivo CSV inclui as seguintes informações:

- **Nome**: Nome do jogador
- **País**: País de origem
- **Time de Destaque**: Equipes principais
- **Número Total de Mapas Jogados**: Experiência competitiva
- **Número Total de Rounds Jogados**: Volume de jogo
- **Diferença entre Baixas/Mortes**: Eficiência de eliminações
- **Relação Baixas/Mortes (K/D)**: Métrica de performance
- **Rating**: Avaliação geral do jogador

## 🚀 Configuração e Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**:
```bash
git clone <repository-url>
cd csgo-analysis
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**:
```bash
streamlit run streamlit_app.py
```

4. **Acesse no navegador**:
A aplicação será aberta automaticamente em `http://localhost:8501`

## 📚 Documentação da API

### Estrutura da Aplicação

#### Função Principal
```python
def main()
```
Função principal que coordena toda a aplicação Streamlit.

#### Funções de Carregamento de Dados

##### `load_data()`
```python
@st.cache_data
def load_data() -> pd.DataFrame
```
**Descrição**: Carrega e processa os dados do arquivo CSV.

**Retorno**: DataFrame com os dados dos jogadores ou None em caso de erro.

**Exemplo de uso**:
```python
df = load_data()
if df is not None:
    # Processar dados
    print(f"Dados carregados: {len(df)} jogadores")
```

#### Funções de Análise Estatística

##### `create_statistics_overview(df, column)`
```python
def create_statistics_overview(df: pd.DataFrame, column: str) -> dict
```
**Descrição**: Gera uma visão estatística geral de uma coluna específica.

**Parâmetros**:
- `df`: DataFrame com os dados
- `column`: Nome da coluna para análise

**Retorno**: Dicionário com estatísticas (média, mínimo, máximo, mediana, desvio padrão)

**Exemplo**:
```python
stats = create_statistics_overview(df, 'rating')
print(f"Rating médio: {stats['mean']:.2f}")
```

#### Funções de Visualização

##### `plot_statistics_bar_chart(df, column, title, ylabel, color)`
```python
def plot_statistics_bar_chart(
    df: pd.DataFrame, 
    column: str, 
    title: str, 
    ylabel: str, 
    color: str = 'blue'
) -> go.Figure
```
**Descrição**: Cria um gráfico de barras interativo com estatísticas.

**Parâmetros**:
- `df`: DataFrame com os dados
- `column`: Coluna para análise
- `title`: Título do gráfico
- `ylabel`: Rótulo do eixo Y
- `color`: Cor das barras (padrão: 'blue')

**Retorno**: Figura Plotly interativa

**Exemplo**:
```python
fig = plot_statistics_bar_chart(
    df, 'kd', 
    'Estatísticas K/D', 
    'Relação K/D', 
    'red'
)
st.plotly_chart(fig)
```

##### `plot_country_distribution(df)`
```python
def plot_country_distribution(df: pd.DataFrame) -> go.Figure
```
**Descrição**: Cria gráfico de distribuição de jogadores por país.

**Parâmetros**:
- `df`: DataFrame com os dados

**Retorno**: Figura Plotly com distribuição por país

##### `plot_rating_distribution(df)`
```python
def plot_rating_distribution(df: pd.DataFrame) -> go.Figure
```
**Descrição**: Cria histograma da distribuição de ratings.

**Parâmetros**:
- `df`: DataFrame com os dados

**Retorno**: Histograma Plotly interativo

##### `plot_kd_vs_rating_scatter(df, title_suffix, top_n, min_maps)`
```python
def plot_kd_vs_rating_scatter(
    df: pd.DataFrame, 
    title_suffix: str = "", 
    top_n: int = None, 
    min_maps: int = None
) -> go.Figure
```
**Descrição**: Cria gráfico de dispersão K/D vs Rating.

**Parâmetros**:
- `df`: DataFrame com os dados
- `title_suffix`: Texto adicional para o título
- `top_n`: Número de top jogadores (opcional)
- `min_maps`: Filtro mínimo de mapas (opcional)

**Retorno**: Gráfico de dispersão Plotly

**Exemplo**:
```python
# Análise top 20 com mais de 750 mapas
fig = plot_kd_vs_rating_scatter(
    df, " (Top 20, Experientes)", 
    top_n=20, 
    min_maps=750
)
```

#### Funções de Insights

##### `display_player_insights(df)`
```python
def display_player_insights(df: pd.DataFrame) -> None
```
**Descrição**: Exibe insights automáticos sobre os dados.

**Parâmetros**:
- `df`: DataFrame com os dados

**Funcionalidades**:
- Calcula correlação K/D vs Rating
- Mostra diversidade geográfica
- Apresenta padrões de performance

## 🎯 Funcionalidades da Interface

### Sidebar (Barra Lateral)

#### Controles de Análise
- **Tipo de Análise**: Seleção entre 5 tipos de análise
- **Filtros Interativos**:
  - Mínimo de mapas jogados (slider)
  - Rating mínimo (slider)
- **Contador de Jogadores**: Atualização em tempo real após filtros

#### Tipos de Análise Disponíveis

1. **Visão Geral**
   - Métricas principais
   - Estatísticas de mapas e K/D
   - Top 20 jogadores

2. **Análise por País**
   - Distribuição geográfica
   - Estatísticas por país
   - Ranking de países

3. **Distribuição de Rating**
   - Histograma de ratings
   - Análise por faixas
   - Concentração de jogadores

4. **Relação K/D vs Rating**
   - Gráficos de dispersão
   - Análise de correlação
   - Visualizações específicas (Top 20, Top 50, etc.)

5. **Análise de Top Players**
   - Comparação de elite
   - Análise personalizada (5-50 jogadores)
   - Detalhes completos

### Componentes Interativos

#### Métricas em Tempo Real
```python
st.metric("Total de Jogadores", len(filtered_df))
st.metric("Rating Médio", f"{filtered_df['rating'].mean():.3f}")
```

#### Filtros Dinâmicos
```python
min_maps = st.sidebar.slider("Mínimo de mapas jogados:", 0, max_maps, 0)
filtered_df = df[df['total_maps'] >= min_maps]
```

#### Tabelas Interativas
```python
st.dataframe(df, use_container_width=True)
```

## 📊 Exemplos de Uso

### Uso Básico
```python
# Executar a aplicação
streamlit run streamlit_app.py
```

### Análise Programática
```python
import pandas as pd
from streamlit_app import load_data, create_statistics_overview

# Carregar dados
df = load_data()

# Analisar ratings
rating_stats = create_statistics_overview(df, 'rating')
print(f"Rating médio: {rating_stats['mean']:.3f}")

# Filtrar top players
top_players = df.head(10)
print(top_players[['name', 'country', 'rating']])
```

### Análise Customizada
```python
# Filtrar jogadores por critérios específicos
experienced_players = df[df['total_maps'] > 1000]
brazilian_players = df[df['country'] == 'Brazil']

# Calcular correlações
correlation = df['kd'].corr(df['rating'])
print(f"Correlação K/D vs Rating: {correlation:.3f}")
```

## 🔧 Personalização

### Adicionando Novas Análises

1. **Criar nova função de análise**:
```python
def plot_custom_analysis(df):
    # Sua análise personalizada
    fig = go.Figure()
    # Configurar gráfico
    return fig
```

2. **Adicionar ao menu principal**:
```python
analysis_type = st.sidebar.selectbox(
    "Selecione o tipo de análise:",
    ["Visão Geral", "Nova Análise"]  # Adicionar aqui
)
```

3. **Implementar na lógica principal**:
```python
elif analysis_type == "Nova Análise":
    fig = plot_custom_analysis(filtered_df)
    st.plotly_chart(fig)
```

### Modificando Estilos

O CSS customizado está definido no início do arquivo:
```python
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        /* Personalizar aqui */
    }
</style>
""", unsafe_allow_html=True)
```

## 📈 Insights Principais

### Correlações Descobertas
- **K/D vs Rating**: Correlação positiva forte (≈0.8)
- **Mapas vs Performance**: Experiência influencia consistência
- **Geografia vs Talento**: Distribuição global interessante

### Padrões Identificados
- Jogadores agressivos: Maior rating proporcionalmente ao K/D
- Jogadores de suporte: K/D alto, rating proporcional
- Experiência: +750 mapas indica jogadores estabelecidos

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Arquivo CSV não encontrado**:
```bash
# Verificar se o arquivo existe
ls -la csgo_dados.csv
```

2. **Dependências em falta**:
```bash
pip install -r requirements.txt
```

3. **Porta ocupada**:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Performance

- Use `@st.cache_data` para operações custosas
- Filtre dados antes de visualizar
- Limite o número de pontos em gráficos grandes

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente melhorias
4. Adicione testes se necessário
5. Submeta um pull request

## 📄 Licença

Este projeto é para fins educacionais e de análise de dados esportivos.

---

**Desenvolvido com ❤️ usando Streamlit, Plotly e Pandas**
