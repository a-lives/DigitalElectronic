from abc import ABC,abstractmethod
from .logic import LogicExp,LogicMap

class Gate(ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def forward(self,*x:LogicExp):
        raise NotImplementedError("gate method forward has not implement!")
    
    
class AND(Gate):
    def __init__(self):
        super().__init__()
        
    def forward(self, *x:LogicExp):
        return 