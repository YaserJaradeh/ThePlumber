import os
import sys
####################################
# Need a more prominent solution
sys.path.append(os.getcwd())
sys.path.append(f'{os.getcwd()}/plumber')
####################################
from flask import Flask, jsonify
from plumber.api import info


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify(info.components)


@app.route('/components', methods=['GET'])
def get_components():
    return jsonify(info.components)


@app.route('/pipelines', methods=['GET'])
def get_pipelines():
    return jsonify(info.pipelines)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

