from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from flask import session
import datetime
import random
from string import ascii_letters
from db import config_db, db
from flask import Flask, render_template, request, url_for, redirect
from model import Usuario
from flaskext.auth import Auth, AuthUser, login_required, logout
from flaskext.auth.auth import SESSION_USER_KEY, SESSION_LOGIN_KEY


def create_app(config_class=Config):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config_class)

    config_db(app)
    auth = Auth(app, login_url_name='index')

    with app.app_context():
        db.create_all()

        def index():
            if request.method == 'POST':
                cpf = request.form['cpf']
                user = Usuario.query.filter(Usuario.cpf == cpf).one_or_none()
                if user is not None:
                    # Authenticate and log in!
                    if user.authenticate(request.form['password']):
                        session[SESSION_USER_KEY] = user.__getstate__()
                        session[SESSION_LOGIN_KEY] = datetime.datetime.utcnow()
                        return redirect(url_for('avaliacao'))
                return 'Failure :('
            return render_template('index.html')

        def home():
            return render_template("index.html")

        def voltar():
            return render_template("home")

        def cadastro():
            if request.method == "POST":
                salt = (generate_salt())
                password = (request.form.get("password"))
                cpf = (request.form.get("cpf"))
                email = (request.form.get("email"))
                nome = (request.form.get("nome"))
                bairro = (request.form.get("bairro"))
                cidade = (request.form.get("cidade"))
                estado = (request.form.get("estado"))

                p = Usuario(salt, password, cpf, email, nome, bairro, cidade, estado)
                db.session.add(p)
                db.session.commit()
                return redirect(url_for("home"))
            return render_template('cadastro.html')

        def generate_salt():
            """ -- """
            return ''.join(random.sample(ascii_letters, 12))

        @login_required()
        def avaliacao():
            return 'Admin! Excellent!'

        def logout_view():
            user_data = logout()
            if user_data is None:
                return 'No user to log out.'
            return 'Logged out user {0}.'.format(user_data['nome'])


        #@app.route("/lista")
        #def lista():
        #    usuarios = Usuario.query.all()
        #    return render_template("lista.html", usuarios=usuarios)

        #@app.route("/atualizar/<int:cpf>", methods=['GET', 'POST'])
        #def atualizar(cpf):
        #    usuario = Usuario.query.filter_by(cpf=cpf).first()
        #    if request.method == "POST":
        #        nome = (request.form.get("nome"))
        #        bairro = (request.form.get("bairro"))
        #        cidade = (request.form.get("cidade"))
        #        estado = (request.form.get("estado"))
        #        email = (request.form.get("email"))

        #        if nome and bairro and cidade and estado and email:
        #            usuario.nome = nome
        #            usuario.bairro = bairro
        #            usuario.cidade = cidade
        #            usuario.estado = estado
        #            usuario.email = email
        #            db.session.commit()
        #        return redirect(url_for("lista"))
        #    return render_template("atualizar.html", usuario=usuario)

        #@app.route("/excluir/<int:cpf>")
        #def excluir(cpf):
        #    usuario = Usuario.query.filter_by(cpf=cpf).first()
        #    db.session.delete(usuario)
        #    db.session.commit()

        #    usuarios = Usuario.query.all()
        #    return render_template("lista.html", usuarios=usuarios)

        app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
        app.add_url_rule('/home', 'home', home, methods=['GET'])
        app.add_url_rule('/cadastro', 'cadastro', cadastro, methods=['GET', 'POST'])
        app.add_url_rule('/avaliacao', 'avaliacao', avaliacao, methods=['GET', 'POST'])
        app.add_url_rule('/logout/', 'logout', logout_view)

        return app
