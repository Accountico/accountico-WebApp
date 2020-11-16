from sql_alchemy import banco
# from modelos.cliente import ClienteModel


class OrcamentoModel(banco.Model):
    __tablename__ = 'orcamentos'
    orcamento_id = banco.Column(banco.String, primary_key=True)
    orcamento_nome = banco.Column(banco.String(100))
    orcamento_valor = banco.Column(banco.Float(precision=2))
    orcamento_status = banco.Column(banco.String(15))
    orcamento_observacao = banco.Column(banco.String(200))
    orcamento_previsao = banco.Column(banco.String(10))
    orcamento_pagamento = banco.Column(banco.String(25))
    orcamento_cliente_id = banco.Column(banco.String)

    def __init__(self, orcamento_id, orcamento_nome, orcamento_valor, orcamento_status, orcamento_observacao, orcamento_previsao, orcamento_pagamento, orcamento_cliente_id):
        self.orcamento_id = orcamento_id
        self.orcamento_nome = orcamento_nome
        self.orcamento_valor = orcamento_valor
        self.orcamento_status = orcamento_status
        self.orcamento_observacao = orcamento_observacao
        self.orcamento_previsao = orcamento_previsao
        self.orcamento_pagamento = orcamento_pagamento
        self.orcamento_cliente_id = orcamento_cliente_id

    def json(self):
        return {
            'orcamento_id': self.orcamento_id,
            'orcamento_nome': self.orcamento_nome,
            'orcamento_valor': self.orcamento_valor,
            'orcamento_status': self.orcamento_status,
            'orcamento_observacao': self.orcamento_observacao,
            'orcamento_previsao': self.orcamento_previsao,
            'orcamento_pagamento': self.orcamento_pagamento,
            'orcamento_cliente_id': self.orcamento_cliente_id
        }

    @classmethod
    def achar_orcamento(cls, orcamento_id):
        orcamento = cls.query.filter_by(orcamento_id=orcamento_id).first()
        if orcamento:
            return orcamento
        return None

    def salvar_orcamento(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_orcamento(self, orcamento_nome, orcamento_valor, orcamento_status, orcamento_observacao, orcamento_previsao, orcamento_pagamento, orcamento_cliente_id):
        self.orcamento_nome = orcamento_nome
        self.orcamento_valor = orcamento_valor
        self.orcamento_status = orcamento_status
        self.orcamento_observacao = orcamento_observacao
        self.orcamento_previsao = orcamento_previsao
        self.orcamento_pagamento = orcamento_pagamento
        self.orcamento_cliente_id = orcamento_cliente_id

    def deletar_orcamento(self):
        banco.session.delete(self)
        banco.session.commit()
