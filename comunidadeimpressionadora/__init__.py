from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)  # criação do site/app

app.config['SECRET_KEY'] = 'bfca39860e03668bb8d3e66eb1fb09e9'  # configuração da secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'  # configuração do banco de dados

database = SQLAlchemy(app)  # cria o banco de dados
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Acesso não autorizado. Faça login para continuar.'
login_manager.login_message_category = 'alert-info'


from comunidadeimpressionadora import routes

