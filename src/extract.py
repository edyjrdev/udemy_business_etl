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
import sys

creds = Auth().start()
curso_por_pagina = 100
TIMEOUT_API = 300
CACHE_DAYS = 1

# out
pages_dir = 'model/0_bronze/1_page'
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

# Check cache
if os.path.exists(pages_dir):
    files = [f for f in os.listdir(pages_dir) if f.endswith('.json')]
    if files:
        # Check modification time of the first file
        file_path = os.path.join(pages_dir, files[0])
        file_mod_time = os.path.getmtime(file_path)
        if (time.time() - file_mod_time) < (CACHE_DAYS * 86400):
            print(f'Cache válido (menos de {CACHE_DAYS} dias). Pulando extração.')
            sys.exit(0)

base_api = f"https://{creds['account_name']}.udemy.com/api-2.0/organizations/{creds['account_id']}"
endpoints = {
    'course': f'{base_api}/courses/list',
}

auth_str = f"{creds['clientid']}:{creds['secretid']}"
encoded = base64.b64encode(auth_str.encode()).decode()
session = requests.Session()
session.headers.update({"Authorization": f"Basic {encoded}", "Content-Type": "application/json"})

print(endpoints['course'])

response = session.get(f"{endpoints['course']}?page_size={curso_por_pagina}", timeout=TIMEOUT_API)
if response.status_code == 200:
    pagina_atual = 1
    data = response.json()
    total_cursos = data['count']
    proxima_pagina = data['next']
    lista_cursos = data['results']
    print(f'Total de cursos: {total_cursos} | Proxima pagina: {proxima_pagina} | Total Cursos Pagina: {len(lista_cursos)}')
    with open(file=os.path.join(pages_dir, f'pag_{pagina_atual:03}.json'), mode='w', encoding='utf-8') as file_json:
        json.dump(lista_cursos, file_json, ensure_ascii=False, indent=4)
        print(f'Arquivo salvo {file_json.name}')
    while proxima_pagina:
    
        response = session.get(proxima_pagina, timeout=TIMEOUT_API)

        if response.status_code == 200:
            data = response.json()
            proxima_pagina = data['next']
            conteudo_pag = data['results']
            pagina_atual += 1
            print(f'Pagina Atual: {pagina_atual}')
            with open(file=os.path.join(pages_dir, f'pag_{pagina_atual:03}.json'), mode='w', encoding='utf-8') as file_json:
                json.dump(conteudo_pag, file_json, ensure_ascii=False, indent=4)
                print(f'Arquivo salvo {file_json.name}')
        else:
            print(response.status_code, 'erro')
            break
    
    print('Finalizado.')
else:
    print(response.status_code, 'erro')
