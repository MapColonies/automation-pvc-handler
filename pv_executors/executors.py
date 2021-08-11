"""This module include all core manipulation for server"""
import os
import shutil
from configuration import config
from mc_automation_tools import common
from mc_automation_tools import shape_convertor
from stat import *


def create_new_test_dir(source_data, dest_data):
    """This method copy base data dir to new dir"""
    if os.path.exists(source_data):
        if os.path.exists(dest_data):
            shutil.rmtree(dest_data)

        os.makedirs(dest_data)
        # copy_tree(source_data, dest_data)
        copytree(source_data, dest_data)

    else:
        raise FileNotFoundError(f'Source directory not exists: [{source_data}]')


def render_discrete_name(shape_metadata):
    """
    This method will update and save metadata product id to original name + current time str
    :param shape_metadata: original metadata shape file
    :return: new rendered name
    """
    current_time_str = common.generate_datatime_zulu().replace('-', '_').replace(':', '_')
    resp = shape_convertor.add_ext_source_name(shape_metadata, current_time_str)
    return resp




def copytree(src, dst, symlinks=True, ignore=None):
    """
    This method will make recursive copy process from folder to folder - FileSystem
    """
    command = f'cp -r {src}/. {dst}'
    os.system(command)
    # for item in os.listdir(src):
    # try:
    #
    #     s = os.path.join(src, item)
    #     d = os.path.join(dst, item)
    #     # shutil.copymode(s, d)
    #     if os.path.isdir(s):
    #         shutil.copytree(s, d, symlinks, ignore)
    #     else:
    #
    #         shutil.copy2(s, d)
    # except Exception as e:
    #     print(str(e))

    # s = os.path.join(src, item)
    # d = os.path.join(dst, item)
    # # shutil.copymode(s, d)
    # if os.path.isdir(s):
    #     shutil.copytree(s, d, symlinks, ignore, copy_function=shutil.copy,)
    # else:
    #
    #     shutil.copy(s, d)


def copytree2(source_folder, destination_folder):
    from pathlib import Path
    import shutil

    # definiing source and desitnation
    # paths

    files = os.listdir(source_folder)

    # iterating over all the files in
    # the source directory
    for fname in files:
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(source_folder, fname), destination_folder)


def check_path(src):
    """This module validate source directory is valid for ingestion process"""
    if not os.path.exists(src):
        return False, f'Path [{src}] not exists'

    if not os.path.exists(os.path.join(src, config.SHAPES_PATH)):
        return False, f'Path [{os.path.join(src, config.SHAPES_PATH)}] not exists'

    if not os.path.exists(os.path.join(src, config.TIFF_PATH)):
        return False, f'Path [{os.path.join(src, config.TIFF_PATH)}] not exists'

    res = set(config.SHAPE_FILE_LIST).intersection(os.listdir(os.path.join(src, config.SHAPES_PATH)))
    if len(res) != len(config.SHAPE_FILE_LIST):
        return False, f'Path [{os.path.join(src, config.SHAPES_PATH)}] missing files:{set(config.SHAPE_FILE_LIST).symmetric_difference(set(config.SHAPE_FILE_LIST).intersection(os.listdir(os.path.join(src, config.SHAPES_PATH))))}'

    shape_metadata_shp = shape_convertor.shp_to_geojson(os.path.join(src, config.SHAPES_PATH, 'ShapeMetadata.shp'))
    Product_shp = shape_convertor.shp_to_geojson(os.path.join(src, config.SHAPES_PATH, 'Product.shp'))
    Files_shp = shape_convertor.shp_to_geojson(os.path.join(src, config.SHAPES_PATH, 'Files.shp'))
    img_path = os.path.join(src, config.TIFF_PATH)
    res = shape_convertor.generate_oversear_request(shape_metadata_shp, Product_shp, Files_shp, img_path)
    return True, res
