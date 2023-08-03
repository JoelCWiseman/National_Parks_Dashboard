from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# API endpoint to get all park data
@app.route("/api/parks", methods=["GET"])
def get_parks():
    conn = sqlite3.connect("national_parks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parks")
    parks = [{"parkCode": code, "fullName": name, "description": desc, "states": states}
             for code, name, desc, states in cursor.fetchall()]
    conn.close()
    return jsonify({"data": parks})

if __name__ == "__main__":
    app.run(debug=True)