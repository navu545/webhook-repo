from flask_pymongo import PyMongo

# Create MongoDB client instance
# Actual connection is initialized inside create_app()
mongo = PyMongo()
