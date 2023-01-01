class Node:
    def __init__(self, value, prv=None, nxt=None):
        self.value = value
        self.prv = prv
        self.nxt = nxt

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    @classmethod
    def from_iterable(cls, iterable):
        ll = cls()
        for value in iterable:
            ll.append(value)
        return ll

    @classmethod
    def range(cls, start, stop, step=1):
        return cls.from_iterable(range(start, stop, step))

    def _get(self, index) -> Node:
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range: {}".format(index))

        if index < self.size // 2:
            cur = self.head
            for _ in range(index):
                cur = cur.nxt
        else:
            cur = self.tail
            for _ in range(self.size - index - 1):
                cur = cur.prv
        return cur

    def get(self, index):
        return self._get(index).value

    def __getitem__(self, index):
        return self.get(index)

    def set(self, index, value):
        self._get(index).value = value

    def append(self, value):
        if self.size == 0:
            self.head = self.tail = Node(value)
        else:
            self.tail.nxt = Node(value, prv=self.tail)
            self.tail = self.tail.nxt
        self.size += 1

    def prepend(self, value):
        if self.size == 0:
            self.head = self.tail = Node(value)
        else:
            self.head.prv = Node(value, nxt=self.head)
            self.head = self.head.prv
        self.size += 1

    def insert(self, index, value):
        if index == 0:
            self.prepend(value)
        elif index == self.size:
            self.append(value)
        else:
            cur = self._get(index)
            cur.prv.nxt = Node(value, prv=cur.prv, nxt=cur)
            cur.prv = cur.prv.nxt
            self.size += 1

    def remove(self, index):
        if index == 0:
            self.head = self.head.nxt
            self.head.prv = None
        elif index == self.size - 1:
            self.tail = self.tail.prv
            self.tail.nxt = None
        else:
            cur = self._get(index)
            cur.prv.nxt = cur.nxt
            cur.nxt.prv = cur.prv
        self.size -= 1

    def __repr__(self):
        return str(self)

    def __len__(self):
        return self.size

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.nxt

    def __str__(self):
        return " -> ".join(str(node) for node in self)


class CircularLinkedList(LinkedList):

    def _make_circle(self):
        self.tail.nxt = self.head
        self.head.prv = self.tail

    def __init__(self):
        super().__init__()

    def append(self, value):
        super().append(value)
        self._make_circle()

    def prepend(self, value):
        super().prepend(value)
        self._make_circle()

    def insert(self, index, value):
        super().insert(index, value)
        self._make_circle()

    def remove(self, index):
        super().remove(index)
        self._make_circle()

    def __iter__(self):
        cur = self.head
        for _ in range(self.size):
            yield cur.value
            cur = cur.nxt

    def __copy__(self):
        return self.from_iterable(self)

