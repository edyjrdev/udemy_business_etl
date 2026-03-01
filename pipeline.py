# orquetrar ordem de execuçao
import os

pipeline_files = ['extract.py', 'transform.py','translate.py', 'mapa_idioma.py' 'scrap.py',  'scrap_update.py', 'load.py']
# pipeline_files = ['transform.py','translate.py', 'mapa_idioma.py','scrap_update.py', 'load.py']
pipeline_path = 'src'

for file in pipeline_files:
    print(f'Executar {file}')
    os.system(f'poetry run python {pipeline_path}/{file}')    
    print(f'Finalizado {file}')