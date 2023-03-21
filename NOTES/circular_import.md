file1.py
from file2 import foo


def bar():
    return "something"

file2.py
def foo():
    return "hello world"


from file1 import bar