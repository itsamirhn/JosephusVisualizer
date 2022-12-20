from .linkedlist import CircularLinkedList


class Josephus:
    def __init__(self, count):
        self.count = count
        self.victim = 0
        self.soldiers = CircularLinkedList.range(0, count)

    def kill(self):
        if self.soldiers.size == 1:
            return None
        self.victim = (self.victim + 1) % self.soldiers.size
        soldier = self.soldiers[self.victim]
        self.soldiers.remove(self.victim)
        return soldier

    @property
    def survivor(self):
        if self.soldiers.size == 1:
            return self.soldiers[0]
        return None

    def aliveness(self):
        aliveness = [False] * self.count
        for soldier in self.soldiers:
            aliveness[soldier] = True
        return aliveness
