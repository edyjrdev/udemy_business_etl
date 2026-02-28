# Extrair dados da API da Udemy Business
# Etapa 01 courses
# Etapa 02 students
from auth import Auth
import requests
import json
import os
import pandas as pd
import base64

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
