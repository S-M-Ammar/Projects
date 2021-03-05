from flask import Flask,render_template,request
import os
import json
import pandas as pd
from extraction import getSeoResults

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/results',methods=['GET','POST'])
def extract_results():
    if(request.method=="POST"):

        x = json.dumps(request.form['params'])
        paramsDict = eval(json.loads(x))
        response = getSeoResults(paramsDict['fileName'],paramsDict)
        if(type(response)!=str):
            return render_template('resultsPage.html',df_ms_keywords = response[0], df_ms_difficulty = response[1], df_ms_volume = response[2], df_roi_keywords = response[3] , df_roi_difficulty = response[4], df_roi_volume = response[5], df_ew_keywords = response[6], df_ew_difficulty = response[7], df_ew_volume = response[8], df_bto_keywords = response[9], df_bto_difficulty = response[10], df_bto_volume = response[11], df_ms_country = response[12], df_roi_country = response[13], df_ew_country = response[14], df_bto_country = response[15])
        else:
            return "Ooops ! Something wrong with the file."

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(port = int(os.environ.get("PORT", 5000)))
