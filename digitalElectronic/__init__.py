__author__ = "a-lives"
__version__ = "1.0.0"

from . import gate,logic

__all__ = ["gate","logic","LogicExp","symbols","Gate","ANDgate","ORgate","NOTgate","XNORgate","XORgate","ANDNOTgate","ORNOTgate"]


from .logic import LogicExp,symbols
from .gate import Gate,ANDgate,ORgate,NOTgate,XNORgate,XORgate,ANDNOTgate,ORNOTgate