import praw
import re
from src import iq


def login():
    reddit = praw.Reddit("iq_percentile")
    return reddit


# Feel free to suggest additional regex patterns to match
pat_1 = re.compile("iq (of|is) [0-9]+", re.IGNORECASE)
pat_2 = re.compile("[0-9]+\s?iq", re.IGNORECASE)


def run_bot(r):
    subreddit = r.subreddit("SUB_HERE")

    for comment in subreddit.comments(limit=300000):
        text = str(comment.body)
        reg = pat_1.match(text)
        ex = pat_2.match(text)
        try:
            print(reg.group(0))
            print("0")
            token = [int(s) for s in reg.group(0).split() if s.isdigit()]
            percentile = iq.iq(token[0])
            comment.reply("Wow! That IQ is in the " + str(percentile) + "th percentile of IQs!" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
        except AttributeError:
            pass

        try:
            print(ex.group(0))
            print(text)
            print("1")
            token = [int(s) for s in ex.group(0).split() if s.isdigit()]
            percentile = iq.iq(token[0])
            comment.reply("Wow! That IQ is in the " + str(percentile) + " percentile of IQs!" + "\n ^code:https://github.com/kcdode/iq_percentile")
        except AttributeError:
            pass


run_bot(login())
