
import kombu

connection = kombu.Connection('amqp://guest:guest@localhost:5672/')
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(message):
    print(f"Received: {message.body}")

channel.basicconsume(queue='hello', onmessage=callback, auto_ack=True)

channel.start_consuming()
