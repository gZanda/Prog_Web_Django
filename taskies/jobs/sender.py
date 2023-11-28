import pika 
import json

def send_to_queue(mail, password):
  credentials = pika.PlainCredentials('taskies', 'taskiesTp')

  connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
  )

  channel = connection.channel()

  channel.queue_declare(queue='taskies')

  message = {
    'email': str(mail),
    'password': str(password)
  }
    

  channel.basic_publish(
    exchange='',
    routing_key='taskies',
    body=json.dumps(message)
  )

  connection.close