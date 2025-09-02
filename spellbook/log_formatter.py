##############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other
# Merlin-Spellbook Project developers. See top-level LICENSE and COPYRIGHT
# files for dates and other details. No copyright assignment is required to
# contribute to Merlin-Spellbook.
##############################################################################


import logging
import sys

import coloredlogs


FORMATS = {
    "DEFAULT": "[%(asctime)s: %(levelname)s] %(message)s",
    "DEBUG": "[%(asctime)s: %(levelname)s] [%(module)s: %(lineno)d] %(message)s",
}


def setup_logging(logger, log_level="INFO", colors=True):
    """
    Setup and configure Python logging.

    :param `logger`: a logging.Logger object
    :param  `log_level`: logger level
    """
    formatter = logging.Formatter()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(log_level)
    logger.propagate = False

    if colors is True:
        coloredlogs.install(level=log_level, logger=logger, fmt=FORMATS["DEFAULT"])
