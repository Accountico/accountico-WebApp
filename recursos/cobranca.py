from flask.helpers import make_response
from flask.templating import render_template
from flask_restful import Resource, reqparse
from modelos.cobranca import CobrancaModel
from flask_jwt_extended import jwt_required
import psycopg2


def normal_parametros(cobranca_remetente=None, valor_min=0, valor_max=9999999999, limit=50, offset=0, **data):
    if cobranca_remetente:
        return {
            'cobranca_remetente': cobranca_remetente,
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
path_parametro.add_argument('cobranca_remetente', type=str)
path_parametro.add_argument('valor_min', type=float)
path_parametro.add_argument('valor_max', type=float)
path_parametro.add_argument('limit', type=float)
path_parametro.add_argument('offset', type=float)


class Cobrancas(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        data = path_parametro.parse_args()
        validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        parametro = normal_parametros(**validar_data)
        if not parametro.get('cobranca_remetente'):
            consulta = "SELECT * FROM cobrancas WHERE (cobranca_valor >= %s) and (cobranca_valor <= %s) ORDER BY cobranca_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        else:
            consulta = "SELECT * FROM cobrancas WHERE (cobranca_remetente = %s) and (cobranca_valor >= %s) and (cobranca_valor <= %s) ORDER BY cobranca_id ASC LIMIT %s OFFSET %s"
            tupla = tuple([parametro[chave] for chave in parametro])
            cursor.execute(consulta, tupla)
            resultado = cursor.fetchall()
        cobrancas = []
        if resultado:
            for linha in resultado:
                cobrancas.append({
                    'cobranca_id': linha[0],
                    'cobranca_nome': linha[1],
                    'cobranca_descricao': linha[2],
                    'cobranca_remetente': linha[3],
                    'cobranca_valor': linha[4]})
            return cobrancas


def total_parametros(cobranca_remetente=None, valor_min=0, valor_max=9999999999, **data):
    if cobranca_remetente:
        return {
            'cobranca_remetente': cobranca_remetente,
            'valor_min': valor_min,
            'valor_max': valor_max}
    return {
        'valor_min': valor_min,
        'valor_max': valor_max}


pathy_parametro = reqparse.RequestParser()
pathy_parametro.add_argument('cobranca_remetente', type=str)


class TotalCobrancas(Resource):
    def get(self):
        connection = psycopg2.connect(user='postgres', password='admin', host='localhost', port='5432', database='postgres')
        cursor = connection.cursor()
        # data = pathy_parametro.parse_args()
        # validar_data = {chave: data[chave] for chave in data if data[chave] is not None}
        # parametro = total_parametros(**validar_data)
        consulta = "SELECT SUM(cobranca_valor) FROM cobrancas AS total"
        # tupla = tuple([parametro[chave] for chave in parametro])
        cursor.execute(consulta)
        resultado = cursor.fetchone()[0]
        return resultado


argumentos = reqparse.RequestParser()
argumentos.add_argument('cobranca_nome', type=str, required=True, help="Campo 'Nome da transação' não pode estar vazio.")
argumentos.add_argument('cobranca_descricao', type=str, required=False)
argumentos.add_argument('cobranca_remetente', type=str, required=True, help="Campo 'Remetente' não pode estar vazio.")
argumentos.add_argument('cobranca_valor', type=float, required=True, help="Campo 'Valor' não pode estar vazio.")


class Cobranca(Resource):
    def get(self, cobranca_id):
        cobranca = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca:
            return cobranca.json()
        return make_response(render_template("charges.html", message="Cobrança não encontrada."), 404)

    def post(self):
        data = argumentos.parse_args()
        cobranca = CobrancaModel(**data)
        cobranca.salvar_cobranca()
        return make_response(render_template("charges.html", message="Cobrança cadastrada com sucesso!"), 201)


class Cobrar(Resource):
    def delete(self, cobranca_id):
        cobranca = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca:
            try:
                cobranca.deletar_cobranca()
            except 'ERR1001':
                {'message': "Erro ao tentar deletar os dados"}, 500
            return {'message': 'Cobrança deletada com sucesso.'}
        return {'message': 'Cobrança não encontrada.'}, 404  # not Found
