"""
Binary Min-Heap stored as a plain array, ordered by city.distance.

This is the priority queue for "which unvisited city is closest" - pop
the min gives you exactly that. Same idea powers Dijkstra in task 2
(though that one just uses heapq directly instead of this class, since
it needs to key on running path distance, not city.distance).
"""

class MinHeap:
    def __init__(self):
        self._data = []  # just a list, heap property is maintained through swaps

    def __len__(self):
        return len(self._data)

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def push(self, city):
        self._data.append(city)
        self._sift_up(len(self._data) - 1)

    def pop_min(self):
        if not self._data:
            return None
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last  # move last element to root, then fix it back down
            self._sift_down(0)
        return top

    def peek_min(self):
        return self._data[0] if self._data else None

    def _sift_up(self, i):
        # bubble the new element up until its parent is smaller (or we hit the root)
        while i > 0 and self._data[self._parent(i)].distance > self._data[i].distance:
            p = self._parent(i)
            self._data[i], self._data[p] = self._data[p], self._data[i]
            i = p

    def _sift_down(self, i):
        # push the root down until both children are bigger than it
        n = len(self._data)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._data[l].distance < self._data[smallest].distance:
                smallest = l
            if r < n and self._data[r].distance < self._data[smallest].distance:
                smallest = r
            if smallest == i:
                break  # heap property holds now, stop
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest