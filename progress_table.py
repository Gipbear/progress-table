import time


class PT:
    COL_NUM = 5
    cols = {i: [20, 'desc', -1] for i in range(COL_NUM)}

    def __init__(self, iter_obj, position=0, width=20, desc='desc'):
        if not hasattr(iter_obj, '__iter__'):
            raise TypeError('obj is not iterable')
        if position == 0:
            PT.cols = {i: [width, 'desc', -1] for i in range(PT.COL_NUM)}
        elif position >= len(PT.cols):
            for i in range(len(PT.cols), position+1):
                PT.cols[i] = [width, 'desc', -1]
        PT.cols[position][2] = 0
        self.position = position
        self.desc = desc
        self.cnt = 0
        self.length = len(iter_obj)
        self.iter_obj = iter(iter_obj)

    def __iter__(self):
        return self

    def __next__(self):
        self.cnt += 1
        PT.cols[self.position][2] = self.cnt / self.length * 100
        obj = next(self.iter_obj)
        self._set_desc(self.desc, obj)
        self._print_table()
        return obj

    def _set_desc(self, desc, obj):
        desc_ = 'desc'
        if isinstance(desc, str):
            desc_ = desc
        elif hasattr(desc, '__call__'):
            desc_ = desc(obj)
        PT.cols[self.position][1] = desc_

    def _print_table(self):
        tabs = []
        for key, value in PT.cols.items():
            if value[2] == -1:
                continue
            tab = f'\033[4;3{key%8};40m{value[1].ljust(value[0]-6)} {value[2]:5.2f}%\033[0m'
            tabs.append(tab)
        if len(tabs) > 0:
            print(f"\r| {' | '.join(tabs)}", end=" |", flush=True)
            rest = sum([0 if v[2] in [-1, 100] else 1 for v in PT.cols.values()])
            if rest == 0:
                print()

if __name__ == '__main__':
    A = range(3)
    B = range(12)
    C = {f'c_{i}':'0' for i in range(7)}
    for a in PT(A, 0, desc='A'):
        for b in enumerate(PT(B, 1, desc='b in enumerate')):
            for c in PT(C.keys(), 2, desc='this is long long long desc about c'):
                for p in PT(C.items(), 3):
                    time.sleep(0.001)
    for b in enumerate(PT(B, 0, desc='b in enumerate')):
        for p in PT(C.items(), 1, desc=lambda x: x[0]):
            time.sleep(0.001)
