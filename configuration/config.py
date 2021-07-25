from mc_automation_tools import common


PV_ROOT_DIR = common.get_environment_variable("PV_ROOT_DIR", "/tmp/ingestion")
PV_BASE_DATA_DIR = common.get_environment_variable("PV_BASE_DATA_DIR", "1")
PV_TEST_DIR_NAME = common.get_environment_variable("PV_TEST_DIR_NAME", "test_data_automation")
SHAPE_METADATA_NAME = common.get_environment_variable("SHAPE_METADATA_NAME", "ShapeMetadata.shp")
