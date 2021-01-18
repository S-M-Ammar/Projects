from flask import Flask,render_template,request
import pickle

app = Flask(__name__)


@app.route('/')
def begin():
    return render_template('index.html')


@app.route('/index.html',methods=['GET','POST'])
def begin_1():
    return render_template('index.html')

@app.route('/endpage.html',methods=['GET','POST'])
def end():
    met_score = int(request.form['Meticulous'])
    comp_score = int(request.form['Compliance'])
    resp_score = int(request.form['Responsible'])
    resl_score = int(request.form['Resilience'])
    compt_score = int(request.form['Competance'])
    employment_level = request.form['employment_type']
    education_level = request.form['education_level']
    mbti_result = request.form['mbti_result']
    model = pickle.load(open('score_estimator.pkl','rb'))
    features = []
    features.extend([met_score,comp_score,resp_score,resl_score,compt_score])

    if(employment_level=='Other'):
        features.append(1)
    else:
        features.append(0)

    if(education_level=='College'):
        features.append(1)
    else:
        features.append(0)

    if(mbti_result=='The Individualistic Doer - ISTP'):
        features.append(1)
    else:
        features.append(0)

    pred = model.predict([features])
    pred = round(pred[0][0],0)
    print(pred)
    return render_template('endpage.html',prediction=pred)


if __name__ == '__main__':
    app.run()
