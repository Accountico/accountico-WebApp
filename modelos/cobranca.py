from sql_alchemy import banco


class CobrancaModel(banco.Model):
    __tablename__ = 'cobrancas'
    cobranca_id = banco.Column(banco.Integer, primary_key=True)
    cobranca_nome = banco.Column(banco.String(30))
    cobranca_descricao = banco.Column(banco.String(200))
    cobranca_remetente = banco.Column(banco.String(50))
    cobranca_valor = banco.Column(banco.Float())

    def __init__(self, cobranca_nome, cobranca_descricao, cobranca_remetente, cobranca_valor):
        self.cobranca_nome = cobranca_nome
        self.cobranca_descricao = cobranca_descricao
        self.cobranca_remetente = cobranca_remetente
        self.cobranca_valor = cobranca_valor

    def json(self):
        return {
            'cobranca_id': self.cobranca_id,
            'cobranca_nome': self.cobranca_nome,
            'cobranca_descricao': self.cobranca_descricao,
            'cobranca_remetente': self.cobranca_remetente,
            'cobranca_valor': self.cobranca_valor
        }

    @classmethod
    def achar_cobranca(cls, cobranca_id):
        cobranca = cls.query.filter_by(cobranca_id=cobranca_id).first()
        if cobranca:
            return cobranca
        return None

    def salvar_cobranca(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_cobranca(self, cobranca_banco, cobranca_vencimento, cobranca_pagamento, cobranca_observacao, cobranca_valor, cobranca_orcamento_id):
        self.cobranca_banco = cobranca_banco
        self.cobranca_vencimento = cobranca_vencimento
        self.cobranca_pagamento = cobranca_pagamento
        self.cobranca_observacao = cobranca_observacao
        self.cobranca_valor = cobranca_valor
        self.cobranca_orcamento_id = cobranca_orcamento_id

    def deletar_cobranca(self):
        banco.session.delete(self)
        banco.session.commit()
