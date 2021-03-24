

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_cad = [
    ConfigOption(
        'CAD_LIBRARY_FUSION',
        "True",
        "Whether to attempt fusion of multiple CAD libraries. "
        "If True, will return symbols from the first library in the priority "
        "order within which a suitable candidate is found. If False, will "
        "only return symbols from the first library in the priority order."
    ),
    ConfigOption(
        'CAD_LIBRARY_PRIORITY',
        "['manual']",
        "Priority order for the CAD asset libraries."
    ),
    ConfigOption(
        'CAD_MANUAL_LIBRARY_PATH',
        "os.path.join(INSTANCE_ROOT, 'cad')",
        "The folder containing your manually created CAD data."
    ),
    ConfigOption(
        'CAD_MANUAL_MATERIALS_LIBRARY_PATH',
        "os.path.join(CAD_MANUAL_LIBRARY_PATH, 'materials')",
        "The folder containing your manually created CAD material definitions."
    ),
    ConfigOption(
        'CAD_MANUAL_PSL_LIBRARY_PATH',
        "os.path.join(CAD_MANUAL_LIBRARY_PATH, 'psl')",
        "The folder containing your manually created CAD asset references."
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_cad,
                          doc="CAD Subsystem Configuration")
