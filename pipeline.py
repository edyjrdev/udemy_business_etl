# orquetrar ordem de execuçao
import os
import time

pipeline_files = ['extract.py', 'transform.py', 'translate.py', 'load.py', 'scrap.py',  'scrap_update.py']
pipeline_path = 'src'

start_pipeline = time.time()
print(f'Pipeline iniciou {time.ctime(start_pipeline)}')

for file in pipeline_files:
    print(f'Executar {file}')
    start_script = time.time()
    os.system(f'poetry run python {pipeline_path}/{file}')    
    end_script = time.time()
    print(f'Finalizado {file}. Tempo: {end_script - start_script:.2f}s')

end_pipeline = time.time()
print(f'Pipeline terminou. Tempo total: {end_pipeline - start_pipeline:.2f}s')