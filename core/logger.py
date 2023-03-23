import logging


def create_logger():
    logger = logging.getLogger('qristo')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to Info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create file handler and set level to Error
    fh = logging.FileHandler('logs\qristo.log')
    fh.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger