from flask_restful import Resource, reqparse
from modelos.cliente import ClienteModel
from flask_jwt_extended import jwt_required
import sqlite3


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


class Clientes(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('cliente_nome'):
            consulta = "SELECT * FROM clientes LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM clientes WHERE (cliente_nome = ?) LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        clientes = []
        for linha in resultado:
            clientes.append({
                'cliente_id': linha[0],
                'cliente_cpf': linha[1],
                'cliente_cnpj': linha[2],
                'cliente_nome': linha[3],
                'cliente_telefone': linha[4],
                'cliente_celular': linha[5],
                'cliente_email': linha[6]})
        return {'clientes': clientes}


class Cliente(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('cliente_cpf', type=str, required=False)
    argumentos.add_argument('cliente_cnpj', type=str, required=False)
    argumentos.add_argument('cliente_nome', type=str, required=True, help="Campo 'nome cliente' não pode estar vazio.")
    argumentos.add_argument('cliente_telefone', type=str, required=False)
    argumentos.add_argument('cliente_celular', type=str, required=False)
    argumentos.add_argument('cliente_email', type=str, required=False)

    def get(self, cliente_id):
        cliente = ClienteModel.achar_cliente(cliente_id)
        if cliente:
            return cliente.json()
        return {'message': 'Cliente não encontrado.'}, 404  # Not Found

    @jwt_required
    def post(self, cliente_id):
        if ClienteModel.achar_cliente(cliente_id):
            return {"message": "Id de Cliente '{}' Já existe.".format(cliente_id)}, 400  # bad request
        data = Cliente.argumentos.parse_args()
        cliente = ClienteModel(cliente_id, **data)
        try:
            cliente.salvar_cliente()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return cliente.json()

    @jwt_required
    def put(self, cliente_id):
        data = Cliente.argumentos.parse_args()
        cliente_encontrado = ClienteModel.achar_cliente(cliente_id)
        if cliente_encontrado:
            cliente_encontrado.atualizar_cliente(**data)
            cliente_encontrado.salvar_cliente()
            return cliente_encontrado.json(), 200  # OK
        cliente = ClienteModel(cliente_id, **data)
        try:
            cliente.salvar_cliente()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return cliente.json(), 201  # created

    @jwt_required
    def delete(self, cliente_id):
        cliente = ClienteModel.achar_cliente(cliente_id)
        if cliente:
            try:
                cliente.deletar_cliente()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Cliente deletado com sucesso.'}
        return {'message': 'Cliente não encontrado.'}, 404  # not Found
