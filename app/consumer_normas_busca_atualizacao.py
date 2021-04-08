#!/usr/bin/env python
import pika, sys, os
import json
import normas as nm

def main():

    
    fila = 'normas_orgaos_reg_ida'

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',port=5672))
    connection = pika.BlockingConnection(parameters)
    
    channel = connection.channel()

    channel.queue_declare(queue='fila')

    def callback(ch, method, properties, body):
        print(" [x] Recebidos %r" % body)

        #chamada api de órgãos externos para verificar atualizacoes
        #-------------------request aqui------------
        print("Normas enviadas para verificar atualizações")

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