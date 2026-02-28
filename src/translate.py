import os
import json
from deep_translator import GoogleTranslator

# in
pages_dim = 'model/1_silver'
cache_file = 'model/0_bronze/translation_cache.json'

dim_list = ['categoria.json',
            'idioma_audio.json',
            'idioma_legenda.json',
            'topico.json']

translator = GoogleTranslator(source='auto', target='pt')

cache = {}
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f'Cache carregado com {len(cache)} termos.')
    except Exception as e:
        print(f'Erro ao carregar cache: {e}')

translation_count = 0

def get_translation(text):
    global translation_count
    if text in cache:
        return cache[text]
    try:
        translated = translator.translate(text)
        cache[text] = translated
        translation_count += 1
        if translation_count % 50 == 0:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=4)
            print(f'Cache salvo parcial: {len(cache)} termos.')
        return translated
    except Exception as e:
        print(f'Erro ao traduzir "{text}": {e}')
        return text

for dim in dim_list:
    dim_path = os.path.join(pages_dim, dim)
    if os.path.exists(dim_path):
        try:
            with open(file=dim_path, mode='r', encoding='utf-8') as file_json:
                data = json.load(file_json)
                print(f'Arquivo lido {file_json.name}')

            new_data = []
            if dim == 'categoria.json':
                for item in data:
                    if isinstance(item, dict):
                        new_data.append(item)
                    else:
                        trans = get_translation(item)
                        new_data.append({'categoria': item, 'categoria_ptbr': trans})
            

            elif dim == 'idioma_legenda.json':
                for item in data:
                    if isinstance(item, dict):
                        new_data.append(item)
                    else:
                        trans = get_translation(item)
                        new_data.append({'idioma_legenda': item, 'idioma_legenda_ptbr': trans})

            elif dim == 'topico.json':
                total = len(data)
                for i, item in enumerate(data):
                    if i % 10 == 0:
                        print(f'Traduzindo topico {i}/{total}...')
                    if isinstance(item, dict):
                        new_data.append(item)
                    else:
                        trans = get_translation(item[1])
                        new_data.append({'id_topico': item[0], 'titulo': item[1], 'url': item[2], 'titulo_ptbr': trans})

            elif dim == 'idioma_audio.json':
                for item in data:
                    if isinstance(item, dict):
                        new_data.append(item)
                    else:
                        trans = get_translation(item[1])
                        new_data.append({'idioma_audio': item[0], 'titulo': item[1], 'english_title': item[2], 'idioma_audio_ptbr': trans})

            if new_data:
                with open(file=dim_path, mode='w', encoding='utf-8') as file_out:
                    json.dump(new_data, file_out, ensure_ascii=False, indent=4)
                    print(f'Arquivo traduzido salvo {file_out.name}')

                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache, f, ensure_ascii=False, indent=4)
                print(f'Cache atualizado após {dim}')

        except Exception as e:
            print(f'Erro', e)

if cache:
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)
    print('Cache salvo.')