import threading as th
import time
import numpy as np


# On a une variable globale ici
stop_threads = False


def increm_sum(lock: th.Lock, array: np.ndarray, id: int):
    while not stop_threads:
        lock.acquire()
        array += 1
        # En plus d'empêcher l'array de se faire modifier par deux endroits en même temps, on empêche d'afficher
        # en même temps, ce qui pourrait donner des choses farfelues
        print(f"thread{id} : {array}")
        lock.release()
        time.sleep(1)


if __name__ == '__main__':
    lock = th.Lock()
    array = np.ones(5)
    thread0 = th.Thread(target=increm_sum, args=(lock, array, 0))
    thread1 = th.Thread(target=increm_sum, args=(lock, array, 1))
    thread0.start()
    thread1.start()
    time.sleep(10)
    # On change la valeur de la variable globale pour arrêter les threads
    stop_threads = True
    thread0.join()
    thread1.join()
    print(array)
