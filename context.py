def subsets(target):
    N = len(target)
    ordered = list(target)
    masks = [bin(x)[2:].zfill(N) for x in range(2 ** N)]
    res = []
    for m in masks:
        sset = set()
        for i, char in enumerate(m):
            if char == '1':
                sset.add(ordered[i])
        res.append(sset)
    return res


class Context():
    class Presentation():

        def __init__(self, t, data):
            if not t in ['line', 'column']:
                raise Error('Unknown type')
            self.__data = data
            self.__type = t

        def __getitem__(self, key):
            if self.__type == 'line':
                return list(self.__data[key])
            else:
                return [x[key] for x in self.__data]

        def __len__(self):
            if self.__type == 'line':
                return len(self.__data)
            else:
                return len(self.__data[0])

    def __init__(self, *lst):
        self.__data = lst
        self.lines = self.Presentation('line', self.__data)
        self.columns = self.Presentation('column', self.__data)
        self.g_size = len(self.lines)
        self.m_size = len(self.columns)


    def transpose(self):
        tmp = self.g_size
        self.g_size = self.m_size
        self.m_size = tmp
        tmp = self.lines
        self.lines = self.columns
        self.columns = tmp

    def __str__(self):
        res = 'G\M ' + ' '.join([str(x) for x in range(self.m_size)]) + '\n\n'
        res = res + '\n'.join([str(i) + '   ' + ' '.join(x) for i, x in enumerate(self.lines)])
        return str(res)

    def __X_to_Y(self, items, size, something):
        x = 2 ** size - 1
        for thing in something:
            x = x & int(''.join(items[thing]), 2)
        res = []
        for d in range(size + 1):
            if x & 2 ** d:
                res.append(size - 1 - d)
        return set(res)

    def M_to_G(self, m):
        return self.__X_to_Y(self.columns, self.g_size, m)

    def G_to_M(self, g):
        return self.__X_to_Y(self.lines, self.m_size, g)

    def is_pseudointent(self, P):
        P_dash = self.M_to_G(P)
        P_dash_dash = self.G_to_M(P_dash)
        if P == P_dash_dash:
            return False
        for Q in subsets(P):
            if Q != P and self.is_pseudointent(Q):
                Q_dash = self.M_to_G(Q)
                Q_dash_dash = self.G_to_M(Q_dash)
                if not Q_dash_dash.issubset(P):
                    return False
        return True

    def __is_gen(self, D, B):
        if not (type(B) is set) and (type(D) is set):
            raise Exception('wrong type' + str(type(B)) + " " + str(type(D)))
        # check 1
        if not B.issubset(range(self.m_size)):
            raise Exception('B is not subset of M')
        #check 2sb
        if self.G_to_M(self.M_to_G(B)) != B:
            raise Exception("B''!=B")
        return D.issubset(B) and self.G_to_M(self.M_to_G(D)) == B

    def is_nmingen(self, D, B):
        if not self.__is_gen(D, B):
            return False
        ssets = subsets(D)
        ssets.remove(D)
        for E in ssets:
            if self.G_to_M(self.M_to_G(E)) == self.G_to_M(self.M_to_G(D)):
                return False
        return D != self.G_to_M(self.M_to_G(D))

    def gen_impl_cover(self):
        res = []
        for F in subsets(range(self.m_size)):
            if self.is_nmingen(F, self.G_to_M(self.M_to_G(F))):
                impl = str(F) + "->" + str(self.G_to_M(self.M_to_G(F)) - F)
                res.append(impl)
        return res


if __name__ == '__main__':
    ctx1 = Context('1001', '1010', '0110', '0111')
    print(ctx1)
