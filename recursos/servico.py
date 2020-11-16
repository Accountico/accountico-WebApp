from flask_restful import Resource, reqparse
from modelos.servico import ServicoModel
from flask_jwt_extended import jwt_required
import sqlite3


def normal_parametros(servico_nome=None, limit=50, offset=0, **data):
    if servico_nome:
        return {
            'servico_nome': servico_nome,
            'limit': limit,
            'offset': offset}
    return {
        'limit': limit,
        'offset': offset}


path_parametro = reqparse.RequestParser()
path_parametro.add_argument('servico_nome', type=str)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class Servicos(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('servico_nome'):
            consulta = "SELECT * FROM servicos LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM servicos WHERE (servico_nome = ?) LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        servicos = []
        for linha in resultado:
            servicos.append({
                'servico_id': linha[0],
                'servico_nome': linha[1],
                'servico_status': linha[2],
                'servico_observacao': linha[3],
                'servico_orcamento_id': linha[4]})
        return {'servicos': servicos}


class Servico(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('servico_nome', type=str, required=True, help="campo 'nome serviço' não pode estar vazio.")
    argumentos.add_argument('servico_status', type=str, required=True, help="situação do serviço precisa ser informada.")
    argumentos.add_argument('servico_observacao', type=str, required=False)
    argumentos.add_argument('servico_orcamento_id', type=str, required=True, help="orçamento deve ser informado.")

    def get(self, servico_id):
        servico = ServicoModel.achar_servico(servico_id)
        if servico:
            return servico.json()
        return {'message': 'Serviço não encontrado.'}, 404  # Not Found

    @jwt_required
    def post(self, servico_id):
        if ServicoModel.achar_servico(servico_id):
            return {"message": "Id de serviço '{}' Já existe.".format(servico_id)}, 400  # bad request
        data = Servico.argumentos.parse_args()
        servico = ServicoModel(servico_id, **data)
        try:
            servico.salvar_servico()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return servico.json()

    @jwt_required
    def put(self, servico_id):
        data = Servico.argumentos.parse_args()
        servico_encontrado = ServicoModel.achar_servico(servico_id)
        if servico_encontrado:
            servico_encontrado.atualizar_servico(**data)
            servico_encontrado.salvar_servico()
            return servico_encontrado.json(), 200  # OK
        servico = ServicoModel(servico_id, **data)
        try:
            servico.salvar_servico()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return servico.json(), 201  # created

    @jwt_required
    def delete(self, servico_id):
        servico = ServicoModel.achar_servico(servico_id)
        if servico:
            try:
                servico.deletar_servico()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Orçamento deletado com sucesso.'}
        return {'message': 'Orçamento não encontrado.'}, 404  # not Found
