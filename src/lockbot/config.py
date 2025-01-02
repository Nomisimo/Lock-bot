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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_message(message, category='general'):
    logger.info(f"[{category.upper()}] {message}")


def load_config(path=None) -> ConfigParser:
    global PATH_CONFIG, CONFIG
    if path is not None and path.exists():
        PATH_CONFIG = path

    if not PATH_CONFIG.exists():
        assert PATH_TEMPLATE.exists()
        PATH_CONFIG.write_text(PATH_TEMPLATE.read_text())
        log_message(f"new config file created at {PATH_CONFIG.resolve()}.\n\tUpdate the file.")
        raise ConfigError(f"The file @{PATH_CONFIG.resolve()} was created.")

    CONFIG = ConfigParser()
    CONFIG.read(PATH_CONFIG)
    log_message(f"The config loaded from {PATH_CONFIG.resolve()}", "config")

def show_config():
    dconfig = {k: dict(v) for k,v in dict(CONFIG).items()}
    log_message(f"the current config of lockbot:\n{pformat(dconfig)}", "config")

def _test():
    load_config()
    show_config()
    
if __name__ == "__main__":
    _test()