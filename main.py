from flask import Flask, request, jsonify
from handle_hostnames import run_driver, add_hosts
from pg_admin import get_folio_id, insert_pass_logs, get_pass_logs, is_authenticated
from support import run_bot, send_message

# Run the Telegram bot
run_bot()

# Initialize Flask application
app = Flask(__name__)

# Dictionary to store active drivers
drivers = {}  # {hostname: driver_instance}


def check_authenticated(func):
    """
    Decorator function to check if the user is authenticated.

    Args:
        func: The function to be wrapped.

    Returns:
        wrapper: The wrapper function.
    """
    async def wrapper(*args, **kwargs):
        authenticated = is_authenticated(request.json['user'], request.json['password'])
        if authenticated:
            result = await func()
            if result != "NOT_FOUND":
                insert_pass_logs(user=request.json['user'], username=request.json['username'],
                                 hostname=request.json['hostname'], action=request.json["action"])
            return result
        else:
            return jsonify("NOT_AUTHENTICATED", 404)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/", methods=['POST'])
def start_session():
    """
    Endpoint to start a session for a specific hostname.

    Expects a JSON payload with the hostname.
    If the hostname is not in the drivers dictionary, it initializes a driver instance for it.
    """
    hostname = request.json['hostname']
    if hostname not in drivers:
        drivers[hostname] = run_driver(hostname)
    return "Driver start"


@app.route('/delete-driver', methods=["POST"])
def delete_driver():
    """
    Endpoint to delete a driver instance for a specific hostname.

    Expects a JSON payload with the hostname to be deleted.
    """
    host = request.json['hostname']
    del drivers[host]
    return 'power'


@app.route("/change-password", methods=['POST'])
@check_authenticated
async def change_password():
    """
    Endpoint to change the password for a user.

    Expects a JSON payload with the hostname, username, and password.
    """
    hostname = request.json['hostname']
    folio_id = get_folio_id(request.json['username'])
    result = drivers[hostname].change_password(folio_id=folio_id, username=request.json["username"])
    return result


@app.route("/error-1154", methods=["POST"])
@check_authenticated
async def error_1154():
    """
    Endpoint to fix error 1154 for a user.

    Expects a JSON payload with the hostname, username, and password.
    """
    hostname = request.json['hostname']
    folio_id = get_folio_id(request.json['username'])
    result = drivers[hostname].fix_error_1154(folio_id=folio_id, username=request.json["username"])
    return result


@app.route("/get-details", methods=["POST"])
@check_authenticated
async def get_details():
    """
    Endpoint to get details of a user.

    Expects a JSON payload with the hostname, username, and password.
    """
    hostname = request.json['hostname']
    folio_id = get_folio_id(request.json['username'])
    result = drivers[hostname].get_details(folio_id=folio_id, username=request.json["username"])
    return result


@app.route("/call-support", methods=["POST"])
def call_support():
    """
    Endpoint to call support.

    Expects JSON payload with hostname, username, and message for support.
    """
    send_message(
        f"Hostname: {request.json['hostname']}\nUser: {request.json['username']}\nMessage:\n{request.json['message']}")
    return "200"


@app.route("/pass-logs", methods=['GET'])
def passing_logs():
    """
    Endpoint to retrieve password change logs.
    """
    logs = get_pass_logs()
    return logs


if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000)
