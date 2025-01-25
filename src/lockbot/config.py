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


def load_config(path=None) -> ConfigParser:
    global PATH_CONFIG, CONFIG
    if path is not None and Path(path).exists():
        PATH_CONFIG = Path(path)

    if not PATH_CONFIG.exists():
        assert PATH_TEMPLATE.exists()
        PATH_CONFIG.write_text(PATH_TEMPLATE.read_text())
        logger.info(f"new config file created at {PATH_CONFIG.resolve()}.\n\tUpdate the file.")
        raise ConfigError(f"The file @{PATH_CONFIG.resolve()} was created.")

    CONFIG = ConfigParser()
    CONFIG.read(PATH_CONFIG)
    
    update_loglevels()
    logger.info(f"The config loaded from {PATH_CONFIG.resolve()}")

def show_config():
    dconfig = {k: dict(v) for k,v in dict(CONFIG).items()}
    logger.info(f"the current config of lockbot:\n{pformat(dconfig)}")


def update_loglevels():
    levels = dict(CONFIG["logging"])
    
    levels = {k: CONFIG["logging"].getint(k) for k in CONFIG["logging"]}
    for name, lvl in levels.items():
        logging.getLogger(name).setLevel(lvl)
    logger.info(f"Updated loglevel for {list(levels)}")
    

def test_logger(logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)
    logger.debug("this is debug")
    logger.info("this is info")
    logger.warning("this is warning")
    logger.error("this is error")

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
    return {int(key) for key, val in CONFIG["auth"].items() if val == "True"}

def get_path(section, option, fallback=sentinel):
    """ Adding pathlib.Path to get function.
    """
    val = get(section, option, fallback)
    path = Path(val).resolve()
    if not path.exists():
        raise ConfigError(f"The {path=} doesnt exists. Defined at [{section}] {option}")
    return path

def _test_config():
    load_config()
    update_loglevels()
    test_logger()
    show_config()
    # get_path("dev", "path_data")
    

if __name__ == "__main__":
    _test_config()