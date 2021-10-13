from flask import Flask
from flask import Response
from flask_healthz import healthz
from flask_healthz import HealthError
from mc_automation_tools import common
app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")
from http.server import BaseHTTPRequestHandler, HTTPServer
from pv_executors import executors
from configuration import config
import os
import json

os.environ['RND_FOLDER_NAME'] = ""


def printok():
    print("Everything is fine")


def liveness():
    try:
        printok()
    except Exception:
        raise HealthError("Can't connect to the file")


def readiness():
    try:
        printok()
    except Exception:
        raise HealthError("Can't connect to the file")


app.config.update(
    HEALTHZ={
        "live": "app.liveness",
        "ready": "app.readiness",
    }
)


@app.route('/createTestDir')
def generate_new_test_dir():
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    dest = config.PV_TEST_DIR_NAME

    source = os.path.join(root, base)
    dest = os.path.join(root, dest)
    os.environ['RND_FOLDER_NAME'] = ""
    response = _helper_copy_request(source, dest)
    return response


@app.route('/updateShape')
def change_shape_metadata():
    root = config.PV_ROOT_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, dest, 'Shapes', config.SHAPE_METADATA_NAME)

    response = _helper_name_changer(dest)
    return response


@app.route('/updateWatchShape')
def change_watch_shape_metadata():
    root = config.PV_ROOT_DIR
    watch_dir = config.PV_WATCH_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, watch_dir, dest,os.environ['RND_FOLDER_NAME'], 'Shapes', config.SHAPE_METADATA_NAME)

    response = _helper_name_changer(dest)
    return response


def _helper_name_changer(dest):
    try:
        resp = executors.render_discrete_name(dest)
        msg = json.dumps({'message': f'Source name changed into: {resp}', 'source': f'{resp}'})
        return Response(msg, status=201, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


@app.route('/validatePath')
def validate_path():
    root = config.PV_ROOT_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, dest)

    response = _helper_path_validator(dest)
    return response


@app.route('/validateWatchPath')
def validate_watch_path():
    root = config.PV_ROOT_DIR
    watch_dir = config.PV_WATCH_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'])

    response = _helper_path_validator(dest)
    return response


def _helper_path_validator(dest):
    try:
        state, resp = executors.check_path(dest)
        if state:
            msg = json.dumps(
                {'message': f'directory: {dest} include all relevant file', 'failure': False, 'json_data': resp})
            return Response(msg, status=200, mimetype='application/json')
        else:
            msg = json.dumps({'message': f'directory: {dest} failed on validation', 'failure': True, 'json_data': resp})
            return Response(msg, status=200, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


@app.route('/createWatchDir')
def generate_watch_dir():
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    watch_dir = config.PV_WATCH_DIR
    dest = config.PV_TEST_DIR_NAME
    os.environ['RND_FOLDER_NAME'] = common.generate_uuid()
    source = os.path.join(root, base)
    dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'])

    response = _helper_copy_request(source, dest)
    return response


@app.route('/')
def start_page():
    try:
        msg = json.dumps({'message': 'main page of pvc handler for qa testing'})
        return Response(msg, status=200, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


def _helper_copy_request(source, dest):
    try:
        print('1')
        executors.create_new_test_dir(source, dest)
        print('2')
        msg = json.dumps({'message': f'created copy of: {source} directory into: {dest}', 'source': f'{source}',
                          'newDesination': f'{dest}'})
        print('3')
        return Response(msg, status=201, mimetype='application/json')

    except NotADirectoryError as e1:
        msg = json.dumps({'message': f'Directory not found: {source}'})
        return Response(msg, status=404, mimetype='application/json')
        # return {'message': f'Directory not found: {source}'}, 404

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
