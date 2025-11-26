#Mechanic_App/utils/util
import jose
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone, timedelta
from flask import request, jsonify
from functools import wraps
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or "Gee Mechanic Shop"


#Encode token for customer
def encode_token(customer_id):
    payload = {
        "exp" : datetime.now(timezone.utc) + timedelta (days = 0, hours = 1),
        "iat" : datetime.now(timezone.utc),
        "sub" : str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

#Decode token for customer
def token_required(f): #This puts more force or the token function
    @wraps(f) #wraps the function in the decorator i presume
    def decorated(*args, **kwargs): #whatever the router function is and its params i presume
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            if not token:
                return jsonify({"Message": "Missing Token"}), 400 #checks if a token exist, if not runs erro
            
            #destructure/decode the token to a variable
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                customer_id = data['sub'] #you assigned whatever data that you got for sub to member id to make sure the member logged in is the right member based on the decode
            except ExpiredSignatureError as e:
                return jsonify({"Message": "Expired signature"}), 400
            except JWTError as e:
                return jsonify({"Message": "Invalid Token"}), 400
            return f(customer_id, *args, **kwargs)#return the function based on whatevere is in the route as params hence args and kwargs
        else:
            return jsonify({"Message": "You need to be Logged in to access this"}), 400
        
    return decorated #return the function at the end
            

#Encode token for Mechanic
def encode_token(mechanic_id):
    payload = {
        "exp" : datetime.now(timezone.utc) + timedelta (days = 0, hours = 1),
        "iat" : datetime.now(timezone.utc),
        "sub" : str(mechanic_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f): #This puts more force or the token function
    @wraps(f) #wraps the function in the decorator i presume
    def decorated(*args, **kwargs): #whatever the router function is and its params i presume
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            if not token:
                return jsonify({"Message": "Missing Token"}), 400 #checks if a token exist, if not runs erro
            
            #destructure/decode the token to a variable
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                mechanic_id = data['sub'] #you assigned whatever data that you got for sub to member id to make sure the member logged in is the right member based on the decode
            except ExpiredSignatureError as e:
                return jsonify({"Message": "Expired signature"}), 400
            except JWTError as e:
                return jsonify({"Message": "Invalid Token"}), 400
            return f(mechanic_id, *args, **kwargs)#return the function based on whatevere is in the route as params hence args and kwargs
        else:
            return jsonify({"Message": "You need to be Logged in to access this"}), 400
        
    return decorated #return the function at the end
            

