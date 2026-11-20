from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "hello im big duck"

@app.route("/hi/<name>")
def hi(name):
    return f"hi{name}"


if __name__  == "__main__":
    app.run(debug=True)