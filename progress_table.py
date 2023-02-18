import time


class PT:
    """Return PT object
    Print progress table to visualize the for loop progress
    :param object obj: Iterable object
    :param int col: The nth column of the table, defaults to 0
    :param int width: The width of the desc field, defaults to 20
    :param str or func desc: Processing description, defaults to 'desc'
    :param bool switch: Controls whether the for loop is decorated, defaults to True
    :raises TypeError: Object is not iterable
    """

    COL_NUM = 5
    TABLE = {i: [20, 'desc', -1] for i in range(COL_NUM)}

    def __new__(cls, obj, col=0, width=20, desc='desc', switch=True):
        if switch == False:
            return obj
        return object.__new__(cls)

    def __init__(self, obj, col=0, width=20, desc='desc', switch=True):
        if not hasattr(obj, '__iter__'):
            raise TypeError('obj is not iterable')
        self.col = col
        self._init_table(width)
        self.desc = desc
        self.cnt = 0
        self.length = len(obj)
        self.iter_obj = iter(obj)

    def __iter__(self):
        return self

    def __next__(self):
        PT.TABLE[self.col][2] = self.cnt / self.length * 100
        try:
            obj = next(self.iter_obj)
            self._set_desc(self.desc, obj)
            self._print_table()
            self.cnt += 1
            return obj
        except StopIteration:
            PT.TABLE[self.col][2] = self.cnt / self.length * 100
            self._print_table()
            raise StopIteration

    def _init_table(self, width):
        if self.col == 0:
            PT.TABLE = {i: [width, 'desc', -1] for i in range(PT.COL_NUM)}
        elif self.col >= len(PT.TABLE):
            for i in range(len(PT.TABLE), self.col+1):
                PT.TABLE[i] = [width, 'desc', -1]
        PT.TABLE[self.col][2] = 0
        PT.TABLE[self.col][0] = width

    def _set_desc(self, desc, obj):
        desc_ = 'desc'
        if isinstance(desc, str):
            desc_ = desc
        elif hasattr(desc, '__call__'):
            desc_ = desc(obj)
        PT.TABLE[self.col][1] = desc_

    def _print_table(self):
        tabs = []
        for key, value in PT.TABLE.items():
            if value[2] == -1:
                continue
            tab = f'\033[4;3{key%8};40m{value[1].ljust(value[0]-6)} {value[2]:5.2f}%\033[0m'
            tabs.append(tab)
        if len(tabs) > 0:
            print(f"\r| {' | '.join(tabs)}", end=" |", flush=True)
            rest = sum([0 if v[2] in [-1, 100] else 1 for v in PT.TABLE.values()])
            if rest == 0:
                print()

if __name__ == '__main__':
    A = range(3)
    B = range(2)
    C = {f'c_{i}':'0' for i in range(50)}
    for a in PT(obj=A, col=0, desc='A'):
        for b in enumerate(PT(B, 1, desc='b in enumerate', switch=False)):
            # desc should not too long
            for c in PT(C.keys(), 2, desc='this is long long long desc about c'):
                    time.sleep(0.001)
            # Best, the sibling cycles have the same length of desc
            for p in PT(C.items(), 2):
                    time.sleep(0.001)
    for b in enumerate(PT(B, 0, desc='b in enumerate')):
        for c in PT(C.items(), 1, desc=lambda x: x[0]):
            time.sleep(0.001)
