from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token
# rom recursos.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout, atributos
from modelos.usuario import UserModel
# from recursos.cliente import Clientes, Cliente
# from recursos.cobranca import Cobrancas, Cobranca
# from recursos.movimentacao import Movimentacoes, Movimentacao
# from recursos.orcamento import Orcamentos, Orcamento
# from recursos.servico import Servicos, Servico
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from config_json import *


app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL # 'postgres://postgres:admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'access_token'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_acesso_invalidado():
    return jsonify({'message': 'You have been logged out.'}), 401


@app.route('/clientes', methods=['GET', 'POST', 'PUT'])  # Clientes
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_clientes():
    return jsonify()


@app.route('/clientes/cliente_id', methods=['GET', 'POST', 'PUT'])  # Cliente
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_clientes_por_id():
    return jsonify()


@app.route('/cobrancas', methods=['GET', 'POST', 'PUT'])  # Cobrancas
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_cobrancas():
    return jsonify()


@app.route('/cobrancas/<string:cobranca_id>', methods=['GET', 'POST', 'PUT'])  # Cobranca
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_cobrancas_por_id():
    return jsonify()


@app.route('/movimentacoes', methods=['GET', 'POST', 'PUT'])  # Movimentacoes
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_movimentacoes():
    return jsonify()


@app.route('/movimentacoes/<string:movimentacao_id>', methods=['GET', 'POST', 'PUT'])  # Movimentacao
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_movimentacoes_por_id():
    return jsonify()


@app.route('/usuarios/<int:usuario_id>', methods=['GET', 'POST', 'PUT'])  # Usuario
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_usuarios():
    return jsonify()


@app.route('/cadastro', methods=['POST'])
@cross_origin(origin='/*', headers=['Content-Type'])
def post():
    data = request.get_json()
    nome = data["usuario_nome"]
    sobrenome = data["usuario_sobrenome"]
    login = data["usuario_login"]
    senha = data["usuario_senha"]
    user = UserModel(nome, sobrenome, login, senha)
    if UserModel.achar_por_login(login):
        return {'message': 'usuario já cadastrado.'}
    user.salvar_usuario()
    return {'message': 'usuario cadastrado com sucesso!'}, 201


@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*', headers=['Content-Type'])
def usuario_login():
    data = request.get_json()
    login = data['usuario_login']
    senha = data['usuario_senha']
    user = UserModel.achar_por_login(login)
    if user and safe_str_cmp(user.usuario_senha, senha):
        token_acesso = create_access_token(identity=user.usuario_id)
        return {'access_token': token_acesso}, 200
    return {'message': 'login ou senha inválidos!'}, 401


@app.route('/logout', methods=['POST' 'OPTIONS'])  # UsuarioLogout
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def logout_usuario():
    return jsonify()


@app.route('/orcamentos', methods=['GET', 'POST', 'PUT'])  # Orcamentos
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_orcamentos():
    return jsonify()


@app.route('/orcamentos/<string:orcamento_id>', methods=['GET', 'POST', 'PUT'])  # Orcamento
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_orcamentos_por_id():
    return jsonify()


@app.route('/servicos', methods=['GET', 'POST', 'PUT'])  # Servicos
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_servicos():
    return jsonify()


@app.route('/servicos/<string:servico_id>', methods=['GET', 'POST', 'PUT'])  # Servico
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listar_servicos_por_id():
    return jsonify()


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
