from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group07:cn8q649p@158.108.182.0:2255/exceed_group07'
mongo = PyMongo(app)

melodyCollection = mongo.db.melody
countingCollection = mongo.db.counting


@app.route('/count' , methods=['GET'])
def get_count():
    query = countingCollection.find_one_or_404()
    count = {'count': query['count']}
    return count.values()

@app.route('/counter', methods=['PATCH'])
def counter():
    data = request.json
    filt = {'type': 'washinghand'}
    getter = get_count()
    counter = getter["count"] + 1
    counting = {"$set":{'count':counter}}
    countingCollection.update_one(filt,counting)

    return {'result': 'Someone is washing hand'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)