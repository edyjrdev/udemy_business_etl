import os
import json

# in
pages_scrap = 'model/0_bronze/3_scrap'
arquivo_cursos = r'model\1_silver\curso.json'

if os.path.exists(pages_scrap):
    scraps = os.listdir(pages_scrap)
    scrap_list = []
    for scrap in scraps:
        scrap_path = os.path.join(pages_scrap, scrap)
        try:
            with open(file=scrap_path, mode='r', encoding='utf-8') as scrap_json:
                scrap_data = json.load(scrap_json)
                print(f'Arquivo lido {scrap_json.name}')
                scrap_list.append(scrap_data)
        except Exception as e:
            print(f'Erro ao ler {scrap_path}', e)

if os.path.exists(arquivo_cursos):
    try:
        # Primeiro, lemos o arquivo completamente em modo leitura ('r')
        with open(file=arquivo_cursos, mode='r', encoding='utf-8') as file_json:
            conteudo = file_json.read().strip()
            # Tratamento para arquivo vazio (evita erro de JSON)
            cursos_data = json.loads(conteudo) if conteudo else []

        # Criamos um mapeamento por URL para busca rápida
        # Isso garante que manteremos todo o conteúdo original e atualizaremos apenas os matches
        scrap_dict = {s.get('url'): s for s in scrap_list if s.get('url')}

        for curso in cursos_data:
            url_curso = curso.get('url')
            if url_curso in scrap_dict:
                scrap = scrap_dict[url_curso]
                # Atualiza somente as colunas com correspondência
                curso['nota'] = scrap.get('nota')
                curso['num_alunos'] = scrap.get('num_alunos')
                curso['num_avaliacoes'] = scrap.get('num_avaliacoes')
                curso['valor'] = scrap.get('valor')
                curso['moeda'] = scrap.get('moeda')

        # Agora que o processamento terminou, abrimos para escrita ('w') e salvamos
        with open(file=arquivo_cursos, mode='w', encoding='utf-8') as file_json:
            json.dump(cursos_data, file_json, ensure_ascii=False, indent=4)
            print(f'Arquivo salvo {arquivo_cursos}')

    except Exception as e:
        print(f'Erro ao processar {arquivo_cursos}:', e)
else:
    print(f'Arquivo {arquivo_cursos} nao localizado')