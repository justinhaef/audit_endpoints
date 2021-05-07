from dataclasses import dataclass
from deepdiff import DeepDiff
import logging
log = logging.getLogger(__name__)

@dataclass
class Parser:
    """ Class for Parsing different JSON files """
    standard: object

    def _endpoint_compare(self, config):
        """ Take endpoint json and compare to standard json.
            Return difference between the two.
        """
        ddiff = DeepDiff(config, self.standard, ignore_order=True)
        return ddiff

    def compare(self, config: dict, filename: str) -> dict:
        diff = self._endpoint_compare(config)
        if not config['items']['SystemUnit.Name']['value']:
            name = "Unknown"
        else:
            name = config['items']['SystemUnit.Name']['value']
        try:
            data = {
                'filename': filename,
                'name': name,
                'difference': diff['values_changed']
            }
        except KeyError as e:
            log.error(f"KeyError of {e} making data object: {name}")
        return data

