from flask import Flask, request, jsonify
from handle_hostnames import run_driver, add_hosts
from pg_admin import get_folio_id, insert_pass_logs, get_pass_logs, is_authenticated
from support import run_bot, send_message



run_bot()

app = Flask(__name__)

drivers = {}  # localhost: driver1


@app.route("/", methods=['POST'])
def start_session():
    print(request.json)
    hostname = request.json['hostname']
    if hostname not in drivers:
        drivers[hostname] = run_driver(hostname)
    print(drivers)
    return "Driver start"


@app.route('/delete-driver', methods=["POST"])
def delete_driver():
    host = request.json['hostname']
    del drivers[host]
    return 'power'


@app.route("/change-password", methods=['POST'])
def change_password():
    authenticated = is_authenticated(request.json['user'], request.json['password'])
    if authenticated:
        hostname = request.json['hostname']
        folio_id = get_folio_id(request.json['username'])
        result = drivers[hostname].change_password(folio_id=folio_id)
        if result == "PASSWORD_CHANGED":
            insert_pass_logs(user=request.json['user'], username=request.json['username'],
                             hostname=request.json['hostname'])
        return result
    else:
        return jsonify("NOT_AUTHENTICATED", 404)


@app.route("/call-support", methods=["POST"])
def call_support():
    send_message(f"Hostname: {request.json['hostname']}\nUser: {request.json['username']}\nMessage:\n{request.json['message']}")
    return "200"

@app.route("/pass-logs", methods=['GET'])
def passing_logs():
    logs = get_pass_logs()
    return logs


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
