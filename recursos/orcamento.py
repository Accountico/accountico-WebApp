from flask_restful import Resource, reqparse
from modelos.orcamento import OrcamentoModel
from flask_jwt_extended import jwt_required
import psycopg2


def normal_parametros(orcamento_nome=None, valor_min=0, valor_max=999999999999, limit=50, offset=0, **data):
    if orcamento_nome:
        return {
            'orcamento_nome': orcamento_nome,
            'valor_min': valor_min,
            'valor_max': valor_max,
            'limit': limit,
            'offset': offset}
    return {
            'valor_min': valor_min,
            'valor_max': valor_max,
            'limit': limit,
            'offset': offset}


path_parametro = reqparse.RequestParser()
path_parametro.add_argument('orcamento_nome', type=str)
path_parametro.add_argument('valor_min', type=float)
path_parametro.add_argument('valor_max', type=float)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class Orcamentos(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('orcamento_nome'):
            consulta = "SELECT * FROM orcamentos WHERE (orcamento_valor >= %s) and (orcamento_valor <= %s) LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        else:
            consulta = "SELECT * FROM orcamentos WHERE (orcamento_nome = %s) and (orcamento_valor >= %s) and (orcamento_valor <= %s) LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        orcamentos = []
        if resultado:
            for linha in resultado:
                orcamentos.append({
                    'orcamento_id': linha[0],
                    'orcamento_nome': linha[1],
                    'orcamento_valor': linha[2],
                    'orcamento_status': linha[3],
                    'orcamento_observacao': linha[4],
                    'orcamento_previsao': linha[5],
                    'orcamento_pagamento': linha[6],
                    'orcamento_cliente_id': linha[7]})
            return {'orcamentos': orcamentos}


class Orcamento(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('orcamento_nome', type=str, required=True, help="campo 'nome orçamento' não pode estar vazio.")
    argumentos.add_argument('orcamento_valor', type=float, required=True, help="valor do orçamento precisa ser informado.")
    argumentos.add_argument('orcamento_status', type=str, required=True, help="situação do orçamento precisa ser informada.")
    argumentos.add_argument('orcamento_observacao', type=str, required=False)
    argumentos.add_argument('orcamento_previsao', type=str, required=False)
    argumentos.add_argument('orcamento_pagamento', type=str, required=True, help="forma de pagamento deve ser informada.")
    argumentos.add_argument('orcamento_cliente_id', type=str, required=True, help="cliente deve ser informado.")

    def get(self, orcamento_id):
        orcamento = OrcamentoModel.achar_orcamento(orcamento_id)
        if orcamento:
            return orcamento.json()
        return {'message': 'Orçamento não encontrado.'}, 404  # Not Found

    @jwt_required
    def post(self, orcamento_id):
        if OrcamentoModel.achar_orcamento(orcamento_id):
            return {"message": "Id do orçamento '{}' Já existe.".format(orcamento_id)}, 400  # bad request
        data = Orcamento.argumentos.parse_args()
        orcamento = OrcamentoModel(orcamento_id, **data)
        try:
            orcamento.salvar_orcamento()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return orcamento.json()

    @jwt_required
    def put(self, orcamento_id):
        data = Orcamento.argumentos.parse_args()
        orcamento_encontrado = OrcamentoModel.achar_orcamento(orcamento_id)
        if orcamento_encontrado:
            orcamento_encontrado.atualizar_orcamento(**data)
            orcamento_encontrado.salvar_orcamento()
            return orcamento_encontrado.json(), 200  # OK
        orcamento = OrcamentoModel(orcamento_id, **data)
        try:
            orcamento.salvar_orcamento()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return orcamento.json(), 201  # created

    @jwt_required
    def delete(self, orcamento_id):
        orcamento = OrcamentoModel.achar_orcamento(orcamento_id)
        if orcamento:
            try:
                orcamento.deletar_orcamento()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Orçamento deletado com sucesso.'}
        return {'message': 'Orçamento não encontrado.'}, 404  # not Found
