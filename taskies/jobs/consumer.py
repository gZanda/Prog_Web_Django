import pika
import json
from mail_sender import send_to_gmail

def main():
  credentials = pika.PlainCredentials('taskies', 'taskiesTp')

  connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
  )

  channel = connection.channel()

  channel.queue_declare(queue='taskies')

  def callback(ch, method, properties, body):
    send_to_gmail(json.loads(body))

  channel.basic_consume(queue='taskies', on_message_callback=callback, auto_ack=True)

  channel.start_consuming()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    try:
      sys.exit(0)
    except SystemExit:
      os._exit()