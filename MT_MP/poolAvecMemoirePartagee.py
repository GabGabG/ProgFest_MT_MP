import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np

def increm(process_id):
    global shared_array_name
    global lock
    with lock:
        shared_array = shared_memory.SharedMemory(name=shared_array_name)
        array = np.ndarray((10,), int, shared_array.buf)
        array += 1
        print(f"Process {process_id} : {array}")
    shared_array.close()


def worker_init(shared_name, lock_):
    global shared_array_name
    global lock
    lock = lock_
    shared_array_name = shared_name


if __name__ == '__main__':
    lock = mp.Lock()
    shared_array = shared_memory.SharedMemory(create=True, size=80)
    with mp.Pool(6, worker_init, (shared_array.name, lock)) as pool:
        pool.map(increm, range(6))
    shared_array.close()
    shared_array.unlink()
