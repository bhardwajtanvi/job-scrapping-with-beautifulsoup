from flask import Flask,redirect,url_for,render_template,request
import talent
from talent import find_jobs_from
import json
desired_characs=['titles','companies','links']


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/result.html',methods=['POST','GET'])
def display():
        if request.method == 'POST':
            job = request.form['job-title']
            loc = request.form['location']
            sum_num=find_jobs_from('Talent',job,loc,desired_characs)
            return render_template("result.html",sum_num=sum_num)


if __name__ == "__main__":
    app.run(debug=False)
