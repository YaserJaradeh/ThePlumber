import os
import sys
####################################
# Need a more prominent solution
sys.path.append(os.getcwd())
sys.path.append(f'{os.getcwd()}/plumber')
####################################
from flask import Flask, jsonify, url_for, request
from flask_cors import CORS, cross_origin
from plumber.api import info
from plumber.pipeline.pipeline_manager import PipelineParser
from plumber.components import StanfordClient, OLLIEClient
from typing import Union, List


app = Flask(__name__)
cors = CORS(app)

kwargs = {}
stan = StanfordClient()
ollie = OLLIEClient()
kwargs['stanford_client'] = stan
kwargs['ollie_client'] = ollie


@app.route('/', methods=['GET'], strict_slashes=False)
@cross_origin()
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


@app.route('/components', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_components():
    return jsonify([component.as_dict() for component in info.components])


@app.route('/pipelines', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_pipelines():
    return jsonify([pipeline.as_dict() for pipeline in info.pipelines])


@app.route('/run', methods=['PUT', 'POST'], strict_slashes=False)
@cross_origin()
def run_pipeline():
    config = request.get_json(silent=False)
    error, extractors, resolvers, linkers = get_and_check_parameters(config)
    if error is not None:
        return jsonify({'errors': f"The following components are invalid {error}"}), 400
    template = {
        "pipeline": {
            "name": "plumber pipeline",
            "components": {
                "extractor": extractors,
                "linker": linkers,
                "resolver": resolvers,
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


def __lookup_class_name(class_name: Union[str, List], component_type: str) -> Union[List[str], str]:
    if isinstance(class_name, str):
        full_class_name = class_name.replace('_', '').lower().strip() + component_type.lower().strip()
        classes_map = PipelineParser.classes_map()
        keys = [key.replace('_', '').lower().strip() for key in classes_map.keys()]
        return None if full_class_name in keys else class_name
    else:
        results = []
        for name in class_name:
            results.append(__lookup_class_name(name, component_type))
        return [r for r in results if r is not None]


def get_and_check_parameters(config):
    extractors = "dummy" if "extractor" not in config or config["extractor"] is None else config["extractor"]
    resolvers = "dummy" if "resolver" not in config or config["resolver"] is None else config["resolver"]
    linkers = "dummy" if "linker" not in config or config["linker"] is None else config["linker"]
    if isinstance(extractors, list):
        extractors = "dummy" if len(extractors) == 0 else extractors
    if isinstance(resolvers, list):
        resolvers = "dummy" if len(resolvers) == 0 else resolvers
    if isinstance(linkers, list):
        linkers = "dummy" if len(linkers) == 0 else linkers
    invalid_extractors = __lookup_class_name(extractors, "extractor")
    invalid_linkers = __lookup_class_name(linkers, "linker")
    invalid_resolvers = __lookup_class_name(resolvers, "resolver")
    invalids = invalid_extractors if isinstance(invalid_extractors, list) else [invalid_extractors]
    invalids += invalid_linkers if isinstance(invalid_linkers, list) else [invalid_linkers]
    invalids += invalid_resolvers if isinstance(invalid_resolvers, list) else [invalid_resolvers]
    invalids = [v for v in invalids if v is not None]
    if len(invalids) > 0:
        return invalids, None, None, None
    return None, extractors, resolvers, linkers


if __name__ == "__main__":
    from plumber.main import plumber_logo
    print(plumber_logo)
    app.run(host='0.0.0.0', port=5000)

