import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import urllib.parse

import os

to = os.environ["EMAIL_TO"]

def lambda_handler(event, context):

    servidor_email = smtplib.SMTP(os.environ["SMTP_SERVER"], os.environ["SMTP_PORT"])
    servidor_email.starttls()
    servidor_email.login(os.environ["SMTP_MAIL"], os.environ["SMTP_PASS"])
    
    body_request = decode_body(event.get('body'))
    content = handle_body_content(event.get('body'))
    email = body_request.get('reply_to')

    servidor_email.sendmail(email, to, content.as_string().encode('utf-8'))
        
    servidor_email.quit()

    redirectURL = os.environ["SUCCESS_PAGE"]
    return {
        'statusCode': 302,
        'headers': { 'Location': redirectURL }
    }


def decode_body(body):
    url_unquoted = urllib.parse.unquote(body)
    
    base64_bytes = base64.b64decode(url_unquoted)
    base64_message = base64_bytes.decode('utf-8')
    
    data = urllib.parse.parse_qs(base64_message)
    
    assunto = 'Contato através do Portifólio'
    
    if 'assunto' in data:
        assunto = data.get('assunto')[0]
    
    return {
        "nome": data.get('nome')[0],
        "reply_to": data.get('email')[0],
        "assunto": assunto,
        "mensagem": data.get('mensagem')[0]
    }
    
    
def handle_body_content(body):
    
    body = decode_body(body)
    
    nome = body.get('nome')
    email = body.get('reply_to')
    assunto = body.get('assunto')
    mensagem = body.get('mensagem')
    
    msg = MIMEMultipart('alternative')
    msg.set_charset("utf-8")
    msg['From'] = email
    msg['reply-to'] = email
    msg['To'] = to
    msg['Subject'] = assunto
    
    print('Receiving an email')
    print(f'From: {email}')
    print(f'Message: {mensagem}')
  
    header_str = "<h2>Hey Rickys, você tem uma nova mensagem! 😉</h2>"
    nome_header_str = "<h3 style='color:#fff;background:#2c3e50;width:50%'>Nome</h3>"
    nome_content_str = f"<p>{nome}</p>"
    msg_header_str = "<h3 style='color:#fff;background:#2c3e50;width:50%'>Mensagem</h3>"
    msg_content_str = f"<p>{mensagem}</p>"
    
    html_str = header_str + nome_header_str + nome_content_str + msg_header_str + msg_content_str
    
    html = MIMEText(html_str, 'html', 'utf-8')

    msg.attach(html)

    return msg;