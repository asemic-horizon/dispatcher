from pydantic import BaseModel
from enum import Enum 

class DispatcherEnum(Enum):
    #  remember: instance methods refer to a single member,
    #  e.g Colors.RED  rather than to the Colors enum
    def __init__(self, value, func=None):
        super().__init__()
        self._value_ = value
        self.call = func

    # a class method is needed to add functionality to the Enum  itself
    # (e.g. Colors.RED is unable to add a property "_call" to Colors.BLUE)
    @classmethod
    def assign(cls, member, func):
        member.call = func

    @classmethod
    def from_dict(cls, d):
        # fix unassigned
        d.update({key:None for key in cls.__members__ if key not in d})
        for key, value in d.items():
            cls.assign(cls[key], value)
    
    def __call__(self,*args,**kwargs):
        return self.call(*args,**kwargs)

def Dispatcher(member_dict, name = None):
    from hashlib import md5
    if name is None:
        name = str(md5(str(member_dict).encode()).hexdigest()[:6])
    attrs = {member.upper():member for member in member_dict}
    funcs = {member.upper():func for member, func in member_dict.items()}
    cls = MappedEnum(name,attrs)
    cls.from_dict(funcs)
    return cls