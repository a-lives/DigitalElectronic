from abc import ABC, abstractmethod
import typing as t
import warnings

import numpy as np
import manim
from manim import (
    VGroup,
    VMobject,
    Rectangle,
    Square,
    Circle,
    Triangle,
    Arc,
    Text,
    Tex,
    MathTex,
)
from manim import LEFT, RIGHT, UP, DOWN, UL, DL, UR, DR, ORIGIN
import manim.utils.color as C

from .logic import LogicExp, LogicVar, Operator, symbols


# 用来可视化的网格图
class Graph(VGroup):
    def __init__(self, shape: t.Iterable[int]):
        super().__init__()


""" 
可视化思路：
网格存放每个点上的内容，方便判断
提供注册与删除注册方法
网格包含原件表，原件表内包含注册节点信息

走线规则：
走线只能纵横
线距限制
吸附网格
不能穿过器件

自动走线：
建立打分机制，通过贪心算法与广度优先搜索结合寻找解

元件分布规则：
从输入到输出按层级分
可以建立群组，影响排序

"""


# TODO 实现端口映射
# TODO 实现文本标记添加
class Device(ABC):
    def __init__(self):
        super().__init__()
        self.inputs = None
        self.outputs = None

    # TODO 端口输入输出序号合并
    @property
    def input_ports(self) -> int:
        raise NotImplementedError("Deivce property input_ports has no implement")

    @property
    def output_ports(self) -> int:
        raise NotImplementedError("Deivce property output_ports has no implement")

    def __call__(self, *args, **kwargs):
        self.inputs = args, kwargs
        self.outputs = self.forward(*args, **kwargs)
        if isinstance(self.outputs, LogicExp):
            self.outputs.port = self
        else:
            # NOTE 本来想令端口支持各种东西，但想想还是算了，纯数字吧
            for port, output in enumerate(self.outputs):
                output.port = (self, port)  # 为输出添加对应端口
        return self.outputs

    # 返回一个manim的可视化对象
    def visualize(
        self,
    ) -> t.Union[VMobject, VGroup]:
        raise NotImplementedError("Deivce method visualize has no implement")

    # 通过端口号获取相对器件中心点的端口位置，方便接线
    def input_port_to_pos(self) -> manim.Vector:
        raise NotImplementedError("Deivce method input_port_to_pos has no implement")

    # 通过端口号获取相对器件中心点的端口位置，方便接线
    def output_port_to_pos(self) -> manim.Vector:
        raise NotImplementedError("Deivce method output_port_to_pos has no implement")

    @classmethod
    def build(cls, num: int, *args, **kwds):
        assert num > 0
        return [cls(*args, **kwds) for _ in range(num)]

    @abstractmethod
    def forward(self, *args, **kwargs):
        pass

    def sample_wave(self, *inputs: t.Callable) -> t.Tuple[t.Sequence[float]]:
        raise NotImplementedError("Deivce method draw_wave has no implement")


class Gate(Device):
    def __init__(self):
        super().__init__()

    @property
    def input_ports(self):
        return (
            len(self.inputs)
            if self.inputs and not isinstance(self.inputs, LogicExp)
            else 0
        )

    @property
    def output_ports(self):
        return (
            len(self.outputs)
            if self.outputs and not isinstance(self.outputs, LogicExp)
            else 0
        )

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

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VMobject:
        rect = Rectangle(width=1.6, height=2, color=color).move_to(ORIGIN)
        circle = Circle(radius=1, color=color).move_to(ORIGIN)
        circle.shift(RIGHT * 0.8)
        obj = manim.Union(rect, circle, color=color)
        return obj.scale(scale)


# 或门
class ORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.OR

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VMobject:
        # rect = Square(side_length=2,color=color)
        circle1 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle2 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle3 = Circle(radius=2.5, color=color).move_to(ORIGIN)
        circle1.shift(DL)
        circle2.shift(UL)
        circle3.shift(LEFT * 4)
        obj1 = manim.Intersection(circle1, circle2)
        obj2 = manim.Difference(obj1, circle3, color=color).shift(RIGHT)
        return obj2.scale(scale)


