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
    subreddit = r.subreddit("SUBREDDIT HERE")

    for comment in subreddit.comments(limit=300000):
        text = str(comment.body)
        reg = pat_1.match(text)
        ex = pat_2.match(text)

        # Try matching "iq is/of xxx"
        try:
            print(reg.group(0))
            # print(text)
            token = [int(s) for s in reg.group(0).split() if s.isdigit()]
            percentile = iq.iq(token[0])
            if percentile is 1:
                comment.reply("Wow! You're so smart I can't even find a percentile for you!"
                              "" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
            elif percentile is 0:
                comment.reply("Wow! You are a truly feeble mind!" +
                              "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
            else:
                comment.reply("Wow! That IQ is in the " + str(percentile) + "th percentile of IQs!" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile")

        except AttributeError:
            pass

        # Try matching "xxx iq"
        try:
            print(ex.group(0))
            # print(text)
            token = [int(s) for s in ex.group(0).split() if s.isdigit()]
            percentile = iq.iq(token[0])
            if percentile is 1:
                comment.reply("Wow! You're so smart I can't even find a percentile for you!"
                              "" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
            elif percentile is 0:
                comment.reply("Wow! You are a truly feeble mind!" +
                              "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
            else:
                comment.reply("Wow! That IQ is in the " + str(percentile) + "th percentile of IQs!" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile")
        except AttributeError:
                pass


run_bot(login())
