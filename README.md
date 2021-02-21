# exceed--backend

## route
/melody/create, method=POST
- For create a melody by receive the json from the frontend in this for match
```json
{
    "title": "baby shark",
    "note": ["A3", "A3",  "A3", "F3", "C4", "A3", "F3", "C4", "A3"]
}
```
- If the melody title is the same as the melody title already in the database. The melody will not create and return `{"result": "This title has been used"}`
- If the melody created. return `{"result": "Create successfully"}`
- Note must be an array of string (40 string)

/melody/select?title=..., methods=PATCH
- For selecting notes to play on the hardware
- If the melody title is exist on database. Select that melody and return `{"result" : "Select successfully"}`. If not return `{"result": "Cannot found the melody"}`
- For example, /melody/select?title=baby shark

/melody/select, methods=GET
- For get the note that we selected on the frontend. The json will return in this format
```json
{
    "result" : 
        [
            31, 33, 35, 37, 39, 
            41, 33, 35, 37, 39, 
            33, 35, 37, 39, 44,
            33, 35, 37, 39, 58
        ]
}
```
- This route **for hardware**

/count , methods=GET
- For get the total number of times the melody has been played
- Return in this format
```json
{
    "count": 1
}
```

/counter, methods=PATCH
- For update the total number of times the melody has been played
- This route **for hardware**
- Use this route when the hardware is working

/melody/list, methods=GET
- For get all the melody title and notes on the database
```json
{
    "result" :
    [
        {
            "name": "baby shark",
            "notes": [740,659,0,494,554,587,554,554,587,554,440]
        },
        {
            "name": "did that",
            "notes": [31, 659, 659, 659, 31]
        }
    ]
}
```

/melody/delete?title=..., methods=DELETE
- For delete the melody in the database
- If this function is working correctly, return with this format
```json
{
    "result": "1 documents deleted."
}
```
