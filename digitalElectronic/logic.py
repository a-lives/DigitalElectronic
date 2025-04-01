from abc import ABC, abstractmethod
from enum import StrEnum
import typing as t
import pandas as pd

LogicType: t.TypeAlias = t.Union["LogicExp", "LogicVar"]


class Operator(StrEnum):
    AND = ""
    OR = "+"
    XOR = "^"
    XNOR = "."
    NOT = "'"


# TODO 添加对 1 0 True False 等的运算支持
class LogicExp:
    def __init__(self, *vars: LogicType, op: Operator):
        self.vars = vars
        self.op = op
        # 简单整理式子
        if not self.op in (Operator.NOT, None):
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
        return LogicExp(other, self, op=Operator.AND)

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
        return LogicExp(other, self, op=Operator.OR)

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
        return LogicExp(self, other, op=Operator.XOR)

    def __rxor__(self, other: LogicType) -> "LogicExp":
        if not isinstance(other, LogicExp):
            raise NotImplementedError(
                "LogicExp can only xor with another LogicExp or LogicVar!"
            )
        return LogicExp(other, self, op=Operator.XOR)

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
        # if self.op is Operator.AND:
        #     return self.op.value.join(str(var) for var in self.vars)
        if self.op is Operator.NOT:
            if self.vars[0].op is None:
                return str(self.vars[0]) + "'"
            else:
                return "(" + str(self.vars[0]) + ")'"
        else:
            return self.op.value.join(
                (
                    str(var)
                    if var.op in (Operator.AND,Operator.NOT,None)
                    else "(" + str(var) + ")"
                )
                for var in self.vars
            )

    def simplify(self) -> "LogicExp":
        # TODO 实现化简
        pass

    def subs(self,table:dict["LogicVar",bool]) -> bool:
        if self.op is None:
            return table[self]
        elif self.op is Operator.AND:
            result = 1
            for var in self.vars:
                result = result and var.subs(table)
            return result
        elif self.op is Operator.OR:
            result = 0
            for var in self.vars:
                result = result or var.subs(table)
            return result
        elif self.op is Operator.NOT:
            return not self.vars[0].subs(table)
        elif self.op is Operator.XOR:
            result = self.vars[0]
            for var in self.vars[1:]:
                result = result ^ var.subs(table)
            return result
        else:
            result = self.vars[0]
            for var in self.vars[1:]:
                result = not (result ^ var.subs(table))
            return result
        
    def get_truth_table(self,vars:t.Tuple["LogicVar"],output_name="Y") -> pd.DataFrame:
        dic = {var.name : [] for var in vars}
        dic[output_name] = []
        for i in range(2**len(vars)):
            for j in range(len(vars)):
                dic[vars[j].name].append((i>>j)%2)
            dic[output_name].append(int(self.subs({vars[j]:(i>>j)%2 for j in range(len(vars))})))
        df = pd.DataFrame(dic)
        return df
        
        

class LogicVar(LogicExp):
    def __init__(self, name: str, value: bool = None):
        super().__init__(op=None)
        assert not name is None
        self.name = name
        self.value = value

    def __str__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)


ONE = LogicVar("1", True)
ZERO = LogicVar("0", False)


def symbols(names: str) -> t.Tuple[LogicVar]:
    results = []
    for name in names.split(" "):
        results.append(LogicVar(name))
    return tuple(results)
