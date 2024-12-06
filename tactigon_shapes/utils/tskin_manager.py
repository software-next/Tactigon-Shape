from flask import current_app
from typing import Optional, Union

from ..models import TSkin, TSkinConfig, VoiceConfig, Hand

TSKIN_EXTENSION = "tskin"

def load_tskin(config: TSkinConfig, voice: Optional[VoiceConfig]):
    current_app.extensions[TSKIN_EXTENSION] = TSkin(config, voice)

def start_tskin():
    tskin = get_tskin()

    if tskin:
        tskin.start()
        return tskin

def stop_tskin():
    tskin = get_tskin()

    if tskin:
        tskin.join(1.0)

    reset_tskin()

def get_tskin() -> Optional[TSkin]:
    if TSKIN_EXTENSION in current_app.extensions:
        if isinstance(current_app.extensions[TSKIN_EXTENSION], TSkin):
            return current_app.extensions[TSKIN_EXTENSION]

    return None

def reset_tskin():
    current_app.extensions[TSKIN_EXTENSION] = None