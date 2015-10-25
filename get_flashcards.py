"Main app to get flashcards for web"

import os, json
import pandas as pd
from flask import Flask
from flask.ext.cors import CORS
#pip install -U flask-cors
import subprocess

app = Flask(__name__)

CORS(app)

def scan_data_and_return_json(category):
	response = []
	path_to_json = 'data/'
	json_files = [s for s in os.listdir(path_to_json) if s.endswith('.json') and s.startswith(category.split('=')[1])]
	for js in json_files:
		with open(os.path.join(path_to_json, js)) as json_file:
			response.append(json.load(json_file))
	return json.dumps(response)	

@app.route("/<category>")
def get_flashcards(category):
	#Comment this to make it look into data folder
	path_to_json = 'data/'
	json_files = [s for s in os.listdir(path_to_json) if s.endswith('.json') and s.startswith(category.split('=')[1])]
	if not json_files:
		p = subprocess.Popen("python mine_wordnet.py " + category.split('=')[1], stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
	return scan_data_and_return_json(category)
 
if __name__ == '__main__':
    app.run()