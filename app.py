from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from recursos.cliente_cnpj import ClientesCnpj, ClienteCnpj, ClienteCnpjs
from recursos.cliente_cpf import ClientesCpf, ClienteCpf, ClienteCpfs
from recursos.cobranca import Cobrancas, Cobranca
from recursos.movimentacao import Movimentacoes, Movimentacao
from recursos.orcamento import Orcamentos, Orcamento
from recursos.servico import Servicos, Servico
from recursos.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from modelos.usuario import UserModel
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from werkzeug.security import safe_str_cmp
# from config_json import DATABASE_URL


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost:5432/postgres'
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


@app.route('/')
def login():
    if login_ok(request):
        return render_template("index.html")
    return render_template('login.html', message="")


@app.route('/register')
def register():
    if login_ok(request):
        return render_template("login.html")
    return render_template('register.html')


@app.route('/home')
def home():
    if login_ok(request):
        return render_template("index.html")
    return render_template("login.html", message="sem autorização")


@app.route('/client')
def client():
    if login_ok(request):
        return render_template("client.html")
    return render_template("login.html", message="sem autorização")


@app.route('/services')
def services():
    if login_ok(request):
        return render_template("services.html")
    return render_template("login.html", message="sem autorização")


def login_ok(req):
    login = req.cookies.get("login")
    senha = req.cookies.get("senha")
    user = UserModel.achar_por_login(login)
    return user is not None and safe_str_cmp(user.usuario_senha, senha)


api.add_resource(ClientesCpf, '/clientes-cpf')
api.add_resource(ClienteCpf, '/clientescpf')
api.add_resource(ClienteCpfs, '/clientescpfs/<string:cliente_id>')
api.add_resource(ClientesCnpj, '/clientes-cnpj')
api.add_resource(ClienteCnpj, '/clientescnpj')
api.add_resource(ClienteCnpjs, '/clientescnpjs/<string:cliente_id>')
api.add_resource(Cobrancas, '/cobrancas')
api.add_resource(Cobranca, '/cobrancas/<string:cobranca_id>')
api.add_resource(Movimentacoes, '/movimentacoes')
api.add_resource(Movimentacao, '/movimentacao')
api.add_resource(Orcamentos, '/orcamentos')
api.add_resource(Orcamento, '/orcamentos/<string:orcamentos_id>')
api.add_resource(Servicos, '/servicos')
api.add_resource(Servico, '/servicos/<string:servicos_id>')
api.add_resource(Usuario, '/usuarios/<int:user_id>')
api.add_resource(UsuarioRegistro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
