from abc import ABC,abstractmethod
import typing as t
from .logic import LogicExp

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

# TODO 逻辑门的基本实现，能对输入的逻辑表达式进行运算，对输入的门进行连接，连接产生GateMap

class Gate(ABC,Node):
    def __init__(self):
        super().__init__()
        
    def __call__(self,*args):
        # TODO 实现面对表达式进行运算，面对门进行连接
        pass
        
    @abstractmethod
    def forward(self,*x:LogicExp):
        raise NotImplementedError("gate method forward has not implement!")
    
# 门组合成GateMap
class GateMap:
    def __init__(self):
        pass
    
    
class ANDgate(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 
    
class ORgate(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 
    
class NOTgate(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 
    
class XORgate(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 
    
class XNORgate(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 