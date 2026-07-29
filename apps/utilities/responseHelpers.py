from flask import jsonify, make_response

def success(message="Success", status_code=200):
    return make_response(jsonify({"status_code":status_code, "message":message}), 200)

def success_data(data, status_code=200):
    return make_response(jsonify({"status_code":status_code, "message":"Successfull!", "data":data}), 200)

def not_found(message, status_code=404):
    return make_response(jsonify({"status_code":status_code, "error":"Not Found", "message":message}), 404)

def defined_error(message, error="Defined Error", status_code=499):
    return make_response(jsonify({"status_code":status_code, "error":error, "message":message}), 499)

def parameter_error(message, error="Parameter Error", status_code=400):
    return make_response(jsonify({"status_code":status_code, "error":error, "message":message}), 400)

def authorization_error(status_code=403):
    return make_response(jsonify({"status_code":status_code, "error":"Forbidden", "message":"Sorry! Permission Denied."}), 403)

def invalid_params(status_code=400):
    return make_response(jsonify({"status_code":status_code, "error":"Invalid Parameters"}), 400)

def bad_request(message="", error="Bad Request", status_code=400):
    return make_response(jsonify({"status_code":status_code, "error":error, "message":f"{message}"}), 400)

def subscription_required(
    message="Langganan bengkel belum aktif atau sudah kedaluwarsa.",
    status_code=402
):
    return make_response(
        jsonify({
            "status_code": status_code,
            "error": "Subscription Required",
            "message": message
        }),
        status_code
    )