import json

def busca_titulo_sap(cd_titulo):
    #chamar API de integração com SAP
    #-------------request------------
    titulo = json.dumps({'titulo': cd_titulo,'valor': "550.34", 'vencimento': '01/06/2021', 'favorecido':'Casa do Parafuso LTDA', 'data de criacao':'10/04/2021'}, sort_keys=True, indent=4)
    return titulo