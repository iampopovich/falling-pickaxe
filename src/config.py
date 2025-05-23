import json
import os
import shutil

# If config.json does not exist, copy from default.config.json
if not os.path.exists("config.json"):
    print("config.json not found. Copying default.config.json to config.json.")
    shutil.copy("default.config.json", "config.json")

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)