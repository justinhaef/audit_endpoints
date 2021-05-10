import json
import argparse
import logging
from datetime import datetime
from tqdm import tqdm
from pathlib import Path
from parser import Parser
from cleaner import Cleaner
from converter import Converter

# pip install deepdiff
from deepdiff import DeepDiff

logging.basicConfig(
    filename=Path('app.log'),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

#-----Helper Functions-----#

def get_folders(parent_folder):
    """ Grab the Folder names for all endpoint models"""
    endpoint_models = list()
    endpoint_folders = parent_folder.iterdir()
    for endpoints in endpoint_folders:
        if endpoints.is_dir():
            endpoint_models.append(endpoints.name)
    logging.debug(f'Found Folder Names: {endpoint_models}')
    return endpoint_models


def get_standard_config(endpoint):
    standard_config_folder = Path(f'./Endpoint/{endpoint}/Gold/').iterdir()
    for config in standard_config_folder:
        if config.is_file():
            standardConfig = config
            logging.debug(f'Standard config for {endpoint} found {config}')
        else:
            logging.error(f'No standard config file found for {endpoint}')
    return standardConfig


def gather_endpoints(endpoint):
    endpoint_files = list()
    endpoint_config_folder = Path(f'./Endpoint/{endpoint}/InstallBase/').iterdir()
    for endpoint in endpoint_config_folder:
        if endpoint.is_file():
            endpoint_files.append(endpoint)
        logging.debug(f'Found Endpoints: {endpoint.name}')
    return endpoint_files


#-----main function------#

def main(endpoint_models: list):
    """ Loop over endpoint models, search file directory for endpoints
        and compare to a standard endpoint config.
    """
    audit_list = list()
    for model in tqdm(endpoint_models, desc="Looping over endpoint models..."):
        # first get the gold standard config file
        standard_config_file = get_standard_config(model)

        # now open that standard file
        with open(standard_config_file, 'r') as standard_config:
            standard_config_json = json.load(standard_config)
        
        audit = Parser(standard_config_json)

        # gather endpoint filenames
        endpoint_config_files = gather_endpoints(model)

        for endpoint in tqdm(endpoint_config_files, desc="Looping over endpoint config files..."):
            with open(endpoint, 'r') as endpoint_file:
                endpoint_json = json.load(endpoint_file)

            config_diff = audit.compare(endpoint_json, endpoint.name)
            
            cleaner = Cleaner(config_diff)
            cleaned = cleaner.clean()
            audit_list.append({f"{model}": cleaned})
    
    today = datetime.today()
    convert = Converter(audit_list)
    convert.to_csv(Path(f'./output/{today.date()}.csv'))
    return audit_list


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        Cisco Video Endpoint Configuration Audit Application
    """,
    )

    argument_parser.add_argument(
        "-l",
        "--limit",
        help="Run whole application or limit to only functions",
        dest="limit",
        choices=['DX80', 'all'],
        default='all',
        required=False,
    )

    args = argument_parser.parse_args()
    endpoint_models = get_folders(Path('./Endpoint'))
    
    if args.limit == 'all':
        result = main(endpoint_models)
    elif args.limit in endpoint_models:
        model = list()
        model.append(args.limit)
        result = main(model)
    else:
        print(f'Sorry but {args.limit} not found in given inventory.')
        print(f'Please try again using one of these options: {endpoint_models}')

    if result:
        today = datetime.today()
        # convert = Convert(result)
        # convert.to_csv(Path(f'./output/{today.date()}.csv'))
        with open(Path(f'./output/{today.date()}.json'), 'w') as outfile:
            json.dump(result, outfile, indent=4)

        
        print(f'Audit complete.')
    else:
        print(f'There were no results from the audit.')