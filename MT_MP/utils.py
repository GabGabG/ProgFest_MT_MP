import matplotlib.pyplot as plt
import matplotlib
from pytube import YouTube

matplotlib.use("TkAgg")


class PrintInPlot:

    def __init__(self, initial_message: str = "", initial_position: tuple = (0.5, 0.5)):
        self.fig, self.ax = plt.subplots()
        win = self.fig.canvas.manager.window
        win.overrideredirect(1)
        win.tkraise()
        self.ax.axis("off")
        self.__txt = self.ax.text(*initial_position, s=initial_message)
        self.__txt.set_clip_on(False)
        plt.show(block=False)

    @property
    def text(self):
        return self.__txt

    @text.setter
    def text(self, message: str):
        self.__txt.set_text(message)

    def pause_plot(self, time_interval):
        plt.pause(time_interval)

    def close_fig(self):
        plt.close(self.fig)


class ProgressBar:

    def __init__(self, max_len: float, increm: int = 10, done_char: str = "🭲", pending_char: str = "-"):
        self.__max_len = max_len
        self.__increm = increm
        self.done_char = done_char
        self.pending_char = pending_char
        self.__is_done = False

    def progress_str(self, current_len: float, nb_decimals: int = 0):
        percent = (current_len / self.__max_len) * 100
        nb_done_char = int(percent // self.__increm)
        nb_pending_char = int(100 // self.__increm - nb_done_char)
        progression = self.done_char * nb_done_char + self.pending_char * nb_pending_char
        message = f"[{progression}] {percent:.{nb_decimals}f}%"
        if percent >= 100:
            self.__is_done = True
        return message

    def print_progress(self, current_len: float, nb_decimals: int = 0, other_messages_before: tuple = None,
                       other_messages_after: tuple = None):
        message = self.progress_str(current_len, nb_decimals)
        if other_messages_before is not None:
            message = "".join(other_messages_before) + message
        if other_messages_after is not None:
            message += "".join(other_messages_after)
        print("\r" + message, sep="")

    @property
    def is_done(self):
        return self.__is_done


class YouTubeViewsCounter:

    def __init__(self, url: str):
        self.url = url
        self.__yt_object = YouTube(self.url)

    def update_yt_obj(self):
        self.__yt_object = YouTube(self.url)

    def view_count(self):
        try:
            views = self.__yt_object.views
        except TypeError:
            views = -1
        return views

    def video_len(self):
        return self.__yt_object.length

    @property
    def yt_object(self):
        return self.__yt_object
