from flask import Flask, request # flask requires installation
from flask_cors import CORS
from attendance import post_api, get_api, get_category_api, get_specific_api
import json

app = Flask(__name__)
CORS(app) #needed to be removed once all is dockerized

def category_checker(check):
    checker = ['room_name', 'room_start', 'room_finish', 'name', 'email', 'time', 'overall_time', 'platform']
    for req in check:
        if req not in checker: return False
    return True

@app.route('/', methods=['GET'])
def get_mysql():
    results = get_api() #return an array with lots of tuples inside, viewed as string arrays in html
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    #resultsJSON = { "results": json.dumps(results)}
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

@app.route('/category', methods=['GET'])
def get_mysql_category():
    categories = request.args.get('categories')
    
    flag = category_checker(categories.split(","))
    if not flag: return "<h1>Categories don't match </h1>"
    
    results = get_category_api(categories)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    #resultsJSON = { "results": json.dumps(results) }
    resultsJSON = json.dumps(results) 
    return resultsJSON

@app.route('/specifics', methods=['GET'])
def get_mysql_specefic():
    input_type = request.args.get('type')
    input_text = request.args.get('input')
    categories = request.args.get('categories')
    
    if categories != "*":
        flag = category_checker(categories.split(","))
        if not flag: return "<h1>Categories don't match</h1>"
    
    results = get_specific_api(categories, input_type, input_text)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    #resultsJSON = { "results": json.dumps(results) } 
    resultsJSON = json.dumps(results)
    return resultsJSON
    

if __name__ == '__main__':
    app.run(host='0.0.0.0') # the host ip is for docker reasons only