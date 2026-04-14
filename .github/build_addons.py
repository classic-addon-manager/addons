import json
import os
from glob import glob

import yaml

directory = os.getcwd()
output_file = "addons.json"
combined_data = []

# We only support .YAML extensions
for filepath in glob("**/*.yaml", recursive=True):
    if ".github" in filepath:
        continue
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
        combined_data.append(data)

combined_data.sort(key=lambda x: x.get("name", ""))

with open(output_file, "w") as outfile:
    json.dump(combined_data, outfile)
