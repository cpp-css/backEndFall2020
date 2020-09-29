from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    port = os.getenv("PORT", 9090)
    app.run(host="localhost", port=port, threaded=True, debug=False)