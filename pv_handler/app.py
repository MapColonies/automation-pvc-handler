from flask import Flask
from flask import Response, request
from flask_healthz import healthz
from flask_healthz import HealthError
from mc_automation_tools import common

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")
from http.server import BaseHTTPRequestHandler, HTTPServer
from discrete_kit.functions import metadata_convertor
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


@app.route('/deleteTestDir', methods=['GET'])
def delete_test_dir():
    folder_name = request.args.get("folder")
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    # dest = config.PV_TEST_DIR_NAME
    # dest = config.PV_TEST_DIR_NAME

    dest = os.path.join(root, config.PV_WATCH_DIR, folder_name)
    response = _helper_delete_folder(dest)
    return response


@app.route('/deleteFromFolder', methods=['GET'])
def delete_file_from_folder():
    folder_name = request.args.get('folder')
    file_name = request.args.get('file')
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    dest = os.path.join(root, config.PV_WATCH_DIR, folder_name)
    response = _helper_delete_file_from_folder(dest, file_name)
    return response


@app.route('/createTestDir')
def generate_new_test_dir():
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    dest = config.PV_TEST_DIR_NAME

    source = os.path.join(root, base)
    dest = os.path.join(root, config.PV_WATCH_DIR, dest)
    os.environ['RND_FOLDER_NAME'] = ""
    response = _helper_copy_request(source, dest)
    return response


@app.route('/updateShape')
def change_shape_metadata():
    root = config.PV_ROOT_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, config.PV_WATCH_DIR, dest, 'Shapes', config.SHAPE_METADATA_NAME)

    response = _helper_name_changer(dest)
    return response


@app.route('/updateWatchShape')
def change_watch_shape_metadata():
    root = config.PV_ROOT_DIR
    watch_dir = config.PV_WATCH_DIR
    # dest = config.PV_TEST_DIR_NAME
    dest = os.environ['RND_FOLDER_NAME']
    # dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'], 'Shapes', config.SHAPE_METADATA_NAME)
    dest = os.path.join(root, watch_dir, dest, 'Shapes', config.SHAPE_METADATA_NAME)
    response = _helper_name_changer(dest)
    return response


def _helper_delete_file_from_folder(dest, filename):
    try:
        executors.delete_file_from_dir(dest, filename)
        msg = json.dumps({'message': f'{filename} from {dest}  deleted successfully'})
        return Response(msg, status=200, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


def _helper_delete_folder(dest):
    try:
        executors.delete_test_dir(dest)
        msg = json.dumps({'message': f'{dest} folder deleted successfully'})
        return Response(msg, status=200, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


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
    dest = os.path.join(root, config.PV_WATCH_DIR, dest)

    response = _helper_path_validator(dest)
    return response


@app.route('/validateWatchPath')
def validate_watch_path():
    root = config.PV_ROOT_DIR
    watch_dir = config.PV_WATCH_DIR
    # dest = config.PV_TEST_DIR_NAME
    dest = os.environ['RND_FOLDER_NAME']
    # dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'])
    dest = os.path.join(root, watch_dir, dest)

    response = _helper_path_validator(dest)
    return response

    # a


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
        msg = json.dumps({'message': f'internal server error - {str(e)}', 'failure': True})
        return Response(msg, status=500, mimetype='application/json')


def _helper_max_zoom_change(dir, max_zoom):
    """
    :param dir: parent dir of all related tfw files
    :param max_zoom: max zoom value to be updated on tfw
    :return: response of the request - code and related message -json format
    """

    if not max_zoom:
        msg = json.dumps(
            {'message': "Bad Request", "failure": True, 'json_data': "most provide 'max_zoom' parameter on request'"})
        return Response(msg, status=400, mimetype='application/json')
    if not os.path.exists(dir) or not os.listdir(dir):
        msg = json.dumps(
            {'message': "Directory not found / Empty directory", "failure": True,
             'json_data': "Directory not found / Empty directory"})
        return Response(msg, status=409, mimetype='application/json')
    try:
        resp = metadata_convertor.replace_discrete_resolution(dir, max_zoom)
        state = all(d['success'] for d in resp)
        if state:
            msg = json.dumps(
                {'message': f'All tfw files in directory: {dir} were changed', 'failure': False, 'json_data': resp})
            return Response(msg, status=200, mimetype='application/json')
        else:
            msg = json.dumps(
                {'message': f'failed update files on directory: {dir}', 'failure': True, 'json_data': resp})
            return Response(msg, status=409, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


@app.route('/changeMaxZoom')
def change_max_zoom_resolution():
    max_zoom = request.args.get('max_zoom')
    root = config.PV_ROOT_DIR
    dest = config.PV_TEST_DIR_NAME
    dest = os.path.join(root, config.PV_WATCH_DIR, dest)
    response = _helper_max_zoom_change(dest, max_zoom)
    return response


@app.route('/changeWatchMaxZoom')
def change_watch_max_zoom_resolution():
    max_zoom = request.args.get('max_zoom')
    root = config.PV_ROOT_DIR
    watch_dir = config.PV_WATCH_DIR
    # dest = config.PV_TEST_DIR_NAME
    dest = os.environ['RND_FOLDER_NAME']
    # dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'])
    dest = os.path.join(root, watch_dir, dest)

    response = _helper_max_zoom_change(dest, max_zoom)
    return response


@app.route('/createWatchDir')
def generate_watch_dir():
    root = config.PV_ROOT_DIR
    base = config.PV_BASE_DATA_DIR
    watch_dir = config.PV_WATCH_DIR
    # dest = config.PV_TEST_DIR_NAME
    os.environ['RND_FOLDER_NAME'] = common.generate_uuid()
    dest = os.environ['RND_FOLDER_NAME']
    source = os.path.join(root, base)
    # dest = os.path.join(root, watch_dir, dest, os.environ['RND_FOLDER_NAME'])
    dest = os.path.join(root, watch_dir, dest)

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
        executors.create_new_test_dir(source, dest)
        msg = json.dumps({'message': f'created copy of: {source} directory into: {dest}', 'source': f'{source}',
                          'newDesination': f'{dest}'})
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
