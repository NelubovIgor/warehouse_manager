from array import array
from contextlib import contextmanager

@contextmanager
def ctx():
    print(1)
    try: yield
    finally: print(2)

with ctx(), ctx():
    print(3)

a = array('i', [1, 2, 3])
b = memoryview(a).cast("B")
a[0] = 256
# print(b[0], b[1])
