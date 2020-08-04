# import os
# from flask import Flask, request, jsonify, render_template, redirect
# from werkzeug.utils import secure_filename
# # added 7/13/20
# import numpy as np
# import pickle
# from fastai import *
# from fastai.vision import *
# import os
# cwd = os.getcwd()
# path = cwd + '/model'
# # ################
# app = Flask(__name__)
# # added same day
# doneness_model = load_learner(path,'stage_doneness.pkl')
# shape_model = load_learner(path,'stage_shape.pkl')
# toppings_model = load_learner(path,'stage_topping.pkl')
# #toppings_model = pickle.load(open('model/stage_topping.pkl','rb'))
# #with open(f'model/stage_topping.pkl', "rb") as f:
#  #   toppings_model = pickle.load(f)
#  #   toppings_model = load_learner(f)
# # #########################
# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/result',methods = ['GET', 'POST'])
# def result():
#     if request.method == "POST":
#         if request.files:       
#             new_image = request.files["inputfile"]
#             # basepath = os.path.dirname(__file__)
#             # file_path = os.path.join(basepath, 'static/images', secure_filename(new_image.filename))
#             # new_image.save(file_path)   
#             path = "static/images"
#             file_path = os.path.join(path, secure_filename(new_image.filename))
#             new_image.save(file_path) 
#             # new_image = request.files["inputfile"]
#             # basepath = os.path.dirname(__file__)
#             # file_path = os.path.join(basepath, 'static/images', secure_filename(new_image.filename))
#             #new_image.save(file_path)
#             #reopening saved image(toppings)
#             reopened_image = open_image(file_path)
#             predict_toppings = toppings_model.predict(reopened_image)
#             print(predict_toppings[0])
#             toppings = predict_toppings[0]
#             toppings_accuracy = str(max(predict_toppings[2]) *100)
#             toppings_accuracy = toppings_accuracy.strip('tensor(')
#             toppings_accuracy = (toppings_accuracy.strip(').'))
#             print(toppings_accuracy)
#             #*******************************************************
#             #   working on shape model
#             #-------------------------------------------------------
#             #reopening saved image(shape)
#             shape_image = open_image(file_path)
#             predict_shape = shape_model.predict(shape_image)
#             print(predict_shape[0])
#             #------------------------------------------
#             shape = predict_shape[0]
#             shape_accuracy = str(max(predict_shape[2]) *100)
#             shape_accuracy = shape_accuracy.strip('tensor(')
#             shape_accuracy = (shape_accuracy.strip(').'))
#             print(shape_accuracy)
#             #*******************************************************
#             #   working on doneness model
#             #-------------------------------------------------------
#             #reopening saved image(doneness)
#             doneness_image = open_image(file_path)
#             predict_doneness = doneness_model.predict(doneness_image)
#             print(predict_doneness[0])
#             #------------------------------------------
#             doneness = predict_doneness[0]
#             doneness_accuracy = str(max(predict_doneness[2]) *100)
#             doneness_accuracy = doneness_accuracy.strip('tensor(')
#             doneness_accuracy = (doneness_accuracy.strip(').'))
#             print(doneness_accuracy)
#             # return render_template('result.html', address = file_path, 
#             #                                       toppings = toppings, 
#             #                                       toppings_accuracy = toppings_accuracy, 
#             #                                       shape = shape,
#             #                                       shape_accuracy = shape_accuracy, 
#             #                                       doneness = doneness, 
#             #                                       doneness_accuracy = doneness_accuracy )
#             # image file name and the prediction is this on above line 
#             # new_image.save(secure_filename(new_image.filename))                 
#             # print(new_image)
#     # predict_doneness = doneness_model.predict(new_image)
#     # predict_shape = shape_model.predict(new_image)
#     # return render_template('result.html', toppings = )
#     return render_template('result.html', address = file_path, 
#                                                   toppings = toppings, 
#                                                   toppings_accuracy = toppings_accuracy, 
#                                                   shape = shape,
#                                                   shape_accuracy = shape_accuracy, 
#                                                   doneness = doneness, 
#                                                   doneness_accuracy = doneness_accuracy )
# if __name__ == '__main__':
#     app.run(debug=True)

