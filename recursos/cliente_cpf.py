from flask_restful import Resource, reqparse
from flask.helpers import make_response
from flask import render_template
from modelos.cliente_cpf import ClienteModel
import psycopg2


def normal_parametros(cliente_nome=None, limit=50, offset=0, **data):
    if cliente_nome:
        return {
            'cliente_nome': cliente_nome,
            'limit': limit,
            'offset': offset}
    return {
            'limit': limit,
            'offset': offset}


path_parametro = reqparse.RequestParser()
path_parametro.add_argument('cliente_nome', type=str)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class ClientesCpf(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('cliente_nome'):
            consulta = "SELECT * FROM pessoafisica ORDER BY cliente_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        else:
            consulta = "SELECT * FROM pessoafisica WHERE (cliente_nome = %s) ORDER BY cliente_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        pessoafisica = []
        if resultado:
            for linha in resultado:
                pessoafisica.append({
                    'cliente_id': linha[0],
                    'cliente_cpf': linha[1],
                    'cliente_nome': linha[2],
                    'cliente_telefone': linha[3],
                    'cliente_celular': linha[4],
                    'cliente_email': linha[5]})
            return {'pessoafisica': pessoafisica}


argumentos = reqparse.RequestParser()
argumentos.add_argument('cliente_cpf', type=str, required=True, help="Campo 'CPF' não pode estar vazio.")
argumentos.add_argument('cliente_nome', type=str, required=True, help="Campo 'nome cliente' não pode estar vazio.")
argumentos.add_argument('cliente_telefone', type=str, required=False)
argumentos.add_argument('cliente_celular', type=str, required=False)
argumentos.add_argument('cliente_email', type=str, required=False)


class ClienteCpf(Resource):
    def get(self, cliente_id):
        cliente = ClienteModel.achar_cliente(cliente_id)
        if cliente:
            return cliente.json()
        return {'message': 'Cliente não encontrado.'}, 404  # return make_response(render_template("client.html", message="Cliente não encontrado."), 404)

    def post(self):
        data = argumentos.parse_args()
        nome_encontrado = ClienteModel(**data)
        if nome_encontrado.achar_cliente_cpf(data['cliente_cpf']):
            return {'message': 'Cliente já cadastrado'}, 409
        cliente = ClienteModel(**data)
        cliente.salvar_cliente()
        return {'message': 'Cliente cadastrado com sucesso!'}, 201  # return make_response(render_template("client.html", message="Cliente cadastrado com sucesso!"), 201)


class ClienteCpfs(Resource):
    def put(self, cliente_id):
        data = argumentos.parse_args()
        cliente_encontrado = ClienteModel.achar_cliente(cliente_id)
        if cliente_encontrado:
            cliente_encontrado.atualizar_cliente(**data)
            cliente_encontrado.salvar_cliente()
            return {'message': 'Dados alterados com sucesso!'}  # return make_response(render_template("client.html", message="Cliente alterado com sucesso!"), 200)
        dados = argumentos.parse_args()
        cliente = ClienteModel(**dados)
        cliente.salvar_cliente()
        return {'message': 'Cliente cadastrado com sucesso!'}  # return make_response(render_template("client.html", message="Cliente cadastrado com sucesso!"), 201)

    def delete(self, cliente_id):
        cliente = ClienteModel.achar_cliente(cliente_id)
        if cliente:
            try:
                cliente.deletar_cliente()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500  # make_response(render_template("client.html", message="Erro ao tentar deletar os dados"), 500)
            return {'message': 'Cliente deletado com sucesso.'}, 200  # return make_response(render_template("client.html", message="Cliente deletado com sucesso."), 200)
        return {'message': 'Cliente não encontrado.'}, 404  # return make_response(render_template("client.html", message=""), 404)
