from dataclasses import dataclass
import csv
import json
import logging
log = logging.getLogger(__name__)

@dataclass
class Converter:
    """ Class to convert json object to csv """
    models_list: list

    def to_csv(self, path_to_save):
        try:
            with open(path_to_save, 'w') as output:
                csv_writer = csv.writer(output)
                count = 0
                for devices in self.models_list:
                    # devices_json = json.dumps(devices)
                    if count == 0:
                        model = list(devices.keys())
                        csv_writer.writerow(model)
                        csv_writer.writerow(devices[model]['filename'])
                        csv_writer.writerow(devices[model]['system name'])
                        count += 1
                    csv_writer.writerow(devices[model]["differences"])
                

        except Exception as e:
            log.error(f'Error with CSV Output: {e}')

        