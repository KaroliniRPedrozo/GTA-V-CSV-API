import pandas as pd
import plotly.express as px
import sqlite3

# --- Nomes dos Arquivos ---
NOME_ARQUIVO_CSV = 'gta_data.csv'
NOME_BANCO_DADOS = 'gta_players.db'

def carregar_dados_csv():
    """Carrega o histórico de médias mensais do CSV."""
    try:
        dados_csv = pd.read_csv(NOME_ARQUIVO_CSV)
    except pd.errors.ParserError:
        dados_csv = pd.read_csv(NOME_ARQUIVO_CSV, sep=';')
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{NOME_ARQUIVO_CSV}' não encontrado. Pulando dados históricos.")
        return None
        
    # Converte para data
    try:
        dados_csv['mes'] = pd.to_datetime(dados_csv['mes'])
    except Exception as e:
        print(f"Erro ao converter 'mes' do CSV: {e}")
        print("Verifique se o CSV está limpo (sem 'Last 30 Days' etc.)")
        return None
    
    # Padroniza os nomes das colunas
    dados_csv = dados_csv.rename(columns={'mes': 'data', 'jogadores': 'contagem'})
    
    # Adiciona a coluna 'tipo' para o gráfico
    dados_csv['tipo'] = 'Média Mensal (Histórico)'
    
    return dados_csv

def carregar_dados_api():
    """Carrega os dados em tempo real (coletados) do banco SQLite."""
    try:
        conn = sqlite3.connect(NOME_BANCO_DADOS)
        dados_api = pd.read_sql_query(
            "SELECT timestamp, contagem_jogadores FROM jogadores_gta", 
            conn,
            parse_dates=['timestamp']
        )
        conn.close()
        
        # Padroniza os nomes das colunas
        dados_api = dados_api.rename(columns={'timestamp': 'data', 'contagem_jogadores': 'contagem'})
        
        # Adiciona a coluna 'tipo' para o gráfico
        dados_api['tipo'] = 'Tempo Real (API)'
        
        return dados_api
    except Exception as e:
        print(f"Aviso: Não foi possível ler o banco de dados da API '{NOME_BANCO_DADOS}'. {e}")
        return None

def plotar_grafico_combinado(df):
    """Cria e exibe o gráfico interativo combinado."""
    if df is None or df.empty:
        print("Nenhum dado para plotar.")
        return
        
    print("Gerando gráfico combinado com Plotly...")

    # --- Mapeamento de Cores ---
    mapa_de_cores = {
        'Média Mensal (Histórico)': '#FFFFFF',  # Branco
        'Tempo Real (API)': '#2CA02C'          # Verde
    }
    
    # --- Mapeamento de Marcadores ---
    mapa_de_marcadores = {
        'Média Mensal (Histórico)': False, # Sem bolinhas
        'Tempo Real (API)': True          # Com bolinhas
    }

    fig = px.line(
        df,
        x='data',
        y='contagem',
        title='Histórico Completo de Jogadores de GTA V',
        labels={'data': 'Data', 'contagem': 'Jogadores', 'tipo': 'Fonte dos Dados'},
        color='tipo',                  # <-- A mágica: cria uma linha por 'tipo'
        markers=df['tipo'].map(mapa_de_marcadores), # Aplica marcadores baseado no tipo
        color_discrete_map=mapa_de_cores # Usa nosso mapa de cores
    )

    # --- Aplica o Modo Escuro ---
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Data",
        yaxis_title="Número de Jogadores",
        legend_title_text='Fonte dos Dados' # Título da legenda
    )

    # --- Adiciona os Botões de Filtro ---
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=30, label="30 dias", step="day", stepmode="backward"),
                dict(count=3, label="3 meses", step="month", stepmode="backward"),
                dict(count=6, label="6 meses", step="month", stepmode="backward"),
                dict(count=1, label="1 ano", step="year", stepmode="backward"),
                dict(count=3, label="3 anos", step="year", stepmode="backward"),
                dict(count=6, label="6 anos", step="year", stepmode="backward"),
                dict(label="Tudo", step="all")
            ]),
            bgcolor="#333",
            activecolor="#555"
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )

    fig.show()
    print("Gráfico pronto. Verifique seu navegador!")

# --- Principal ---
if __name__ == "__main__":
    print("Carregando dados históricos do CSV...")
    df_csv = carregar_dados_csv()
    
    print("Carregando dados em tempo real da API (do banco)...")
    df_api = carregar_dados_api()
    
    # Junta os dois DataFrames em um só
    df_final = pd.concat([df_csv, df_api])
    
    # Garante que está tudo em ordem de data
    if not df_final.empty:
        df_final = df_final.sort_values(by='data')
    
    plotar_grafico_combinado(df_final)
