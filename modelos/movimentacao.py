from sql_alchemy import banco
# from modelos.cliente import ClienteModel


class MovimentacaoModel(banco.Model):
    __tablename__ = 'movimentacoes'
    movimentacao_id = banco.Column(banco.String, primary_key=True)
    movimentacao_origem = banco.Column(banco.String(150))
    movimentacao_valor = banco.Column(banco.Float(precision=2))
    movimentacao_parcela = banco.Column(banco.String(5))
    movimentacao_vencimento = banco.Column(banco.String(10))
    movimentacao_transacao = banco.Column(banco.String(20))
    movimentacao_tipo = banco.Column(banco.String(25))
    movimentacao_cliente_id = banco.Column(banco.String)

    def __init__(self, movimentacao_id, movimentacao_origem, movimentacao_valor, movimentacao_parcela, movimentacao_vencimento, movimentacao_transacao, movimentacao_tipo, movimentacao_cliente_id):
        self.movimentacao_id = movimentacao_id
        self.movimentacao_origem = movimentacao_origem
        self.movimentacao_valor = movimentacao_valor
        self.movimentacao_parcela = movimentacao_parcela
        self.movimentacao_vencimento = movimentacao_vencimento
        self.movimentacao_transacao = movimentacao_transacao
        self.movimentacao_tipo = movimentacao_tipo
        self.movimentacao_cliente_id = movimentacao_cliente_id

    def json(self):
        return {
            'movimentacao_id': self.movimentacao_id,
            'movimentacao_origem': self.movimentacao_origem,
            'movimentacao_valor': self.movimentacao_valor,
            'movimentacao_parcela': self.movimentacao_parcela,
            'movimentacao_vencimento': self.movimentacao_vencimento,
            'movimentacao_transacao': self.movimentacao_transacao,
            'movimentacao_tipo': self.movimentacao_tipo,
            'movimentacao_cliente_id': self.movimentacao_cliente_id
        }

    @classmethod
    def achar_movimentacao(cls, movimentacao_id):
        movimentacao = cls.query.filter_by(movimentacao_id=movimentacao_id).first()
        if movimentacao:
            return movimentacao
        return None

    def salvar_movimentacao(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_movimentacao(self, movimentacao_origem, movimentacao_valor, movimentacao_parcela, movimentacao_vencimento, movimentacao_transacao, movimentacao_tipo, movimentacao_cliente_id):
        self.movimentacao_origem = movimentacao_origem
        self.movimentacao_valor = movimentacao_valor
        self.movimentacao_parcela = movimentacao_parcela
        self.movimentacao_vencimento = movimentacao_vencimento
        self.movimentacao_transacao = movimentacao_transacao
        self.movimentacao_tipo = movimentacao_tipo
        self.movimentacao_cliente_id = movimentacao_cliente_id

    def deletar_movimentacao(self):
        banco.session.delete(self)
        banco.session.commit()
