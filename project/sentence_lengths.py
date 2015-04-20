import data_handler
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

data = data_handler.DataHandler()



def get_distribution(f):

    raw = f.read().decode("ascii", "ignore")

    sents = sent_tokenize(raw.replace("\n", " "))
    c = Counter()
    total = 0
    for s in sents:
        c[len(s.split(" "))] += 1
        total += 1
    return c, total


def get_author_dist(author):
    files = data.load_author(author)
    full_counter = Counter()
    full_total = 0
    for f in files:
        cur_c, cur_t = get_distribution(f)
        full_total += cur_t
        for k,v in cur_c.items():
            full_counter[k] += v

    return full_counter, full_total



c, total = get_author_dist('dickens')

print c
subtotal = 0

# for l in xrange(7000):
#     subtotal += c[l]
#     if subtotal > total/3:
#         print l
#         subtotal = 0

