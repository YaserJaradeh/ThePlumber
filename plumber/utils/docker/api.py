import spacy
from flask import Flask, request, jsonify
from typing import List


api = Flask(__name__)

model_dir = "/app/my_nlp"
nlp = spacy.load(model_dir)


@api.route('/link', methods=['POST'])
def get_companies() -> List:
    data = request.json
    result = []
    try:
        doc = nlp(data['text'])
        for ent in doc.ents:
            result.append({'text': ent.text, 'type': ent.label_, 'uri': ent.kb_id_})
        return jsonify(result)
    except:
        return jsonify(result)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)
