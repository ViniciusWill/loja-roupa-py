from flask import Flask, render_template
from app.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.secret_key = "loja-roupa-key"
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html", logo_header="imagens/logo.ico")

    return app