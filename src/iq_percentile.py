import praw
import re
import random
from src import percentiles


starters = ["Golly gee! ", "Wowza! ", "Sweet Butter Crumpets! ", "Gasp! ", "Sweet Baby Jesus! ",
            "Incredible! ", "Holy Moly! ", "By Jove! ", "Gee Willikers! ", "Gazooks! "]

# Feel free to suggest additional regex patterns to match
# patterns = {"iq is/of xxx,xxx", "xxx,xxx iq"}
patterns = {"iq (of|is) [0-9]+(,[0-9]+)?", "[0-9]+(,[0-9]+)?\s?iq"}

# Running list of comment's I've already replied to. Manually CTRL-A-DEL'ed periodically
file = open("repliedto.txt", "a")


def login():
    reddit = praw.Reddit("iq_percentile")
    return reddit


def run_bot(r, visited):
    subreddit = r.subreddit("iamverysmart")
    num_posts = 20

    for submission in subreddit.hot(limit=num_posts):

        submission.comments.replace_more(limit=0)
        comment_list = submission.comments.list()

        for comment in comment_list:
            # Make sure we don't comment twice
            if comment.permalink() in visited:
                continue

            for pattern in patterns:
                text = str(comment.body)
                regex = re.search(re.compile(pattern, re.IGNORECASE), text)
                if regex:
                    print(regex.group(0) + "\n" + text + "\n" + comment.permalink() + "\n\n")

                    # Lookup percentile from extracted the integer in the matched string
                    num = percentiles.get_iq_perc(int(re.findall("\d+,?\d+?", regex.group(0))[0]))
                    if num is 1:
                        comment.reply(random.choice(starters) + "That's so smart I can't even find a percentile for it!"
                                      "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                      "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                    elif num is 0:
                        comment.reply(random.choice(starters) + "That IQ suggests a truly feeble mind!" +
                                      "\n\n ^^^code:https://github.com/kcdode/iq_percentile  "
                                      "^^^^^I-am-still-in-testing-PM-me-if-I-fucked-up")
                    else:
                        comment.reply(random.choice(starters) + "That IQ is in the " + str(num) +
                                      "th percentile of people!" +
                                      "\n\n ^^^code:https://github.com/kcdode/iq_percentile "
                                      "^^^I-am-still-in-testing-PM-me-if-I-fucked-up")


                    # Add to list of already replied-to comments, so future exectuion won't reply again
                    file.write(comment.permalink())
                    file.write("\n")

f = [line.rstrip() for line in open("repliedto.txt", "r")]

run_bot(login(), f)
