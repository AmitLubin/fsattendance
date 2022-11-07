from flask import Flask, request # flask requires installation
from flask_cors import CORS
from attendance import post_api, get_api
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_mysql():
    results = get_api() #return an array with lots of tuples inside, viewed as string arrays in html
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    resultsJSON = json.dumps(results)
    return resultsJSON
    

@app.route('/', methods=['POST'])
def insert_csv():
    folder = str(request.get_data())
    print(folder)
    print(request.get_data())
    if folder[0] == 'b': 
        folder = folder.rsplit('b')[1]
    folder = folder.replace("'", "")
    return post_api(folder)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0') # the host ip is for docker reasons only