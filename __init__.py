from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

import requests
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Route pour extraire les commits d'un repository via l'API GitHub
@app.route('/commits', methods=['GET'])
def get_commits():
    # URL de l'API GitHub pour les commits
    repo_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Requête pour récupérer les données des commits
        response = requests.get(repo_url)
        response.raise_for_status()
        commits = response.json()
        
        # Extraction des informations intéressantes : auteur et date
        result = [
            {
                "author": commit.get("commit", {}).get("author", {}).get("name", "Unknown"),
                "date": commit.get("commit", {}).get("author", {}).get("date", "Unknown")
            }
            for commit in commits
        ]
        
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Route pour extraire les minutes d'une chaîne de date donnée
@app.route('/extract-minutes/<date_string>', methods=['GET'])
def extract_minutes(date_string):
    try:
        # Conversion de la chaîne de date en objet datetime
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minutes = date_object.minute
        return jsonify({"minutes": minutes})
    except ValueError:
        return jsonify({"error": "Invalid date format. Use format 'YYYY-MM-DDTHH:MM:SSZ'"}), 400


if __name__ == "__main__":
  app.run(debug=True)
#proute
