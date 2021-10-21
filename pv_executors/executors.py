"""This module include all core manipulation for server"""
import os
import shutil
from pathlib import Path
import discrete_kit.configuration.config
import jsonschema.validators
from discrete_kit.functions.shape_functions import *
from discrete_kit.validator.schema_validator import *
from configuration import config
from mc_automation_tools import common
from mc_automation_tools import shape_convertor
from stat import *


def create_new_test_dir(source_data, dest_data):
    """This method copy base data dir to new dir"""
    if os.path.exists(source_data):
        if os.environ['RND_FOLDER_NAME']:
            if os.path.exists(os.path.dirname(dest_data)):
                shutil.rmtree(os.path.dirname(dest_data))
        else:
            if os.path.exists(dest_data):
                shutil.rmtree(dest_data)

        os.makedirs(dest_data)
        # copy_tree(source_data, dest_data)
        copytree(source_data, dest_data)

    else:
        raise NotADirectoryError(f'Source directory not exists: [{source_data}]')


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
    missing_set_files = []
    if not os.path.exists(src):
        return False, f'Path [{src}] not exists'

    # if not os.path.exists(os.path.join(src, config.SHAPES_PATH)):
    #     return False, f'Path [{os.path.join(src, config.SHAPES_PATH)}] not exists'
    if not find_if_folder_exists(src, config.SHAPES_PATH):
        return False, f'Path [{os.path.join(src, config.SHAPES_PATH)}] not exists'

    if not find_if_folder_exists(src, config.TIFF_PATH):
        return False, f'Path [{os.path.join(src, config.TIFF_PATH)}] not exists'

    ret_folder = get_folder_path_by_name(src, config.SHAPES_PATH)
    for file_name in discrete_kit.configuration.config.files_names:
        for ext in discrete_kit.configuration.config.files_extension_list:
            ret_extension_validation, missing = discrete_kit.configuration.config.validate_ext_files_exists(
                os.path.join(ret_folder, file_name), ext)
            if not ret_extension_validation:
                missing_set_files.append(missing)
    if missing_set_files:
        return False, f'Path [{os.path.join(src, config.SHAPES_PATH)}] missing files:{set(missing_set_files)}'

    json_object_res = ShapeToJSON(ret_folder)
    try:
        with open(Path(Path(__file__).resolve()).parent.parent / 'jsons/shape_file.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(json_object_res.get_json_output()), f, ensure_ascii=False)
    except IOError:
        return False, "Cannot write json file to run validation on schema."
    dir_name = os.path.dirname(__file__)
    dir_name = Path(Path(dir_name).resolve()).parent
    full_path = os.path.join(dir_name, discrete_kit.configuration.config.SCHEMA_FOLDER,
                             discrete_kit.configuration.config.JSON_NAME)
    schema_file = open(full_path, 'r')
    schema_data_to_comp = json.load(schema_file)
    if validate_json_types(schema_data_to_comp,
                           json_object_res.get_json_output()) is None:
        return True, json_object_res.created_json
    else:
        return False, validate_json_types(json_object_res.get_json_output())


def find_if_folder_exists(directory, folder_to_check):
    os.walk(directory)
    directory_lists = [x[0] for x in os.walk(directory)]
    for current_dir in directory_lists:
        if folder_to_check in current_dir:
            return True
    return False


def get_folder_path_by_name(path, name):
    p_walker = [x[0] for x in os.walk(path)]
    path = ("\n".join(s for s in p_walker if name.lower() in s.lower()))
    return path
