from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def health():
    return jsonify({
        "project": "DevSecOps Cisco IOS CIS Audit & Trivy Scan",
        "status": "running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
