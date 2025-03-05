import os

from flask_cors import CORS
from flask import Flask, g, send_file
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from endpoints import v1
from utils.database import SessionLocal
from utils.config import STORAGE_PATH, STORAGE_DIRECTORIES
from utils.exception import ResponseException

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_request
def before_request():
    g.db = SessionLocal()
    g.user = None


@app.after_request
def after_request(response):
    if hasattr(g, 'db') and g.db is not None:
        g.db.close()
    return response


@app.errorhandler(NoResultFound)
def no_result_found_handler(e):
    return {'status': 'not_found', 'result': -1, 'payload': {'message': str(e)}}, 404


@app.errorhandler(MultipleResultsFound)
def multiple_result_found_handler(e):
    return {'status': 'multiple_result_found', 'result': -1, 'payload': {'message': str(e)}}, 403


@app.errorhandler(ResponseException)
def app_exception_handler(e):
    return {'status': e.status, 'result': e.result, 'payload': e.payload}, e.status_code


@app.errorhandler(KeyError)
def app_exception_handler(e):
    return {'status': 'not_enough_params', 'result': -1, 'payload': str(e)}, 403


@app.errorhandler(AssertionError)
def app_exception_handler(e):
    return {'status': 'assertion_error', 'result': -1, 'payload': str(e)}, 403


@app.errorhandler(ValueError)
def app_exception_handler(e):
    return {'status': 'invalid_params', 'result': -1, 'payload': str(e)}, 403


@app.errorhandler(IndexError)
def app_exception_handler(e):
    return {'status': 'unknown_error', 'result': -1, 'payload': str(e)}, 403


@app.route('/storage/<string:directory>/<path:path>', methods=['GET'])
def storage_get(directory, path):
    if directory not in STORAGE_DIRECTORIES:
        raise ResponseException()
    try:
        return send_file(str(os.path.join(STORAGE_PATH, directory, path)))
    except Exception as e:
        raise ResponseException(
            payload={'message': str(e).split(': ')[1].split('/storage')[1]},
            status='file_not_found',
            status_code=404,
        )


app.register_blueprint(v1.bp)
