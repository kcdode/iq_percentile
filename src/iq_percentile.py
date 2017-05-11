import praw
import re
from src import iq



def login():
    reddit = praw.Reddit("iq_percentile")
    return reddit


# Feel free to suggest additional regex patterns to match
# If there are more patterns in the future I will probably switch to a list of regex matchers
# and loop through.
pat_1 = re.compile("iq (of|is) [0-9]+", re.IGNORECASE)
pat_2 = re.compile("[0-9]+\s?iq", re.IGNORECASE)


def run_bot(r):
    subreddit = r.subreddit("iamverysmart")

    num_posts = 4

    for submission in subreddit.hot(limit=num_posts):
        submission.comments.replace_more(limit=0)
        comment_list = submission.comments.list()

        for comment in comment_list:
            text = str(comment.body)
            reg = re.search(pat_1, text)
            ex = re.search(pat_2, text)

            # Try matching "iq is/of xxx"
            if reg:
                print(reg.group(0))
                print(text)
                print(comment.permalink())
                print("\n\n")

                token = [int(s) for s in reg.group(0).split() if s.isdigit()]
                percentile = iq.iq(token[0])
                if percentile is 1:
                    comment.reply("Wow! That's so smart I can't even find a percentile for it!"
                                  "" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                       "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                elif percentile is 0:
                    comment.reply("Wow! That IQ suggests a truly feeble mind!" +
                                  "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                  "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                else:
                    comment.reply("Wow! That IQ is in the " + str(percentile) + "th percentile of people!" +
                                  "\n\n ^^^^^code:https://github.com/kcdode/iq_percentile "
                                  "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")

            # Try matching "xxx iq"
            if ex:
                print(ex.group(0))
                print(text)
                print(comment.permalink())
                print("\n\n")

                token = [int(s) for s in ex.group(0).split() if s.isdigit()]
                percentile = iq.iq(token[0])
                if percentile is 1:
                    comment.reply("Wow! That's so smart I can't even find a percentile for it!"
                                  "" + "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                       "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                elif percentile is 0:
                    comment.reply("Wow! That IQ suggests a truly feeble mind!" +
                                  "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                  "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                else:
                    comment.reply("Wow! That IQ is in the " + str(percentile) + "th percentile of people!" +
                                  "\n\n ^^^^^code:https://github.com/kcdode/iq_percentile "
                                  "^^^^^I-am-still-in-testing-tell-me-if-I-fucked-up")




run_bot(login())
