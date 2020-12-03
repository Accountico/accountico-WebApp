from config_json import DATABASE_URL
from flask.helpers import make_response
from flask import render_template
from flask_restful import Resource, reqparse
from modelos.cobranca import CobrancaModel
import psycopg2

def returnCharge():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    consulta = "SELECT cobranca_id, cobranca_nome, cobranca_descricao, cobranca_remetente, cobranca_valor FROM cobrancas"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    cobrancas = []
    for linha in resultado:
        cobrancas.append({
            'cobranca_id': linha[0],
            'cobranca_nome': linha[1],
            'cobranca_descricao': linha[2],
            'cobranca_remetente': linha[3],
            'cobranca_valor': linha[4]})
    return cobrancas
class Cobrancas(Resource):
    def get(self):
        return returnCharge()
        
class TotalCobrancas(Resource):
    def get(self):
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        consulta = "SELECT SUM(cobranca_valor) FROM cobrancas AS total"
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
            return make_response(cobranca.json())
        return make_response(render_template("charges.html", message="Cobrança não encontrada."), 404)

    def post(self):
        data = argumentos.parse_args()
        cobranca = CobrancaModel(**data)
        cobranca.salvar_cobranca()
        cobrancas = returnCharge()
        return make_response(render_template("reportCharge.html", cobrancas = cobrancas),201)

class Cobrar(Resource):
    def post(self, cobranca_id):
        cobranca = CobrancaModel.achar_cobranca(cobranca_id)
        if cobranca:
            cobranca.deletar_cobranca()
        cobrancas = returnCharge()
        return make_response(render_template("reportCharge.html", cobrancas = cobrancas),201)
