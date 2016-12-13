from pprint import pprint
from random import randint
from context import Context


class Vertex():
    def __init__(self, context, obj):
        self.obj = obj
        self.context = context
        self.closed = False

    def generate_children(self):
        res = []
        last = self.obj[-1] if len(self.obj) > 0 else -1
        for new in range(last + 1, self.context.g_size):
            new_vertex = Vertex(self.context, self.obj + [new])
            res.append(new_vertex)
        return res

    def close(self):
        g_to_m = self.context.G_to_M(self.obj)
        m_to_g = self.context.M_to_G(g_to_m)
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


class Concept():
    def __init__(self, G, M):
        self.G = G
        self.M = M
        self.children = set()
        self.parents = set()

    def __str__(self):
        return "{G:" + str(self.G) + "; M:" + str(self.M) + "}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash("{G:" + str(self.G) + "; M:" + str(self.M) + "}")

    def __eq__(self, other):
        if other is None:
            return False
        return self.G == other.G and self.M == other.M


def __derive(context, result, vertex):
    children = vertex.generate_children()
    vertex.close()
    if vertex.is_canonical():
        result.add(vertex)
        for child in children:
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
        item = Concept(set(v.obj), context.G_to_M(v.obj))
        if transposed:
            item = Concept(context.G_to_M(v.obj), set(v.obj))
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
    concepts.sort(key=lambda x: len(x.G), reverse=True)  # descending
    for level in range(len(concepts)):
        c = concepts[level]
        for k in reversed(range(level)):
            oc = concepts[k]
            if set(c.G).issubset(oc.G) and not istransitive(oc, c):
                c.parents.add(oc)
                oc.children.add(c)


if __name__ == '__main__':
    ctx1 = Context('1001', '1010', '0110', '0111')
    print(ctx1)
    print()
    concepts = close_by_one(ctx1)
    pprint(concepts)
    build_lattice(concepts)
    for c in concepts:
        print('___________________')
        print(str(c) + ' : ')
        print(c.children)
    # ctx1 = Context('10010111','11101011','11111100','01010101','11100101')
    concepts = close_by_one(ctx1)
    build_lattice(concepts)
    memory = 0
    for c in concepts:
        memory += len(c.children) + len(c.parents)
    print(memory)
    print(len(concepts))