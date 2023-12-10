from enum import Enum
from intbase import InterpreterBase


# Enumerated type for our different language data types
class Type(Enum):
    INT = 1
    BOOL = 2
    STRING = 3
    CLOSURE = 4
    OBJECT = 5
    NIL = 6


class Closure:
    def __init__(self, func_ast, env):
        self.captured_env = env.copy()
        self.func_ast = func_ast
        self.type = Type.CLOSURE


class Object:
    PROTO_DEF = "proto"

    def __init__(self):
        self.dict = {}

    def set(self, field, val):
        self.dict[field] = val

    def get(self, field):
        if field in self.dict:
            return self.dict[field]

        cur_obj = self
        while Object.PROTO_DEF in cur_obj.dict:
            proto_val = cur_obj.dict[Object.PROTO_DEF]
            if proto_val.type() == Type.NIL:
                break
            cur_obj = proto_val.value()
            if field in cur_obj.dict:
                return cur_obj.dict[field]

        return None
    
    def from_self(self, field):
        return field in self.dict
        


# Represents a value, which has a type and its value
class Value:
    def __init__(self, t, v=None):
        self.t = t
        self.v = v

    def value(self):
        return self.v

    def type(self):
        return self.t

    def set(self, other):
        self.t = other.t
        self.v = other.v


def create_value(val):
    if val == InterpreterBase.TRUE_DEF:
        return Value(Type.BOOL, True)
    elif val == InterpreterBase.FALSE_DEF:
        return Value(Type.BOOL, False)
    elif val == InterpreterBase.NIL_DEF:
        return Value(Type.NIL, None)
    elif val == InterpreterBase.OBJ_DEF:
        return Value(Type.OBJECT, Object())
    elif isinstance(val, str):
        return Value(Type.STRING, val)
    elif isinstance(val, int):
        return Value(Type.INT, val)
    else:
        raise ValueError("Unknown value type")


def get_printable(val):
    if val.type() == Type.INT:
        return str(val.value())
    if val.type() == Type.STRING:
        return val.value()
    if val.type() == Type.BOOL:
        if val.value() is True:
            return "true"
        return "false"
    return None
