import cPickle as pickle
from model import MyModel, get_data
import json
import flask
from pymongo import MongoClient
import pprint
import urllib2 as u2
from urllib2 import urlopen, HTTPError
from utils import *
import pandas as pd
import time

def get_json(url):
    try:
        response = urlopen(url)
    except HTTPError as e:
        print "Url Can not be found"
        return None
    return json.loads(response.read())

def print_results(stored, risk_dict):
    for k, v in stored.iteritems():
        print "object id is {}. Probability as Fraud is {:04.3f}. The event is {} risk".format(k, v, risk_dict[k])

def process(stored, collection):
    """
    get response from heroku instance and make predictions
    """
    count = 10
    url = 'define_url'
    while keep_predict and count > 0:
        data = get_json(url)
        ob_id = data['object_id']
        if ob_id not in stored.keys():
            series = pd.Series(data)
            X = preprocess_series(series)
            prob = model.predict_proba(X)[0][1]
            stored[ob_id] = prob
            data['fraud'] = prob
            collection.insert_one(data)
        count -= 1
    # return stored
def convert_to_risk(stored):
    risk_dict = {}
    for k in stored.keys():
        prob = stored[k]
        if prob < 0.5:
            risk_dict[k] = 'no'
        elif prob >= 0.5 and prob < 0.7:
            risk_dict[k] = 'low'
        elif prob >= 0.7 and prob < 0.8:
            risk_dict[k] = 'medium'
        else:
            risk_dict[k] = 'high'
    return risk_dict

if __name__ == "__main__":
    with open('model.pkl') as f:
        model = pickle.load(f)
    client = MongoClient()
    db = client['fraud']
    #db['events'].drop()
    collection = db['events']
    print "number of collections before {}".format(collection.count())
    stored = dict()
    keep_predict = True
    repeat = 4
    while repeat > 0:
        print "number of repeat left is {}".format(repeat)
        process(stored, collection)
        time.sleep(10)
        repeat -= 1

    risk_dict = convert_to_risk(stored)
    print_results(stored, risk_dict)

    for c in collection.find():
        print c.get('object_id')

    print "number of collections after {}".format(collection.count())
    client.close()
