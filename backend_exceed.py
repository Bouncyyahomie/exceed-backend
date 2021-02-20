from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

melodyCollection = mongo.db.melody
countingCollection = mongo.db.counting

melody_note = {
    "B0": 31, "C1": 33, "C-1": 35, "D1": 37, "D-1": 39,
    "E1": 41, "F1": 44, "F-1": 46, "G1": 49, "G-1": 52,
    "A1": 55, "A-1": 58, "B1": 62, "C2": 65, "C-2": 69,
    "D2": 73, "D-2": 78, "E2": 82, "F2": 87, "F-2": 93,
    "G2": 98, "G-2": 104, "A2": 110, "A-2": 117, "B2": 123,
    "C3": 131, "C-3": 139, "D3": 147, "D-3": 156, "E3": 165,
    "F3": 175, "F-3": 185, "G3": 196, "G-3": 208, "A3": 220,
    "A-3": 233, "B3": 247, "C4": 262, "C-4": 277, "D4": 294,
    "D-4": 311, "E4": 330, "F4": 349, "F-4": 370, "G4": 392,
    "G-4": 415, "A4": 440, "A-4": 466, "B4": 494, "C5": 523,
    "C-5": 554, "D5": 587, "D-5": 622, "E5": 659, "F5": 698,
    "F-5": 740, "G5": 784, "G-5": 831, "A5": 880, "A-5": 932,
    "B5": 988, "C6": 1047, "C-6": 1109, "D6": 1175, "D-6": 1245,
    "E6": 1319, "F6": 1397, "F-6": 1480, "G6": 1568, "G-6": 1661,
    "A6": 1760, "A-6": 1865, "B6": 1976, "C7": 2093, "C-7": 2217,
    "D7": 2349, "D-7": 2489, "E7": 2637, "F7": 2794, "F-7": 2960,
    "G7": 3136, "G-7": 3322, "A7": 3520, "A-7": 3729, "B7": 3951,
    "C8": 4186, "C-8": 4435, "D8": 4699, "D-8": 4978, "_": 0
}

reverse_dict = dict((v,k) for k,v in melody_note.items())

@app.route('/melody/create', methods=['POST'])
@cross_origin()
def create_melody():
    data = request.json
    filt = {"title": data["title"]}
    query = melodyCollection.find_one(filt)
    if query is not None:
        return {"result": "This title has been used"}
    data_note = data["note"]
    note_to_int = []
    for note in data_note:
        if note not in melody_note:
            return {"result": f"{note} is unknown note"}
        note_to_int.append(melody_note[note])
    myMelody = {
        "type": "melody",
        "title": data["title"],
        "note": note_to_int,
    }
    melodyCollection.insert_one(myMelody)
    return {"result": "Create successfully"}

@app.route('/melody/select', methods=['PATCH'])
@cross_origin()
def select_melody_on_db():
    # data = request.json #title name
    mytitle = request.args.get("title")
    filt1 = {"type": "melody", "title": mytitle}
    query = melodyCollection.find_one(filt1)
    if query is None:
        return {"result": "Cannot found the melody"}
    
    filt2 = {"type" : "selector"}
    selector_query = melodyCollection.find_one(filt2)
    if selector_query is None:
        mySelector = {
            "type": "selector",
            "note": query["note"],
            "title": query["title"]
        }
        melodyCollection.insert_one(mySelector)
    else:
        updated_content = {"$set": {
            "title": query["title"],
            "note": query["note"]
            }}
        melodyCollection.update_one(filt2, updated_content)
    return {"result" : "Select successfully"}

#for hardware
@app.route('/melody/select', methods=['GET'])
@cross_origin()
def select_melody_on_hardware():
    query = melodyCollection.find_one({"type" : "selector"})
    output = query["note"]
    return {"result": output}

@app.route('/count' , methods=['GET'])
@cross_origin()
def get_count():
    query = countingCollection.find_one_or_404()
    count = {'count': query['count']}
    return count

@app.route('/counter', methods=['PATCH'])
@cross_origin()
def counter():
    # data = request.json
    filt = {'type': 'washinghand'}
    getter = get_count()
    counter = getter["count"] + 1
    counting = {"$set":{'count':counter}}
    countingCollection.update_one(filt,counting)

    return {'result': 'Someone is washing hand'}

#ดึง list เพลงที่บันทึกไว้
@app.route('/melody/list', methods=['GET'])
@cross_origin()
def get_melody_list():
    query = melodyCollection.find({"type": "melody"})
    output = []
        
    for ele in query:
        data_note = ele["note"]
        int_to_string = []
        for note in data_note:
            int_to_string.append(reverse_dict[note])
        output.append({
            "name": ele["title"],
            "notes": int_to_string
        })
    return {"result": output}

@app.route('/melody/delete',methods=['DELETE'])
@cross_origin()
def delete_melody():
    mytitle = request.args.get("title")
    filt = {"type": "melody", "title": mytitle}
    query = melodyCollection.find_one(filt)
    if query is None:
        return {"result": "Cannot found the melody"}
    x = melodyCollection.delete_many({"title": mytitle})
    return {'result' : f'{x.deleted_count} documents deleted.'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3002', debug=True)