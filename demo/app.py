# DELIBERATELY INSECURE DEMO APP — DO NOT DEPLOY.
# Exists only so the pipeline in this repo has real findings to report.
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Hard-coded credential (secrets scan / SAST should flag this)
DB_PASSWORD = "Pr0d-Db-P@ssw0rd-2026!"


@app.route("/user")
def get_user():
    # SQL injection: user input concatenated into the query
    name = request.args.get("name", "")
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    return str(conn.execute(query).fetchall())


@app.route("/ping")
def ping():
    # Command injection: user input passed to a shell
    host = request.args.get("host", "127.0.0.1")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


if __name__ == "__main__":
    # Debug mode exposes the interactive debugger
    app.run(host="0.0.0.0", debug=True)
