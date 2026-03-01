import pandas as pd
import os
import json

# in
pages_dim = 'model/1_silver'

idioma_audio_path = os.path.join(pages_dim, 'idioma_audio.json')
idioma_legenda_path = os.path.join(pages_dim, 'idioma_legenda.json')
mapa_idioma = 'mapa_idioma'
mapa_idioma_json = os.path.join(pages_dim, mapa_idioma + '.json')

def criar_mapa_idiomas(path_audio, path_legenda):
    # 1. Carregar os arquivos JSON
    with open(path_audio, 'r', encoding='utf-8') as f:
        data_audio = json.load(f)
    
    with open(path_legenda, 'r', encoding='utf-8') as f:
        data_legenda = json.load(f)

    # 2. Converter para DataFrames
    df_audio = pd.DataFrame(data_audio)
    df_legenda = pd.DataFrame(data_legenda)

    # 3. Função de agrupamento (Lógica de Tronco Linguístico)
    def definir_grupo(texto):
        if not texto: return "Outros"
        t = texto.lower()
        
        # Mapeamento de palavras-chave para Grupos
        if any(x in t for x in ["english", "inglês"]): return "Língua Inglesa"
        if any(x in t for x in ["spanish", "espanhol"]): return "Língua Espanhola"
        if any(x in t for x in ["portugue", "português"]): return "Língua Portuguesa"
        if any(x in t for x in ["chinese", "chinês", "zh_"]): return "Língua Chinesa"
        if any(x in t for x in ["french", "francês"]): return "Língua Francesa"
        if any(x in t for x in ["german", "alemão", "deutsch"]): return "Língua Alemã"
        if any(x in t for x in ["italian", "italiano"]): return "Língua Italiana"
        if any(x in t for x in ["dutch", "holandês", "nederlands"]): return "Língua Holandesa"
        if any(x in t for x in ["russian", "russo"]): return "Língua Russa"
        if any(x in t for x in ["japanese", "japonês"]): return "Língua Japonesa"
        if any(x in t for x in ["hindi", "hi_in"]): return "Língua Indiana (Hindi/etc)"
        
        return "Outros Idiomas"

    # 4. Processar Áudio
    # Usamos o 'english_title' para classificar o grupo
    df_audio['lingua'] = df_audio['english_title'].apply(definir_grupo)
    
    # 5. Processar Legenda
    # Usamos o 'idioma_legenda' para classificar o grupo
    df_legenda['lingua'] = df_legenda['idioma_legenda'].apply(definir_grupo)

    # 6. Unificar em uma única Dimensão de Idiomas
    # Padronizamos os nomes das colunas para o merge
    base_audio = df_audio[['idioma_audio_ptbr', 'lingua']].rename(columns={'idioma_audio_ptbr': 'nome_exibicao'})
    base_legenda = df_legenda[['idioma_legenda_ptbr', 'lingua']].rename(columns={'idioma_legenda_ptbr': 'nome_exibicao'})

    # Concatenar e remover duplicatas
    dim_idiomas = pd.concat([base_audio, base_legenda]).drop_duplicates().reset_index(drop=True)
    
    return dim_idiomas

def salva_mapa_idiomas(df_final):
    print("Mapa de Idiomas criado com sucesso!")
    # print(df_final.sort_values(by="lingua").to_string())
    
    # Salvar resultado
    df_final.to_json(mapa_idioma_json, orient='records', indent=4, force_ascii=False ) 

# agrupando idiomas
df_final = criar_mapa_idiomas(idioma_audio_path, idioma_legenda_path)
salva_mapa_idiomas(df_final)