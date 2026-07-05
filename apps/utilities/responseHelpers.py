from flask import jsonify, make_response

def success(message="Successfull", statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":message}), 200)

def success_data(data, statusCode=200):
    return make_response(jsonify({"statusCode":statusCode, "message":"Successfull!", "data":data}), 200)

def not_found(message, statusCode=404):
    return make_response(jsonify({"statusCode":statusCode, "error":"Not Found", "message":message}), 404)

def defined_error(message, error="Defined Error", statusCode=499):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "message":message}), 499)

def parameter_error(message, error="Parameter Error", statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "message":message}), 400)

def authorization_error(statusCode=403):
    return make_response(jsonify({"statusCode":statusCode, "error":"Forbidden", "message":"Sorry! Permission Denied."}), 403)

def invalid_params(statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "error":"Invalid Parameters"}), 400)

def bad_request(message="", error="Bad Request", statusCode=400):
    return make_response(jsonify({"statusCode":statusCode, "error":error, "message":f"{message}"}), 400)