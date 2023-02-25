import json
import functools
from typing import List


class JsonHandler:
    def __init__(self, fn):
        self.fn = fn
        try:
            with open(self.fn, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

        except FileNotFoundError:
            with open(self.fn, 'w', encoding='utf-8') as f:
                json.dump([], f)
                json_data = []
        
        finally:
            self.list: List[int] = json_data
                
    def update(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            with open(self.fn, 'r+', encoding='utf-8') as f:
                json.dump(self.list, f)
            return res
        return wrap
    
    @update
    def append(self, value):
        self.list.append(value)
    
    @update
    def pop(self, index):
        return self.list.pop(index)
    
    @update
    def remove(self, value):
        self.list.remove(value)
        
    def find(self, value):
        for i in range(len(self.list)):
            if self.list[i] == value:
                return i
        raise ValueError

    def __iter__(self):
        return iter(self.list)

    def __str__(self):
        return str(self.list)
    