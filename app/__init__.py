from flask import Flask

from app.webhook.routes import webhook
from app.main.routes import main
from app.api.routes import api
from app.extensions import mongo


# Creating our flask app
def create_app():

    # app = Flask(__name__)
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config["MONGO_URI"] = "mongodb://localhost:27017/database"
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(main)
    app.register_blueprint(webhook)
    app.register_blueprint(api)
    
    return app
