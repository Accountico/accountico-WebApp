from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from recursos.cobranca import Cobrancas, Cobranca, Cobrar, TotalCobrancas, returnCharge
from recursos.movimentacao import Movimentacoes, Movimentacao, Movimento, TotalMovimentos, returnMoviments
from recursos.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout, retornaValores
from modelos.usuario import UserModel
from flask_jwt_extended import JWTManager
from werkzeug.security import safe_str_cmp
from config_json import DATABASE_URL
from flask_sslify import SSLify


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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
        return render_template("login.html")
    return render_template('login.html', message="")

@app.route('/reportcharge')
def reportCharge():
    if login_ok(request):
        cobrancas = returnCharge()
        return render_template("reportCharge.html", cobrancas = cobrancas)
    return render_template('login.html', message="Sem autorização.")

@app.route('/reportmoviments')
def reportMoviments():
    if login_ok(request):
        movimentacoes = returnMoviments()
        return render_template("reportMoviment.html", movimentacoes = movimentacoes)
    return render_template('login.html', message="Sem autorização.")

@app.route('/register')
def register():
    if login_ok(request):
        return render_template("login.html")
    return render_template("register.html")

@app.route('/home')
def home():
    if login_ok(request):
       return retornaValores()
    return render_template("login.html", message="Sem autorização.")


@app.route('/cobranca')
def client():
    if login_ok(request):
        return render_template("charges.html")
    return render_template("login.html", message="Sem autorização.")


@app.route('/services')
def services():
    if login_ok(request):
        return render_template("services.html")
    return render_template("login.html", message="Sem autorização.")

@app.route('/movimentacao')
def payments():
    if login_ok(request):
        return render_template("moviments.html")
    return render_template("login.html", message="Sem autorização.")


def login_ok(req):
    login = req.cookies.get("login")
    senha = req.cookies.get("senha")
    user = UserModel.achar_por_login(login)
    return user is not None and safe_str_cmp(user.usuario_senha, senha)

api.add_resource(Cobrancas, '/cobrancas')  # GET
api.add_resource(Cobranca, '/cobranca')  # POST
api.add_resource(Cobrar, '/cobrar/<string:cobranca_id>') # DELETE
api.add_resource(TotalCobrancas, '/totalcobrancas')  # GET
api.add_resource(Movimentacoes, '/movimentacoes')
api.add_resource(Movimentacao, '/movimentacao')
api.add_resource(Movimento, '/movimento/<string:movimentacao_id>')
api.add_resource(TotalMovimentos, '/totalmovimentos')
api.add_resource(Usuario, '/usuarios/<int:user_id>')
api.add_resource(UsuarioRegistro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    # app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)
    sslify = SSLify(app.run(ssl_context=('cert.pem', 'key.pem'), debug=True))
