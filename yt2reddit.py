#!/usr/bin/env python3
import html
import re
import time

import colorama
import configparser
import praw
import requests


BASE_URL = "https://youtube.com/{}/{}/videos" \
           "?flow=grid&sort=dd&view=0&nohtml5=False"
BASE_VIDEO_URL = "https://youtube.com/watch?v={}"

VIDEO_INFO_MATCHER = re.compile(r'dir="ltr"'
                                r'title="(.+?)".+'
                                r'href="/watch?v=(.+?)"')


def main():
    config = configparser.ConfigParser()
    config.read("reddit.ini")
    reddit = praw.Reddit("yt2reddit")
    reddit.login(config["LoginInfo"]["username"],
                 config["LoginInfo"]["password"])
    subreddit = reddit.get_subreddit(config["SubredditInfo"]["name"])
    url = BASE_URL.format(
        "user" if config["ChannelInfo"]["user"] else "channel",
        config["ChannelInfo"]["identifier"]
    )
    old_videos = None

    while True:
        response = requests.get(url)
        response.raise_for_status()
        videos = set(VIDEO_INFO_MATCHER.findall(response.text))
        if old_videos is not None:
            new_videos = videos - old_videos
            for (title, video_id) in new_videos:
                title = html.unescape(title)
                url = BASE_VIDEO_URL.format(video_id)
                print(colorama.Fore.GREEN, end="")
                print("Found new video:")
                print("    Title:", end=" ")
                print(colorama.Fore.RESET, end="")
                print(title)
                print(colorama.Fore.GREEN, end="")
                print("    URL:", end=" ")
                print(colorama.Fore.RESET, end="")
                print(url)
                try:
                    subreddit.submit(title, url=link, resubmit=True)
                except:
                    print(colorama.Fore.YELLOW, end="")
                    print("Encountered error, but will keep running")
                    print(colorama.Fore.RESET, end="")
                    traceback.print_exc()
            if not new_videos:
                print(colorama.Fore.RED, end="")
                print("No new videos.")
                print(colorama.Fore.RESET, end="")
        old_videos = videos
        time.sleep(config["ProgramSettings"].getfloat("interval"))


if __name__ == "__main__":
    main()
