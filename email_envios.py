import smtplib
from email.mime.text import MIMEText

def enviar_email(destinatario, assunto, mensagem):
    remetente = 'ofcsmurilo@gmail.com'
    senha = 'ldzi kjbc qisc pdqc'

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)
    print('enviado')

