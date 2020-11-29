from flask.helpers import make_response
from flask import render_template
from flask_restful import Resource, reqparse
from modelos.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('usuario_login', type=str, required=True, help="Campo 'login' não pode estar vazio.")
atributos.add_argument('usuario_senha', type=str, required=True, help="Campo 'senha' não pode estar vazio.")
atributos.add_argument('usuario_nome', type=str, required=True, help="Campo 'nome' não pode estar vazio.")
atributos.add_argument('usuario_sobrenome', type=str, required=True, help="Campo 'sobrenome' não pode estar vazio.")

atributos_login = reqparse.RequestParser()
atributos_login.add_argument('usuario_login', type=str, required=True, help="Campo 'login' não pode estar vazio.")
atributos_login.add_argument('usuario_senha', type=str, required=True, help="Campo 'senha' não pode estar vazio.")


class Usuario(Resource):
    def get(self, usuario_id):
        user = UserModel.achar_usuario(usuario_id)
        if user:
            return user.json()
        return {'message': 'User not Found.'}, 404  # Not Found

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
            return make_response(render_template("register.html", message="Usuario já cadastrado!"), 409)
        user = UserModel(**data)
        user.salvar_usuario()
        return make_response(render_template("login.html", message="Usuario cadastrado com sucesso!"), 201)


class UsuarioLogin(Resource):
    @classmethod
    def post(cls):
        data = atributos_login.parse_args()
        user = UserModel.achar_por_login(data['usuario_login'])
        if user and safe_str_cmp(user.usuario_senha, data['usuario_senha']):
            # token_acesso = create_access_token(identity=user.usuario_id)
            r = make_response(render_template("index.html"))
            r.set_cookie("login", data['usuario_login'], samesite="Strict")
            r.set_cookie("senha", data['usuario_senha'], samesite="Strict")
            return r
        return make_response(render_template("login.html", message="Usuário ou senha incorreta"), 401)


class UsuarioLogout(Resource):
    def post(self):
        r = make_response(render_template("login.html", message="Deslogou com sucesso!"))
        r.set_cookie("login", "")
        r.set_cookie("senha", "")
        # jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        # BLACKLIST.add(jwt_id)
        return r
