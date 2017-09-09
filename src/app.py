from flask import Flask, render_template, request
import requests, json, time
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def hello():
    return render_template('index.html')

@app.route('/model_summery',methods=['POST'])
def model_summery():
    client = MongoClient()
    db = client['fraud']

    collection = db['events']
    all_prob_fraud=[]
    all_risk_fraud=[]

    total_instances = collection.count()
    total_fraud = collection.find({'fraud': 1}).count()
    percentage_fraud = total_fraud*100.0/total_instances
    total_hr = collection.find({'risk': 'High'})
    total_mr = collection.find({'risk': 'Medium'})
    total_lr = collection.find({'risk': 'Low'})


    return render_template('result.html',total = total_instances,fraud=total_fraud, per=percentage_fraud) #,hr=total_hr,mr=total_mr,lr=total_lr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
