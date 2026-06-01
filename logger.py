# SCHICHT: Infrastruktur — Logging

from datetime import datetime


def log(msg):
    print("[" + str(datetime.now()) + "] " + msg)


def log_error(msg):
    print("[" + str(datetime.now()) + "] ERROR: " + msg)


def log_warning(msg):
    print("[" + str(datetime.now()) + "] WARN: " + msg)


def log_info(msg):
    print("[" + str(datetime.now()) + "] INFO: " + msg)


def log_debug(msg):
    print("[" + str(datetime.now()) + "] DEBUG: " + msg)


def log_trace(msg):
    print("[" + str(datetime.now()) + "] TRACE: " + msg)
