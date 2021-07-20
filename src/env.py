import toml
import os


def load_config(filename: str = os.path.relpath("../config.toml")):
    with open(filename, "r") as fh:
        return toml.load(fh)


def save_to_config(filename: str = os.path.relpath("../config.toml")):
    with open(filename, "w") as fh:
        return toml.dump(CONFIG, fh)


CONFIG = load_config()