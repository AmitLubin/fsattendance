from flask import Flask, request # flask requires installation
from flask_cors import CORS
from attendance import post_api, get_category_api, get_specific_api, get_avg_api
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)
CORS(app) #needed to be removed once all is dockerized

def category_second_checker(categories):
    checker = ['room_name', 'room_start', 'room_finish', 'name', 'email', 'time', 'overall_time', 'platform']
    for req in categories:
        if req not in checker: return False
    return True

def category_checker(categories):
    if categories == None: categories="*"
    else:
        flag = category_second_checker(categories.split(","))
        if not flag: return False
    return categories
    

@app.route('/', methods=['POST'])
def insert_csv():
    load_dotenv()
    source_ssh = os.getenv("SSH_ADDRESS")
    os.system(f'scp -i .ssh/id_rsa -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {source_ssh} ./csv_files/')
    folder = './csv_files/'
    return post_api(folder)

@app.route('/raw', methods=['GET'])
def get_raw_info():
    categories = category_checker(request.args.get('categories'))
    if not categories: return {
        "results": "<h1>Categories don't match</h1>",
        "status_code": 404
    }
    
    results = get_category_api(categories)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    return results

@app.route('/rawspec', methods=['GET'])
def get_raw_spec_info():
    input_type = request.args.get('type')
    input_text = request.args.get('input')
    categories = category_checker(request.args.get('categories'))
    if not categories: return {
        "results": "<h1>Categories don't match</h1>",
        "status_code": 404
    }
    dynamic = request.args.get('dynamic')
    if dynamic == None: dynamic = False
    
    results = get_specific_api(categories, input_type, input_text, dynamic)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    return results

@app.route('/rawavg', methods=['GET'])
def get_raw_avg():
    input_text = request.args.get('input')
    dynamic = request.args.get('dynamic')
    if dynamic == None: dynamic = False
    else: dynamic = True
    
    results = get_avg_api(input_text, dynamic)
    if results == 0: return "<h1> Something went wrong! </h1>"
    return results

@app.route('/', methods=['GET'])
def get_mysql_category():
    categories = category_checker(request.args.get('categories'))
    if not categories: return {
        "results": "<h1>Categories don't match</h1>",
        "status_code": 404
    }
    
    results = get_category_api(categories)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    resultsJSON = {
        "results": json.dumps(results),
        "status_code": 200
    }
    return resultsJSON

@app.route('/specific', methods=['GET'])
def get_mysql_specefic():
    input_type = request.args.get('type')
    input_text = request.args.get('input')
    categories = category_checker(request.args.get('categories'))
    if not categories: return {
        "results": "<h1>Categories don't match</h1>",
        "status_code": 404
    }
    dynamic = request.args.get('dynamic')
    if dynamic == None: dynamic = False
    else: dynamic = True
    
    results = get_specific_api(categories, input_type, input_text, dynamic)
    if len(results[0]) == 0: return "<h1> no results! </h1>"
    resultsJSON = {
        "results": json.dumps(results),
        "status_code": 200
    }
    return resultsJSON
    
@app.route('/average', methods=['GET'])
def get_average():
    input_text = request.args.get('input')
    dynamic = request.args.get('dynamic')
    if dynamic == None: dynamic = False
    else: dynamic = True
    
    results = get_avg_api(input_text, dynamic)
    if results == 0: return "<h1> Something went wrong! </h1>"
    resultsJSON = {
        "results": results,
        "status_code": 200
    }
    return resultsJSON
    

if __name__ == '__main__':
    app.run(host='0.0.0.0') # the host ip is for docker reasons only