import requests
import sqlite3
import time
from datetime import datetime

# --- Configuração ---
# ▼▼▼ COLE SUA CHAVE DA API AQUI DENTRO DAS ASPAS ▼▼▼
SUA_CHAVE_API = "COLOQUE_SUA_CHAVE_API_AQUI" 
APP_ID_GTAV = "271590"
NOME_BANCO_DADOS = "gta_players.db"
INTERVALO_SEGUNDOS = 600 # 600 segundos = 10 minutos
# --------------------

URL_API = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={APP_ID_GTAV}&key={SUA_CHAVE_API}"

def criar_banco():
    """Cria o banco de dados e a tabela se não existirem."""
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogadores_gta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        contagem_jogadores INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print(f"Banco de dados '{NOME_BANCO_DADOS}' verificado/criado.")

def get_players_online():
    """Busca o número atual de jogadores na API da Steam."""
    try:
        response = requests.get(URL_API)
        response.raise_for_status() # Lança um erro se a requisição falhar
        dados = response.json()
        
        if dados.get('response') and dados['response'].get('result') == 1:
            return dados['response']['player_count']
        else:
            print(f"Erro na resposta da API: {dados}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
        return None

def salvar_no_banco(contagem_jogadores):
    """Salva o carimbo de data/hora e a contagem de jogadores no banco SQLite."""
    if contagem_jogadores is None:
        return
        
    conn = sqlite3.connect(NOME_BANCO_DADOS)
    cursor = conn.cursor()
    timestamp_atual = datetime.now()
    
    cursor.execute(
        "INSERT INTO jogadores_gta (timestamp, contagem_jogadores) VALUES (?, ?)",
        (timestamp_atual, contagem_jogadores)
    )
    conn.commit()
    conn.close()
    print(f"[{timestamp_atual.strftime('%Y-%m-%d %H:%M:%S')}] Salvo: {contagem_jogadores} jogadores.")

# --- Loop Principal ---
if __name__ == "__main__":
    if SUA_CHAVE_API == "COLOQUE_SUA_CHAVE_API_AQUI":
        print("ERRO: Por favor, edite o script 'coletor.py' e adicione sua chave da API da Steam.")
    else:
        criar_banco()
        print(f"Iniciando coletor. Verificando a cada {INTERVALO_SEGUNDOS / 60} minutos.")
        print("Deixe este terminal aberto. Pressione Ctrl+C para parar.")
        try:
            while True:
                contagem = get_players_online()
                salvar_no_banco(contagem)
                time.sleep(INTERVALO_SEGUNDOS) # Pausa o script pelo tempo definido
        except KeyboardInterrupt:
            print("\nColetor interrompido pelo usuário.")
