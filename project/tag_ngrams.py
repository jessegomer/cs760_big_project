import data_handler
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from copy import deepcopy
import numpy as np
import random
from sklearn import svm, cross_validation
from collections import Counter
from nltk.util import ngrams
from pprint import pprint
import pickle
authors = ['dickens', 'doyle', 'fitzgerald', 'austen']
data = data_handler.DataHandler()
pickle_name = 'C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/common_tag_ngram.pickle'

def get_top(c, n):
    most_common =  c.most_common(n)
    out = []
    for item, count in most_common:
        out.append(item)
    return out


def tag_files():
    for author in authors:
        tagged_sents = []
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore").replace(u"\n", u" ").replace(u"\t", " ").replace(u"  ", u" ").lower()
            f.close()
            for s in sent_tokenize(text):
                words = word_tokenize(s)
                tagged_sents.append(nltk.pos_tag(words))
        pname = 'C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/tagged_' + author + '.pickle'
        pickle.dump(tagged_sents, open(pname, 'wb'))
        print tagged_sents

t_a = pickle.load(open('C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/tagged_austen.pickle'))
for s in t_a:
    print s

def gen_common_ngram(cutoff):
    #outfile = open(pickle_name, 'wb')
    c1, c2, c3, c4, c5, c6, c7 = Counter(), Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    for index, author in enumerate(authors):
        author_sents = []
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore").replace(u"\n", u" ").replace(u"\t", " ").replace(u"  ", u" ").lower()
            f.close()
            author_sents.extend(sent_tokenize(text))
        for s in author_sents:
            words = word_tokenize(s)
            tags = nltk.pos_tag(words)
            print tags
            for ng in ngrams(words, 1):
                c1[ng] += 1
            for ng in ngrams(words, 2):
                c2[ng] += 1
            for ng in ngrams(words, 3):
                c3[ng] += 1
            for ng in ngrams(words, 4):
                c4[ng] += 1
            for ng in ngrams(words, 5):
                c4[ng] += 1
            for ng in ngrams(words, 6):
                c4[ng] += 1
            for ng in ngrams(words, 7):
                c4[ng] += 1
   # most_common = {1:get_top(c1, cutoff), 2:get_top(c2, cutoff), 3:get_top(c3,cutoff), 4:get_top(c4, cutoff)}
    #pprint(most_common)
    #pickle.dump(most_common, outfile)
    #outfile.close()



def gen_ngram_counts(n, chunk_size):
    outname = 'C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/' + str(n) + 'gram' + str(chunk_size)+ '.csv'
    common = set((pickle.load(open(pickle_name, 'rb')))[n])
    outfile = open(outname, 'w')
    for index, author in enumerate(authors):
        author_sents = []
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore").replace(u"\n", u" ").replace(u"\t", " ").replace(u"  ", u" ").lower()
            f.close()
            author_sents.extend(sent_tokenize(text))
        for i in xrange(0,len(author_sents)-len(author_sents)%chunk_size, chunk_size):
            chunk = author_sents[i:i+chunk_size]
            c = Counter()
            data_line = []
            for s in chunk:
                for ng in ngrams(word_tokenize(s), n):
                    c[ng] += 1
            for common_ng in common:
                data_line.append(float(c[common_ng])/float(sum(c.values())) if sum(c.values()) > 0 else 0)
            data_line.append(index)
            outfile.write(",".join([str(element) for element in data_line])+'\n')
    outfile.close()

# chunk_sizes = [5, 10, 20, 40, 60, 80]
# for i in range(1, 5):
#     for cs in chunk_sizes:
#         gen_ngram_counts(i, cs)
#         print i, cs





def run_test(n, cs):

    dickens, doyle, fitzgerald, austen = [], [], [], []
    author_rows = [dickens, doyle, fitzgerald, austen]
    xs = []
    ys = []
    for line in data.load_file('computed',  str(n) + 'gram' + str(cs) + '.csv'):
        data_line = [float(c) for c in line.split(',')]
        data_line[-1] = int(data_line[-1])

        author_rows[data_line[-1]].append(data_line[:-1])
        if len(author_rows[data_line[-1]]) > 24000/cs:
            continue
        xs.append(data_line[:-1])
        ys.append(data_line[-1])


    print len(dickens), len(doyle), len(fitzgerald), len(austen)
    print len(xs)

    xs = np.asarray(xs)
    ys = np.asarray(ys)

    skf = cross_validation.StratifiedKFold(ys, 10, shuffle=True)
    total_correct = 0.0
    total = 0.0
    for train_instance, test_instance in skf:
        clf = svm.LinearSVC()
        clf.fit(xs[train_instance], ys[train_instance])
        predicted = clf.predict(xs[test_instance])
        for p, a in zip(predicted, ys[test_instance]):
            total += 1
            if p == a:
                total_correct += 1
            else:
                #print p, a
                pass
    print "n=",n, "  cs=", cs
    print total, total_correct, total_correct/total



run_test(2, 20)

#
# chunk_sizes = [5, 10, 20, 40, 60, 80]
# for i in range(1, 5):
#     for cs in chunk_sizes:
#         run_test(i, cs)