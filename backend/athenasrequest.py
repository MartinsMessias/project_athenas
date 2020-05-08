import requests

database = []


def add_dado(key, value):
    database.append({key: value})


def show(u, p):
    session = requests.Session()
    response = session.get('https://athenas.lyceum.com.br/AOnline/AOnline/avisos/T016D.tp')
    print('Conexão com portal...', response)

    # Login
    response = session.get(
        f'https://athenas.lyceum.com.br/AOnline/web/loginsm?origem=form-aluno&url_origem=%2FAOnline%2FAOnline%2Favisos%2FT016D.tp&username={u}&password={p}',
        cookies=session.cookies.get_dict())
    print('Login...', response)

    # Token
    response = session.get('https://athenas.lyceum.com.br/AOnline/XSRFScript', cookies=session.cookies.get_dict())
    inicio_token = response.text.find('Techne.cronos_xsrf_token="')
    token = response.text[inicio_token + 26:inicio_token + 65]
    print('Token...', response)

    # Requisitar infos do aluno
    data = {'_id': 'blkEscolhaAluno.drpAluno'}
    session.headers.update({'cronos_xsrf_token': token, 'X-Requested-With': 'XMLHttpRequest', 'Connection': 'close'})
    response = session.post('https://athenas.lyceum.com.br/AOnline/AOnline/avisos/T016D.ajax',
                            cookies=session.cookies.get_dict(), headers=session.headers, data=data)

    print('Infos do aluno...', response)

    add_dado('info_aluno', response.json()['data']['records'][0])

    # Pagar disciplinas
    data = {
        '_id': 'grpDisciplinas',
        '_p_0': database[0]['info_aluno'][0],
        '_p_1': ''
    }
    response = session.post('https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.ajax',
                            cookies=session.cookies.get_dict(), headers=session.headers, data=data)
    print('Disciplinas...', response)

    for data in response.json()['data']['records']:
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

        # Pegar notas das disciplinas
        data = {
            '_id': 'gpfNotasDisciplina',
            '_p_0': database[0]['info_aluno'][0],
            '_p_1': cod_disciplina,
            '_p_2': cod_turma,
            '_p_3': ano,
            '_p_4': sla,
            '_p_5': ''
        }

        response = session.post('https://athenas.lyceum.com.br/AOnline/AOnline/avaliacao/T012D.ajax',
                                cookies=session.cookies.get_dict(), headers=session.headers, data=data)
        dados = []
        for dado in response.json()['data']['records']:
            dados.append({
                'id': dado[0],
                'avaliacao': dado[1],
                'nota': dado[6],
            })

        add_dado('disciplinas', {
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
            'notas': dados,
        })

    return get_database()


def get_database():
    return database
