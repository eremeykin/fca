import sys
import random

attrib_names = [
    'top-left-square',
    'top-middle-square',
    'top-right-square',
    'middle-left-square',
    'middle-middle-square',
    'middle-right-square',
    'bottom-left-square',
    'bottom-middle-square',
    'bottom-right-square',
    'class'
]


def make_intent(example):
    global attrib_names
    return set([i + ':' + str(k) for i, k in zip(attrib_names, example)])


cv_res = {
    "positive_positive": 0,
    "positive_negative": 0,
    "negative_positive": 0,
    "negative_negative": 0,
    "contradictory": 0,
    "total": 0,
}


def check_intersect(context_plus, context_minus, example, num_sub=1):
    global cv_res
    pos = 0
    neg = 0
    intent = make_intent(example)
    num_sub = int (num_sub)
    for i in range(num_sub):
        t = set(random.sample(example, random.randrange(len(intent))))
        for j in context_plus:
            if t.issubset(j):
                pos += len(t)
        for k in context_minus:
            if t.issubset(k):
                neg += len(t)

    def score(pos, neg):
        return pos * 1. / (neg + 1)

    threshold = 1.1
    if score(pos, neg) > threshold:
        if example[-1] == 'positive':
            cv_res['positive_positive'] += 1
        else:
            cv_res['negative_positive'] += 1
    elif score(neg, pos) > threshold:
        if example[-1] == 'positive':
            cv_res['positive_negative'] += 1
        else:
            cv_res['negative_negative'] += 1
    else:
        cv_res['contradictory'] += 1


def check_hypothesis(context_plus, context_minus, example):
    global cv_res
    eintent = make_intent(example)
    big_context = context_plus + context_minus
    labels = {}
    for e in big_context:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        if not candidate_intent:
            continue
        closure = [make_intent(i) for i in big_context
                   if make_intent(i).issuperset(candidate_intent)]
        res = reduce(lambda x, y: x & y if x & y else x | y, closure)
        for cs in ['positive', 'negative']:
            if 'class:' + cs in res:
                labels[cs] = True
                labels[cs + '_res'] = candidate_intent

                print('classified as %s, reason:' % cs)
                # print candidate_intent
                # print res
            #    print labels
    if labels.get("positive", False) and labels.get("negative", False):
        cv_res["contradictory"] += 1
        return
    if example[-1] == "positive" and labels.get("positive", False):
        cv_res["positive_positive"] += 1
    if example[-1] == "negative" and labels.get("positive", False):
        cv_res["negative_positive"] += 1
    if example[-1] == "positive" and labels.get("negative", False):
        cv_res["positive_negative"] += 1
    if example[-1] == "negative" and labels.get("negative", False):
        cv_res["negative_negative"] += 1


if __name__ == "__main__":
    max_index = '2' #sys.argv[1]
    for index in range(1, int(max_index)):
        index = str(index)
        q = open("train" + index + ".csv", "r")
        train = [a.strip().split(",") for a in q]
        plus = [a for a in train if a[-1] == "positive"]
        minus = [a for a in train if a[-1] == "negative"]
        q.close()
        w = open("test" + index + ".csv", "r")
        unknown = [a.strip().split(",") for a in w]
        w.close()
        for elem in unknown:
            print(elem)
            cv_res['total'] += 1
            check_intersect(plus, minus, elem, len(elem) / 2)
    for k, v in cv_res.items():
        cv_res[k] = v * 1. / cv_res["total"]
    print(cv_res)