# 非门
class NOTgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.NOT

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VGroup:
        tri = Triangle().rotate(30 * manim.DEGREES).move_to(ORIGIN)
        circle = Circle(radius=0.1, color=color)
        circle.move_to(tri.get_right())
        circle.shift(RIGHT * 0.1)
        obj = VGroup(tri, circle)
        return obj.scale(scale)


# 异或门
class XORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.XOR

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VGroup:
        # rect = Square(side_length=2,color=color)
        circle1 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle2 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle3 = Circle(radius=2.5, color=color).move_to(ORIGIN)
        arc = Arc(
            radius=2.5, start_angle=-0.363, angle=2 * 0.363, color=color
        )  # 0.363 硬算的
        circle1.shift(DL)
        circle2.shift(UL)
        circle3.shift(LEFT * 4)
        arc.shift(LEFT * 4.2)
        obj1 = manim.Intersection(circle1, circle2)
        obj2 = manim.Difference(obj1, circle3, color=color)
        obj3 = VGroup(arc, obj2).shift(RIGHT)
        return obj3.scale(scale)


# 同或门
class XNORgate(Gate):
    def __init__(self):
        super().__init__()

    @property
    def op(self):
        return Operator.XNOR

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VGroup:
        # rect = Square(side_length=2,color=color)
        circle1 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle2 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle3 = Circle(radius=2.5, color=color).move_to(ORIGIN)
        circle4 = Circle(radius=0.1, color=color).move_to(ORIGIN)
        arc = Arc(
            radius=2.5, start_angle=-0.363, angle=2 * 0.363, color=color
        )  # 0.363 硬算的
        circle1.shift(DL)
        circle2.shift(UL)
        circle3.shift(LEFT * 4)
        arc.shift(LEFT * 4.2)
        circle4.shift(RIGHT * 0.832)  # 1.732 - 1 + 0.1 = 0.832
        obj1 = manim.Intersection(circle1, circle2)
        obj2 = manim.Difference(obj1, circle3, color=color)
        obj3 = VGroup(arc, obj2, circle4).shift(RIGHT)
        return obj3.scale(scale)


# 与非门
class ANDNOTgate(Device):
    def __init__(self):
        super().__init__()

    def forward(self, *x):
        return ~LogicExp(*x, op=Operator.AND)

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VGroup:
        rect = Rectangle(width=1.6, height=2, color=color).move_to(ORIGIN)
        circle = Circle(radius=1, color=color).move_to(ORIGIN)
        circle0 = Circle(radius=0.1, color=color).move_to(ORIGIN)
        circle.shift(RIGHT * 0.8)
        circle0.shift(RIGHT * 1.9)
        obj = manim.Union(rect, circle, color=color)
        obj2 = VGroup(obj, circle0)
        return obj2.scale(scale)


# 或非门
class ORNOTgate(Device):
    def __init__(self):
        super().__init__()

    def forward(self, *x):
        return ~LogicExp(*x, op=Operator.OR)

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VGroup:
        # rect = Square(side_length=2,color=color)
        circle1 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle2 = Circle(radius=2, color=color).move_to(ORIGIN)
        circle3 = Circle(radius=2.5, color=color).move_to(ORIGIN)
        circle0 = Circle(radius=0.1, color=color).move_to(ORIGIN)
        circle1.shift(DL)
        circle2.shift(UL)
        circle3.shift(LEFT * 4)
        circle0.shift(RIGHT * 0.832)  # 1.732 - 1 + 0.1 = 0.832
        obj1 = manim.Intersection(circle1, circle2)
        obj2 = manim.Difference(obj1, circle3, color=color)
        obj3 = VGroup(obj2, circle0).shift(RIGHT)
        return obj3.scale(scale)


class SimpleNOTGate(Device):
    def __init__(self, work: bool = False):
        super().__init__()
        self.work = work  # 起标记作用时不工作

    def __call__(self, x):
        self.inputs = x
        self.outputs = self.forward(x)
        self.outputs.port = self.inputs.port  # 简单小圈圈非门不改变port
        return self.outputs

    def forward(self, x):
        return ~x if self.work else x

    def visualize(self, color: C.ManimColor = C.BLUE_C, scale: float = 1) -> VMobject:
        circle = Circle(radius=0.1, color=color)
        return circle.scale(scale)


