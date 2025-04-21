from flask import Flask
from config import Config




def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    from home.models import db
    db.init_app(app=app)

    from home.api_v1 import api
    app.register_blueprint(api,url_prefix='/cardiacservice')


    from flask_cors import CORS
    CORS(app)
    return app