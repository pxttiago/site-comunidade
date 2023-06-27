from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, FormCriarConta


app = Flask(__name__)

lista_usuarios = ['User1', 'User2', 'User3', 'User4', 'User5']


app.config['SECRET_KEY'] = 'bfca39860e03668bb8d3e66eb1fb09e9'


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'submit_login' in request.form:
        flash(f'Login realizado com sucesso no e-mail {form_login.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
    if form_criarconta.validate_on_submit() and 'submit_criarconta' in request.form:
        flash(f'Conta criada com sucesso para o e-mail {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


if __name__ == '__main__':
    app.run(debug=True)
