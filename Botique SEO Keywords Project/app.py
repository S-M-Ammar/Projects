from flask import Flask,render_template,request
import os

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/results',methods=['GET','POST'])
def extract_results():
    return render_template('results.html')

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run(port = int(os.environ.get("PORT", 5000)))
