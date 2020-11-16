from flask import Flask, jsonify
from flask_restful import Api
from recursos.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from recursos.cliente import Clientes, Cliente
from recursos.cobranca import Cobrancas, Cobranca
from recursos.movimentacao import Movimentacoes, Movimentacao
from recursos.orcamento import Orcamentos, Orcamento
from recursos.servico import Servicos, Servico
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'thisisaverylongmessagethatnobodywillevertryorknowjustbytryingbecauseitssohardtoguessthissecretkeyitisbutitsonlyletterssopaciencemaynullit'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
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


api.add_resource(Clientes, '/clientes')
api.add_resource(Cliente, '/clientes/<string:cliente_id>')
api.add_resource(Cobrancas, '/cobrancas')
api.add_resource(Cobranca, '/cobrancas/<string:cobranca_id>')
api.add_resource(Movimentacoes, '/movimentacoes')
api.add_resource(Movimentacao, '/movimentacoes/<string:movimentacao_id>')
api.add_resource(Usuario, '/usuarios/<int:usuario_id>')
api.add_resource(UsuarioRegistro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(Orcamentos, '/orcamentos')
api.add_resource(Orcamento, '/orcamentos/<string:orcamento_id>')
api.add_resource(Servicos, '/servicos')
api.add_resource(Servico, '/servicos/<string:servico_id>')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
