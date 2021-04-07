import pika

def insere_fila (queue,routing_key,body):

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange='',
                            routing_key=routing_key,
                            body=body)

        return "OK"
    except Exception as error:
         return str(error)
    finally:
        if connection is not None:
            connection.close()
    