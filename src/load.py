import pandas as pd
import os
import json

sep_csv ='|'
enconding = 'utf-8'
# in
pages_dim = 'model/1_silver'
# out
dim_gold = 'model/2_gold'
if not os.path.exists(dim_gold):
    os.makedirs(dim_gold)



# mapper de colunas
map_file_hearders ={
    "categoria_curso.json":{0:'id_curso', 1:'categoria'},
    "categoria.json":{0:'categoria',1:'categoria_ptbr'},
    "curso.json":{0:'id',1:'titulo',2: 'url',3: 'aulas',4:'videos',5: 'idioma', 6:'categoria',7: 'subcategoria',8: 'quizes',
    9: 'testes',10: 'tem_legenda',11: 'video_duracao',12: 'data_atualizacao',13: 'nivel',
    14: 'chamada',15: 'descricao',16: 'nota',17: 'num_alunos',18: 'num_avaliacoes',19: 'valor',20: 'moeda',21: 'data_extracao'},
    "instrutor_curso.json":{0:'id_curso',1: 'instrutor'},
    "instrutor.json":{0:'instrutor'},
    "idioma_audio_curso.json":{0:'id_curso',1: 'idioma_audio'},
    "idioma_audio.json":{0:'idioma_audio',1:'titulo',2:'english_title',3:'idioma_audio_ptbr'},
    "idioma_legenda_curso.json":{1:'id_curso',1: 'idioma_legenda'},
    "idioma_legenda.json":{0:'idioma_legenda', 1:'idioma_legenda_ptbr'},
    "topico_curso.json":{0:'id_curso',1:'topico'},
    "topico_curso.json":{0:'id_curso',1:'topico'},
    "topico.json":{0:'id_topico',1:'titulo',2:'url',3:'titulo_ptbr'},
    "mapa_idioma.json":{0:'idioma',1:'lingua'}
}


if os.path.exists(pages_dim):
    files = os.listdir(pages_dim)
    for file in files:
        file_path = os.path.join(pages_dim, file)
        df = pd.read_json(file_path)
        colunas = map_file_hearders[file]
        
        df.rename(columns=colunas, inplace=True)
        try:
            name_csv = file.replace('.json','.csv')
            file_csv = os.path.join(dim_gold,name_csv) 
            
            df.to_csv(file_csv, index=False, sep=sep_csv, encoding=enconding, quotechar='"', header=True)
        except Exception as e:
            print(f'Erro na criacao de {file}', e)

# 1. Initialize the ExcelWriter
name_xlsx = 'udemy_consolidado.xlsx' 
name_xlsx_path = os.path.join(dim_gold, name_xlsx)

# O segredo está aqui: o 'with' mantém o arquivo aberto até o fim do loop
with pd.ExcelWriter(name_xlsx_path, engine='xlsxwriter') as writer:
    for file in files:
        file_path = os.path.join(pages_dim, file)
        
        try:
            # Lendo o JSON
            df = pd.read_json(file_path)
            # 1. Renomear colunas mantendo a ordem original
            # Se o JSON não tem nomes, o pandas usa números (0, 1, 2...)
            colunas = map_file_hearders[file]
            df.rename(columns=colunas, inplace=True)
            
            # 2. Definir o nome da aba (máximo 31 caracteres)
            sheet_name = file.replace('.json', '')[:31]
            
            # 3. Salvar na sheet específica dentro do mesmo arquivo
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"Sheet '{sheet_name}' adicionada com sucesso.")
            
        except Exception as e:
            print(f'Erro ao processar {file}: {e}')

print(f"Successfully created {name_xlsx_path} with multiple sheets.")


