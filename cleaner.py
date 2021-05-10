from dataclasses import dataclass
import logging
import json
log = logging.getLogger(__name__)

@dataclass
class Cleaner:
    """ Class for Cleaning different JSON files """
    differences: object
    removable_list = [
        "root['deviceId']", 
        "root['items']['SystemUnit.Name']['value']",
        ]

    def clean(self) -> object:
        """ Take object already passed to class and remove
            confusing naming, remove unneeded differences, 
            and return a JSON file. 
        """
        cleaned_diff = {}
        # include the static values
        cleaned_diff['filename'] = self.differences["filename"]
        cleaned_diff['system name'] = self.differences["name"]
        cleaned_diff['differences'] = {}
        
        # loop over the differences and remove items
        try:
            for key, value in self.differences['difference'].items():
                if key not in self.removable_list:
                    key = key.split("root['items']")[1]
                    cleaned_diff['differences'][key] = value
        except Exception as e:
            log.error(f'Error cleaning {self.differences["filename"]}: {e}')
        return cleaned_diff
            
