from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):  # formulário para criação de contas
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    submit_criarconta = SubmitField('Criar Conta')

    # função que verifica se o username já existe
    def validate_username(self, username):  # o nome da função deve começar com validate_
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome de usuário indisponível.')

    # função que verifica se o e-mail já existe
    def validate_email(self, email):  # o nome da função deve começar com validate_
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):  # formulário para login
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil',
                            validators=[FileAllowed(['jpg', 'jpeg', 'png'])],
                            render_kw={'style': 'display: block; margin-top: 5px;'})
    curso_excel = BooleanField('Excel Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_ppt = BooleanField('Power Point Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    submit_editarperfil = SubmitField('Salvar')
    
    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Nome de usuário já cadastrado. Cadastre um nome de usuário diferente.')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado. Cadastre um novo e-mail.')