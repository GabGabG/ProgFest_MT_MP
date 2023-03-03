import threading as th
import time
from pytube import YouTube
from utils import YouTubeViewsCounter, ProgressBar


def fonction():
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    start = time.time()
    now = start
    view_counter = YouTubeViewsCounter(video_url)
    previous_views = view_counter.view_count()
    vid_len = view_counter.video_len()
    total_diff = 0
    progress_bar = ProgressBar(vid_len)
    while not progress_bar.is_done:
        view_counter.update_yt_obj()
        progression = progress_bar.progress_str(now - start)
        views = view_counter.view_count()
        if views == -1:
            views = previous_views
        diff = views - previous_views
        total_diff += diff
        if total_diff >= 0:
            diff = f"+{total_diff}"
        print(f"\r{views} vues ({diff} depuis le début), {progression}", end="")
        previous_views = views
        wait = 0.05
        time.sleep(wait)
        now = time.time()


if __name__ == '__main__':
    thread = th.Thread(target=fonction)
    thread.start()
    thread.join()
