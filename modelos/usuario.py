from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key=True)
    usuario_login = banco.Column(banco.String(80)) # email
    usuario_senha = banco.Column(banco.String(40))
    usuario_nome = banco.Column(banco.String(15))
    usuario_sobrenome = banco.Column(banco.String(20))

    def __init__(self, usuario_login, usuario_senha, usuario_nome, usuario_sobrenome):
        self.usuario_login = usuario_login
        self.usuario_senha = usuario_senha
        self.usuario_nome = usuario_nome
        self.usuario_sobrenome = usuario_sobrenome

    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'usuario_login': self.usuario_login,
            'usuario_senha': self.usuario_senha,
            'usuario_nome': self.usuario_nome,
            'usuario_sobrenome': self.usuario_sobrenome
        }

    @classmethod
    def achar_usuario(cls, usuario_id):
        user = cls.query.filter_by(usuario_id=usuario_id).first()
        if user:
            return user
        return None

    @classmethod
    def achar_por_login(cls, usuario_login):
        user = cls.query.filter_by(usuario_login=usuario_login).first()
        if user:
            return user
        return None

    def salvar_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    def deletar_usuario(self):
        banco.session.delete(self)
        banco.session.commit()
