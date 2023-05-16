from mc_automation_tools import common


PV_ROOT_DIR = common.get_environment_variable("PV_ROOT_DIR",  "/home/shayavr/ingestion_data/ingestion")
# PV_ROOT_DIR = common.get_environment_variable("PV_ROOT_DIR", "/home/shayavr/ingestion_data/ingestion")
UPDATE_GPKG = common.get_environment_variable("UPDATE_GPKG", "/update_gpkg")
# PV_ROOT_DIR = common.get_environment_variable("PV_ROOT_DIR", "/layerSources")


PV_WATCH_DIR = common.get_environment_variable("PV_WATCH_DIR", "watch")
PV_BASE_DATA_DIR = common.get_environment_variable("PV_BASE_DATA_DIR", "1")
PV_TEST_DIR_NAME = common.get_environment_variable("PV_TEST_DIR_NAME", "test_data_automation")
SHAPE_METADATA_NAME = common.get_environment_variable("SHAPE_METADATA_NAME", "ShapeMetadata.shp")
GEOPACKAGE_FOLDER = common.get_environment_variable('GEOPACKAGE_FOLDER','geopackage')


SHAPES_PATH = common.get_environment_variable('SHAPES_PATH', 'Shapes')
TIFF_PATH = common.get_environment_variable('TIFF_PATH', 'tiff')
# SHAPE_FILE_LIST = ['Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_FILE_LIST = ['Files.shp', 'Files.dbf', 'Product.shp', 'Product.dbf', 'ShapeMetadata.shp', 'ShapeMetadata.dbf']
SHAPE_METADATA_FILE = common.get_environment_variable('SHAPE_METADATA_FILE', 'ShapeMetadata.shp')