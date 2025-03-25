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
        # 简单整理式子
        if not self.op in (Operator.NOT,None):
            newvars = []
            for var in vars:
                if var.op is self.op:
                    newvars.extend(var.vars)
                else:
                    newvars.append(var)
            self.vars = tuple(newvars)
        
    def __and__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.AND)
    
    def __rand__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only and with another LogicExp or LogicVar!"
            )
        return LogicExp(other,self, op=Operator.AND)
    
    def __or__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.OR)
    
    def __ror__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only or with another LogicExp or LogicVar!"
            )
        return LogicExp(other,self , op=Operator.OR)

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
    
    def __xor__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xor with another LogicExp or LogicVar!"
            )
        return LogicExp(self,other, op=Operator.XOR)
    
    def __rxor__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xor with another LogicExp or LogicVar!"
            )
        return LogicExp(other,self, op=Operator.XOR)

    def and_(self, other: LogicType) -> "LogicExp":
        return self.__mul__(other)

    def or_(self, other: LogicType) -> "LogicExp":
        return self.__add__(other)

    def xor(self, other: LogicType) -> "LogicExp":
        return self.__xor__(other)

    def xnor(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xnor with another LogicExp or LogicVar!"
            )
        return LogicExp(self, other, op=Operator.XNOR)
    
    def __invert__(self) -> "LogicExp":
        return LogicExp(self, op=Operator.NOT)

    def __str__(self) -> str:
        if self.op is Operator.AND:
            return self.op.value.join(str(var) for var in self.vars)
        elif self.op is Operator.NOT:
            if self.vars[0].op is None:
                return str(self.vars[0]) + "'"
            else:
                return "(" + str(self.vars[0]) + ")'"
        else:
            return "(" + self.op.value.join(str(var) for var in self.vars) + ")"

    def simplify(self) -> "LogicExp":
        # TODO implement
        pass


class LogicVar(LogicExp):
    def __init__(self, name: str, value: bool = None):
        super().__init__(op=None)
        assert not name is None
        self.name = name
        self.value = value

    def __str__(self):
        return self.name


def symbols(names: str) -> t.Tuple[LogicVar]:
    results = []
    for name in names.split(" "):
        results.append(LogicVar(name))
    return tuple(results)
