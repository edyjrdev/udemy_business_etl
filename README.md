# Udemy Business ETL Pipeline

Este projeto é um pipeline de ETL (Extract, Transform, Load) desenvolvido em Python para extrair dados da API da Udemy Business, processá-los, traduzir termos para Português (PT-BR) e enriquecer as informações através de Web Scraping.

## 📋 Visão Geral

O pipeline automatiza o fluxo de dados seguindo a arquitetura de medalhão (Bronze, Silver, Gold - implícito), garantindo que os dados sejam extraídos de forma incremental e processados eficientemente.

### Funcionalidades Principais
*   **Extração Incremental:** Baixa dados de cursos da API da Udemy com paginação e cache local para evitar requisições duplicadas.
*   **Tradução Automática:** Traduz categorias, idiomas e tópicos utilizando a API do Google Translate, com sistema de cache para otimizar custos e tempo.
*   **Relatório Consolidado:** Gera um arquivo Excel (`udemy_consolidado.xlsx`) com todos os dados integrados para análise.
*   **Orquestração:** Script centralizado para executar todas as etapas do pipeline sequencialmente.
*   **Gerenciamento de Dependências:** Utiliza Poetry.

## 🚀 Arquitetura do Pipeline

O projeto é modularizado em scripts localizados em `src/`, orquestrados pelo `pipeline.py`. O fluxo de dados segue as seguintes etapas:

1.  **`extract.py`**:
    *   **Função:** Extração de dados brutos da API da Udemy Business.
    *   **Lógica:** Realiza paginação automática e verifica se o arquivo da página já existe localmente para evitar requisições desnecessárias (Cache de Arquivo).
    *   **Saída:** Arquivos JSON em `model/0_bronze/1_page/pag_*.json`.

2.  **`transform.py`** (Inferido):
    *   **Função:** Limpeza e normalização.
    *   **Lógica:** Processa os arquivos da camada Bronze, normaliza estruturas e separa dimensões.
    *   **Saída:** Arquivos JSON em `model/1_silver/` (ex: `categoria.json`, `instrutor.json`).

3.  **`translate.py`**:
    *   **Função:** Enriquecimento e Tradução.
    *   **Lógica:** Lê as dimensões da camada Silver, traduz termos para PT-BR usando Google Translate e atualiza os arquivos originais.
    *   **Cache:** Utiliza `model/0_bronze/translation_cache.json` para armazenar termos já traduzidos e economizar chamadas de API.
    *   **Saída:** Atualiza os arquivos em `model/1_silver/` adicionando campos com sufixo `_ptbr`.

4.  **`load.py`** (Inferido):
    *   **Função:** Carga de dados.
    *   **Lógica:** Consome os dados tratados da camada Silver para o destino final (Data Warehouse ou Banco de Dados).

5.  **`scrap.py` & `scrap_update.py`** (Inferido):
    *   Realiza raspagem de dados complementares que não estão disponíveis na API padrão.

## 🛠️ Pré-requisitos

*   Python 3.x
*   Poetry para gerenciamento de dependências.
*   Credenciais de API da Udemy Business.

## ⚙️ Configuração

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd udemy_business_etl
    ```

2.  **Instale as dependências:**
    ```bash
    poetry install
    ```

3.  **Configure as Credenciais:**
    Crie um arquivo `auth/credencial.json` (ou configure a classe `Auth` conforme sua implementação) com as chaves:
    *   `clientid`
    *   `secretid`
    *   `account_id`
    *   `account_name`

## ▶️ Como Executar

Para rodar o pipeline completo utilizando o Poetry:

```bash
poetry run python pipeline.py
```

O script exibirá o progresso de cada etapa e o tempo de execução.

## 📂 Estrutura de Pastas

A estrutura do projeto é organizada para separar lógica, dados e configurações:

*   `src/`: Contém o código fonte dos scripts do pipeline.
    *   `extract.py`: Extração da API.
    *   `transform.py`: Limpeza e normalização.
    *   `translate.py`: Tradução de termos.
    *   `load.py`: Carga de dados.
    *   `scrap.py` / `scrap_update.py`: Web scraping complementar.
*   `model/`: Data Lake local (armazenamento de arquivos).
    *   `0_bronze/`: Dados brutos.
        *   `1_page/`: Respostas JSON paginadas da API.
        *   `translation_cache.json`: Cache de traduções.
    *   `1_silver/`: Dados processados e normalizados (Dimensões).
    *   `2_gold/`: Dados agregados e finais.
        *   `udemy_consolidado.xlsx`: [📥 Baixar Amostra](model/2_gold/udemy_consolidado.xlsx)
*   `auth/`: Credenciais e segurança (não versionado).
    *   `credencial.json`: Chaves de acesso à API.
*   `pipeline.py`: Script principal de orquestração.
*   `pyproject.toml`: Definição de dependências do projeto.

---
Desenvolvido para automação de dados corporativos da Udemy.
