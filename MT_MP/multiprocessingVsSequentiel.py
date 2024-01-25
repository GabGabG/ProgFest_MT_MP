import multiprocessing as mp
import numpy as np
import time
import matplotlib.pyplot as plt
import cupy as cp
import psutil
import tqdm


def autocorrelation_cpu_sequentiel_ameliore(array):
    array = np.array(array)

    def func(x):
        return np.correlate(x, x, mode="same")

    if array.ndim == 2:
        autocorrs = np.apply_along_axis(func, 1, array)
    else:
        autocorrs = func(array)
    return autocorrs


def autocorrelation_cpu_sequentiel_base(array):
    autocorrs = np.zeros_like(array)
    for i in range(len(array)):
        autocorrs[i] = np.correlate(array[i], array[i], mode="same")
    return autocorrs


def autocorrelation_multiprocess_base(array):
    return np.correlate(array, array, mode="same")


def autocorrelation_gpu(array):
    g_array = cp.array(array)

    def func(x):
        return cp.convolve(x, x, mode="same")

    ret = cp.apply_along_axis(func, 1, g_array)
    return cp.asnumpy(ret)


if __name__ == '__main__':
    n_cpu = psutil.cpu_count(logical=True)
    nb_arrayss = range(100, 1_001, 100)
    N = 30
    times = np.zeros((5, len(nb_arrayss), N))
    p_bar = tqdm.tqdm(total=len(nb_arrayss) * N, desc="Benchmarking")
    for j in range(N):
        for i, nb_arrays in enumerate(nb_arrayss):
            arrays = [np.random.normal(i, 1, 10000) for i in range(nb_arrays)]
            start_multiprocess_base = time.time()
            with mp.Pool(n_cpu) as pool:
                output_mp = np.array(pool.map(autocorrelation_multiprocess_base, arrays))
            end_multiprocess_base = time.time()
            output_seq_ameliore = autocorrelation_cpu_sequentiel_ameliore(arrays)
            end_seq_ameliore = time.time()
            with mp.Pool(n_cpu) as pool:
                output_mp2 = np.concatenate(
                    pool.map(autocorrelation_cpu_sequentiel_ameliore, np.array_split(arrays, n_cpu)))
            end_multiprocess_ameliore = time.time()
            output_seq_base = autocorrelation_cpu_sequentiel_base(arrays)
            end_seq_base = time.time()
            time_mp_base = end_multiprocess_base - start_multiprocess_base
            time_seq_ameliore = end_seq_ameliore - end_multiprocess_base
            time_mp_ameliore = end_multiprocess_ameliore - end_seq_ameliore
            time_seq_base = end_seq_base - end_multiprocess_ameliore
            start_gpu = time.time()
            output_gpu = autocorrelation_gpu(arrays)
            end_gpu = time.time()
            time_gpu = end_gpu - start_gpu
            times[:, i, j] = time_seq_base, time_seq_ameliore, time_mp_base, time_mp_ameliore, time_gpu
            p_bar.update()
    times_mean, times_std = np.mean(times, axis=-1), np.std(times, axis=-1)
    colors = ["red", "blue", "green", "orange", "purple"]
    labels = ["Loop", "Vec", "MP", "MP + Vec", "GPU"]
    for i, (mean, std, color, label) in enumerate(zip(times_mean, times_std, colors, labels)):
        plt.plot(nb_arrayss, mean, label=label, color=color)
        plt.fill_between(nb_arrayss, mean - std, mean + std, alpha=0.2, color=color)
    plt.legend()
    plt.ylabel(f"Temps [s] (moyenne de {N} essais)")
    plt.xlabel("Nombre de vecteurs de taille 10000 [-]")
    plt.savefig("benchmark_seq_mp_gpu.pdf", bbox_inches="tight", pad_inches=0.1, dpi=300)
    plt.show()
