import pythonbasictools as pbt
import time
import numpy as np


def func(a, b, t):
    time.sleep(t)
    return a + b


# @pbt.decorators.log_func(logging_func=print)
def apply_func(n, t, nb_workers):
    return pbt.multiprocessing_tools.apply_func_multiprocess(
        func,
        iterable_of_args=[
            (np.random.randint(0, 100), np.random.randint(0, 100), t)
            for _ in range(n)
        ],
        nb_workers=nb_workers,
        verbose=True,
        desc=f"Apply func {n} times with t={t} and nb_workers={nb_workers}",
        unit="arg",
    )


if __name__ == '__main__':
    N, T = 128, 0.2
    apply_func(N, T, 0)
    apply_func(N, T, 1)
    apply_func(N, T, 2)
    apply_func(N, T, -1)
    apply_func(N, T, -2)
