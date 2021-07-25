"""This module include all core manipulation for server"""
import os
import shutil
from configuration import config
from mc_automation_tools import common
from mc_automation_tools import shape_convertor

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





def copytree(src, dst, symlinks=False, ignore=None):
    """
    This method will make recursive copy process from folder to folder - FileSystem
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
