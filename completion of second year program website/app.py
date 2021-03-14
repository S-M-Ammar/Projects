  
from flask import Flask,render_template,request
import os
import json
import pandas as pd
import numpy as np
import pickle
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/results',methods=['GET','POST'])
def result_page():
    print(request.form)
    mission = 0
    match_region_perf = 0
    fast_app = 0
    uni_major_classics = 0
    uni_major_science = 0
    uni_major_finance = 0
    low_income = 0
    subject = 0


    mission = request.form['mission']
    match_region_perf = request.form['performance_level']
    fast_app = request.form['fast_app']

    if("low_income" in request.form):
        low_income = 1
    
    if("Subject_Tech_Map" in request.form):
        subject = 1
    
    if(request.form['meal_preference']=="classics"):
        uni_major_classics = 1
    elif(request.form['meal_preference']=="exerciseScience"):
        uni_major_science = 1
    else:
        uni_major_finance = 1
    
    model = pickle.load(open('OUTCOME_4_Complete_Y2.pkl','rb'))
    pred = model.predict([[match_region_perf,mission,fast_app,uni_major_classics,uni_major_science,uni_major_finance,low_income,subject]])
    if(pred[0]==0):
        return render_template("index-final.html",pred="Not Completed")
    else:
        return render_template("index-final.html",pred="Completed")

    


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(port = int(os.environ.get("PORT", 5000)))