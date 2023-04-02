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

def getJSON(type, msg):
    return jsonify(
        {type: msg}
    )

def existKeyRequest(keys, req):
    for key in keys:
        if key not in req.keys():
            return getJSON( "error"," getting unwanted fields")
                
        if  req[key] == '':
            return getJSON("error", " missing mandatory fields")
                

@app.route("/signIn",  methods=["POST"])
def handleSignIN():
    global conection 
    app.logger.info(f'{conection}')
    if request.method == "POST":
        req =None
        content_type = request.headers.get('Content-Type')
        
        if (content_type == 'application/json'):
            req = request.json
        else:
            req = dict(request.form)
        
        resp =  existKeyRequest(['username', 'password'], req)
        if resp:
            return resp,400
        
        accountExist, err = conection.findUserByUsername(req['username'])
        if err:
            printErrorLog(err)
            return getJSON("error"," DB issue, Try again"), 500
        
        if accountExist == []: #username is not present in DB
            printErrorLog(f"username isnot present in db{req['username']}")
            return getJSON("error"," invalid input "), 400
        printInfoLog(f'{req} \n {accountExist}')
        #username is present in DB
        validPassword = check_password_hash(accountExist[0][1],  req['password'])

        if validPassword: #valid password
            return getJSON("msg", " voila user in !!!!"), 200
        
        #invalid password
        return getJSON("error"," invalid input "), 400
        

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

        resp =  existKeyRequest(['username', 'password', 'age', 'gender'], req)
            
        
        if resp:
            return resp,400
        
        try:
            req['password'] = generate_password_hash(req['password'], method='sha256')
            
        except Exception as e:
            printErrorLog(e)
            return getJSON("error"," invalid input"), 400
        
        accountExist, err = conection.findUserByUsername(req['username'])
        if err:
            printErrorLog(err)
            return getJSON("error"," DB issue, Try again"), 500
        
        if accountExist == []: #username is not present in DB then we need to inser username
            err = conection.insertAccount(req) 
            if err:
                printErrorLog(err)
                return getJSON("error"," DB issue, Try again"), 500
    
        

        else:
            printErrorLog("username is already present")
            return getJSON("error","  Username taken"), 400
            
        
        
        #getJSON(err)
        return req
    
    
    
    #app.logger.info(f'{conection}')
    return render_template("signUp.html")
