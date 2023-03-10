from flask import Flask, request, jsonify
from iacopilot import __main__

app = Flask(__name__)
copilot = __main__.IaCopilot()

@app.route('/load_ia', methods=['POST'])
def load_context():
    data = request.json
    id = data.get('id')
    if id:
        try:
            copilot.load_ia(id)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        return jsonify({'status': 'error', 'message': 'ID parameter is missing'})

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data['query']

    answer = copilot.ask_gpt(query).strip()

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()