from sql_alchemy import banco
# from modelos.servico import ServicoModel


class CobrancaModel(banco.Model):
    __tablename__ = 'cobrancas'
    cobranca_id = banco.Column(banco.String, primary_key=True)
    cobranca_banco = banco.Column(banco.String(20))
    cobranca_vencimento = banco.Column(banco.String(10))
    cobranca_pagamento = banco.Column(banco.String(19))
    cobranca_observacao = banco.Column(banco.String(200))
    cobranca_valor = banco.Column(banco.Float(precision=2))
    cobranca_orcamento_id = banco.Column(banco.String)
    # cobranca_documento = banco.Column(img??.String)

    def __init__(self, cobranca_id, cobranca_banco, cobranca_vencimento, cobranca_pagamento, cobranca_observacao, cobranca_valor, cobranca_orcamento_id):
        self.cobranca_id = cobranca_id
        self.cobranca_banco = cobranca_banco
        self.cobranca_vencimento = cobranca_vencimento
        self.cobranca_pagamento = cobranca_pagamento
        self.cobranca_observacao = cobranca_observacao
        self.cobranca_valor = cobranca_valor
        self.cobranca_orcamento_id = cobranca_orcamento_id
        # self.cobranca_documento = cobranca_documento

    def json(self):
        return {
            'cobranca_id': self.cobranca_id,
            'cobranca_banco': self.cobranca_banco,
            'cobranca_vencimento': self.cobranca_vencimento,
            'cobranca_pagamento': self.cobranca_pagamento,
            'cobranca_observacao': self.cobranca_observacao,
            'cobranca_valor': self.cobranca_valor,
            'cobranca_orcamento_id': self.cobranca_orcamento_id
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
