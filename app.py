import json
from pathlib import Path

# pip install deepdiff
from deepdiff import DeepDiff


def gather_endpoints(endpoints_dir):
    endpoint_files = list()
    for endpoint in Path(endpoints_dir).iterdir():
        if endpoint.is_file():
            endpoint_files.append(endpoint)
        print(f'Found Endpoints: {endpoint.name}')
    return endpoint_files

def endpoint_compare(endpoint, goldStandard):
    """ Take endpoint json and compare to standard json.
        Return difference between the two.
    """
    ddiff = DeepDiff(endpoint, goldStandard, ignore_order=True)
    return ddiff

def endpoint_loop(endpoint, goldStandard):
    diff = endpoint_compare(endpoint, goldStandard)
    data = {
        'name': endpoint['items']['SystemUnit.Name']['value'],
        'difference': diff
    }
    return data

if __name__ == "__main__":
    audit_list = list()

    goldStandard_file = './Endpoint/DX80/Gold/goldstandard.json'
    with open(goldStandard_file, 'r') as goldStandard:
        goldStandard = json.load(goldStandard)
    
    endpoints = gather_endpoints('./Endpoint/DX80/InstallBase/')
    for endpoint in endpoints:
        with open(endpoint, 'r') as endpoint_file:
            endpoint = json.load(endpoint_file)
            audit_return = endpoint_loop(endpoint, goldStandard)
            audit_list.append(audit_return)
    print(json.dumps(audit_list, indent=4))