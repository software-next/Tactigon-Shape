from functools import wraps
from flask import current_app

from .extension import SocketApp

def get_socket_app() -> SocketApp:
    return current_app.extensions[SocketApp.name]