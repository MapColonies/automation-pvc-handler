from configuration import config
from pv_executors import executors
from mc_automation_tools import common
import os

root = config.PV_ROOT_DIR
base = config.PV_BASE_DATA_DIR
dest = config.PV_TEST_DIR_NAME

source = os.path.join(root, base)
dest = os.path.join(root,dest)
executors.create_new_test_dir(source, dest)
executors.render_discrete_name(os.path.join(dest, 'Shapes', 'ShapeMetadata.shp'))

