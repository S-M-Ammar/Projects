from flask import Flask,render_template,request
from get_betting_results import get_betting_results
import os
from flask_cors import CORS
import json


app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/error",methods=['POST'])
def show_error():
    return render_template("errorpage.html")

@app.route("/results",methods=['POST'])
def get_results():
    data = request.get_json()

    x = get_betting_results(data['Home_Team'],data['Away_Team'])
    if(type(x)==str):
      return {}
    else:
      return {'home_score':x[2],'away_score':x[3],'home_chance':x[0],'away_chance':x[1]}


@app.route("/showResults",methods=['POST'])
def showResults():
    print(request.form['params'])
    x = json.dumps(request.form['params'])
    y = eval(json.loads(x))
    return render_template("result_page.html",home_score=y['home_score'],away_score=y['away_score'],home_chance=y['home_chance'],away_chance=y['away_chance'])


if __name__ == '__main__':
  app.config['ENV'] = 'development'
  app.config['DEBUG'] = True
  app.run(port = int(os.environ.get("PORT", 5000)))