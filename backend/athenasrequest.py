import requests

DATABASE = []
site = requests.session()


def get_nota_disciplina(matricula, cod_disciplina, cod_turma, ano, sla, cookies_d, token):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'cronos_xsrf_token': token,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://athenas.lyceum.com.br',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.tp',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    }

    data = {
        '_id': 'gpfNotasDisciplina',
        '_p_0': matricula,
        '_p_1': cod_disciplina,
        '_p_2': cod_turma,
        '_p_3': ano,
        '_p_4': sla,
        '_p_5': ''
    }

    response_ava = requests.post('https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.ajax', headers=headers,
                                 cookies=cookies_d, data=data)
    r_ava = response_ava.json()
    dados = []
    for dado in r_ava['data']['records']:
        dados.append({
            'id': dado[0],
            'avaliacao': dado[1],
            'nota': dado[6],
        })
    return dados


def show(u, s):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://unimeta.edu.br/portal-academico/',
        'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
    }

    response = site.get('https://athenas.lyceum.com.br/AOnline/AOnline/avisos/T016D.tp', headers=headers)
    cookies = {}
    try:
        globals()
        cookies = {
            'JSESSIONID': response.cookies.items()[0][1],
        }
    except IndexError:
        pass

    url_login = f'https://athenas.lyceum.com.br/AOnline/web/loginsm?origem=form-aluno&url_origem=%2FAOnline%2FAOnline%2Favisos%2FT016D.tp&username={u}&password={s}'
    response = site.get(url_login, cookies=cookies)

    if response.status_code != 200:
        print('Erro no login! \nVerifique seus dados de acesso!\nRetorno: HTTP Status ', response.status_code)
        return None
    else:
        print('[Login - OK]')

        # Pegar token de sessão
        response = site.get('https://athenas.lyceum.com.br/AOnline/XSRFScript', headers=headers)
        inicio_token = response.text.find('Techne.cronos_xsrf_token="')
        token = response.text[inicio_token + 26:inicio_token + 65]

        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'cronos_xsrf_token': token,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://athenas.lyceum.com.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://athenas.lyceum.com.br/AOnline/AOnline/avisos/T016D.tp',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        }

        data = {
            '_id': 'blkEscolhaAluno.drpAluno'
        }

        response = requests.post('https://athenas.lyceum.com.br/AOnline/AOnline/avisos/T016D.ajax', headers=headers,
                                 cookies=cookies, data=data)
        r = response.json()
        dados_aluno = r["data"]["records"][0][1]
        matricula = r['data']['records'][0][0]
        DATABASE.append({'id_aluno': dados_aluno, 'matricula': matricula})

        # Pegar todas as disciplinas
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'cronos_xsrf_token': token,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://athenas.lyceum.com.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.tp',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        }

        data = {
            '_id': 'grpDisciplinas',
            '_p_0': DATABASE[0]['matricula'],
            '_p_1': ''
        }

        response = requests.post('https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.ajax', headers=headers,
                                 cookies=cookies, data=data)

        r = response.json()

        for data in r['data']['records']:
            disciplina = data[0].split(' - ')[1]
            aulas_previstas = data[3]
            aulas_ministradas = data[4]
            faltas_permitidas = data[5]
            percentual_presenca = data[6]
            faltas = data[7]
            cod_disciplina = data[9]
            cod_turma = data[10]
            ano = data[11]
            data_inicial = data[12]
            data_final = data[13]
            situacao = data[14]
            sla = data[15]

            dados_disciplina = get_nota_disciplina(matricula, cod_disciplina, cod_turma, ano, sla, cookies, token)

            DATABASE.append({
                'sla': sla,
                'disciplina': disciplina,
                'cod_disciplina': cod_disciplina,
                'aulas_previstas': aulas_previstas,
                'aulas_ministradas': aulas_ministradas,
                'faltas_permitidas': faltas_permitidas,
                'percentual_presenca': percentual_presenca,
                'faltas': faltas,
                'cod_turma': cod_turma,
                'ano': ano,
                'data_inicial': data_inicial,
                'data_final': data_final,
                'situacao': situacao,
                'notas': dados_disciplina,
            })
    return DATABASE



