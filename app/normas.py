#!/usr/bin/python

import psycopg2
from config import config
from datetime import datetime

def insere_norma(cd_norma, ds_norma, cd_orgao_regulamentador):
    
    sql = """INSERT INTO normas(cd_norma, ds_norma, cd_orgao_regulamentador, dt_atualizacao)
             VALUES(%s, %s, %s, %s);"""
    conn = None
    
    now = datetime.now()
    dt_atualizacao = str(now.year).zfill(4) + "/" + str(now.month).zfill(2) + "/" + str(now.day).zfill(2)

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (cd_norma.upper(), ds_norma.upper(), cd_orgao_regulamentador.upper(), dt_atualizacao))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        return "OK"
    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()

def lista_normas():
    
    sql = """SELECT * FROM normas ORDER BY cd_norma;"""
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

def atualiza_norma(cd_norma, ds_norma, cd_orgao_regulamentador):
    
    sql = """UPDATE normas SET ds_norma = %s, cd_orgao_regulamentador = %s, dt_atualizacao = %s WHERE cd_norma = %s;"""
    conn = None
    
    now = datetime.now()
    dt_atualizacao = str(now.year).zfill(4) + "/" + str(now.month).zfill(2) + "/" + str(now.day).zfill(2)

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        
        # execute the UPDATE statement
        cur.execute(sql, (ds_norma.upper(), cd_orgao_regulamentador.upper(), dt_atualizacao, cd_norma.upper()))
        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
           
        return "OK"
     
    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()

def exclui_norma(cd_norma):
    
    sql = """DELETE FROM normas WHERE cd_norma = %s;"""
    conn = None
    updated_rows = 0
    
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        
        # execute the DELETE statement
        cur.execute(sql, (str(cd_norma.upper()),))
        updated_rows = cur.rowcount
        
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        
        if updated_rows > 0:
            return "Norma excluída com sucesso"
        else:
            return "Norma não encontrada. Nenhum resgistro excluído"

    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()

def consulta_norma(cd_norma):
    
    sql = """SELECT * FROM normas WHERE cd_norma = %s;"""
    conn = None

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(sql, (str(cd_norma.upper()),))

        data = cur.fetchall()

        # close communication with the database
        cur.close()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
         return str(error)
    finally:
        if conn is not None:
            conn.close()