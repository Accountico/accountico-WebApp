from sql_alchemy import banco


class ClienteModel(banco.Model):
    __tablename__ = 'pessoafisica'
    cliente_id = banco.Column(banco.Integer, primary_key=True)
    cliente_cpf = banco.Column(banco.String(20))
    cliente_nome = banco.Column(banco.String(60))
    cliente_telefone = banco.Column(banco.String(15))
    cliente_celular = banco.Column(banco.String(15))
    cliente_email = banco.Column(banco.String(80))
    # cliente_cadastro = banco.Column(banco.String(30))

    def __init__(self, cliente_cpf, cliente_nome, cliente_telefone, cliente_celular, cliente_email):
        self.cliente_cpf = cliente_cpf
        self.cliente_nome = cliente_nome
        self.cliente_telefone = cliente_telefone
        self.cliente_celular = cliente_celular
        self.cliente_email = cliente_email

    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'cliente_cpf': self.cliente_cpf,
            'cliente_nome': self.cliente_nome,
            'cliente_telefone': self.cliente_telefone,
            'cliente_celular': self.cliente_celular,
            'cliente_email': self.cliente_email,
        }

    @classmethod
    def achar_cliente(cls, cliente_id):
        cliente = cls.query.filter_by(cliente_id=cliente_id).first()
        if cliente:
            return cliente
        return None

    def achar_cliente_cpf(cls, cliente_cpf):
        cliente = cls.query.filter_by(cliente_cpf=cliente_cpf).first()
        if cliente:
            return cliente
        return None

    def salvar_cliente(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_cliente(self, cliente_cpf, cliente_nome, cliente_telefone, cliente_celular, cliente_email):
        self.cliente_cpf = cliente_cpf
        self.cliente_nome = cliente_nome
        self.cliente_telefone = cliente_telefone
        self.cliente_celular = cliente_celular
        self.cliente_email = cliente_email

    def deletar_cliente(self):
        banco.session.delete(self)
        banco.session.commit()
