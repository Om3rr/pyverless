import argparse
import importlib
import importlib.util
from collections import OrderedDict

import yaml

from pyverless import ServerlessFramework


def import_fw(fw_name):
    try:
        module_path, module_attr = fw_name.split(":")
        module = importlib.import_module(module_path)
        for attr in module_attr.split("."):
            module = getattr(module, attr)
    except Exception as e:
        raise Exception(f"Could not import {fw_name}") from e
    if not isinstance(module, ServerlessFramework):
        raise Exception(f"{fw_name} is not a ServerlessFramework")
    return module


def generate(sls_framework: 'ServerlessFramework', output_file: str):
    with open(output_file, 'w') as f:
        f.write(yaml.dump(sls_framework.__dict__()))


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())


def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)


def main():
    parser = argparse.ArgumentParser("Generate a pyverless project")
    parser.add_argument("framework_module", help="The file to generate the project from, main:sls", default="main:sls")
    parser.add_argument("--output", default="serverless.yml", help='The output file')
    args = parser.parse_args()
    fw = import_fw(args.framework_module)
    generate(fw, args.output)


setup_yaml()
if __name__ == '__main__':
    main()
