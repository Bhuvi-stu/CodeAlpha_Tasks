"""Initial, intentionally vulnerable application used for the before scan."""
from flask import Flask, request
import sqlite3

app = Flask(__name__)
app.secret_key = "development-secret-change-me"


@app.get("/user")
def get_user():
    username = request.args.get("username", "")
    connection = sqlite3.connect("users.db")
    query = f"SELECT username FROM users WHERE username = '{username}'"
    row = connection.execute(query).fetchone()
    connection.close()
    return row[0] if row else "Not found"


if __name__ == "__main__":
    app.run(debug=True)
