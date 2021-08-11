from mc_automation_tools import common


PV_ROOT_DIR = common.get_environment_variable("PV_ROOT_DIR", "/tmp/ingestion")
PV_WATCH_DIR = common.get_environment_variable("PV_WATCH_DIR", "/tmp/watch")
PV_BASE_DATA_DIR = common.get_environment_variable("PV_BASE_DATA_DIR", "1")
PV_TEST_DIR_NAME = common.get_environment_variable("PV_TEST_DIR_NAME", "test_data_automation")
SHAPE_METADATA_NAME = common.get_environment_variable("SHAPE_METADATA_NAME", "ShapeMetadata.shp")


SHAPES_PATH = common.get_environment_variable('SHAPES_PATH', 'Shapes')
TIFF_PATH = common.get_environment_variable('TIFF_PATH', 'tiff')
# SHAPE_FILE_LIST = ['Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_FILE_LIST = ['Files.shp', 'Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_METADATA_FILE = common.get_environment_variable('SHAPE_METADATA_FILE', 'ShapeMetadata.shp')