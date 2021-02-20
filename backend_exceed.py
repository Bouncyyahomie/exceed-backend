from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['MONGO_URI'] = 'mongodb://exceed_group07:cn8q649p@158.108.182.0:2255/exceed_group07'
mongo = PyMongo(app)

melodyCollection = mongo.db.melody
countingCollection = mongo.db.counting

melody_note = {
    "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39,
    "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52,
    "A1": 55, "AS1": 58, "B1": 62, "C2": 65, "CS2": 69,
    "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93,
    "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123,
    "C3": 131, "CS3": 139, "D3": 147, "DS3": 156, "E3": 165,
    "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220,
    "AS3": 233, "B3": 247, "C4": 262, "CS4": 277, "D4": 294,
    "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392,
    "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523,
    "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698,
    "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932,
    "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245,
    "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661,
    "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093, "CS7": 2217,
    "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960,
    "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951,
    "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
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
    output = {
        "note": query["note"]
    }
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
def delete_melody():
    mytitle = request.args.get("title")
    filt = {"type": "melody", "title": mytitle}
    query = melodyCollection.find_one(filt)
    if query is None:
        return {"result": "Cannot found the melody"}
    melodyCollection.delete_one(query)
    return {'result' : 'Deleted successfully'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)