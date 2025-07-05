import json
from pathlib import Path
from typing import Any

PATH_TASK_CONFIG = Path(__file__).parents[1] / "config" / "tasks_geometry.json"


def get_task_config_param(json_url: str) -> Any:
    """Retrieves a specific parameter from the task configuration JSON file.

    :param json_url: The path to the desired parameter, in the format
        "key_element/key_property".
    :return: The value of the requested configuration parameter.
    """

    config = load_json_file(PATH_TASK_CONFIG)
    json_url = json_url.lstrip("/").rstrip("/")
    list_keys = json_url.split("/")
    key_element = list_keys[0]
    key_property = list_keys[1]

    if key_element not in config:
        raise KeyError(f"Element '{key_element}' not found in configuration.")
    if key_property not in config[key_element]:
        raise KeyError(
            f"Property '{key_property}' not found for element '{key_element}' in"
            " configuration."
        )
    return config[key_element][key_property]


def load_json_file(filepath: str | Path) -> dict:
    """
    Loads a JSON file and returns its contents as a dictionary.

    :param filepath: Path to the JSON file.
    :return: Dictionary with the parsed JSON data.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {filepath}: {e}")
