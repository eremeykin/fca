__author__ = 'eremeykin'
from pprint import pprint
from concept import Concept
from context import Context
import pandas as pd

class Vertex():

    def __init__(self, context, obj):
        self.obj = obj
        self.context = context
        self.closed = False

    def generate_children(self):
        res = []
        names = self.context.objects_names()
        last = names.index(self.obj[-1]) if len(self.obj) > 0 else -1
        for new in names[last+1:]:
            new_vertex = Vertex(self.context, self.obj + [new])
            res.append(new_vertex)
        return res

    def close(self):
        g_to_d = self.context.g_to_d(self.obj)
        d_to_g = self.context.d_to_g(g_to_d)
        rest = sorted([x for x in d_to_g if x not in self.obj])
        self.concept = Concept(d_to_g, g_to_d)
        self.obj = self.obj + rest
        self.closed = True


    def is_canonical(self):
        return self.obj == sorted(self.obj)

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
    vertex.close()
    print('in')
    if vertex.is_canonical():
        all_concepts.add(vertex.concept)
        print(len(all_concepts), vertex.concept)
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
    print('build_lattice')
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
    from context import  *
    df = pd.DataFrame(data=[['x', 's', 'n', 't'],
                            ['x', 's', 'y', 't'],
                            ['b', 's', 'w', 't'],
                            ['x', 'y', 'w', 't'],
                            ['b', 'y', 'w', 't']], index=['g1', 'g2', 'g3', 'g4', 'g5'],
                      columns=['m1', 'm2', 'm3', 'm4'])
    c = Context(df)
    v = Vertex(c, ['g4','g5'])
    print(v.generate_children())
    v.close()
    print(v)