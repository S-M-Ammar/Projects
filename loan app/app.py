from flask import Flask,render_template,request
from mailjet_rest import Client
import os

payment_amount = None
user_data = {}


api_key = 'eade989f48f986b7ec5a484be8a666d3'
api_secret = '130871b2935661b0c6a0aad34db3848e'

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

app = Flask(__name__)

data = {
  'Messages': [
    {
      "From": {
        "Email": "syed.ammar.98sep@gmail.com",
        "Name": "Syed Muhammad Ammar"
      },
      "To": [
        {
          "Email": "batch16.120@gmail.com",
          "Name": "Client 1"
        }
      ],
      "Subject": "Loan Application Moniready",
      "TextPart": "Congratulations. You Application is approved",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}



@app.route("/")
def home():
    return render_template('index.html')


@app.route("/form.html",methods=['GET','POST'])
def form_1():
    # print(request.form['payment'])
    payment_amount = request.form['payment']
    print(payment_amount)
    return render_template('form.html')


@app.route("/form1.html",methods=['GET','POST'])
def form_2():
    return render_template('form1.html')


@app.route("/end.html",methods=['GET','POST'])
def end_page():

    if(request.method=="POST"):
        print(request.form)
        user_data['firstName'] = request.form['firstName']
        user_data['lastName'] = request.form['lastName']
        user_data['age'] = request.form['user_age']
        if(request.form['value']=="single"):
            user_data['martial_status_single'] = 1
            user_data['martial_status_married'] = 0
        elif(request.form['value']=="married"):
            user_data['martial_status_single'] = 0
            user_data['martial_status_married'] = 1
        else:
            user_data['martial_status_single'] = 0
            user_data['martial_status_married'] = 0

    #     result = mailjet.send.create(data=data)
    #     print(result.status_code)
    #     print(result.json())
    return render_template('end.html')


app.run(debug=True,host='localhost',port=3000)