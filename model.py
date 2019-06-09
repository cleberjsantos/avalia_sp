import hashlib
import datetime
from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from flaskext.auth import AuthUser, get_current_user_data
from sqlalchemy.ext.declarative import synonym_for


bind_db = 'transporte_sp'


def encrypt_password(password):
    """ """
    pwsd = hashlib.md5(b'AG%sNJ' % password.encode()).hexdigest()
    encrypted_password = '%s%s%s' % (pwsd[0:8].lower(), pwsd[8:24].upper(), pwsd[24:].lower())
    return encrypted_password.encode('utf-8')


class Usuario(db.Model, AuthUser):
    __bind_key__ = bind_db
    __tablename__ = 'usuario'
    salt = db.Column("salt", String(12))
    password = Column("password", String(255))
    cpf = Column(String(11), primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    nome = Column(String(100))
    bairro = Column(String(50))
    cidade = Column(String(30))
    estado = Column(String(20))
    data_criacao = Column(DateTime(), default=datetime.datetime.utcnow())
    avaliacao = db.relationship('Avaliacao', backref='avaliacao', lazy='dynamic')

    def __init__(self, salt, password, cpf, email, nome, bairro, cidade, estado):
        self.salt = salt
        self.password = encrypt_password(password)
        self.cpf = cpf
        self.email = email
        self.nome = nome
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def __repr__(self):
        return '<Usuario {}>'.format(self.email)

    def __getstate__(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'created': self.data_criacao,
        }

    def authenticate(self, password):
        """
        Attempts to verify the password and log the user in. Returns true if 
        succesful.
        """
        if self.password == encrypt_password(password):
            return True
        return False

    @classmethod
    def load_current_user(cls, apply_timeout=True):
        data = get_current_user_data(apply_timeout)
        if not data:
            return None
        return cls.query.filter(cls.cpf == data['cpf']).one_or_none()


class Avaliacao(db.Model):
    __bind_key__ = bind_db
    __tablename__ = 'avaliacao'

    id_avaliacao = Column(Integer, primary_key=True, autoincrement=True)
    nota = Column(Integer, nullable=False, index=True)
    comentario = Column(Text, nullable=False, index=True)
    placa = Column(String, nullable=True)
    usuario = Column(String, ForeignKey('usuario.cpf'), nullable=False)
    linha = Column(String, nullable=True)
    viacao = Column(String, nullable=False)
    data_criacao = Column(DateTime(), default=datetime.datetime.utcnow())
    data_avaliacao = Column(DateTime(), default=datetime.datetime.utcnow())

    def __init__(self, nota, comentario, placa, linha, viacao, usuario):
        self.nota = nota
        self.comentario = comentario
        self.placa = placa
        self.linha = linha
        self.viacao = viacao
        self.usuario = usuario

    def __repr__(self):
        return '<Avaliacao {}>'.format(self.id_avaliacao)
