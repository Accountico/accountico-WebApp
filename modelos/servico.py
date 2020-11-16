from sql_alchemy import banco
# from modelos.orcamento import OrcamentoModel


class ServicoModel(banco.Model):
    __tablename__ = 'servicos'
    servico_id = banco.Column(banco.String, primary_key=True)
    servico_nome = banco.Column(banco.String(100))
    servico_status = banco.Column(banco.String(25))
    servico_observacao = banco.Column(banco.String(200))
    servico_orcamento_id = banco.Column(banco.String)

    def __init__(self, servico_id, servico_nome, servico_status, servico_observacao, servico_orcamento_id):
        self.servico_id = servico_id
        self.servico_nome = servico_nome
        self.servico_status = servico_status
        self.servico_observacao = servico_observacao
        self.servico_orcamento_id = servico_orcamento_id

    def json(self):
        return {
            'servico_id': self.servico_id,
            'servico_nome': self.servico_nome,
            'servico_status': self.servico_status,
            'servico_observacao': self.servico_observacao,
            'servico_orcamento_id': self.servico_orcamento_id
        }

    @classmethod
    def achar_servico(cls, servico_id):
        servico = cls.query.filter_by(servico_id=servico_id).first()
        if servico:
            return servico
        return None

    def salvar_servico(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_servico(self, servico_nome, servico_status, servico_observacao, servico_orcamento_id):
        self.servico_nome = servico_nome
        self.servico_status = servico_status
        self.servico_observacao = servico_observacao
        self.servico_orcamento_id = servico_orcamento_id

    def deletar_servico(self):
        banco.session.delete(self)
        banco.session.commit()
