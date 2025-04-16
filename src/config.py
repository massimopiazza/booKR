from os import path as op
import yaml
import jsonschema

# build file paths relative to project root
BASE_DIR = op.abspath(op.join(op.dirname(__file__), ".."))
CONFIG_FILE = op.join(BASE_DIR, "config.yaml")
SCHEMA_FILE = op.join(BASE_DIR, op.join("src", "config_schema.json"))

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# load JSON schema and config file
_schema = load_yaml(SCHEMA_FILE)
_config = load_yaml(CONFIG_FILE)

# convert keys in 'annotation_type_map' to strings (if they are not already)
if "annotation_type_map" in _config:
    _config["annotation_type_map"] = { str(k): v for k, v in _config["annotation_type_map"].items() }

# validate config file format using JSON schema
jsonschema.validate(instance=_config, schema=_schema)

# expose config values (default values provided as a backup)
ANNOTATION_DB_PATTERN   = _config.get("annotation_db_pattern", "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/AEAnnotation*.sqlite")
LIBRARY_DB_PATTERN      = _config.get("library_db_pattern", "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary*.sqlite")
ANNOTATION_TYPE_MAP     = _config.get("annotation_type_map", {"1": "HIGH-IMPORTANCE", "3": "MID-IMPORTANCE"})
MIN_ANNOTATION_LENGTH   = _config.get("min_annotation_length", 80)
ANNOTATION_HEX_PALETTE  = _config.get("annotation_hex_palette", ["#2e9599", "#f7dc66", "#f36943", "#f1184c", "#a8216b"])