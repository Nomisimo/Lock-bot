import logging
from pathlib import Path
from configparser import ConfigParser
from pprint import pformat

PATH_CONFIG = Path("config.cfg")
PATH_TEMPLATE = Path(__file__).parent.joinpath("config_template.cfg")
CONFIG = None


class ConfigError(Exception):
    """Exception for not loaded config / ..."""

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)-8s - %(name)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# reduce logging for httpx
logging.getLogger("httpx").setLevel(logging.WARNING)



def log(message, category='general', level=logging.INFO):
    logger.log(level, f"[{category.lower()}] {message}")


def load_config(path=None) -> ConfigParser:
    global PATH_CONFIG, CONFIG
    if path is not None and path.exists():
        PATH_CONFIG = path

    if not PATH_CONFIG.exists():
        assert PATH_TEMPLATE.exists()
        PATH_CONFIG.write_text(PATH_TEMPLATE.read_text())
        log(f"new config file created at {PATH_CONFIG.resolve()}.\n\tUpdate the file.")
        raise ConfigError(f"The file @{PATH_CONFIG.resolve()} was created.")

    CONFIG = ConfigParser()
    CONFIG.read(PATH_CONFIG)
    log(f"The config loaded from {PATH_CONFIG.resolve()}", "config")

def show_config():
    dconfig = {k: dict(v) for k,v in dict(CONFIG).items()}
    log(f"the current config of lockbot:\n{pformat(dconfig)}", "config")



sentinel = object()
def get(section, option, fallback=sentinel):
    """ retrieve a value from the config file.
    The sentinel is a custom value to allow 'None' to be a possible fallback value.
    """
    if CONFIG is None:
        raise ConfigError("the config is not loaded.")
    if fallback is not sentinel:
        return CONFIG.get(section, option, fallback=fallback)
    return CONFIG.get(section, option)

def get_authorized():
    if CONFIG is None:
        raise ConfigError("the config is not loaded.")
    return {int(key) for key, val in CONFIG["authorized"].items() if val == "True"}


def _test_config():
    load_config()
    show_config()
    

# if __name__ == "__main__":
    # _test()