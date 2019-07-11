from flask import jsonify, Flask

app = Flask(__name__)
from app import views

app.static_folder = 'static'
app.config['STATIC_FOLDER'] = 'static'

app.run(host="127.0.0.1", port=7000)

