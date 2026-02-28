# Extrair dados da API da Udemy Business
# Etapa 01 courses
# Etapa 02 students
from auth import Auth
import requests
import json
import os
import pandas as pd
import base64
import time

creds = Auth().start()
curso_por_pagina = 100
TIMEOUT_API = 300

# out
pages_dir = 'model/0_bronze/1_page'
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

base_api = f"https://{creds['account_name']}.udemy.com/api-2.0/organizations/{creds['account_id']}"
endpoints = {
    'course': f'{base_api}/courses/list',
}

auth_str = f"{creds['clientid']}:{creds['secretid']}"
encoded = base64.b64encode(auth_str.encode()).decode()
session = requests.Session()
session.headers.update({"Authorization": f"Basic {encoded}", "Content-Type": "application/json"})

print(endpoints['course'])

pagina_atual = 1
while True:
    file_name = os.path.join(pages_dir, f'pag_{pagina_atual:03}.json')
    
    if os.path.exists(file_name):
        print(f'Pagina {pagina_atual} ja existe no cache. Pulando.')
        pagina_atual += 1
        continue

    url = f"{endpoints['course']}?page_size={curso_por_pagina}&page={pagina_atual}"
    
    response = session.get(url, timeout=TIMEOUT_API)
    
    if response.status_code == 200:
        data = response.json()
        lista_cursos = data['results']
        
        if not lista_cursos:
            print('Nenhum curso encontrado nesta pagina. Finalizando.')
            break
            
        with open(file=file_name, mode='w', encoding='utf-8') as file_json:
            json.dump(lista_cursos, file_json, ensure_ascii=False, indent=4)
            print(f'Arquivo salvo {file_json.name}')
            
        if not data.get('next'):
            print('Ultima pagina alcancada.')
            break
            
        pagina_atual += 1
    else:
        print(f'Erro {response.status_code} na pagina {pagina_atual}')
        break

print('Finalizado.')
