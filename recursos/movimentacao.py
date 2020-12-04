from config_json import *
from flask_restful import Resource, reqparse
from flask.helpers import make_response
from flask import render_template
from modelos.movimentacao import MovimentacaoModel
import psycopg2

def returnMoviments():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    consulta = "SELECT movimentacao_id, movimentacao_nome, movimentacao_descricao, movimentacao_destino, movimentacao_valor FROM movimentacoes"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    movimentacoes = []
    for linha in resultado:
        movimentacoes.append({
            'movimentacao_id': linha[0],
            'movimentacao_nome': linha[1],
            'movimentacao_descricao': linha[2],
            'movimentacao_destino': linha[3],
            'movimentacao_valor': linha[4]})
    return movimentacoes

class Movimentacoes(Resource):
    def get(self):
        return returnMoviments()
class TotalMovimentos(Resource):
    def get(self):
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        consulta = "SELECT SUM(movimentacao_valor) FROM movimentacoes AS total"
        cursor.execute(consulta)
        resultado = cursor.fetchone()[0]
        return resultado

argumentos = reqparse.RequestParser()
argumentos.add_argument('movimentacao_nome', type=str, required=True, help="Campo 'Nome da transação' não pode estar vazio!")
argumentos.add_argument('movimentacao_descricao', type=str, required=False)
argumentos.add_argument('movimentacao_destino', type=str, required=True, help="Campo 'Destino' não pode estar vazio!")
argumentos.add_argument('movimentacao_valor', type=float, required=True, help="Campo 'Valor' não pode estar vazio!")

class Movimentacao(Resource):
    def get(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            return make_response(movimentacao.json())
        return make_response(render_template("moviments.html", message="Movimentação não encontrada."), 404)

    def post(self):
        data = argumentos.parse_args()
        movimentacao = MovimentacaoModel(**data)
        movimentacao.salvar_movimentacao()
        movimentacoes = returnMoviments()
        return make_response(render_template("reportMoviment.html", movimentacoes = movimentacoes), 201)

class Movimento(Resource):
    def post(self, movimentacao_id):
        movimentacao = MovimentacaoModel.achar_movimentacao(movimentacao_id)
        if movimentacao:
            movimentacao.deletar_movimentacao()
        movimentacoes = returnMoviments()
        return make_response(render_template("reportMoviment.html", movimentacoes = movimentacoes),201)
