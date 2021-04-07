import psycopg2
from config import config
from datetime import date
import json

def insere_integracao(ds_sistema, ds_url_api, dt_inicial = date.today, dt_final = date.today, qt_dias=0):
    
    sql = """INSERT INTO integracao_bi(ds_sistema, ds_url_api, dt_inicial, dt_final, qt_dias)
             VALUES(%s, %s, %s, %s, %s);"""
    conn = None

    if dt_inicial == date.today and dt_final == date.today:
        dt_ini = ""
        dt_fim = ""
    else:
        dt_ini = dt_inicial
        dt_fim = dt_final
    
    if qt_dias == 0:
        dias = ""
    else:
        dias = qt_dias

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (ds_sistema.upper(), ds_url_api.lower(), dt_ini, dt_fim, dias))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        return "Parametrizacao realizada com sucesso"
    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()

def lista_apis():
    #Listar APIs passiveis de integração
    #-------------requests------------
    apis = json.dumps([
	{"ds_sistema":"Legado - Gestao de Processos",
	"ds_url_api":"http://legado/gpi/fabril/listar",
	"ds_descricao":"informacoes dados fabris tais como...",
	"parametros":"data inicial, final e quantidade de dias"},
	{"ds_sistema":"Legado - Gestao de Processos",
	"ds_url_api":"http://legado/gpi/producao/consultar",
	"ds_descricao":"informacoes de producao tais como...",
	"parametros":"data inicial, final e quantidade de dias"},
	{"ds_sistema":"Legado - Gestao de Processos",
	"ds_url_api":"http://legado/gpi/insumos/previstos/listar",
	"ds_descricao":"informacoes de isumos tais como...",
	"parametros":"data inicial, final e quantidade de dias"},
	{"ds_sistema":"Legado - Gestao de Processos",
	"ds_url_api":"http://legado/gpi/planejamento/listar",
	"ds_descricao":"informacoes dados fabris tais como...",
	"parametros":"data inicial, final e quantidade de dias"}
     ], sort_keys=True, indent=4)

    return apis

def lista_integracoes():
    
    sql = """SELECT * FROM integracao_bi ORDER BY ds_sistema;"""
    conn = None

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql)

        data = cur.fetchall()

        # close communication with the database
        cur.close()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()