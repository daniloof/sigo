from flask import Flask, request, jsonify
import normas as nm
import json
import send_queue as sq
import receive_queue as rq
import gpi_financeiro as gf
import integracao_bi as ib

app = Flask(__name__)

@app.route('/api/normas/inserir', methods=['POST'])
def normas_inserir():
    content = request.get_json(silent=True)
    data = json.dumps(content)
    data = json.loads(data)
    
    #result['getpoolstatus']['data']['networkdiff']

    cd_norma = data['cd_norma']
    ds_norma = data['ds_norma']
    cd_orgao_regulamentador = data['cd_orgao_regulamentador']

    return nm.insere_norma(cd_norma, ds_norma, cd_orgao_regulamentador)


@app.route('/api/normas/listar', methods=['GET'])
def normas_listar():

    data = nm.lista_normas()
    data = json.dumps(data,default=str, indent=4)

    return data


@app.route('/api/normas/alterar', methods=['POST'])
def normas_alterar():
    content = request.get_json(silent=True)
    data_j = json.dumps(content)
    data = json.loads(data_j)

    cd_norma = data['cd_norma']
    ds_norma = data['ds_norma']
    cd_orgao_regulamentador = data['cd_orgao_regulamentador']

    resultado = nm.atualiza_norma(cd_norma, ds_norma, cd_orgao_regulamentador)

    if resultado == "OK":
        try:
            #posta fila rabbitMQ para atualizacao do sistema legado
            fila = sq.insere_fila("normas_legado","normas_legado",data_j)

            if fila == "OK":
                return "Norma atualizada com sucesso"
            else:
                return fila
        except Exception as error:
            return str(error)
    else:
        return resultado

@app.route('/api/normas/excluir/<uuid>', methods=['POST'])
def normas_excluir(uuid):

    data = nm.exclui_norma(uuid)

    return data

@app.route('/api/normas/consultar/<uuid>', methods=['GET'])
def normas_consultar(uuid):

    data = nm.consulta_norma(uuid)
    data = json.dumps(data,default=str, indent=4)

    return data

@app.route('/api/normas/buscar-atualizacao/', methods=['GET'])
def normas_buscar():

    data = nm.lista_normas()
    
    for x in data:
        x_json = json.dumps(x,default=str, indent=4)   
        sq.insere_fila("normas_orgaos_reg_ida","normas_orgaos_reg_ida",x_json)

    data = json.dumps(data,default=str, indent=4)

    return data

@app.route('/api/normas/receber-atualizacao', methods=['POST'])
def normas_receber():
    content = request.get_json(silent=True)
    data_j = json.dumps(content)

    #posta fila rabbitMQ para atualizacao do sistema de Normas
    fila = sq.insere_fila("volta_normas_orgaos_reg","volta_normas_orgaos_reg",data_j)

    #posta fila rabbitMQ para atualizacao do sistema legado
    fila = sq.insere_fila("normas_legado","normas_legado",data_j)

    if fila == "OK":
        return "Topico recebido para atualizacao"
    else:
        return fila

@app.route('/api/gpi/financeiro/titulo/<uuid>', methods=['GET'])
def titulo_consultar(uuid):

    data = gf.busca_titulo_sap(uuid)
    
    return data

@app.route('/api/integracao-bi/inserir', methods=['POST'])
def integracao_inserir():
    content = request.get_json(silent=True)
    data = json.dumps(content)
    data = json.loads(data)
    
    ds_sistema = data['ds_sistema']
    ds_url_api = data['ds_url_api']
    dt_inicial = data['dt_inicial']
    dt_final = data['dt_final']
    qt_dias = data['qt_dias']

    return ib.insere_integracao(ds_sistema, ds_url_api, dt_inicial, dt_final, qt_dias)

@app.route('/api/integracao-bi/apis/listar', methods=['GET'])
def integracao_bi_api_listar():

    data = ib.lista_apis()
    
    return data

@app.route('/api/integracao-bi/listar', methods=['GET'])
def integracao_bi_listar():

    data = ib.lista_integracoes()
    data = json.dumps(data,default=str, indent=4)

    return data

@app.route('/api/integracao-bi/integrar', methods=['GET'])
def integracao_bi_integrar():

    #lista as integracoes parametrizadas pelo usuario
    data = ib.lista_integracoes()
    
    #para cada integracao chamar a respectiva api e retornar dados para o BI
    for x in data:
        
        #chamar a API aqui
        #---------request--------
        
        #simulando retorno da api
        x_json = json.dumps({'dado1': "valor1",'dado2': "valor2", 'dado3': "valor", 'dadoN':"valorN"}, sort_keys=True, indent=4)
        
        #insere na fila para integracao
        sq.insere_fila("integracao_bi","integracao_bi",x_json)

    return "Topicos enviados para integracao com o BI"

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)