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
        self.vars = vars  # 变量
        self.op = op  # 操作符
        self.name = None  # 名称
        self.value = None  # 值
        self.port: t.Tuple["Device", int] = (
            None  # 设备以及端口号，如果该表达式从device中出来
        )
        # 简单整理式子
        if not self.op in (Operator.NOT, None):
            newvars = []
            for var in vars:
                if var.op is self.op and var.port is None:      # 防止化简破环端口映射
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
                    if var.op in (Operator.AND, Operator.NOT, None)
                    else "(" + str(var) + ")"
                )
                for var in self.vars
            )

    def __hash__(self):
        return hash(self.__str__())

    def is_(self, other: LogicType) -> bool:
        return hash(self) == hash(other)

    def in_(self, others: tuple) -> bool:
        return bool(sum(self.is_(other) for other in others))

    def simplify(self) -> "LogicExp":
        # TODO 实现化简
        pass

    def subs(self, table: dict[LogicType, bool]) -> bool:
        if self.in_(table.keys()):
            assert not self.name is None
            return table[self]
        elif not self.value is None:
            return self.value
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
        elif self.op is Operator.XNOR:
            result = self.vars[0]
            for var in self.vars[1:]:
                result = not (result ^ var.subs(table))
            return result
        else:
            # TODO 问题处理
            return None

    # 获取真值表
    def get_truth_table(
        self, vars: t.Tuple[LogicType], output_name="Y"
    ) -> pd.DataFrame:
        dic = {var.name: [] for var in vars}
        dic[output_name] = []
        for i in range(2 ** len(vars)):
            for j in range(len(vars)):
                dic[vars[j].name].append((i >> j) % 2)
            dic[output_name].append(
                int(self.subs({vars[j]: (i >> j) % 2 for j in range(len(vars))}))
            )
        df = pd.DataFrame(dic)
        return df

    # 获取最小项
    def minterms(self, vars: t.Tuple[LogicType]) -> t.Tuple["LogicExp"]:
        truth_table = self.get_truth_table(vars)
        minterms = []
        for i in range(2 ** len(vars)):
            if truth_table["Y"][i]:
                temp_vars = []
                for var in vars:
                    if truth_table.loc[i, var.name]:
                        temp_vars.append(var)
                    else:
                        temp_vars.append(LogicExp(var, op=Operator.NOT))
                minterms.append(LogicExp(*temp_vars, op=Operator.AND))
        return tuple(minterms)


# 逻辑变量
class LogicVar(LogicExp):
    def __init__(self, name: str, value: bool = None):
        super().__init__(op=None)
        assert not name is None
        self.name = name
        self.value = value

    def __str__(self):
        return self.name


ONE = LogicVar("1", True)
ZERO = LogicVar("0", False)


# 获取逻辑变量
def symbols(names: str) -> t.Tuple[LogicVar]:
    results = []
    for name in names.split(" "):
        results.append(LogicVar(name))
    return tuple(results)
