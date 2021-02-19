from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group07:cn8q649p@158.108.182.0:2255/exceed_group07'
mongo = PyMongo(app)

melodyCollection = mongo.db.melody
countingCollection = mongo.db.counting

@app.route('/melody/create', methods=['POST'])
def create_melody():
    data = request.json
    filt = {"title": data["title"]}
    query = melodyCollection.find_one(filt)
    if query is not None:
        return {"result": "This title has been used"}
    myMelody = {
        "type": "melody",
        "title": data["title"],
        "note": data["note"],
    }
    melodyCollection.insert_one(myMelody)
    return {"result": "Create successfully"}

@app.route('/melody/select', methods=['PATCH'])
def select_melody_on_db():
    # data = request.json #title name
    mytitle = request.args.get("title")
    filt1 = {"type": "melody", "title": mytitle}
    query = melodyCollection.find_one(filt1)
    if query is None:
        return {"result": "Cannot found the melody"}

    filt2 = {"type" : "selector"}
    updated_content = {"$set": {
        "title": query["title"],
        "note": query["note"]
        }}
    melodyCollection.update_one(filt2, updated_content)
    return {"result" : "Select successfully"}

#for hardware
@app.route('/melody/select', methods=['GET'])
def select_melody_on_hardware():
    query = melodyCollection.find_one({"type" : "selector"})
    output = {
        "note": query["note"]
    }
    return {"result": output}

@app.route('/count' , methods=['GET'])
def get_count():
    query = countingCollection.find_one_or_404()
    count = {'count': query['count']}
    return count

@app.route('/counter', methods=['PATCH'])
def counter():
    # data = request.json
    filt = {'type': 'washinghand'}
    getter = get_count()
    counter = getter["count"] + 1
    counting = {"$set":{'count':counter}}
    countingCollection.update_one(filt,counting)

    return {'result': 'Someone is washing hand'}

#ดึง list เพลงที่บรรทึกไว้
@app.route('/melody/list', methods=['GET'])
def get_melody_list():
    query = melodyCollection.find({"type": "melody"})
    output = []
    for ele in query:
        output.append({
            "title": ele["title"]
        })
    return {"result": output}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)