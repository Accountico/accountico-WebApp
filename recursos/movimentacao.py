from flask_restful import Resource, reqparse
from flask.helpers import make_response
from flask import render_template
from modelos.movimentacao import MovimentacaoModel
import psycopg2


def normal_parametros(movimentacao_destino=None, valor_min=0, valor_max=9999999999, limit=50, offset=0, **data):
    if movimentacao_destino:
        return {
            'movimentacao_destino': movimentacao_destino,
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
path_parametro.add_argument('movimentacao_destino', type=str)
path_parametro.add_argument('valor_min', type=float)
path_parametro.add_argument('valor_max', type=float)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


def total_parametros(movimentacao_destino=None, valor_min=0, valor_max=9999999999, **data):
    if movimentacao_destino:
        return {
            'movimentacao_destino': movimentacao_destino,
            'valor_min': valor_min,
            'valor_max': valor_max}
    return {
        'valor_min': valor_min,
        'valor_max': valor_max}


pathy_parametro = reqparse.RequestParser()
pathy_parametro.add_argument('movimentacao_destino', type=str)


class TotalMovimentos(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = pathy_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = total_parametros(**validar_data)
        consulta = "SELECT SUM(movimentacao_valor) FROM movimentacoes"
        tupla = tuple([parametro[chave] for chave in parametro])
        cursor.execute(consulta, tupla)
        resultado = cursor.fetchone()[0]
        return resultado


class Movimentacoes(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('movimentacao_destino'):
            consulta = "SELECT * FROM movimentacoes WHERE (movimentacao_valor >= %s) and (movimentacao_valor <= %s) ORDER BY movimentacao_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        else:
            consulta = "SELECT * FROM movimentacoes WHERE (movimentacao_destino = %s) and (movimentacao_valor >= %s) and (movimentacao_valor <= %s) ORDER BY movimentacao_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        movimentacoes = []
        if resultado:
            for linha in resultado:
                movimentacoes.append({
                    'movimentacao_id': linha[0],
                    'movimentacao_nome': linha[1],
                    'movimentacao_descricao': linha[2],
                    'movimentacao_destino': linha[3],
                    'movimentacao_valor': linha[4]})
            return {'movimentacoes': movimentacoes}


argumentos = reqparse.RequestParser()
argumentos.add_argument('movimentacao_nome', type=str, required=True, help="Campo 'Nome da transação' não pode estar vazio!")
argumentos.add_argument('movimentacao_descricao', type=str, required=False)
argumentos.add_argument('movimentacao_destino', type=str, required=True, help="Campo 'Destino' não pode estar vazio!")
argumentos.add_argument('movimentacao_valor', type=float, required=True, help="Campo 'Valor' não pode estar vazio!")


class Movimentacao(Resource):
    def get(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            return movimentacao.json()
        return make_response(render_template("moviments.html", message="Movimentação não encontrada."), 404)

    def post(self):
        data = argumentos.parse_args()
        mov = MovimentacaoModel(**data)
        mov.salvar_movimentacao()
        return make_response(render_template("moviments.html", message="Movimentação cadastrada com sucesso!"), 201)


class Movimento(Resource):
    def delete(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            try:
                movimentacao.deletar_movimentacao()
            except 'ERR1001':
                make_response(render_template("moviments.html", message=" Erro ao tentar deletar os dados."), 500)
            return make_response(render_template("moviments.html", message="Cobrança deletada com sucesso!"), 200)
        return make_response(render_template("moviments.html", message="Cobrança não encontrada."), 404)
