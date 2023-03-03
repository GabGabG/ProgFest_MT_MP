import multiprocessing as mp
import time
from utils import PrintInPlot

input_ = "input.txt"


def fonction():
    stop = False
    pp = PrintInPlot()
    while not stop:
        with open(input_, "r") as in_:
            message = in_.read()
            pp.text = message
            if "END" in message:
                pp.close_fig()
                stop = True  # On arrête le thread si END est dans le message.
                # Si pas de END, le process va tout le temps rouler.
            else:
                wait = 0.1
                pp.pause_plot(wait)
                time.sleep(wait)  # Pour ne pas lire trop souvent, on attend 0.1 seconde


if __name__ == '__main__':
    process = mp.Process(target=fonction)
    process.start()
    process.join()
    process.close()
