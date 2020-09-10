from flask import jsonify


def internal_server_error(message=None):
    payload = {"error": 500}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = 500
    return response
