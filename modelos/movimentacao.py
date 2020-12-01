from sql_alchemy import banco
# from modelos.cliente import ClienteModel

class MovimentacaoModel(banco.Model):
    __tablename__ = 'movimentacoes'
    movimentacao_id = banco.Column(banco.Integer, primary_key=True)
    movimentacao_nome = banco.Column(banco.String(30))
    movimentacao_descricao = banco.Column(banco.String(200))
    movimentacao_destino = banco.Column(banco.String(50))
    movimentacao_valor = banco.Column(banco.Float())


    def __init__(self, movimentacao_nome, movimentacao_descricao, movimentacao_destino, movimentacao_valor):
        self.movimentacao_nome = movimentacao_nome
        self.movimentacao_descricao = movimentacao_descricao
        self.movimentacao_destino = movimentacao_destino
        self.movimentacao_valor = movimentacao_valor

    def json(self):
        return {
            'movimentacao_id': self.movimentacao_id,
            'movimentacao_nome': self.movimentacao_nome,
            'movimentacao_descricao': self.movimentacao_descricao,
            'movimentacao_destino': self.movimentacao_destino,
            'movimentacao_valor': self.movimentacao_valor
        }

    @classmethod
    def achar_movimentacao(cls, movimentacao_id):
        movimentacao = cls.query.filter_by(movimentacao_id=movimentacao_id).first()
        if movimentacao:
            return movimentacao
        return None

#    @classmethod
#    def somar_movimentacao(cls, movimentacao_id):
#        valores = cls.query.filter_by(movimentacao_id=movimentacao_id).first()

    def salvar_movimentacao(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_movimentacao(self):
        banco.session.delete(self)
        banco.session.commit()
