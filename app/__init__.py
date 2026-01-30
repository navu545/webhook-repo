from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo


# Creating our flask app
def create_app():

    app = Flask(__name__, template_folder="../ui")
    
    #test route
    @app.route('/')
    def api_root():
        return 'Welcome guys'
    
    #Establish connection with mongoDB
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"

    #DB to app connection
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
