from modulefinder import ModuleFinder
import sys
import json
import math
from os import path, getcwd
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from threading import Event
from typing import Optional, List, Tuple, Iterable

from tactigon_gear import  __version__ as tactigon_gear_version, TSkinConfig, GestureConfig, Gesture, Hand, Angle, Touch, \
    OneFingerGesture, TwoFingerGesture
from tactigon_gear.models import TBleSelector

if sys.platform != "darwin":
    from tactigon_speech import __version__ as tactigon_speech_version, TSkin_Speech as OldTSkin, VoiceConfig as OldVoiceConfig, \
        Transcription, TSpeech, TSpeechObject, HotWord
else:
    from tactigon_gear import TSkin as OldTSkin
    tactigon_speech_version = None

BASE_PATH = getcwd()

TACTIGON_GEAR = tactigon_gear_version
TACTIGON_SPEECH = tactigon_speech_version

class TSkinOrientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class TSkinInclination(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4

@dataclass
class Wand:
    x: float
    y: float

    def toJSON(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }

@dataclass
class Position:
    angle: Angle
    orientation: TSkinOrientation
    wand: Wand
    # inclination_roll: Optional[TSkinInclination]
    # inclination_pitch: Optional[TSkinInclination]

    def toJSON(self) -> dict:
        return {
            "angle": self.angle.toJSON(),
            "orientation": self.orientation.value,
            "wand": self.wand.toJSON()
        }

if sys.platform != "darwin":
    HotWords = Tuple[HotWord, Optional[Iterable["HotWords"]]]

    @dataclass
    class TranscriptionWithPath(Transcription):
        @classmethod
        def FromTranscription(cls, transcription: Transcription):
            return TranscriptionWithPath(
                transcription.text,
                transcription.path,
                transcription.time,
                transcription.timeout
            )

        def filter_tree(self, tree: Optional[TSpeechObject]) -> Optional[TSpeechObject]:
            def f(tree: Optional[TSpeechObject], tree_path: List[HotWord]) -> Optional[TSpeechObject]:
                if not tree:
                    return

                if not tree_path:
                    return tree

                node, *rest = tree_path

                branches = [branch.children for branch in tree.t_speech if node in branch.hotwords]

                if not branches:
                    return tree

                filtered_tree, *_ = branches

                return f(filtered_tree, rest)

            return f(tree, self.path) if self.path else tree
        
        def __str__(self):
            return F"TranscriptionWithPath {self.text}, Path: {', '.join([hw.word for hw in self.path] if self.path else [])}, Time: {self.time}, Timeout: {self.timeout}"
        
    @dataclass
    class VoiceConfig(OldVoiceConfig):
        voice_commands_notification: Optional[str] = path.join("config", "audio", "trigger.wav")
        voice_commands: Optional[TSpeechObject] = None

        stop_hotword = None # type: ignore

        @classmethod
        def FromJSON(cls, json: dict):
            _t = super().FromJSON(json)
            _t.stop_hotword = None # type: ignore
            _t.voice_commands = TSpeechObject.FromJSON(json["voice_commands"]) if "voice_commands"in json and json["voice_commands"] else None
            _t.voice_commands_notification = json["voice_commands_notification"] if "voice_commands_notification" in json else None
            return _t
        
        def toJSON(self) -> dict:
            d = super().toJSON()
            d["voice_commands"] = self.voice_commands.toJSON() if self.voice_commands else None
            d["voice_commands_notification"] = self.voice_commands_notification
            return d

    class TSkin(OldTSkin):
        def __init__(self, config: TSkinConfig, voice_config: Optional[VoiceConfig], debug: bool = False):
            if voice_config is None:
                raise ValueError("Missing the configuration for the voice")
            
            OldTSkin.__init__(self, config, voice_config, debug=debug)

        @property
        def can_listen(self):
            return True

        @property
        def touch_preserve(self) -> Optional[Touch]:
            self._update_touch.acquire()
            touch = self._touch
            self._update_touch.release()
            return touch

else:
    @dataclass
    class VoiceConfig:
        @classmethod
        def FromJSON(cls, json: dict):
            return cls()
        
        def toJSON(self) -> dict:
            return {}
        
    @dataclass
    class HotWord:
        @classmethod
        def FromJSON(cls, json: dict):
            return cls()
        
        def toJSON(self) -> dict:
            return {}
        
    HotWords = Tuple[HotWord, Optional[Iterable["HotWords"]]]
        
    @dataclass
    class TSpeechObject:
        @classmethod
        def FromJSON(cls, json: dict):
            return cls()
        
        def toJSON(self) -> dict:
            return {}
        
    class TSkin(OldTSkin):
        def __init__(self, config: TSkinConfig, voice: Optional[VoiceConfig], debug: bool = False):
            OldTSkin.__init__(self, config, debug)

        @property
        def touch_preserve(self) -> Optional[Touch]:
            self._update_touch.acquire()
            touch = self._touch
            self._update_touch.release()
            return touch

@dataclass
class ModelGesture:
    gesture: str
    label: str
    description: Optional[str] = None

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            json["gesture"],
            json["label"],
            json["description"] if "description" in json and json["description"] else None
        )

    def toJSON(self) -> dict:
        return {
            "gesture": self.gesture,
            "label": self.label,
        }

