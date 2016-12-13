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
        g_to_m = self.context.g_to_m(self.obj)
        m_to_g = self.context.m_to_g(g_to_m)
        rest = sorted([x for x in m_to_g if x not in self.obj])
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
        return "G:(" + ','.join([str(x) for x in self.obj]) + ")"

    def __repr__(self):
        return "G:(" + ','.join([str(x) for x in self.obj]) + ")"


def __derive(context, result, vertex):
    children = vertex.generate_children()
    vertex.close()
    if vertex.is_canonical():
        result.add(vertex)
        for child in children:
            print(len(result))
            __derive(context, result, child)


def close_by_one(context):
    res = []
    transposed = False
    if context.g_size > context.m_size:
        context.transpose()
        transposed = True
    vertices = set()
    __derive(context, vertices, Vertex(context, []))
    for v in vertices:
        item = Concept(v.obj, context.g_to_m(v.obj))
        if transposed:
            item = Concept(context.g_to_m(v.obj), v.obj)
        res.append(item)
    return res


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
    for level in range(len(concepts)):
        c = concepts[level]
        for k in reversed(range(level)):
            oc = concepts[k]
            if set(c.g).issubset(oc.g) and not istransitive(oc, c):
                c.parents.add(oc)
                oc.children.add(c)


if __name__ == '__main__':
    data = [[1, 0, 0, 1], [1, 0, 1, 0], [0, 1, 1, 0], [0, 1, 1, 1]]
    col = ['a','b','c','d']
    ind = ['1','2','3','4']
    # ind = ['g'+str(i) for i in range(len(data))]
    # col = ['m'+str(j) for j in range(len(data[0]))]
    df = pd.DataFrame(data=data, index=ind, columns=col)
    ctx1 = Context(df)
    print(ctx1)
    print()
    concepts = close_by_one(ctx1)
    pprint(concepts)
    print(len(concepts))

    build_lattice(concepts)
    for c in concepts:
        print('___________________')
        print(str(c) + ' : ')
        print(c.children)

