from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def check_security_headers(url):
    headers_to_check = [
        "X-XSS-Protection",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy"
    ]

    missing_headers = []

    response = requests.get(url)
    for header in headers_to_check:
        if header not in response.headers:
            missing_headers.append(header)

    return missing_headers

@app.route("/", methods=["GET", "POST"])
def index():
    missing_headers = []

    if request.method == "POST":
        target_url = request.form["target_url"]
        missing_headers = check_security_headers(target_url)

    return render_template("index.html", missing_headers=missing_headers)

if __name__ == "__main__":
    app.run(debug=True)
