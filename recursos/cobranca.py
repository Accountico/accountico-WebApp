from flask_restful import Resource, reqparse
from modelos.cobranca import CobrancaModel
from flask_jwt_extended import jwt_required
import psycopg2


def normal_parametros(cobranca_orcamento_id=None, limit=50, offset=0, **data):
    if cobranca_orcamento_id:
        return {
            'cobranca_orcamento_id': cobranca_orcamento_id,
            'limit': limit,
            'offset': offset}
    return {
        'limit': limit,
        'offset': offset}


path_parametro = reqparse.RequestParser()
path_parametro.add_argument('cobranca_orcamento_id', type=str)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class Cobrancas(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('cobranca_orcamento_id'):
            consulta = "SELECT * FROM cobrancas LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        else:
            consulta = "SELECT * FROM cobrancas WHERE (cobranca_orcamento_id = %s) LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        cobrancas = []
        if resultado:
            for linha in resultado:
                cobrancas.append({
                    'cobranca_id': linha[0],
                    'cobranca_banco': linha[1],
                    'cobranca_vencimento': linha[2],
                    'cobranca_pagamento': linha[3],
                    'cobranca_observacao': linha[4],
                    'cobranca_valor': linha[5],
                    'cobranca_orcamento_id': linha[6]})
            return {'cobrancas': cobrancas}


class Cobranca(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('cobranca_banco', type=str, required=True, help="nome do banco não pode estar vazio.")
    argumentos.add_argument('cobranca_vencimento', type=str, required=False)
    argumentos.add_argument('cobranca_pagamento', type=str, required=False)
    argumentos.add_argument('cobranca_observacao', type=str, required=False)
    argumentos.add_argument('cobranca_valor', type=str, required=True, help="valor da cobrança não pode estar vazio")
    argumentos.add_argument('cobranca_orcamento_id', type=str, required=True, help="numero do orçamento deve ser informado")

    def get(self, cobranca_id):
        cobranca = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca:
            return cobranca.json()
        return {'message': 'Cobrança não encontrada.'}, 404  # Not Found

    @jwt_required
    def post(self, cobranca_id):
        if CobrancaModel.achar_cobranca(cobranca_id):
            return {"message": "Id de cobrança '{}' Já existe.".format(cobranca_id)}, 400  # bad request
        data = Cobranca.argumentos.parse_args()
        cobranca = CobrancaModel(cobranca_id, **data)
        try:
            cobranca.salvar_cobranca()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return cobranca.json()

    @jwt_required
    def put(self, cobranca_id):
        data = Cobranca.argumentos.parse_args()
        cobranca_encontrado = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca_encontrado:
            cobranca_encontrado.atualizar_cobranca(**data)
            cobranca_encontrado.salvar_cobranca()
            return cobranca_encontrado.json(), 200  # OK
        cobranca = CobrancaModel(cobranca_id, **data)
        try:
            cobranca.salvar_cobranca()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return cobranca.json(), 201  # created

    @jwt_required
    def delete(self, cobranca_id):
        cobranca = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca:
            try:
                cobranca.deletar_cobranca()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Cobrança deletada com sucesso.'}
        return {'message': 'Cobrança não encontrada.'}, 404  # not Found
