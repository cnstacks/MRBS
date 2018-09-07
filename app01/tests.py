from django.test import TestCase

# Create your tests here.
for i in range(10):
    x = i
# for循环没有作用域;
print(x)
