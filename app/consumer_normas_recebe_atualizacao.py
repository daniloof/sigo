#!/usr/bin/env python
import pika, sys, os
import json
import normas as nm

def main():

    
    fila = 'volta_normas_orgaos_reg'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='fila')

    def callback(ch, method, properties, body):
        print(" [x] Recebidos %r" % body)

        #chamada call back da api de órgãos externos para atualizacoes internas
        data = json.loads(body)
        cd_norma = data['cd_norma']
        ds_norma = data['ds_norma']
        cd_orgao_regulamentador = data['cd_orgao_regulamentador']

        resultado = nm.atualiza_norma(cd_norma, ds_norma, cd_orgao_regulamentador)

    channel.basic_consume(queue=fila, on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando novos topicos. Para sair pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)