import os
from flask import Flask, request, jsonify, render_template, redirect,url_for, Response
from werkzeug.utils import secure_filename
# added 7/13/20
###################################
##
# dependencies for reflections on database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask_sqlalchemy import SQLAlchemy 
# dependencies for AWS image download
import boto3
import botocore
##
###########################
import numpy as np
import pickle
from fastai import *
from fastai.vision import *
# import os
cwd = os.getcwd()
path = cwd + '/model'
# ################
app = Flask(__name__)
# added same day
doneness_model = load_learner(path,'stage_doneness.pkl')
shape_model = load_learner(path,'stage_shape.pkl')
toppings_model = load_learner(path,'stage_topping.pkl')
#toppings_model = pickle.load(open('model/stage_topping.pkl','rb'))
#with open(f'model/stage_topping.pkl', "rb") as f:
 #   toppings_model = pickle.load(f)
 #   toppings_model = load_learner(f)
###############################################
########## connection to the database
connection_string = "postgres:kafuiroot@mypostgresdb.cwaco2snnhc7.us-east-2.rds.amazonaws.com/pizzaeye"
engine = create_engine(f'postgresql://{connection_string}')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{connection_string}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
##creating a class model to reflect the columns in our database
class Pizza(db.Model):
    image = db.Column(db.Integer, primary_key=True)
    pizza_shape = db.Column(db.String(15))
    pizza_doneness = db.Column(db.String(15))
    pizza_type = db.Column(db.String(15))
    url = db.Column(db.String(60))
    def __init__(image,pizza_shape,pizza_doneness,pizza_type,url):
        self.image = image
        self.pizza_shape = pizza_shape
        self.pizza_doneness = pizza_doneness
        self.pizza_type = pizza_type
# #########################
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/result',methods = ['GET', 'POST'])
def result():
    if request.method == "POST":
        if request.files:
            new_image = request.files["inputfile"]
            # basepath = os.path.dirname(__file__)
            # file_path = os.path.join(basepath, 'static/images', secure_filename(new_image.filename))
            # new_image.save(file_path)
            path = "static/images/uploadImage"
            file_path = os.path.join(path, secure_filename(new_image.filename))
            new_image.save(file_path)
            # new_image = request.files["inputfile"]
            # basepath = os.path.dirname(__file__)
            # file_path = os.path.join(basepath, 'static/images', secure_filename(new_image.filename))
            #new_image.save(file_path)
            #reopening saved image(toppings)
            reopened_image = open_image(file_path)
            predict_toppings = toppings_model.predict(reopened_image)
            print(predict_toppings[0])
            toppings = predict_toppings[0]
            toppings_accuracy = str(max(predict_toppings[2]) *100)
            toppings_accuracy = toppings_accuracy.strip('tensor(')
            toppings_accuracy = (toppings_accuracy.strip(').'))
            print(toppings_accuracy)
            #*******************************************************
            #   working on shape model
            #-------------------------------------------------------
            #reopening saved image(shape)
            shape_image = open_image(file_path)
            predict_shape = shape_model.predict(shape_image)
            print(predict_shape[0])
            #------------------------------------------
            shape = predict_shape[0]
            shape_accuracy = str(max(predict_shape[2]) *100)
            shape_accuracy = shape_accuracy.strip('tensor(')
            shape_accuracy = (shape_accuracy.strip(').'))
            print(shape_accuracy)
            #*******************************************************
            #   working on doneness model
            #-------------------------------------------------------
            #reopening saved image(doneness)
            doneness_image = open_image(file_path)
            predict_doneness = doneness_model.predict(doneness_image)
            print(predict_doneness[0])
            #------------------------------------------
            doneness = predict_doneness[0]
            doneness_accuracy = str(max(predict_doneness[2]) *100)
            doneness_accuracy = doneness_accuracy.strip('tensor(')
            doneness_accuracy = (doneness_accuracy.strip(').'))
            print(doneness_accuracy)
            # return render_template('result.html', address = file_path,
            #                                       toppings = toppings,
            #                                       toppings_accuracy = toppings_accuracy,
            #                                       shape = shape,
            #                                       shape_accuracy = shape_accuracy,
            #                                       doneness = doneness,
            #                                       doneness_accuracy = doneness_accuracy )
            # image file name and the prediction is this on above line
            # new_image.save(secure_filename(new_image.filename))
            # print(new_image)
    # predict_doneness = doneness_model.predict(new_image)
    # predict_shape = shape_model.predict(new_image)
    # return render_template('result.html', toppings = )
    return render_template('result.html', address = file_path,
                                                  toppings = toppings,
                                                  toppings_accuracy = toppings_accuracy,
                                                  shape = shape,
                                                  shape_accuracy = shape_accuracy,
                                                  doneness = doneness,
                                                  doneness_accuracy = doneness_accuracy )
