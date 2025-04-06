from abc import ABC, abstractmethod
import typing as t
import warnings

import manim
from manim import VGroup,VMobject,Rectangle,Square,Circle,Triangle
from manim import LEFT,RIGHT,UP,DOWN,UL,DL,UR,DR,ORIGIN
import manim.utils.color as C

from .logic import LogicExp, Operator

# 用来可视化的网格图
class Graph(VGroup):
    def __init__(self,shape:t.Iterable[int]):
        super().__init__()
        


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


# TODO 实现可视化
class Device(ABC):
    def __init__(self):
        super().__init__()
        self.inputs = None
        self.outputs = None
        
    @property
    def input_ports(self) -> int:
        raise NotImplementedError("Deivce property input_ports has no implement")

    @property
    def output_ports(self) -> int:
        raise NotImplementedError("Deivce property output_ports has no implement")
        
    def __call__(self, *args, **kwargs):
        self.inputs = args,kwargs
        self.outputs = self.forward(*args,**kwargs)
        if isinstance(self.outputs,LogicExp):
            self.outputs.port = self
        else:
            # NOTE 本来想令端口支持各种东西，但想想还是算了，纯数字吧
            for port,output in enumerate(self.outputs):
                output.port = (self,port)   # 为输出添加对应端口
        return self.outputs
    
    def visualize(self,) -> t.Union[VMobject,VGroup]:
        raise NotImplementedError("Deivce method visualize has no implement")
    
    @classmethod
    def build(cls,num:int,*args,**kwds):
        assert num > 0
        return [cls(*args,**kwds) for _ in range(num)]

    @abstractmethod
    def forward(self,*args,**kwargs):
        pass



class Gate(Device):
    def __init__(self):
        super().__init__()
        
    @property
    def input_ports(self):
        return len(self.inputs) if self.inputs and not isinstance(self.inputs,LogicExp) else 0
    
    @property
    def output_ports(self):
        return len(self.outputs) if self.outputs and not isinstance(self.outputs,LogicExp) else 0

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
    
    def visualize(self,color:C.ManimColor=C.BLUE_C,scale:float=1) -> VMobject:
        rect = Rectangle(width=1.6,height=2,color=color).move_to(ORIGIN)
        circle = Circle(radius=1,color=color).move_to(ORIGIN)
        circle.shift(RIGHT*0.8)
        obj = manim.Union(rect,circle,color=color)
        return obj.scale(scale)


# 或门
class ORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.OR
    
    def visualize(self,color:C.ManimColor=C.BLUE_C,scale:float=1) -> VMobject:
        # rect = Square(side_length=2,color=color)
        circle1 = Circle(radius=2,color=color)
        circle2 = Circle(radius=2,color=color)
        circle3 = Circle(radius=2.5,color=color)
        circle1.shift(DL)
        circle2.shift(UL)
        circle3.shift(LEFT*4)
        obj1 = manim.Intersection(circle1,circle2)
        obj2 = manim.Difference(obj1,circle3,color=color).shift(RIGHT)
        return obj2.scale(scale)


# 非门
class NOTgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.NOT

    def visualize(self,color:C.ManimColor=C.BLUE_C,scale:float=1) -> VMobject:
        tri = Triangle().rotate(30*manim.DEGREES)
        circle = Circle(radius=0.1,color=color)
        circle.move_to(tri.get_right())
        circle.shift(RIGHT*0.1)
        obj = VGroup(tri,circle)
        return obj.scale(scale)

# TODO 完成其它器件可视化

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