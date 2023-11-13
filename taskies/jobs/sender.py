import pika 
import json

def send_to_queue(mail):
  credentials = pika.PlainCredentials('taskies', 'taskiesTp')

  connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
  )

  channel = connection.channel()

  channel.queue_declare(queue='taskies')

  message = json.dumps(mail)

  channel.basic_publish(
    exchange='',
    routing_key='taskies',
    body=message
  )

  connection.close