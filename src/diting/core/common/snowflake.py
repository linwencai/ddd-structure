from time import time
from random import randint
from datetime import datetime

_candicates = "0123456789ABCDEFGHJKMNPRSTUVWXYZ"

_index_char_map = {index:value for index, value in enumerate(_candicates)}
_char_index_map = {value:index for index, value in enumerate(_candicates)}

class SnowflakeGenerator:
    # 实例范围 [0, 1024)
    # seq 范围 [0, 4096)
    def __init__(self, instance: int=0):
        self.instance = (instance % 1024) << 12
        self.seq = randint(0, 4096-1)
    
    def set_instance(self, instance: int):
        self.instance = (instance % 1024) << 12

    def __iter__(self):
        return self
    
    def __next__(self):
        current = int(time() * 1000)
        
        if self.seq + 1 == 4096:
            self.seq = 0
        else:
            self.seq += 1
            
        value = current << 22 | self.instance | self.seq
        return self.base32(value)

    def base32(self, value):
        arr = [""] * 13
        
        for i in range(13):
            v = (value >> ((12-i)*5)) & 0b11111
            arr[i] = _index_char_map[v]
            
        return "".join(arr)
    
    def unbase32(self, value):
        v = 0
        for index, char in enumerate(value):
            v |= (_char_index_map[char]) << ((12-index)*5)
            
        return v
        
    def parse(self, value):
        return {
            "seq" : value & 0b111111111111,
            "instance" : (value >> 12) & 0b1111111111,
            "timestamp" : value >> 22,
            "datetime" : datetime.fromtimestamp((value >> 22) / 1000)
        }

__instance_num__ = randint(0, 1023)
snowflake = SnowflakeGenerator(__instance_num__)

def generate_snowflake_id():
    return next(snowflake)
