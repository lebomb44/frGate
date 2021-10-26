#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import datetime

import settings
import fct


move_timeout = 0


def run():
    """
        Cyclic execution to update light
    """
    global move_timeout
    try:
        if settings.move_is_enabled is True:

    except Exception as ex:
        fct.log_exception(ex)
