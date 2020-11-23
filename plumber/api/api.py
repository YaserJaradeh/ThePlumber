import os
import sys
####################################
# Need a more prominent solution
sys.path.append(os.getcwd())
sys.path.append(f'{os.getcwd()}/plumber')
####################################
from flask import Flask, jsonify, url_for, request
from plumber.api import info
from plumber.pipeline.pipeline_manager import PipelineParser
from plumber.components import StanfordClient, OLLIEClient


app = Flask(__name__)

kwargs = {}
stan = StanfordClient()
ollie = OLLIEClient()
kwargs['stanford_client'] = stan
kwargs['ollie_client'] = ollie


@app.route('/', methods=['GET'])
def index():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        if rule.endpoint == "static":
            continue
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:40s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    return jsonify(sorted(output))


@app.route('/components', methods=['GET'])
def get_components():
    return jsonify(info.components)


@app.route('/pipelines', methods=['GET'])
def get_pipelines():
    return jsonify(info.pipelines)


@app.route('/run', methods=['PUT', 'POST'])
def run_pipeline():
    config = request.get_json(silent=False)
    template = {
        "pipeline": {
            "name": "plumber pipeline",
            "components": {
                "extractor": config["extractor"],
                "linker": config["linker"],
                "resolver": config["resolver"],
                "reader": "feed",
                "writer": "return"
            },
            "parameters": {
                "content": config["input_text"]
            }
        }
    }
    pipeline, params = PipelineParser.create(template, **kwargs)
    pipeline.consume([1])
    # PipelineParser.clean_up(params)
    return jsonify(pipeline.top_node.terminal_node_set.pop().end())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

