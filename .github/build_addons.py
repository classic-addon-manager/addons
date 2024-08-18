import os
import yaml
import json

directory = os.getcwd()
output_file = "addons.json"
combined_data = []

for filename in os.listdir(directory):
    if filename.endswith(".yaml") or filename.endswith(".yml"):
        with open(os.path.join(directory, filename), 'r') as file:
            data = yaml.safe_load(file)
            combined_data.append(data)

combined_data.sort(key=lambda x: x.get('name', ''))

with open(output_file, 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)