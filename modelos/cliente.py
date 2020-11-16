from sql_alchemy import banco


class ClienteModel(banco.Model):
    __tablename__ = 'clientes'
    cliente_id = banco.Column(banco.String, primary_key=True)
    cliente_cpf = banco.Column(banco.String(20))
    cliente_cnpj = banco.Column(banco.String(20))
    cliente_nome = banco.Column(banco.String(60))
    cliente_telefone = banco.Column(banco.String(10))
    cliente_celular = banco.Column(banco.String(11))
    cliente_email = banco.Column(banco.String(80))
    # cliente_cadastro = banco.Column(banco.String(30))

    def __init__(self, cliente_id, cliente_cpf, cliente_cnpj, cliente_nome, cliente_telefone, cliente_celular, cliente_email):
        self.cliente_id = cliente_id
        self.cliente_cpf = cliente_cpf
        self.cliente_cnpj = cliente_cnpj
        self.cliente_nome = cliente_nome
        self.cliente_telefone = cliente_telefone
        self.cliente_celular = cliente_celular
        self.cliente_email = cliente_email

    def json(self):
        return {
            'cliente_id': self.cliente_id,
            'cliente_cpf': self.cliente_cpf,
            'cliente_cnpj': self.cliente_cnpj,
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

    def salvar_cliente(self):
        banco.session.add(self)
        banco.session.commit()

    def atualizar_cliente(self, cliente_cpf, cliente_cnpj, cliente_nome, cliente_telefone, cliente_celular, cliente_email):
        self.cliente_cpf = cliente_cpf
        self.cliente_cnpj = cliente_cnpj
        self.cliente_nome = cliente_nome
        self.cliente_telefone = cliente_telefone
        self.cliente_celular = cliente_celular
        self.cliente_email = cliente_email

    def deletar_cliente(self):
        banco.session.delete(self)
        banco.session.commit()
