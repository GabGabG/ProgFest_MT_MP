import multiprocessing as mp
import time

import numpy as np


def somme_increm(array: mp.Array, stop: mp.Value, _id: int):
    while not stop:
        # On accède directement au lock de l'array partagé, pas besoin d'en avoir un externe
        with array.get_lock():
            # Ici, on va accéder au contenu de ce que l'array partagé contient
            array_np = np.frombuffer(array.get_obj(), dtype="int32")
            # En modifiant l'array numpy, on modifie aussi l'array partagé
            array_np += 1
            print(f"process{_id} : {array_np}")
        time.sleep(1)


if __name__ == '__main__':
    stop = mp.RawValue("b", 0)  # Un flag pour ne pas arrêter tant que quelque chose n'est pas accompli (ici, 10 secs)
    N = 5
    shared_array = mp.Array("i", N)
    # On accède au contenu de l'array partagé (par défaut qui vaut 0)
    array_base = np.frombuffer(shared_array.get_obj(), dtype="int32")
    # On modifie l'array formé à partir de l'array partagé, ce qui modifie aussi l'array partagé
    array_base[:] = 1
    process0 = mp.Process(target=somme_increm, args=(shared_array, stop, 0))
    process1 = mp.Process(target=somme_increm, args=(shared_array, stop, 1))
    process0.start()
    process1.start()
    time.sleep(10)
    stop.value = 1  # On partage un flag stop pour arrêter les processes après 10 secondes
    process0.join()
    process1.join()
    process0.close()
    process1.close()
    print(array_base)
