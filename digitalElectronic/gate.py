from abc import ABC,abstractmethod
import typing as t
from .logic import LogicExp

class Gate(ABC):
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