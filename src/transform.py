import os
import json
import datetime
from dataclasses import dataclass
import dataclasses
# in
pages_pag = 'model/0_bronze/1_page'
# out
pages_cur = 'model/0_bronze/2_course'

if not os.path.exists(pages_cur):
    os.makedirs(pages_cur)
#out
pages_dim = 'model/1_silver'
if not os.path.exists(pages_dim):
    os.makedirs(pages_dim)


@dataclass
class Curso:
    id: str
    titulo: str
    url:str
    aulas:int
    videos:int
    idioma:str
    categoria:str
    subcategoria:str
    quizes:int
    testes:int
    tem_legenda:bool
    video_duracao:int
    data_atualizacao:str
    nivel:str
    chamada:str
    descricao:str
    nota: float = 0.0
    num_alunos: int = 0
    num_avaliacoes: int = 0
    valor: float = 0.0
    moeda: str = ''
    data_extracao:datetime = datetime.datetime.now()

lista_cursos = []
set_instrutor = set()
set_curso_instrutor = set()
set_categoria = set()
set_categoria_curso = set()
set_topico = set()
set_topico_curso = set()
set_idioma_legenda = set()
set_idioma_legenda_curso = set()
set_idioma_audio = set()
set_idioma_audio_curso = set()


if os.path.exists(pages_pag):
    files = os.listdir(pages_pag)
    for file in files:
        file_path = os.path.join(pages_pag, file)
        with open(file=file_path, mode='r', encoding='utf-8') as file_json:
            lista_cursos_arquivo = json.load(file_json)
            for curso in lista_cursos_arquivo:
                
                categorias=curso['categories']
                topicos=curso['topics']
                instrutores=curso['instructors']
                idiomas_legenda=curso['caption_languages']
                idiomas_audio = curso['caption_locales']
                cat = curso['primary_category']
                if cat:
                    cat = cat['title']  
                subcat = curso['primary_subcategory']
                if subcat:
                    subcat = subcat['title']

                dado_curso = Curso(
                    id=curso['id'],
                    titulo=curso['title'],
                    url=curso['url'],
                    aulas=curso['num_lectures'],
                    videos=curso['num_videos'],
                    idioma=curso['locale']['locale'],
                    categoria=cat,
                    subcategoria=subcat,
                    quizes=curso['num_quizzes'],
                    testes=curso['num_practice_tests'],
                    tem_legenda=curso['has_closed_caption'],
                    video_duracao=curso['estimated_content_length_video'],
                    data_atualizacao=curso['last_update_date'],
                    nivel=curso['level'],
                    chamada=curso['headline'],
                    descricao=curso['description']                 
                )
                
                arquivo_nome = f'{dado_curso.id:03}.json'
                lista_cursos.append(dado_curso)
                file_curso_path = os.path.join(pages_cur, arquivo_nome)
                
                if not os.path.exists(file_curso_path):
                   with open(file=file_curso_path, mode='w', encoding='utf-8') as file_curso:
                        dic_curso = dataclasses.asdict(dado_curso)  
                        json.dump(dic_curso, file_curso, ensure_ascii=False, indent=4)
                        print(f'Arquivo salvo {file_curso.name}')
                else:
                    print(f'Arquivo já existe {file_curso_path}')

                if instrutores:
                    for instrutor in instrutores:
                        set_instrutor.add(instrutor)
                        set_curso_instrutor.add((dado_curso.id, instrutor))
                if categorias:
                    for categoria in categorias:
                        set_categoria.add(categoria)
                        set_categoria_curso.add((dado_curso.id, categoria))
                if topicos:
                    for topico in topicos:
                        set_topico.add((topico['id'], topico['title'], topico['url']))
                        set_topico_curso.add((dado_curso.id, topico['id']))

                if idiomas_legenda:
                    for idioma in idiomas_legenda:
                        set_idioma_legenda.add(idioma)
                        set_idioma_legenda_curso.add((dado_curso.id, idioma))

                if idiomas_audio:
                    for idioma in idiomas_audio:
                        try:
                            locale = idioma['locale']
                            tittle = idioma['title']
                            en_tittle = idioma['english_title']
                            set_idioma_audio.add((locale, tittle, en_tittle))
                            set_idioma_audio_curso.add((dado_curso.id, idioma['locale']))
                        except Exception as e:
                            print(type(idioma), e)
                

arquivo_instrutor = 'instrutor.json'
file_instrutor_path = os.path.join(pages_dim, arquivo_instrutor)
with open(file=file_instrutor_path, mode='w', encoding='utf-8') as file_instrutor:
    json.dump(list(set_instrutor), file_instrutor, ensure_ascii=False, indent=4)
    print(f'Arquivo Instrutor salvo {file_instrutor.name}')
                
