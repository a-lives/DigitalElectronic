__author__ = "a-lives"
__version__ = "1.0.0"

from . import device, logic

__all__ = [
    "device",
    "logic",
    "LogicExp",
    "symbols",
    "Device",
    "Gate",
    "ANDgate",
    "ORgate",
    "NOTgate",
    "XNORgate",
    "XORgate",
    "ANDNOTgate",
    "ORNOTgate",
    "TransmissionGate",
]


from .logic import LogicExp, symbols
from .device import (
    Device,
    Gate,
    ANDgate,
    ORgate,
    NOTgate,
    XNORgate,
    XORgate,
    ANDNOTgate,
    ORNOTgate,
    TransmissionGate,
)
