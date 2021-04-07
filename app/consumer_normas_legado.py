#!/usr/bin/env python
import pika, sys, os
import json
import normas as nm

def main():

    
    fila = 'normas_legado'

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='fila')

    def callback(ch, method, properties, body):
        print(" [x] Recebidos %r" % body)
        
        #chamada api sistema Segurança e Qualidade
        #-------------------request aqui------------
        print("Sistema legado de Segurança e Qualidade atualizado com sucesso")

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