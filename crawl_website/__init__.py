from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '21248020107072124802010025'
    from .views import view
    app.register_blueprint(view, url_prefix='/')
    return app