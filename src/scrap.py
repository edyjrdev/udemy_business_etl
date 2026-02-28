from curl_cffi import requests
import os
import json
import dataclasses

@dataclasses.dataclass
class CursoScrap:
    url: str
    nota: int
    num_alunos: int
    num_avaliacoes: int
    valor: float
    moeda: str

pages_dim = 'model/1_silver' # pasta com cursos
pages_scrap = 'model/0_bronze/3_scrap'
if not os.path.exists(pages_scrap):
    os.makedirs(pages_scrap)

arquivo_cursos = 'curso.json'
cursos_scrap = []
TIMEOUT_API = 300

path_arquivo_cursos = os.path.join(pages_dim, arquivo_cursos)
headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

with open(file=path_arquivo_cursos, mode='r', encoding='utf-8') as file_json:
    lista_cursos = json.load(file_json)
    session = requests.Session()
    for i in lista_cursos:
        courseid = i['id']
        # f'https://serpro.udemy.com/api-2.0/course-landing-components/5180618/me/?components=slider_menu,add_to_cart,buy_button,deal_badge,discount_expiration,price_text,incentives,purchase,redeem_coupon,money_back_guarantee,base_purchase_section,purchase_tabs_context,lifetime_access_context,available_coupons,gift_this_course,buy_for_team
        url_api =  f'https://serpro.udemy.com/api-2.0/course-landing-components/{courseid}/me/?components=slider_menu,add_to_cart,buy_button,deal_badge,discount_expiration,price_text,incentives,purchase,redeem_coupon,money_back_guarantee,base_purchase_section,purchase_tabs_context,lifetime_access_context,available_coupons,gift_this_course,buy_for_team'
        response = session.get(url_api, headers=headers, impersonate="chrome",timeout=TIMEOUT_API)
        
        match response.status_code:
            case 200:
                content = response.json()
                data = content['slider_menu']['data']
                purchase = content['purchase']['data']['list_price']

                curso_scrap = CursoScrap(
                    url=i['url'],
                    nota=data['rating'],
                    num_alunos=data['num_students'],
                    num_avaliacoes=data['num_reviews'],
                    valor=purchase['amount'],
                    moeda=purchase['currency']
                )
                print(f'Curso: {curso_scrap.url} - Nota: {curso_scrap.nota} - Alunos: {curso_scrap.num_alunos}')
                cursos_scrap.append(curso_scrap)
                arquivo_curso = f'{i['id']}-scrap.json'
                path_arquivo_scrap = os.path.join(pages_scrap, arquivo_curso)
                if not os.path.exists(path_arquivo_scrap):        
                    with open(file=path_arquivo_scrap, mode='w', encoding='utf-8') as scrap_json:
                        scrap = dataclasses.asdict(curso_scrap)
                        json.dump(scrap, scrap_json, ensure_ascii=False, indent=4)
                        print(f'Arquivo salvo {scrap_json.name}')
                else:
                    print(f'Arquivo já existe {path_arquivo_scrap}')
            
            case 403:
                print('Acesso Negado')
            case _:
                print('Erro')
    
        