@dataclass
class ModelTouch:
    gesture: OneFingerGesture
    label: str
    description: Optional[str] = None

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            OneFingerGesture(json["gesture"]),
            json["label"],
            json["description"] if "description" in json and json["description"] else None
        )
    
    def toJSON(self) -> dict:
        return {
            "gesture": self.gesture.value,
            "label": self.label
        }

@dataclass
class TSkinModel:
    name: str
    hand: Hand
    date: datetime
    gestures: List[ModelGesture]
    touchs: List[ModelTouch]

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            json["name"],
            Hand(json["hand"]),
            datetime.fromisoformat(json["date"]),
            [ModelGesture.FromJSON(g) for g in json["gestures"]],
            [ModelTouch.FromJSON(g) for g in json["touchs"]],
        )
    
    def toJSON(self):
        return {
            "name": self.name,
            "hand": self.hand.value,
            "date": self.date.isoformat(),
            "gestures": [g.toJSON() for g in self.gestures],
            "touchs": [t.toJSON() for t in self.touchs]
        }

@dataclass
class AppConfig(object):
    DEBUG: bool
    SECRET_KEY: str
    SEND_FILE_MAX_AGE_DEFAULT: int = 1
    MODELS: List[TSkinModel] = field(default_factory=list)
    TSKIN: Optional[TSkinConfig] = None
    TSKIN_VOICE: Optional[VoiceConfig] = None
    MAXIMIZED: bool = True
    FULLSCREEN: bool = False
    file_path: Optional[str] = None

    @classmethod
    def Default(cls, file_path):
        gestures = [
            ModelGesture("up", "Up"),
            ModelGesture("down", "Down"),
            ModelGesture("push", "Up"),
            ModelGesture("pull", "Up"),
            ModelGesture("twist", "Up"),
            ModelGesture("circle", "Up"),
            ModelGesture("swipe_r", "Up"),
            ModelGesture("swipe_l", "Up"),
        ]
        touchs = [
            ModelTouch(OneFingerGesture.SINGLE_TAP, "Tap"),
            ModelTouch(OneFingerGesture.TAP_AND_HOLD, "Tap and hold"),
        ]
        return cls(
            DEBUG=True,
            SECRET_KEY="change-me",
            MODELS=[
                TSkinModel("MODEL_01_L", Hand.LEFT, datetime.now(), gestures, touchs),
                TSkinModel("MODEL_01_R", Hand.RIGHT, datetime.now(), gestures, touchs),
            ],
            file_path=file_path
        )

    @classmethod
    def FromFile(cls, file_path):
        with open(file_path, "r") as config_file:
            return cls.FromJSON(json.load(config_file), file_path)

    @classmethod
    def FromJSON(cls, json: dict, file_path: str):
        return cls(
            json["DEBUG"],
            json["SECRET_KEY"],
            json["SEND_FILE_MAX_AGE_DEFAULT"],
            [TSkinModel.FromJSON(f) for f in json["MODELS"]],
            TSkinConfig.FromJSON(json["TSKIN"]) if "TSKIN" in json and json["TSKIN"] is not None else None,
            VoiceConfig.FromJSON(json["TSKIN_VOICE"]) if "TSKIN_VOICE" in json and json["TSKIN_VOICE"] is not None and sys.platform != "darwin" else None,
            json["MAXIMIZED"],
            json["FULLSCREEN"],
            file_path
            )
    
    def toJSON(self) -> object:
        return {
            "DEBUG": self.DEBUG,
            "SECRET_KEY": self.SECRET_KEY,
            "SEND_FILE_MAX_AGE_DEFAULT": self.SEND_FILE_MAX_AGE_DEFAULT,
            "MODELS": [m.toJSON() for m in self.MODELS],
            "TSKIN": self.TSKIN.toJSON() if self.TSKIN else None,
            "TSKIN_VOICE": self.TSKIN_VOICE.toJSON() if self.TSKIN_VOICE else None,
            "MAXIMIZED": self.MAXIMIZED,
            "FULLSCREEN": self.FULLSCREEN
        }
    
    def save(self):
        if self.file_path:
            with open(self.file_path, "w") as config_file:
                json.dump(self.toJSON(), config_file, indent=2)
        