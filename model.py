import hashlib
import datetime
from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
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
    salt = db.Column("salt", db.String(12))
    password = Column("password", String(255))
    cpf = Column(String(11), nullable=False, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    nome = Column(String(100))
    bairro = Column(String(50))
    cidade = Column(String(30))
    estado = Column(String(20))
    date_created = Column(DateTime(), default=datetime.datetime.utcnow())

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
            'created': self.date_created,
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
