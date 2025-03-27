from enum import Enum
from dataclasses import dataclass

from typing import Optional, Any

class Scope(Enum):
    SERVER = "SERVER_SCOPE"
    CLIENT = "CLIENT_SCOPE"
    SHARED = "SHARED_SCOPE"

class AlarmSearchStatus(Enum):
    ACK = "ACK"
    ACTIVE = "ACTIVE"
    ANY = "ANY"
    CLEARED = "CLEARED"
    UNACK = "UNACK"

class AlarmSeverity(Enum):
    ANY = ""
    CRITICAL = "CRITICAL"

@dataclass
class Device:
    id: str
    name: str

@dataclass
class ZionConfig:
    username: str
    password: str
    url: str = "https://zion.nextind.eu/"
    token: Optional[str] = None

    @classmethod
    def Default(cls):
        return cls(
            "",
            "",
            ZionConfig.url
        )

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(
            json["username"],
            json["password"],
            json["url"] if "url" in json and json["url"] else cls.url
        )
    
    def toJSON(self) -> object:
        return {
            "username": self.username,
            "password": self.password,
            "url": self.url
        }