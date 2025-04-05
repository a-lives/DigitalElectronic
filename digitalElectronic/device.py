from abc import ABC, abstractmethod
import typing as t
import warnings
from .logic import LogicExp, Operator

# 用来可视化的节点
class Node:
    pass


# 用来可视化的网格图
class Graph:
    pass


""" 
可视化思路：
网格存放每个点上的内容，方便判断
提供注册与删除注册方法
网格包含原件表，原件表内包含注册节点信息

布线规则：
走线只能纵横
线距限制
吸附网格

元件分布规则：
从输入到输出按层级分
可以建立群组，影响排序

"""

# TODO 实现重建图功能，目前建图不可更改


class Device(ABC,Node):
    def __init__(self):
        super().__init__()
        self.inputs = None
        
    def __call__(self, *args, **kwargs):
        self.inputs = args,kwargs
        return self.forward(*args,**kwargs)
    
    # 输出
    @property
    def output(self):
        return self.forward(*self.inputs[0],**self.inputs[1])
    
    @classmethod
    def build(cls,num:int,*args,**kwds):
        assert num > 0
        return [cls(*args,**kwds) for _ in range(num)]

    @abstractmethod
    def forward(self, *x: LogicExp):
        raise NotImplementedError("Deivce method has no implement")

class Gate(Device):
    def __init__(self):
        super().__init__()

    # 操作符
    @property
    @abstractmethod
    def op(self):
        raise NotImplementedError("gate property operator has not implement!")

    def forward(self, *x: LogicExp) -> LogicExp:
        return LogicExp(*x, op=self.op)


# 与门
class ANDgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.AND


# 或门
class ORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.OR


# 非门
class NOTgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.NOT


# 异或门
class XORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.XOR


# 同或门
class XNORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.XNOR

# 与非门
class ANDNOTgate(Gate):
    def __init__(self):
        super().__init__()
        
    @property
    def op(self):
        return Operator.NOT
    
    def forward(self, *x):
        return LogicExp(LogicExp(*x,op=Operator.AND),op=self.op)
   
# 或非门 
class ORNOTgate(Gate):
    def __init__(self):
        super().__init__()
        
    @property
    def op(self):
        return Operator.NOT 
    
    def forward(self, *x):
        return LogicExp(LogicExp(*x,op=Operator.OR),op=self.op)
    
    
# 传输门
class TransmissionGate(Device):
    # ouput = x*c + x*~c0
    def __init__(self):
        super().__init__()
        
    def forward(self,x:LogicExp,c:LogicExp,c0:LogicExp):
        if not (~c).is_(c0) or (c).is_(~c0):
            warnings.warn("The two control ends c and c0 of the transmission gate should be opposite")
        return x*c + x*~c0