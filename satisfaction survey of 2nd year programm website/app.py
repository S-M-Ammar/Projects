  
from flask import Flask,render_template,request
import os
import json
import pandas as pd
import numpy as np
import pickle
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index2.html')

@app.route('/results',methods=['GET','POST'])
def result_page():
    cost = request.form['cost']
    bachelors = request.form['bachelors']
    may = request.form['may']
    jun = request.form['jun']
    july = request.form['july']
    aug = request.form['aug']
    sep = request.form['sep']
    sun_percs = request.form['sun_percs']
    transit_score = request.form['transit_score']
    match_subject_park = 0
    match_grade_high_level = 0
    subject_tech_mapping = 0
    uni_major_bioPhysics = 0
    uni_major_ethinic = 0

    if("match_subject_park" in request.form):
         match_subject_park = 1

    if("match_grade_high_level" in request.form):
        match_grade_high_level = 1
    
    if("subject_tech_mapping" in request.form):
        subject_tech_mapping = 1
    
    if(request.form['meal_preference']=="Bio Physics"):
        uni_major_bioPhysics = 1
    else:
         uni_major_ethinic = 1
    
    model = pickle.load(open('OC_Satisfaction_Y2.pkl','rb'))
    prediction = model.predict([[cost,bachelors,may,jun,july,aug,sep,sun_percs,transit_score,match_subject_park,uni_major_bioPhysics,uni_major_ethinic,match_grade_high_level,subject_tech_mapping]])
    final_pred = prediction[0]
    try:
        final_pred = round(final_pred,2)
    except:
        final_pred = round(final_pred,0)
    

    return render_template('index-final2.html',pred=final_pred)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(port = int(os.environ.get("PORT", 5000)))