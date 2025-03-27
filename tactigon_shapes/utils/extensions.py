from flask import current_app

from typing import Optional

from ..modules.socketio import SocketApp
from ..modules.braccio.extension import BraccioInterface
from ..modules.zion.extension import ZionInterface
from ..modules.tskin.manager import TSKIN_EXTENSION

excluded_apps = [SocketApp.name, TSKIN_EXTENSION, "socketio", BraccioInterface.__name__, ZionInterface.__name__]

def stop_apps(exclude: Optional[str] = None):
    l = excluded_apps
    if (exclude):
        l.append(exclude)

    for ext in current_app.extensions:
        if ext in l:
            continue
        current_app.extensions[ext].stop()