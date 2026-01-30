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
    
    # MongoDB connection string
    app.config["MONGO_URI"] = "mongodb+srv://webhookuser:z2Zt6%40jhDYbAM44@github-events-cluster.0rkdbbl.mongodb.net/github_events?appName=github-events-cluster"


    # Initialize MongoDB with Flask app
    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
