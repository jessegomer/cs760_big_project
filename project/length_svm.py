import data_handler
from nltk.tokenize import word_tokenize, sent_tokenize
from copy import deepcopy
import numpy as np
import random
from sklearn import svm, cross_validation


authors = ['dickens', 'doyle', 'fitzgerald', 'austen']

data = data_handler.DataHandler()



def gen_counts():
    blank_count = [0 for i in range(250)]
    outfile = open('C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/length_svn.csv', 'w')
    for index, author in enumerate(authors):
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore")
            f.close()
            paras = text.split('\n\n')
            for para in paras:
                count = deepcopy(blank_count)
                sentences = sent_tokenize(para.replace('\n', ' '))
                for sentence in sentences:
                    l = len(sentence.split(' '))
                    count[l] += 1
                count.append(index)
                outfile.write(",".join([str(i) for i in count]) + '\n')

def gen_counts_with_floor(floor):
    blank_count = [0 for i in range(250)]
    outfile = open('C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/length_floor' + str(floor) + '.csv', 'w')
    for index, author in enumerate(authors):
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore")
            f.close()
            paras = text.split('\n\n')
            for para in paras:
                count = deepcopy(blank_count)
                sentences = sent_tokenize(para.replace('\n', ' '))
                if len(sentences) < floor:
                    continue
                for sentence in sentences:
                    l = len(sentence.split(' '))
                    count[l] += 1
                count.append(index)
                outfile.write(",".join([str(i) for i in count]) + '\n')

def gen_counts_of_blocks(size):
    blank_count = [0 for i in range(250)]
    outfile = open('C:/Users/jesse/PycharmProjects/cs760_big_project/data/computed/length_blocks' + str(size) + '.csv', 'w')
    for index, author in enumerate(authors):
        for f in data.load_author(author):
            text = f.read().decode("ascii", "ignore").replace(u"\n", u" ").replace(u"\t", " ").replace(u"  ", u" ")
            f.close()
            sents = sent_tokenize(text)
            count = deepcopy(blank_count)
            for sent in sents:
                if sum(count) == size:
                    count.append(index)
                    outfile.write(",".join([str(i) for i in count]) + '\n')
                    count = deepcopy(blank_count)
                l = len(sent.split(u' '))
                if l<250:
                    count[l] += 1



#gen_counts_with_floor(2)
#gen_counts_of_blocks(160)

xs = []
ys = []

dickens, doyle, fitzgerald, austen = [], [], [], []
author_rows = [dickens, doyle, fitzgerald, austen]

for line in data.load_file('computed', 'length_blocks20.csv'):
    data_line = [int(c) for c in line.split(',')]
    author_rows[data_line[-1]].append(data_line[:-1])
    if len(author_rows[data_line[-1]]) > 1200:
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
print total, total_correct, total_correct/total



# train_size = 1000
# test_size =  80
# dxs = random.sample(doyle, train_size + test_size)
# axs = random.sample(austen, train_size + test_size)
# xs = dxs[:train_size] + axs[:train_size]
# ys = [0]*train_size + [1]*train_size
#
# clf = svm.LinearSVC()
# clf.fit(xs, ys)
#
# pd = clf.predict(dxs[train_size:])
# pa = clf.predict(axs[train_size:])
# correct, total = 0.0, 0.0
#
# for p in pd:
#     if p == 0:
#         correct += 1
#     total += 1
#
# for p in pa:
#     if p == 1:
#         correct += 1
#     total += 1
#
# print correct/total
