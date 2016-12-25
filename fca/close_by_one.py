from data_preparation import get_raw_data
from fca.concept import Concept
from fca.context import Context

__author__ = 'eremeykin'


class Vertex():
    def __init__(self, context, obj):
        self.obj = obj
        self.context = context
        self.closed = False

    def generate_children(self):
        res = []
        names = self.context.objects_names()
        last = names.index(self.obj[-1]) if len(self.obj) > 0 else -1
        for new in names[last + 1:]:
            new_vertex = Vertex(self.context, self.obj + [new])
            res.append(new_vertex)
        return res

    def is_closed_canonical(self):
        g_to_d = self.context.g_to_d(self.obj)
        d_to_g = self.context.d_to_g(g_to_d)
        self.concept = Concept(d_to_g, g_to_d)
        if len(self.obj) < 1:
            return True
        last = self.obj[-1]
        return d_to_g[len(self.obj) - 1] == last

    def __eq__(self, other):
        if other is None:
            return False
        return self.obj == other.obj and self.context == other.context and self.closed == other.closed

    def __hash__(self):
        return hash(tuple(self.obj))

    def __str__(self):
        s = '?'
        if hasattr(self, 'concept'):
            s = str(self.concept.m)
        return "G:(" + ','.join([str(x) for x in self.obj]) + ");"  # M:\n(" + s + ')'

    def __repr__(self):
        return str(self)


def __derive(context, vertex, all_concepts):
    children = vertex.generate_children()
    if vertex.is_closed_canonical():
        all_concepts.add(vertex.concept)
        for child in children:
            __derive(context, child, all_concepts)


def close_by_one(context):
    concepts = set()
    __derive(context, Vertex(context, []), concepts)
    return build_lattice(list(concepts))


def istransitive(parent, child):
    opened = [parent]
    while opened:
        if child in opened:
            return True
        new_opened = []
        for v in opened:
            generation = v.children
            new_opened.extend(generation)
        opened = new_opened
    return False


def build_lattice(concepts):
    concepts.sort(key=lambda x: len(x.g), reverse=True)  # descending
    root = concepts[0]
    for level in range(len(concepts)):
        c = concepts[level]
        for k in reversed(range(level)):
            oc = concepts[k]
            if set(c.g).issubset(oc.g) and not istransitive(oc, c):
                c.parents.add(oc)
                oc.children.add(c)
    return root


if __name__ == '__main__':
    from fca.context import *

    df = pd.DataFrame(data=[['x', 's', 'n', 't'],
                            ['x', 's', 'y', 't'],
                            ['b', 's', 'w', 't'],
                            ['x', 'y', 'w', 't'],
                            ['b', 'y', 'w', 't']], index=['g1', 'g2', 'g3', 'g4', 'g5'],
                      columns=['m1', 'm2', 'm3', 'm4'])
    c = Context(df)
    root = close_by_one(c)
    opened = [root]
    s = set()
    while opened:
        current = opened.pop()
        s.add(current)
        opened.extend(current.children)
    from pprint import pprint
    from time import time

    pprint(s)
    X, Y = [], []
    for i in range(3, 15):
        start = time()
        d = get_raw_data('data.csv')[:i]
        c = Context(d)
        close_by_one(c)
        t = str(time() - start)
        X.append(i)
        Y.append(t)
        print('i= ' + str(i) + '/15 time:' + t)
    import matplotlib.pyplot as plt

    plt.plot(X, Y)
    plt.show()
