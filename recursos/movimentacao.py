from flask_restful import Resource, reqparse
from modelos.movimentacao import MovimentacaoModel
from flask_jwt_extended import jwt_required
import sqlite3


def normal_parametros(movimentacao_cliente_id=None, valor_min=0, valor_max=9999999999, limit=50, offset=0, **data):
    if movimentacao_cliente_id:
        return {
            'movimentacao_cliente_id': movimentacao_cliente_id,
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
path_parametro.add_argument('movimentacao_cliente_id', type=str)
path_parametro.add_argument('valor_min', type=float)
path_parametro.add_argument('valor_max', type=float)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class Movimentacoes(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('movimentacao_cliente_id'):
            consulta = "SELECT * FROM movimentacoes WHERE (movimentacao_valor >= ?) and (movimentacao_valor <= ?) LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = "SELECT * FROM movimentacoes WHERE (movimentacao_cliente_id = ?) and (movimentacao_valor >= ?) and (movimentacao_valor <= ?) LIMIT ? OFFSET ?"
            tupla = tuple([parametro[chave] for chave in parametro])
            resultado = cursor.execute(consulta, tupla)
        movimentacoes = []
        for linha in resultado:
            movimentacoes.append({
                'movimentacao_id': linha[0],
                'movimentacao_origem': linha[1],
                'movimentacao_valor': linha[2],
                'movimentacao_parcela': linha[3],
                'movimentacao_vencimento': linha[4],
                'movimentacao_transacao': linha[5],
                'movimentacao_tipo': linha[6],
                'movimentacao_cliente_id': linha[7]})
        return {'movimentacoes': movimentacoes}


class Movimentacao(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('movimentacao_origem', type=str, required=True, help="origem do pagamento não pode estar vazia.")
    argumentos.add_argument('movimentacao_valor', type=float, required=True, help="valor do pagamento não pode estar vazio.")
    argumentos.add_argument('movimentacao_parcela', type=str, required=False)
    argumentos.add_argument('movimentacao_vencimento', type=str, required=False)
    argumentos.add_argument('movimentacao_transacao', type=str, required=False)
    argumentos.add_argument('movimentacao_tipo', type=str, required=True, help="tipo de pagamento não pode estar vazio.")
    argumentos.add_argument('movimentacao_cliente_id', type=str, required=True, help="cliente deve ser informado.")

    def get(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            return movimentacao.json()
        return {'message': 'Movimentação não encontrada.'}, 404  # Not Found

    @jwt_required
    def post(self, movimentacao_id):
        if MovimentacaoModel.achar_movimentacao(movimentacao_id):
            return {"message": "Id de movimentação '{}' Já existe.".format(movimentacao_id)}, 400  # bad request
        data = Movimentacao.argumentos.parse_args()
        movimentacao = MovimentacaoModel(movimentacao_id, **data)
        try:
            movimentacao.salvar_movimentacao()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return movimentacao.json()

    @jwt_required
    def put(self, movimentacao_id):
        data = Movimentacao.argumentos.parse_args()
        movimentacao_encontrado = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao_encontrado:
            movimentacao_encontrado.atualizar_movimentacao(**data)
            movimentacao_encontrado.salvar_movimentacao()
            return movimentacao_encontrado.json(), 200  # OK
        movimentacao = MovimentacaoModel(movimentacao_id, **data)
        try:
            movimentacao.salvar_movimentacao()
        except 'ERR1000':
            return {'message': "Erro ao tentar salvar os dados"}, 500
        return movimentacao.json(), 201  # created

    @jwt_required
    def delete(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            try:
                movimentacao.deletar_movimentacao()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Cobrança deletada com sucesso.'}
        return {'message': 'Cobrança não encontrada.'}, 404  # not Found
