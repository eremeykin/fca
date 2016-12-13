import pprint
import sys
from functools import reduce

cv_res = {
    "positive_positive": 0,
    "positive_negative": 0,
    "negative_positive": 0,
    "negative_negative": 0,
    "contradictory": 0,
}

attrib_names = [
    'tl',
    'tm',
    'tr',
    'ml',
    'mm',
    'mr',
    'bl',
    'bm',
    'br',
    'class'
]


def make_intent(example):
    global attrib_names
    return set([i + ':' + str(k) for i, k in zip(attrib_names, example)])


def check_hypothesis(context_plus, context_minus, example):
    #  print example
    eintent = make_intent(example)
    #  print eintent
    eintent.discard('class:positive')
    eintent.discard('class:negative')
    labels = {}
    global cv_res
    for e in context_plus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [make_intent(i) for i in context_minus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])
        from pprint import pprint
        # pprint("closure: "+str(closure))
        #print closure_size * 1.0 / len(context_minus)
        res = reduce(lambda x, y: x & y if x & y else x | y, closure, set())
        # print('res:'+str(res))
        print('cp in res = '+ str('class:positive' in res))
        print('cp in res = '+ str('class:positive' in res))
        for cs in ['positive', 'negative']:
            if 'class:' + cs in res:
                labels[cs] = True
                labels[cs + '_res'] = candidate_intent
                labels[cs + '_total_weight'] = labels.get(cs + '_total_weight', 0) + closure_size * 1.0 / len(
                    context_minus) / len(context_plus)
    for e in context_minus:
        ei = make_intent(e)
        candidate_intent = ei & eintent
        closure = [make_intent(i) for i in context_plus if make_intent(i).issuperset(candidate_intent)]
        closure_size = len([i for i in closure if len(i)])
        #print closure_size * 1.0 / len(context_plus)
        res = reduce(lambda x, y: x & y if x & y else x | y, closure, set())
        for cs in ['positive', 'negative']:
            if 'class:' + cs in res:
                labels[cs] = True
                labels[cs + '_res'] = candidate_intent
                labels[cs + '_total_weight'] = labels.get(cs + '_total_weight', 0) + closure_size * 1.0 / len(
                    context_plus) / len(context_minus)
    # print('example: '+str(example))
    # print('    positive_total_weight: '+str(labels.get("positive_total_weight", "None")))
    # print('    negative_total_weight: '+str(labels.get("negative_total_weight","None")))
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
    index = '1'
    q = open("train" + index + ".csv", "r")
    train = [a.strip().split(",") for a in q]
    plus = [a for a in train if a[-1] == "positive"]
    minus = [a for a in train if a[-1] == "negative"]
    q.close()

    w = open("test" + index + ".csv", "r")
    unknown = [a.strip().split(",") for a in w]
    w.close()

    i = 0
    for elem in unknown[:1]:
        i += 1
        check_hypothesis(plus, minus, elem)
    print(cv_res)
