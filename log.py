import logging


def initialize_log():
    """ Log """
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler("transporte_sp.log")
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    return log


logger = initialize_log()
