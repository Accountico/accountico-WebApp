from flask_restful import Resource, reqparse
from modelos.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('usuario_nome', type=str, required=True, help="Campo 'nome' não pode estar vazio.")
atributos.add_argument('usuario_sobrenome', type=str, required=True, help="Campo 'sobrenome' não pode estar vazio.")
atributos.add_argument('usuario_login', type=str, required=True, help="Campo 'login' não pode estar vazio.")
atributos.add_argument('usuario_senha', type=str, required=True, help="Campo 'senha' não pode estar vazio.")


class Usuario(Resource):
    def get(self, usuario_id):
        user = UserModel.achar_usuario(usuario_id)
        if user:
            return user.json()
        return {'message': 'User not Found.'}, 404  # Not Found

    @jwt_required
    def delete(self, usuario_id):
        user = UserModel.achar_usuario(usuario_id)
        if user:
            user.deletar_usuario()
            return {'message': 'Usuario deletado com sucesso.'}
        return {'message': 'Usuario não encontrado.'}, 404  # not Found


class UsuarioRegistro(Resource):
    def post(self):
        data = atributos.parse_args()
        if UserModel.achar_por_login(data['usuario_login']):
            return {"message": "login '{}' já existente.".format(data['usuario_login'])}
        user = UserModel(**data)
        user.salvar_usuario()
        return {'message': 'Usuario cadastrado com sucesso!'}, 201,  # created


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        data = atributos.parse_args()
        user = UserModel.achar_por_login(data['usuario_login'])
        if user and safe_str_cmp(user.usuario_senha, data['usuario_senha']):
            token_acesso = create_access_token(identity=user.usuario_id)
            return {'access_token': token_acesso}, 200
        return {'message': 'O usuario ou a senha esta incorreta.'}, 401


class UsuarioLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout realizado com sucesso.'}, 200
