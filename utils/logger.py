# -*- coding: utf-8 -*-

import logging


def log():
    logging.basicConfig(
        format='[%(threadName)s][%(module)s][%(levelname)s] %(message)s',
        level=logging.WARNING
    )
    logging.getLogger(__name__).setLevel(logging.DEBUG)

    return logging.getLogger(__name__)
