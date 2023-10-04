from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('contato.html')


@app.route('/enviar', methods=['POST'])
def enviar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        # Configurar o servidor de email
        servidor_email = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_email.starttls()
        servidor_email.login('user@email.com', 'password')

        # Criar o corpo do email
        corpo_email = f"Nome: {nome}\nEmail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}"

        print(corpo_email)

        # Configurar o email
        msg = MIMEText(corpo_email)
        msg['From'] = email
        msg['To'] = 'user@emai.com'
        msg['Subject'] = assunto
        msg['reply-to'] = email

        print(msg)

        # Enviar o email
        servidor_email.sendmail(email, "user@email.com", msg.as_string())
        servidor_email.quit()

        return "Formulário enviado com sucesso!"


if __name__ == '__main__':
    app.run(debug=True)