arquivo_instrutor_curso = 'instrutor_curso.json'
file_instrutor_curso_path = os.path.join(pages_dim, arquivo_instrutor_curso)
with open(file=file_instrutor_curso_path, mode='w', encoding='utf-8') as file_instrutor_curso:
    json.dump(list(set_curso_instrutor), file_instrutor_curso, ensure_ascii=False, indent=4)
    print(f'Arquivo Instrutor Curso salvo {file_instrutor_curso.name}')
                
arquivo_categorias = 'categoria.json'
file_categorias_path = os.path.join(pages_dim, arquivo_categorias)
with open(file=file_categorias_path, mode='w', encoding='utf-8') as file_categorias:
    json.dump(list(set_categoria), file_categorias, ensure_ascii=False, indent=4)
    print(f'Arquivo Categorias salvo {file_categorias.name}')

arquivo_categoria_curso = 'categoria_curso.json'
file_categoria_curso_path = os.path.join(pages_dim, arquivo_categoria_curso)
with open(file=file_categoria_curso_path, mode='w', encoding='utf-8') as file_categoria_curso:
    json.dump(list(set_categoria_curso), file_categoria_curso, ensure_ascii=False, indent=4)
    print(f'Arquivo Categoria Curso salvo {file_categoria_curso.name}')   

arquivo_topico = 'topico.json'
file_topico_path = os.path.join(pages_dim, arquivo_topico)
with open(file=file_topico_path, mode='w', encoding='utf-8') as file_topico:
    json.dump(list(set_topico), file_topico, ensure_ascii=False, indent=4)
    print(f'Arquivo Topico salvo {file_topico.name}')   

arquivo_topico_curso = 'topico_curso.json'
file_topico_curso_path = os.path.join(pages_dim, arquivo_topico_curso) 
with open(file=file_topico_curso_path, mode='w', encoding='utf-8') as file_topico_curso:
    json.dump(list(set_topico_curso), file_topico_curso, ensure_ascii=False, indent=4)
    print(f'Arquivo Topico Curso salvo {file_topico_curso.name}') 

arquivo_idioma_legenda = 'idioma_legenda.json'
file_idioma_legenda_path = os.path.join(pages_dim, arquivo_idioma_legenda)
with open(file=file_idioma_legenda_path, mode='w', encoding='utf-8') as file_idioma_legenda:
    json.dump(list(set_idioma_legenda), file_idioma_legenda, ensure_ascii=False, indent=4)      
    print(f'Arquivo Idioma Legenda salvo {file_idioma_legenda.name}')   

arquivo_idioma_legenda_curso = 'idioma_legenda_curso.json'
file_idioma_legenda_curso_path = os.path.join(pages_dim, arquivo_idioma_legenda_curso)
with open(file=file_idioma_legenda_curso_path, mode='w', encoding='utf-8') as file_idioma_legenda_curso:
    json.dump(list(set_idioma_legenda_curso), file_idioma_legenda_curso, ensure_ascii=False, indent=4)      
    print(f'Arquivo Idioma Legenda Curso salvo {file_idioma_legenda_curso.name}')   

arquivo_idioma_audio = 'idioma_audio.json'
file_idioma_audio_path = os.path.join(pages_dim, arquivo_idioma_audio)
with open(file=file_idioma_audio_path, mode='w', encoding='utf-8') as file_idioma_audio:
    json.dump(list(set_idioma_audio), file_idioma_audio, ensure_ascii=False, indent=4)      
    print(f'Arquivo Idioma Audio salvo {file_idioma_audio.name}')   

arquivo_idioma_audio_curso = 'idioma_audio_curso.json'
file_idioma_audio_curso_path = os.path.join(pages_dim, arquivo_idioma_audio_curso)
with open(file=file_idioma_audio_curso_path, mode='w', encoding='utf-8') as file_idioma_audio_curso:
    json.dump(list(set_idioma_audio_curso), file_idioma_audio_curso, ensure_ascii=False, indent=4)      
    print(f'Arquivo Idioma Audio Curso salvo {file_idioma_audio_curso.name}')   

arquivo_lista_cursos = 'curso.json'
file_lista_cursos_path = os.path.join(pages_dim, arquivo_lista_cursos)
with open(file=file_lista_cursos_path, mode='w', encoding='utf-8') as file_lista_cursos:
    curso_json = []
    for cur in lista_cursos:
        curso_json.append(dataclasses.asdict(cur)) 
    json.dump(curso_json, file_lista_cursos, ensure_ascii=False, indent=4)      
    print(f'Arquivo Curso salvo {file_lista_cursos.name}')   

