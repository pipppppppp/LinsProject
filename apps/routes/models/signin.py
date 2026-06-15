from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from flask import request
from ...database.db_admins import Admins

import time

# SIGNIN MODEL ============================================================ Begin
class SigninModels():
    # SIGN IN ============================================================ Begin
    def signin(datas):
        try:
            # REQUEST DATA ======================================== Start
            username = datas.username.data
            password = datas.password.data
            # REQUEST DATA ======================================== Finish

            # CHECK USER---------------------------------------- Start
            admin = Admins.query.filter_by(
                username=username
            ).first()

            if admin is None:

                return make_response(
                    jsonify({
                        "message" : "Username tidak ditemukan"
                    }),
                    404
                )
            # CHECK USER ---------------------------------------- Finish
            
            # CHECK PASSWORD ---------------------------------------- start
            if admin.password != password:

                return make_response(
                    jsonify({
                        "message": "Password salah"
                    }),
                    401
                )
            # CHECK PASSWORD ---------------------------------------- Finish

            # JWT TOKEN ---------------------------------------- Start
            access_token = create_access_token(
                identity=admin.id
            )
            # JWT TOKEN ---------------------------------------- Finish

            # DATA RESPONSE ---------------------------------------- Start
            response = {
                "id": admin.id,
                "username": admin.username,
                "email": admin.email,
                "token": access_token
}
            # DATA RESPONSE ---------------------------------------- Finish

            # RETURN RESPONSE ======================================== Start
            # return  make_response(
            #     jsonify({
            #         "message":"Successfull!", 
            #         "data":response
            #     }),
            #     200
            # )
            return admin
            # RETURN RESPONSE ======================================== Finish

        except Exception as e:
            return make_response(
                jsonify({
                    "message": "Failed",
                    "error": str(e)
                }),
                500
            )
    # SIGN IN ============================================================ End
# SIGNIN MODEL ============================================================ End
