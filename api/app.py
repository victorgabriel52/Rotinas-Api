from flask import Flask, url_for, render_template, request, redirect, session, flash
from models import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'vitingabriel957kkk'


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tipo = request.form['tipo']
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 🔐 LOGIN
        if tipo == 'login':
            email = request.form['email']
            password = request.form['password']

            cursor.execute(
                "SELECT * FROM usuarios WHERE email = %s",
                (email,)
            )
            usuario = cursor.fetchone()

            if usuario and check_password_hash(usuario['senha'], password):
                session['id'] = usuario['id']
                cursor.close()
                db.close()
                return redirect(url_for('rotinas'))
            else:
                flash('Usuário ou senha inválidos', 'error')

        # 📝 CADASTRO
        elif tipo == 'cadastro':
            nome = request.form['nome']
            email = request.form['email']
            senha = generate_password_hash(request.form['password'])

            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )
            db.commit()

            cursor.close()
            db.close()

            flash('Cadastro realizado com sucesso! Faça login.')
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/rotinas', methods=['GET', 'POST'])
def rotinas():
    user_id = session.get('id')

    if not user_id:
        return redirect(url_for('home'))

    db = get_db()
    cursor = db.cursor(dictionary=True)  # 🔥 CORREÇÃO IMPORTANTE

    # ➕ ADICIONAR ROTINA
    if request.method == 'POST':
        rotina = request.form.get('rotina')

        if rotina:  # evita erro vazio
            cursor.execute(
                "INSERT INTO rotinas (usuario_id, rotina) VALUES (%s, %s)",
                (user_id, rotina)
            )
            db.commit()

        cursor.close()
        db.close()
        return redirect(url_for('rotinas'))

    # 📋 LISTAR ROTINAS
    cursor.execute(
        "SELECT * FROM rotinas WHERE usuario_id = %s",
        (user_id,)
    )
    rotinas = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('rotinas.html', rotinas=rotinas)


# 🗑️ DELETAR ROTINA
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM rotinas WHERE id = %s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('rotinas'))


if __name__ == "__main__":
    app.run(debug=True)