# 传输门
class TransmissionGate(Device):
    order = 0  # 器件编号

    def __init__(self, order: int = None):
        super().__init__()
        self.order = order if order else TransmissionGate.order
        TransmissionGate.order = self.order + 1

    def forward(self, x: LogicExp, c: LogicExp, c0: LogicExp):
        if not (~c).is_(c0) or (c).is_(~c0):
            warnings.warn(
                "The two control ends c and c0 of the transmission gate should be opposite"
            )
        return x * c + x * ~c0

    def visualize(self, color: C.ManimColor = C.WHITE, scale: float = 1) -> VGroup:
        rect = Rectangle(width=2.4, height=2, color=color).move_to(ORIGIN)
        circle = Circle(radius=0.1, color=color).move_to(ORIGIN)
        text = MathTex(f"TG_{self.order}").move_to(rect.get_center())
        circle.shift(UP * 1.1)
        return VGroup(rect, circle, text).scale(scale)


# TODO 对方形芯片的基类进行实现
# 要方便实现引脚名称标记，低电平有效标记
class Chip(Device):
    # 各种方形芯片的基类
    def __init__(self):
        super().__init__()


# TODO 完善时序逻辑电路

class SDevice(Device):
    def __init__(self):
        super().__init__()

    @property
    def states(self) -> t.Tuple[LogicVar]:
        raise NotImplementedError()

    def state_exps(self, *inputs: LogicExp) -> t.Tuple[LogicExp]:
        raise NotImplementedError()

    def update(self, table: t.Dict[LogicExp, bool]):
        for state, value in table.items():
            state.value = value


class SRLatch(SDevice):
    # 或非门SR锁存器
    order = 0

    def __init__(self, order: int = None, Q_value: bool = False, Qi_value=True):
        super().__init__()
        self.order = order if order else SRLatch.order
        SRLatch.order = self.order + 1
        self.q = LogicVar(f"[SRLatch{self.order}]Q", value=Q_value)
        self.qi = LogicVar(f"[SRLatch{self.order}]Q'", value=Qi_value)

    @property
    def states(self):
        return self.q, self.qi

    def state_exps(self, s: LogicExp, r: LogicExp):
        return ~(r + self.qi), ~(s + self.q)

    def forward(self, s: LogicExp, r: LogicExp):
        return ~(r + self.qi), ~(s + self.q)


class SRLatch_AN(SDevice):
    # 与非门SR锁存器
    order = 0

    def __init__(self, order: int = None, Q_value: bool = False, Qi_value=True):
        super().__init__()
        self.order = order if order else SRLatch_AN.order
        SRLatch_AN.order = self.order + 1
        self.q = LogicVar(f"[SRLatch_AN{self.order}]Q", value=Q_value)
        self.qi = LogicVar(f"[SRLatch_AN{self.order}]Q'", value=Qi_value)

    @property
    def states(self):
        return self.q, self.qi

    def state_exps(self, s: LogicExp, r: LogicExp):
        return ~(s * self.qi), ~(r * self.q)

    def forward(self, s: LogicExp, r: LogicExp):
        return ~(s * self.qi), ~(r * self.q)


class SRFF(SDevice):
    # 与非门SR触发器
    order = 0

    def __init__(self, order: int = None, Q_value: bool = False, Qi_value=True):
        super().__init__()
        self.order = order if order else SRFF.order
        SRFF.order = self.order + 1
        self.q = LogicVar(f"[SRFF{self.order}]Q", value=Q_value)
        self.qi = LogicVar(f"[SRFF{self.order}]Q'", value=Qi_value)

    @property
    def states(self):
        return self.q, self.qi

    def state_exps(self, s: LogicExp, r: LogicExp, clk: LogicExp):
        return ~((~(s * clk)) * self.qi), ~((~(r * clk)) * self.q)

    def forward(self, s: LogicExp, r: LogicExp, clk: LogicExp):
        return ~((~(s * clk)) * self.qi), ~((~(r * clk)) * self.q)


