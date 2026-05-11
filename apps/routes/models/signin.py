from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from flask import request


import time

# SIGNIN MODEL ============================================================ Begin
class SigninModels():
    # SIGN IN ============================================================ Begin
    def signin(datas):
        try:
            # Data Response ---------------------------------------- Start
            response = {
                "data" : datas,
            }
            # Data Response ---------------------------------------- Finish
            
            # Return Response ======================================== 
            return  make_response(jsonify({"message":"Successfull!", "data":response}), 200)

        except Exception as e:
            return "Failed:)"
    # SIGN IN ============================================================ End
# SIGNIN MODEL ============================================================ End
