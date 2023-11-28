import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_to_gmail(message):
  EMAIL = "josevitorandrademarques02@gmail.com"

  receiver_email = str(message['email'])
  password = str(message['password'])

  msg = MIMEMultipart()
  msg['From'] = EMAIL
  msg['To'] = receiver_email
  msg['Subject'] = "Cadastro plataforma Taskies."

  body =f"""
    Ola
    Seja bem-vindo(a) a plataforma Taskies.
    Aproveite.

    Suas credenciais de login são:
      email: {receiver_email}
      senha: {password}
  """

  msg.attach(MIMEText(body, 'plain'))

  server = smtplib.SMTP("smtp.gmail.com", 587)

  server.starttls()

  server.login(EMAIL, "qnowmvdekonxhrln")

  server.sendmail(EMAIL, receiver_email, msg.as_string())

  server.quit()