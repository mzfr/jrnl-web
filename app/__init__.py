from flask import jsonify, Flask

app = Flask(__name__)
from app import views

app.run(host="127.0.0.1", port=7000)

