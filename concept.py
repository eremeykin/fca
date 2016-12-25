__author__ = 'eremeykin'

class Concept():
    def __init__(self, g, m):
        self.g = g
        self.m = m
        self.children = set()
        self.parents = set()

    def __str__(self):
        return "{G:" + str(self.g) + "; \nM:\n" + str(self.m) + "}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash("{G:" + str(self.g) + "; \nM:\n" + str(self.m) + "}")

    def __eq__(self, other):
        if other is None:
            return False
        return self.g == other.g and self.m == other.m