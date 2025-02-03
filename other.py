from array import array

a = array('i', [1, 2, 3])
b = memoryview(a).cast("B")
a[0] = 256
print(b[0], b[1])
