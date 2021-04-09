import os

print(os.getcwd())
print(__file__)
print(os.path.basename(__file__))
print(os.path.dirname(__file__))
print(os.path.abspath(__file__))
print("--")
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/test/mk_test.jpg')
norm_path = os.path.normpath(path)
print(norm_path)