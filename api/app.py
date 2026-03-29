from flask import Flask, url_for, render_template, request
from models import *

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tipo = request.form['tipo']

        db = get_db()
        cursor = db.cursor()

        if tipo == 'login':
            email = request.form['email']
            password = request.form['password']


            cursor.execute(
                "SELECT * FROM usuarios WHERE email = %s AND senha = %s",
                (email, password)
            )

            usuario = cursor.fetchone()

            cursor.close()
            db.close()

            if usuario:
                return render_template('rotinas.html')
                
            else:
                return "User não encontrado"
            
        elif tipo == 'cadastro':
            nome = request.form['nome']
            senha = request.form['password']
            email = request.form['email']

            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )

            db.commit()



    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)