# ###################################################
@app.route('/images', methods = ['GET', 'POST'])
def images():
    # create a session(link) from python to db
    session = Session(engine)  
    # query all data   
    results = session.query(Pizza.url).all()
    # close the link
    session.close()
    pizza_url = []
    for i in results:
       pizza_url.append(i[0])
    #print(pizza_url)
    return render_template('images.html', a_pizza = pizza_url)
 #######################################################
@app.route('/dbresult', methods = ['GET', 'POST'])
def dbresult():
    if request.method == "POST":
        req = request.get_data()
        # print(req)
        new_req = req.decode()
        # print(new_req)
        # print(len(new_req))
        global imagekey  
        if (len(new_req) == 60):
            imagekey = new_req[54:60]
        else:
            imagekey = new_req[54:61]   
    # else:
    #     imagekey = request.get_data().decode() 
    print(imagekey)
    # global mypath                           
    # mypath = "static/images/uploadImage/" 
    global a_file_path
    # a_file_path = os.path.join(mypath, secure_filename(imagekey))
    # a_file_path = os.path.join(mypath, imagekey)
    a_file_path =  "static/images/uploadImage/" + imagekey
    print('above a_file_path') 
    print(a_file_path)
    print('its working')
    print(type(imagekey))
    s3 = boto3.client('s3', aws_access_key_id='AKIA5X3VBO5PZRNC24DQ', aws_secret_access_key='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')
    s3.download_file('kafuitrainingimage',imagekey,a_file_path)  
    print('image downloaded')     
    # s3.download_file('kafuitrainingimage',imagekey,"static/images/uploadImage/")
     #reopening saved image(toppings)
    reopened_image = open_image(a_file_path)
    predict_toppings = toppings_model.predict(reopened_image)
    print(predict_toppings[0])
    toppings = predict_toppings[0]
    toppings_accuracy = str(max(predict_toppings[2]) *100)
    toppings_accuracy = toppings_accuracy.strip('tensor(')
    toppings_accuracy = (toppings_accuracy.strip(').'))
    print(toppings_accuracy)   
   

    #-------------------------------------------------------
    #reopening saved image(shape)
    shape_image = open_image(a_file_path)
    predict_shape = shape_model.predict(shape_image)
    print(predict_shape[0])
    #------------------------------------------
    shape = predict_shape[0]
    shape_accuracy = str(max(predict_shape[2]) *100)
    shape_accuracy = shape_accuracy.strip('tensor(')
    shape_accuracy = (shape_accuracy.strip(').'))
    print(shape_accuracy)  
#   working on doneness model
    #-------------------------------------------------------
    #reopening saved image(doneness)
    doneness_image = open_image(a_file_path)
    predict_doneness = doneness_model.predict(doneness_image)
    print(predict_doneness[0])
    #------------------------------------------
    doneness = predict_doneness[0]
    doneness_accuracy = str(max(predict_doneness[2]) *100)
    doneness_accuracy = doneness_accuracy.strip('tensor(')
    doneness_accuracy = (doneness_accuracy.strip(').'))
    print(doneness_accuracy)      
    return render_template('dbresult.html', img = imagekey, toppings = toppings,
                                                  toppings_accuracy = toppings_accuracy, 
                                                  shape = shape,
                                                  shape_accuracy = shape_accuracy,
                                                  doneness = doneness,
                                                  doneness_accuracy = doneness_accuracy )
if __name__ == '__main__':
    app.run(debug=True)