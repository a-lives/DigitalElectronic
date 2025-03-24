from abc import ABC, abstractmethod
from enum import StrEnum
import typing as t

LogicType: t.TypeAlias = t.Union["LogicExp", "LogicVar"]


class Operator(StrEnum):
    AND = ""
    OR = "+"
    XOR = "^"
    XNOR = "."
    NOT = "'"



# TODO not
class LogicExp:
    def __init__(self, *vars: LogicType, op: Operator):
        self.vars = vars
        self.op = op

    def __add__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return self.__class__(self, other, op=Operator.OR)

    def __radd__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return self.__class__(other, self, op=Operator.OR)

    def __mul__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return self.__class__(self, other, op=Operator.AND)

    def __rmul__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return self.__class__(other, self, op=Operator.AND)

    def and_(self, other: LogicType) -> "LogicExp":
        return self.__mul__(other)

    def or_(self, other: LogicType) -> "LogicExp":
        return self.__add__(other)

    def xor(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only xor with another LogicExp or LogicVar!"
            )
        return self.__class__(self, other, op=Operator.XOR)

    def xnor(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, self.__class__):
            raise NotImplementedError(
                "LogicExp can only xnor with another LogicExp or LogicVar!"
            )
        return self.__class__(self, other, op=Operator.XNOR)

    def __str__(self) -> str:
        if self.op is Operator.AND:
            return self.op.value.join(str(var) for var in self.vars)
        else:
            return "(" + self.op.value.join(str(var) for var in self.vars) + ")"

    def simplify(self) -> "LogicExp":
        # TODO implement
        pass


class LogicVar(LogicExp):
    def __init__(self, name: str, value: bool = None):
        assert not name is None
        self.name = name
        self.value = value

    def __add__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.OR)

    def __radd__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return LogicExp(other, self, op=Operator.OR)

    def __mul__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.AND)

    def __rmul__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return LogicExp(other, self, op=Operator.AND)

    def and_(self, other: LogicType) -> "LogicExp":
        return self.__mul__(other)

    def or_(self, other: LogicType) -> "LogicExp":
        return self.__add__(other)

    def xor(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xor with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.XOR)

    def xnor(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xnor with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.XNOR)

    def __str__(self):
        return self.name


def symbols(names: str) -> t.Tuple[LogicVar]:
    results = []
    for name in names.split(" "):
        results.append(LogicVar(name))
    return tuple(results)


class LogicMap:
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        pass
