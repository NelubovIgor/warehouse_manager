from array import array
from contextlib import contextmanager

class Meta(type):
    def __call__(self, *args, **kwds):
        print(1)
        return super().__call__(*args, **kwds)

class A(metaclass=Meta):
    def __init__(self):
        print(2)
    def __new__(cls):
        print(3)
        return super().__new__(cls)

A()
# @contextmanager
# def ctx():
#     print(1)
#     try: yield
#     finally: print(2)

# with ctx(), ctx():
#     print(3)

a = array('i', [1, 2, 3])
b = memoryview(a).cast("B")
a[0] = 256
# print(b[0], b[1])