class SRFF_P(SDevice):
    # 与非门SR脉冲触发器
    order = 0

    def __init__(self, order: int = None, Q_value: bool = False, Qi_value=True):
        super().__init__()
        self.order = order if order else SRFF_P.order
        SRFF_P.order = self.order + 1
        self.SRFF1 = SRFF()
        self.SRFF2 = SRFF(Q_value=Q_value, Qi_value=Qi_value)

    @property
    def states(self):
        return self.q, self.qi

    def state_exps(
        self,
        s: LogicExp,
        r: LogicExp,
        clk: LogicExp,
    ):
        Q1, Q1i = self.SRFF1(s, r, clk)
        Q2, Q2i = self.SRFF2(Q1, Q1i, ~clk)
        return Q1, Q1i, Q2, Q2i

    def forward(self, s: LogicExp, r: LogicExp, clk: LogicExp):
        Q1, Q1i = self.SRFF1(s, r, clk)
        Q2, Q2i = self.SRFF1(Q1, Q1i, ~clk)
        return Q2, Q2i


class JKFF(SDevice):
    order = 0

    def __init__(self, order: int = None):
        super().__init__()
        self.order = order if order else JKFF.order
        JKFF.order = self.order + 1
        self.SRFF1 = SRFF()
        self.SRFF2 = SRFF()

    @property
    def states(self):
        return *self.SRFF1.states, *self.SRFF2.states

    def state_exps(
        self,
        j: LogicExp,
        k: LogicExp,
        clk: LogicExp,
    ):
        Q1, Q1i = self.SRFF1(j * self.SRFF2.qi, k * self.SRFF2.q, clk)
        Q2, Q2i = self.SRFF2(Q1, Q1i, ~clk)
        return Q1, Q1i, Q2, Q2i

    def forward(
        self,
        j: LogicExp,
        k: LogicExp,
        clk: LogicExp,
    ):
        Q1, Q1i = self.SRFF1(j * self.SRFF2.qi, k * self.SRFF2.q, clk)
        Q2, Q2i = self.SRFF2(Q1, Q1i, ~clk)
        return Q2, Q2i

    @classmethod
    def sample_wave(
        cls,
        t_range,
        j: t.Callable[[float], bool],
        k: t.Callable[[float], bool],
        clk: t.Callable[[float], bool],
    ):
        J, K, CLK = symbols("J K CLK")
        x = np.arange(*t_range).tolist()
        outputs = sample_wave_seq(cls, x, {J: j, K: k, CLK: clk})
        return x, *outputs


def sample_wave(
    device_type: type[Device],
    time_seq: t.Sequence[float],
    table: t.Dict[LogicExp, t.Callable[[float], bool]],
) -> t.List[t.List[bool]]:
    syms = table.keys()
    device = device_type()
    outputs: t.Tuple[LogicExp] = device(*syms)
    output_box = [[] for i in range(len(outputs))]
    for t_ in time_seq:
        inputs = {sym: func(t_) for sym, func in table.items()}
        for i, output in enumerate(outputs):
            output_box[i].append(output.subs(inputs))
    return output_box


def sample_wave_seq(
    device_type: type[SDevice],
    time_seq: t.Sequence[float],
    table: t.Dict[LogicExp, t.Callable[[float], bool]],
) -> t.List[t.List[bool]]:
    syms = table.keys()
    device = device_type()
    outputs: t.Tuple[LogicExp] = device(*syms)
    output_box = [[] for _ in range(len(outputs))]
    for t_ in time_seq:
        # 输出
        inputs = {sym: func(t_) for sym, func in table.items()}
        for i, output in enumerate(outputs):
            output_box[i].append(output.subs(inputs))

        # 状态
        state_values = [state.subs(inputs) for state in device.state_exps(*syms)]
        device.update(
            {state: value for state, value in zip(device.states, state_values)}
        )
    return output_box
