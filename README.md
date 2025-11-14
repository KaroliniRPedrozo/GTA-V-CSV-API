# 📊 Dashboard de Jogadores GTA V (Histórico + Tempo Real)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-Made%20with-blue.svg?logo=plotly)
![GitHub last commit](https://img.shields.io/github/last-commit/SEU-USUARIO/SEU-REPOSITORIO)

Um dashboard interativo que combina dados históricos (desde 2015) com dados em tempo real (API da Steam) da contagem de jogadores de Grand Theft Auto V. O gráfico é renderizado em modo escuro com filtros interativos.

---

## ✨ Funcionalidades Principais

* **Gráfico Combinado:** Exibe o histórico de média mensal (desde 2015) e a contagem em tempo real (a cada 10 min) no mesmo gráfico.
* **Interativo:** Feito com Plotly, permite zoom, "pan" e tooltips flutuantes que mostram os dados exatos.
* **Filtros de Tempo:** Inclui botões para zoom rápido ("30 dias", "3 meses", "1 ano", "Tudo", etc.).
* **Estilo Moderno:** Tema escuro (`dark_background`) com linhas de dados coloridas (Branco/Verde) para fácil distinção.
* **Coleta Automática:** O script `coletor.py` constrói seu próprio banco de dados de alta frequência ao longo do tempo.

---

## ⚙️ Como Funciona (Arquitetura)

O projeto é dividido em dois fluxos de dados que se unem no final:

[Fluxo Histórico]

Dados do SteamCharts (Manual) --> gta_data.csv

[Fluxo Tempo Real] 2. API da Steam --> coletor.py --> gta_players.db

[Visualização] (gta_data.csv + gta_players.db) --> grafico_combinado.py --> Gráfico Interativo (Plotly)

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Plotly:** Para a visualização interativa.
* **Pandas:** Para carregar, limpar e combinar os dados.
* **Requests:** Para fazer chamadas à API da Steam.
* **SQLite3:** Para armazenar os dados coletados pela API.

---

## 🚀 Guia de Instalação e Execução

Siga estes passos para rodar o projeto localmente.

### 1. Pré-requisitos

* Você precisa ter o **Git** e o **Python 3.10+** instalados.
* Você precisa de uma **Chave da API da Steam** (gratuita): [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)

### 2. Instalação

Primeiro, clone o repositório e instale as dependências.

```bash
# 1. Clone este repositório
git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
```

## 2. Entre na pasta do projeto

cd SEU-REPOSITORIO

## 3. Instale as bibliotecas necessárias

## (Recomendado: crie um 'requirements.txt' com 'pip freeze > requirements.txt')

pip install pandas plotly requests

### 3. Configuração (Passos Manuais)

Você precisa fazer estes dois passos antes de executar:

**Passo 1: Configurar a Chave da API**
Abra o arquivo `coletor.py`.

Na Linha 9, cole sua Chave da API da Steam na variável `SUA_CHAVE_API`.

```bash
SUA_CHAVE_API = "COLOQUE_SUA_CHAVE_API_AQUI"
```

Salve o arquivo.

**Passo 2: Criar o Arquivo de Histórico (`gta_data.csv`)**
Crie um novo arquivo na pasta do projeto chamado `gta_data.csv`.

Vá ao SteamCharts para GTA V e copie os dados da tabela (de 2015 até hoje).

Formate o CSV: O arquivo deve seguir este formato:

A Linha 1 deve ser exatamente: `mes,jogadores`

A Linha 2 deve ser o primeiro dado (ex: `October 2025,57282.5`)

Remova qualquer linha de texto que não seja dado (ex: `"Last 30 Days"`).

Remova as vírgulas dos números (ex: `57,282.5 -> 57282.5`).

Salve o arquivo `gta_data.csv`.

### 4. Execução (Processo de 2 Terminais)

Este projeto precisa de dois terminais rodando simultaneamente.

**Terminal 1: O Coletor (Deixe rodando)**
Este terminal inicia o "robô" que coleta dados da API e os salva no banco `gta_players.db`.

```bash
python coletor.py
```

Você verá: `Iniciando coletor...` Deixe este terminal aberto e minimizado.

**Terminal 2: O Dashboard**
Este terminal é o que você usa para ver o gráfico.

Espere alguns minutos (10-20 min) para que o Terminal 1 colete alguns dados.

Abra um NOVO terminal.

Execute o script do gráfico combinado:

```bash
python grafico_combinado.py
```

O script vai carregar os dois arquivos (`.csv` e `.db`), juntá-los e abrir o gráfico interativo no seu navegador padrão.

### 📁 Estrutura de Arquivos

```bash
.
├── .gitignore          # (Recomendado: para ignorar o .db)
├── coletor.py          # O robô coletor da API
├── grafico_combinado.py # O script principal do dashboard
├── gta_data.csv        # O histórico manual (você deve criar)
├── gta_players.db      # O banco (criado pelo coletor)
├── LICENSE             # Sua licença (ex: MIT)
└── README.md           # Este arquivo
```
