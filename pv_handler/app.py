from flask import Flask
from flask import Response
from flask_healthz import healthz
from flask_healthz import HealthError
app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")
from pv_executors import executors
from configuration import config
import os
import json

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
    HEALTHZ = {
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
    try:
        executors.create_new_test_dir(source, dest)
        # return Response(f'{"{"}"message": "created copy of: {source} directory into: {dest}{"}"}', status=201, mimetype='application/json')
        msg = json.dumps({'message': f'created copy of: {source} directory into: {dest}', 'source': f'{source}','newDesination':f'{dest}'})
        return Response(msg, status=201, mimetype='application/json')

    except NotADirectoryError as e1:
        msg = json.dumps({'message': f'Directory not found: {source}'})
        return Response(msg, status=404, mimetype='application/json')
        # return {'message': f'Directory not found: {source}'}, 404

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')


@app.route('/updateShape')
def change_shape_metadata():
    root = config.PV_ROOT_DIR
    # base = config.PV_BASE_DATA_DIR
    dest = config.PV_TEST_DIR_NAME

    # source = os.path.join(root, base)
    dest = os.path.join(root, dest, 'Shapes', config.SHAPE_METADATA_NAME)

    try:
        resp = executors.render_discrete_name(dest)
        msg = json.dumps({'message': f'Source name changed into: {resp}','source':f'{resp}'})
        return Response(msg, status=201, mimetype='application/json')

    except Exception as e:
        msg = json.dumps({'message': f'internal server error - {str(e)}'})
        return Response(msg, status=500, mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)