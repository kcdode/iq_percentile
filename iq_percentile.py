import praw
import re
import random
from scipy.stats import norm


starters = ["Golly Gee! ", "Wowza! ", "Sweet Butter Crumpets! ", "Gasp! ", "Sweet Baby Jesus! ",
            "Incredible! ", "Holy Moly! ", "By Jove! ", "Gee Willikers! ", "Gazooks! ", "Aw Lordy! "]

# Feel free to suggest additional regex patterns to match
# patterns = ["iq is/of xxx", "xxx iq"]
patterns = ["iq (of|is) [0-9]+(,[0-9]+)?", "[0-9]+(,[0-9]+)?\s?iq"]

# Running list of comments (locally stored only) I've already replied to. Manually CTRL-A-DEL'ed periodically

replied_to_write = open("repliedto.txt", "a")
replied_to_read = [line.rstrip() for line in open("repliedto.txt", "r")]


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
            if comment.permalink() in visited:
                continue
            reply_to_comment(comment)


def reply_to_comment(comment):
    for pattern in patterns:
        text = str(comment.body)
        regex = re.search(re.compile(pattern, re.IGNORECASE), text)
        if regex:
            print(regex.group(0) + "\n" + text + "\n" + comment.permalink() + "\n\n")

            # Find the number in matched group, run through
            iq = int(re.findall("(\d+)(,\d+)?", regex.group(0))[0][0])  # ¯\_(ツ)_/¯
            num = norm.cdf((iq-100)/float(15))
            if num is 1:
                comment.reply(random.choice(starters) + "That's so smart I can't even find a percentile for it!"
                                                        "\n\n ^Code: ^https://github.com/kcdode/iq_percentile")
            elif num < 0.5:
                comment.reply(random.choice(starters) + "That IQ suggests a truly feeble mind!" +
                              "\n\n ^Code: ^https://github.com/kcdode/iq_percentile")
            else:
                comment.reply(random.choice(starters) + "That IQ is in the " + str(num*100) +
                              "th percentile of people!" +
                              "\n\n ^Code: ^https://github.com/kcdode/iq_percentile")

            replied_to_write.write(comment.permalink())
            replied_to_write.write("\n")
            return


# Right now only checks for 'good bot,' may add more later if I see other common replies
def check_replies(reddit):
    for inbox_reply in reddit.inbox.unread(limit=None):
        body = str(repr(inbox_reply.body))
        regex = re.search(re.compile("good bot", re.IGNORECASE), body)
        if regex:
            print(body + str(inbox_reply.author))
            inbox_reply.reply("[Thank You!](http://i.imgur.com/decjizU.png)")
            reddit.inbox.mark_read([inbox_reply])


run_bot(login(), replied_to_read)
check_replies(login())
