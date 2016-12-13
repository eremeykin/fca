from pprint import pprint
from context import Context
from clouse_by_one import close_by_one, build_lattice


class Rule():
    def __init__(self, A, B, G_cord):
        self.A = A
        self.B = B
        self.conf = len(B.G) / len(A.G)
        self.supp = len(B.G) / G_cord

    def __str__(self):
        return str(self.A) + "->" + str(self.B) + " ; conf = " + str(self.conf) + " , supp = " + str(self.supp)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if other is None:
            return False
        return self.A == other.A and self.B == other.B

    def __hash__(self):
        return hash(str(self.A) + "->" + str(self.B))


def search_rules(lattice, min_supp, min_conf):
    root = lattice[0]
    opened = {root}
    G_cord = len(root.G)
    rules = set()
    i = 0
    while opened:
        new_opened = set()
        for v in opened:
            generation = v.children
            new_opened.update(generation)
            for child in generation:
                rule = Rule(v, child, G_cord)
                i += 1
                print(i)
                if rule.conf >= min_conf and rule.supp >= min_supp and not rule in rules:
                    rules.add(rule)
                    print(rule)
        opened = new_opened
    return rules


ctx1 = Context('1001', '1010', '0110', '0111')
# ctx1 = Context('10010111','11101011','11111100','01010101','11100101')
print(ctx1)
concepts = close_by_one(ctx1)
build_lattice(concepts)
print()
rules = search_rules(concepts, 0, 0)

