from flask import Flask,render_template,request,jsonify
from dependecy import dependency,give_prediction
import json
import requests
import logging

app = Flask(__name__, template_folder='template')
app.config["DEBUG"] = True
@app.route("/")
def data_upload():
    return render_template('reviewdata.html')

@app.route("/prediction_rating/<input>",methods=['GET','POST'])
def prediction_rating(input):
    app.logger.info('Going to get predictions') 
    review,predictions = give_prediction(input)
    context = {'review_to_be_analyzed':review,'predictions':predictions}
    return context

@app.route("/test",methods=['GET','POST'])
def display_prediction():
    data = str(request.form['review'])
    response = requests.get("http://127.0.0.1:5000/prediction_rating/"+data)
    return render_template('reviewdata.html', context = response.json() )
    

if __name__ == '__main__':
    
    app.run()