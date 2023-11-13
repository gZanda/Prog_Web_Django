import smtplib

def send_to_gmail(email):
  EMAIL = "josevitorandrademarques02@gmail.com"
  receiver_email = email

  MESSAGE ="""
    Subject: Cadastro plataforma Taskies.

    Ola
    Seja bem-vindo(a) a plataforma Taskies.
    Aproveite.
  """

  server = smtplib.SMTP("smtp.gmail.com", 587)

  server.starttls()

  server.login(EMAIL, "qnowmvdekonxhrln")

  server.sendmail(EMAIL, receiver_email, MESSAGE)