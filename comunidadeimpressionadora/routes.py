from flask import render_template, redirect, flash, url_for, request
from comunidadeimpressionadora import app, database, bcrypt, login_manager
from googletrans import Translator
from comunidadeimpressionadora.forms import FormLogin, FormEditarPerfil, FormCriarConta, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import os
from PIL import Image


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    traduzir = Translator()  # instância do objeto tradutor
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no e-mail {form_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('homepage'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)  # criptografia da senha
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta, traduzir=traduzir)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout realizado com sucesso.', 'alert-success')
    return redirect(url_for('homepage'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit():
        post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, Autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso', 'alert-success')
        return redirect(url_for('homepage'))
    return render_template('criarpost.html', form_criarpost=form_criarpost)


def salvar_imagem(imagem):
    mail = str(current_user.email)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = 'imagem_' + mail + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = [campo.label.text for campo in form if 'curso_' in campo.name and campo.data]
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_editarperfil = FormEditarPerfil()
    if form_editarperfil.validate_on_submit():
        current_user.username = form_editarperfil.username.data
        current_user.email = form_editarperfil.email.data
        if form_editarperfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editarperfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_editarperfil)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':  # faz com que os campos já estejam preenchidos com os dados atuais do user
        form_editarperfil.username.data = current_user.username
        form_editarperfil.email.data = current_user.email
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_editarperfil=form_editarperfil)

