from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group07:cn8q649p@158.108.182.0:2255/exceed_group07'
mongo = PyMongo(app)

melodyCollection = mongo.db.melody
countingCollection = mongo.db.counting

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)