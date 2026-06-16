import time


def measure(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    print(f"{fn.__name__}: result={result}, time={elapsed:.6f}s")
    return result
