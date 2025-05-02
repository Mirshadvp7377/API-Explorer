from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/explore', methods=['POST'])
def explore_api():
    data = request.json
    method = data.get('method')
    url = data.get('url')
    headers = data.get('headers', {})
    auth_token = data.get('auth_token')
    body = data.get('body', {})

    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=body, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=body, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            return jsonify({'error': 'Invalid HTTP method'}), 400

        return jsonify({
            'status_code': response.status_code,
            'response_headers': dict(response.headers),
            'response_body': response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected erro