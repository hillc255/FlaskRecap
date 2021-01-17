from flask import Flask, request, jsonify, abort
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        return f(jwt, *args, **kwargs)
    return wrapper
app = Flask(__name__)

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token
			
@app.route('/headers')
@requires_auth
def headers(jwt):
    # @TODO unpack the request header
    print(jwt)
    return 'not implemented'

@app.route('/images')
@requires_auth
def images(jwt):
    # @TODO unpack the request header
    print(jwt)
    return 'not implemented'

greetings = {
            'en': 'hello', 
            'es': 'Hola', 
            'ar': 'مرحبا',
            'ru': 'Привет',
            'fi': 'Hei',
            'he': 'שלום',
            'ja': 'こんにちは'
            }

@app.route('/greeting', methods=['GET'])
def greeting_all():
    return jsonify({'greetings': greetings})

@app.route('/greeting/<lang>', methods=['GET'])
def greeting_one(lang):
    print(lang)
    if(lang not in greetings):
        abort(404)
    return jsonify({'greeting': greetings[lang
    ]})

@app.route('/greeting', methods=['POST'])
def greeting_add():
    info = request.get_json()
    if('lang' not in info or 'greeting' not in info):
        abort(422)
    greetings[info['lang']] = info['greeting']
    return jsonify({'greetings':greetings})
