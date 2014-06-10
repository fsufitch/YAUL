from yaul.cache import cache

@cache
def foo(bar):
    import time
    time.sleep(2)
    return str(bar).upper()

print(foo)
print("Running foo('abc')...")
print(foo('abc'))
print("Running foo('abc') again...")
print(foo('abc'))
print("Running foo('abc') again...")
print(foo('abc'))

print("Running foo('def')...")
print(foo('def'))
print("Running foo('def') again...")
print(foo('def'))


