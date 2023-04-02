from flask import Flask, redirect, url_for, render_template, request, json, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
import bcrypt
import models


app = Flask(__name__)

conection = models.DBManger()
app.logger.info(f'{conection}')

def printInfoLog(msg):
    return app.logger.info(msg)

def printErrorLog(msg):
    return app.logger.error(msg)

def getError(msg):
    return jsonify(
        {"error": msg}
    )




@app.route("/signUp", methods=["POST", "GET"])
def handleSignUp():
    global conection 
    app.logger.info(f'{conection}')
    if request.method == "POST":
        req =None
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            req = request.json
        else:
            req = dict(request.form)

        resp, err = None, None
        for key in ['username', 'password', 'age', 'gender']:
            if key not in req.keys():
                resp = getError( " getting unwanted fields")
                break
            if  req[key] == '':
                resp = getError( " missing mandatory fields")
                break
        
        if resp:
            return resp,400
        
        try:
            req['password'] = generate_password_hash(req['password'], method='sha256')
            
        except Exception as e:
            printErrorLog(e)
            return getError(" invalid input")[0], 400
        
        accountExist, err = conection.findUserByUsername(req['username'])
        if err:
            printErrorLog(err)
            return getError(" DB issue, Try again"), 500
        
        if accountExist == []: #username is not present in DB then we need to inser username
            err = conection.insertAccount(req) 
            if err:
                printErrorLog(err)
                return getError(" DB issue, Try again"), 500
    
        

        else:
            printErrorLog("username is already present")
            return getError("  Username taken"), 400
            
        
        
        #getError(err)
        return req
    
    
    
    #app.logger.info(f'{conection}')
    return render_template("signUp.html")


@app.route("/user/<string:name>")
def getUserByUsername(name):
    global conection 
    if request.method == "GET":
        app.logger.info(f'{name}')
        
        return conection.findUserByUsername(name)


